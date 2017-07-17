import os
import sys
import site

path_to_venv = "/home/vlabs-server/sbhs/venv/"
path_to_project_root = "/home/vlabs-server/sbhs/SBHS-Vlabs/"

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir(path_to_venv + 'local/lib/python2.7/site-packages/')

# Add the app's directory to the PYTHONPATHr
sys.path.append(path_to_project_root)
sys.path.append(path_to_project_root + 'sbhs_server/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'sbhs_server.settings'

# Activate your virtual env
activate_env=os.path.expanduser(path_to_venv + "bin/activate_this.py")
execfile(activate_env, dict(__file__=activate_env))

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()