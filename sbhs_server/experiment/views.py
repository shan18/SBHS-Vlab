from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as LOGIN
from sbhs_server.tables.models import Account, Experiment
import json, datetime, os, time
from django.views.decorators.csrf import csrf_exempt
from sbhs_server import settings
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

            #key = str(1)#Temporarily till SBHS class and settings.board dictionary are changed
            #try:
            #    settings.boards[key]["experiment_id"] = e.id
            #except:
            #    print "You found it"
            #reset(req)
			

            STATUS = 1
            MESSAGE = filename
        else:
            STATUS = 0
            MESSAGE = "Your account is not activated yet. Please check your email for activation link."
    else:
        STATUS = 0
        MESSAGE = "Invalid username or password"

    return HttpResponse(json.dumps({"STATUS": STATUS, "MESSAGE": MESSAGE}))
#    return HttpResponse(key)
# @login_required(redirect_field_name=None)
@csrf_exempt
def experiment(req):
    try:
        server_start_ts = int(time.time() * 1000)
        from sbhs_server.settings import boards
        user = req.user
        #print "Loc1"
        #key = str(1)#Temporarily till SBHS class and settings.board dictionary are changed
        #experiment = Experiment.objects.select_related().filter(id=boards[key]["experiment_id"])
        experiment = Experiment.objects.select_related().filter(user_id=user.id).order_by("-id")
        #print "Loc2"
        if True:#user.id == experiment[0].user.id:
            experiment = experiment[0]
            #print "Loc3"
            now = datetime.datetime.now()
            #print "Loc4"
            heat = max(min(int(req.POST.get("heat")), 100), 0)
            #print "Loc5"
            fan = max(min(int(req.POST.get("fan")), 100), 0)
            #print "Loc6"
            #boards[key]["board"].setHeat(heat)
            boards.setHeat(heat)
            #print "Loc7"
            #boards[key]["board"].setFan(fan)
            boards.setFan(fan)
            #print "Loc8"
            #temperature = boards[key]["board"].getTemp()
            temperature = boards.getTemp()
            #print temperature
            #print "Loc9"
            #log_data(boards[key]["board"], key, heat=heat, fan=fan, temp=temperature)
            log_data(boards, 1, heat=heat, fan=fan, temp=temperature)
            #print "Loc10"
            server_end_ts = int(time.time() * 1000)
            timeleft = 0 #TEMPORARY
            STATUS = 1
            MESSAGE = "%s %d %d %2.2f" % (req.POST.get("iteration"),
                                        heat,
                                        fan,
                                        temperature)
            print "Loc11"
            MESSAGE = "%s %s %d %d,%s,%d" % (MESSAGE,
                                        req.POST.get("timestamp"),
                                        server_start_ts,
                                        server_end_ts,
                                        req.POST.get("variables"), timeleft)
            print "Loc12"
            f = open(experiment.log, "a")
            print "Loc13"
            f.write(" ".join(MESSAGE.split(",")[:2]) + "\n")
            print "Loc14"
            f.close()
        else:
            STATUS = 0
            MESSAGE = "You haven't booked this slot."

        return HttpResponse(json.dumps({"STATUS": STATUS, "MESSAGE": MESSAGE}))
    except Exception:
        return HttpResponse(json.dumps({"STATUS": 0, "MESSAGE": "Invalid input. Perhaps the slot has ended. Please book the next slot to continue the experiment."}))

@csrf_exempt
def reset(req):
    try:
        from sbhs_server.settings import boards
        user = req.user
        if user.is_authenticated():
            key = str(1) #Temporarily till SBHS class and settings.board dictionary are changed
            experiment = Experiment.objects.select_related().filter(id=boards[key]["experiment_id"])

            if len(experiment) == 1 and user == experiment[0].user:
                experiment = experiment[0]
                now = datetime.datetime.now()
                boards.setHeat(0)
                boards.setFan(100)
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
        e.logname = e.log.split("/")[-1]
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
