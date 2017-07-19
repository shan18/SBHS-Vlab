from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as LOGIN
from django.views.decorators.csrf import csrf_exempt

import json
import datetime
import os
import time
import random

from sbhs_server.tables.models import Account
from sbhs_server.tables.models import Experiment
from sbhs_server import settings
from sbhs_server import sbhs

from global_values import GlobalValues


def check_connection(req):
    return HttpResponse("TESTOK")


@csrf_exempt
def initiation(req):
    username = req.POST.get("username")
    password = req.POST.get("password")
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            user1 = Account.objects.select_related().filter(id=user.id)
            user1 = user1[0]
            filename = datetime.datetime.strftime(datetime.datetime.now(), "%Y%b%d_%H_%M_%S.txt")
            log_dir = os.path.join(settings.EXPERIMENT_LOGS_DIR, user.username)
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
            f = open(os.path.join(log_dir, filename), "a")
            f.close()

            """ Initialize Global Values """
            GlobalValues.instantaneous_time = 0
            GlobalValues.room_temp = 29 + random.uniform(-2, 2)
            GlobalValues.max_temp = 68 + random.uniform(-0.3, 0.3)

            LOGIN(req, user)
            e = Experiment()
            e.user = user
            e.log = os.path.join(log_dir, filename)
            e.save()

            boards = sbhs.Sbhs(user.coeff_ID)
            global boards

            STATUS = 1
            MESSAGE = filename
        else:
            STATUS = 0
            MESSAGE = "Your account is not activated yet. Please check your email for activation link."
    else:
        STATUS = 0
        MESSAGE = "Invalid username or password"

    return HttpResponse(json.dumps({"STATUS": STATUS, "MESSAGE": MESSAGE}))


@csrf_exempt
def experiment(req):
    # global boards
    try:
        server_start_ts = int(time.time() * 1000)
        user = req.user

        experiment = Experiment.objects.select_related().filter(user_id=user.id).order_by("-id")
        experiment = experiment[0]
        
        now = datetime.datetime.now()
        
        heat = max(min(int(req.POST.get("heat")), 100), 0)
        fan = max(min(int(req.POST.get("fan")), 100), 0)

        boards.set_heat(heat)
        boards.set_fan(fan)

        # scaling heat
        scaled_heat = int((heat * 50) / 100)

        delta_heat = 0
        neg_heat = 1
        delta_fan = 0
        neg_fan = 1
        if GlobalValues.instantaneous_time > 0:
            delta_heat = scaled_heat - GlobalValues.heat_old
            delta_fan = fan - GlobalValues.fan_old

        if delta_heat != 0:
            GlobalValues.flag_heat = 1
            if delta_heat < 0:
                neg_heat = -1
            else:
                neg_heat = 1
        else:
            GlobalValues.flag_heat = 0

        if delta_fan != 0:
            GlobalValues.flag_fan = 1
            if delta_fan < 0:
                neg_fan = -1
            else:
                neg_fan = 1
        else:
            GlobalValues.flag_fan = 0

        temperature = boards.get_temp(
            neg_heat * scaled_heat,
            neg_fan * fan
        )
        GlobalValues.instantaneous_time += 1
        GlobalValues.heat_old = scaled_heat
        GlobalValues.fan_old = fan
        
        log_data(boards, user.coeff_ID, heat=heat, fan=fan, temp=temperature)
        
        server_end_ts = int(time.time() * 1000)
        timeleft = 5999
        STATUS = 1
        MESSAGE = "%s %d %d %2.2f" % (str(GlobalValues.instantaneous_time - 1),  # req.POST.get("iteration"),
                                      heat, fan, temperature)
        
        MESSAGE = "%s %s %d %d,%s,%d" % (MESSAGE,
                                         req.POST.get("timestamp"),
                                         server_start_ts, server_end_ts,
                                         req.POST.get("variables"), timeleft)
        
        f = open(experiment.log, "a")
        f.write(" ".join(MESSAGE.split(",")[:2]) + "\n")
        f.close()
        return HttpResponse(json.dumps({"STATUS": STATUS, "MESSAGE": MESSAGE}))
    except Exception as e:
        return HttpResponse(json.dumps({"STATUS": 0, "MESSAGE": str(e)}))


@csrf_exempt
def reset(req):
    try:
        user = req.user
        if user.is_authenticated():
            experiment = Experiment.objects.select_related().filter(user_id=user.id).order_by("-id")
            experiment = experiment[0]
            now = datetime.datetime.now()
            log_data(boards, experiment.coeff_ID)
    except:
        pass

    return HttpResponse("")


def client_version(req):
    return HttpResponse("3")


@login_required(redirect_field_name=None)
def logs(req):
    experiments = Experiment.objects.select_related().filter(user_id=req.user.id)
    for e in experiments:
        e.log_name = str(e.log).split('/')[-1]
    return render(req, "experiment/logs.html", {"experiments": reversed(experiments)})


@login_required(redirect_field_name=None)
def download_log(req, experiment_id, fn):
    try:
        experiment = Experiment.objects.select_related().filter(user_id=req.user.id, id=experiment_id)
        f = open(experiment[0].log, "r")
        data = f.read()
        f.close()
        return HttpResponse(data, content_type='text/text')
    except:
        return HttpResponse("Requested log file doesn't exist.")


def log_data(sbhs, coeff_id, heat=None, fan=None, temp=None):
    f = open(settings.SBHS_GLOBAL_LOG_DIR + "/" + str(coeff_id) + ".log", "a")
    if heat is None:
        heat = sbhs.get_heat()
    if fan is None:
        fan = sbhs.get_fan()
    if temp is None:
        temp = sbhs.get_temp()

    data = "%d %s %s %s\n" % (int(time.time()), str(heat), str(fan), str(temp))
    f.write(data)
    f.close()


def validate_log_file(req):
    import hashlib
    data = req.POST.get("data")
    data = data.strip().split("\n")
    clean_data = ""
    for line in data:
        columns = line.split(" ")
        if len(columns) >= 6:
            clean_data += (" ".join(columns[0:6]) + "\n")

    checksum = hashlib.sha1(clean_data).hexdigest()

    try:
        e = Experiment.objects.get(checksum=checksum)
        return HttpResponse("TRUE")
    except:
        return HttpResponse("FALSE")
