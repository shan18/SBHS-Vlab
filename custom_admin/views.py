from django.shortcuts import render
from django.http import Http404
from django.contrib.auth.decorators import login_required

from sbhs_server import settings

import subprocess


def check_admin(req):
    if not req.user.is_admin:
        raise Http404


@login_required(redirect_field_name=None)
def profile(req, mid):
    check_admin(req)
    try:
        filename = settings.SBHS_GLOBAL_LOG_DIR + "/" + mid + ".log"
        f = open(filename, "r")
        f.close()
    except:
        raise Http404

    delta_T = 1000
    data = subprocess.check_output("tail -n %d %s" % (delta_T, filename), shell=True)
    data = data.split("\n")
    plot = []
    heat_csv = ""
    fan_csv = ""
    temp_csv = ""

    for t in xrange(len(data)):
        line = data[t]
        entry = line.strip().split(" ")
        try:
            plot.append([int(i) for i in entry[0:-1] + [float(entry[-1])]])
            heat_csv += "%d,%s\\n" % (t+1, entry[1])
            fan_csv += "%d,%s\\n" % (t+1, entry[2])
            temp_csv += "%d,%s\\n" % (t+1, entry[3])
        except:
            continue

    plot = zip(*plot)  # transpose

    return render(req, "custom_admin/profile.html", {
        "mid": mid,
        "delta_T": delta_T,
        "heat": heat_csv,
        "fan": fan_csv,
        "temp": temp_csv
    })
