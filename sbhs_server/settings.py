"""
Django settings for sbhs_server project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import sys #srikant
import socket

hostname = socket.gethostname()
is_production = hostname == "vlabs-Veriton-Series"

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'skjndcijuwhfjc_cnjwcuwuhcnje490fu=@f('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = not is_production

TEMPLATE_DEBUG = not is_production

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "192.168.43.208",
    "192.168.43.144",
    "10.42.0.1",
]

if not DEBUG:
    ALLOWED_HOSTS = [
        "localhost",
        "127.0.0.1",
        "vlabs.iitb.ac.in",
        "vlabs.iitb.ac.in.",
        "10.102.152.15",
    ]

# Application definition

INSTALLED_APPS = (
    # 'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 'south',
    'undelete',
    # 'yaksh',
    # 'taggit',

    'account',
    'admin',
    'experiment',
    'pages',
    'password',
    'sbhs_server.tables',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'sbhs_server.urls'

WSGI_APPLICATION = 'sbhs_server.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

if is_production:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'db_name',
            'USER': 'username',
            'PASSWORD': 'password',
            'HOST': 'localhost',
            'PORT': '3306',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'sbhs.sqlite3'),
        }
    }

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = False

AUTH_USER_MODEL = 'tables.Account'
LOGIN_URL = '/sbhs/enter'
LOGOUT_URL = '/sbhs/logout'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
CSRF_COOKIE_NAME = "pfesgbxra"
SESSION_COOKIE_NAME = "frffvbaVq"

EMAIL_HOST = 'smtp-auth.iitb.ac.in'
EMAIL_PORT = 25
EMAIL_HOST_USER = "username"
EMAIL_HOST_PASSWORD = "password"


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/


if is_production:
    BASE_URL = "http://vlabs.iitb.ac.in/sbhs/"
    FORCE_SCRIPT_NAME = "/sbhs"
    USE_X_FORWARDED_HOST = True
else:
    BASE_URL = "http://127.0.0.1:8000/"

SBHSCLIENT_STATIC_DIR = os.path.join(BASE_DIR, "client_static")
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
    os.path.join(SBHSCLIENT_STATIC_DIR, "zipped"),
)
STATIC_ROOT = os.path.join(BASE_DIR, "production_static_files")

if is_production:
    STATIC_URL = 'http://vlabs.iitb.ac.in/sbhs/static/'
else:
    STATIC_URL = '/static/'

# TEMPLATE_DIRS = (
#     os.path.join(BASE_DIR, "production_static_files"),
#     os.path.join(BASE_DIR, 'templates/'),
# )

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

import warnings
warnings.filterwarnings(
        'ignore', r"DateTimeField .* received a naive datetime",
        RuntimeWarning, r'django\.db\.models\.fields')

if not is_production:
    import logging
    l = logging.getLogger('django.db')
    l.setLevel(logging.DEBUG)
    l.addHandler(logging.StreamHandler())

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            'django.db': {
                'level': 'DEBUG',
                'handlers': ['console'],
            },
        }
    }
else:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'file': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': os.path.join(BASE_DIR, 'log/django_error.log'),
            }
        },
        'loggers': {
            'django.request': {
                'handlers': ['file'],
                'level': 'ERROR',
                'propagate': True,
            }
        }
    }

EXPERIMENT_LOGS_DIR = os.path.join(BASE_DIR, 'experiments')

if not is_production:
    SBHS_ADMINS = (
        # ("Amol Mandhane", "+91-9999999999", "amol_mandhane@iitb.ac.in"),
        # ("Amol Mandhane", "+91-9999999999", "amol_mandhane@iitb.ac.in"),
        ("Shantanu Acharya", "+91-0123456789", "thegeek.004@gmail.com"),
    )
else:
    from sbhs_server.sbhs_admin_config import SBHS_ADMINS

SBHS_GLOBAL_LOG_DIR = os.path.join(BASE_DIR, 'log')
