from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as LOGIN
from sbhs_server.tables.models import Account
from sbhs_server.tables.models import Experiment
import json
import datetime
import os
import time
from django.views.decorators.csrf import csrf_exempt
from sbhs_server import settings
from sbhs_server import sbhs
# Create your views here.
# 


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
            logdir = os.path.join(settings.EXPERIMENT_LOGS_DIR, user.username)
            if not os.path.exists(logdir):
                os.makedirs(logdir)
            f = open(os.path.join(logdir, filename), "a")
            f.close()
            

            LOGIN(req, user)
            e = Experiment()
            e.user = user
            e.log=os.path.join(logdir, filename)
            e.save()
            boards = sbhs.Sbhs()

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
    #global boards
    try:
        server_start_ts = int(time.time() * 1000)
        
        user = req.user
        
        
        experiment = Experiment.objects.select_related().filter(user_id=user.id).order_by("-id")
        
        
        experiment = experiment[0]
        
        now = datetime.datetime.now()
        
        heat = max(min(int(req.POST.get("heat")), 100), 0)
        
        fan = max(min(int(req.POST.get("fan")), 100), 0)
        
        
        boards.setHeat(heat)
        
        boards.setFan(fan)
        
        temperature = boards.getTemp()
        
        log_data(boards, 1, heat=heat, fan=fan, temp=temperature)
        
        server_end_ts = int(time.time() * 1000)
        timeleft = 5999
        STATUS = 1
        MESSAGE = "%s %d %d %2.2f" % (req.POST.get("iteration"),
                                    heat,
                                    fan,
                                    temperature)
        
        MESSAGE = "%s %s %d %d,%s,%d" % (MESSAGE,
                                    req.POST.get("timestamp"),
                                    server_start_ts,
                                    server_end_ts,
                                    req.POST.get("variables"), timeleft)
        
        f = open(experiment.log, "a")
        
        f.write(" ".join(MESSAGE.split(",")[:2]) + "\n")
        
        f.close()
        return HttpResponse(json.dumps({"STATUS": STATUS, "MESSAGE": MESSAGE}))
    except Exception:
        return HttpResponse(json.dumps({"STATUS": 0, "MESSAGE": "Invalid input. Perhaps the slot has ended. Please book the next slot to continue the experiment."}))

@csrf_exempt
def reset(req):
    try:
        user = req.user
        if user.is_authenticated():
			
            experiment = Experiment.objects.select_related().filter(user_id=user.id).order_by("-id")

            experiment = experiment[0]
            now = datetime.datetime.now()
            log_data(boards, key)
                
    except:
        pass

    return HttpResponse("")

def client_version(req):
    return HttpResponse("3")

@login_required(redirect_field_name=None)
def logs(req):
    experiments = Experiment.objects.select_related().filter(user_id=req.user.id)
    for e in experiments:
        e.logname = e.log.split("\\")[-1]
    return render(req, "experiment/logs.html", {"experiments": reversed(experiments)})

@login_required(redirect_field_name=None)
def download_log(req, experiment_id, fn):
    try:
        experiment = Experiment.objects.select_related().filter(user_id=user.id).order_by("-id")
        #assert req.user.id == experiment.user.id
        f = open(experiment[0].log, "r")
        data = f.read()
        f.close()
        return HttpResponse(data, content_type='text/text')
    except:
        return HttpResponse("Requested log file doesn't exist.")
		
#------------------Changes required----------------------------
def log_data(sbhs, mid, heat=None, fan=None, temp=None):
    f = open(settings.SBHS_GLOBAL_LOG_DIR + "/" + str(mid) + ".log", "a")
    if heat is None:
        heat = sbhs.getHeat()
    if fan is None:
        fan = sbhs.getFan()
    if temp is None:
        temp = sbhs.getTemp()

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
