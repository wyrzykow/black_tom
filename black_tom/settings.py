"""
Django settings for your TOM project.

Originally generated by 'django-admin startproject' using Django 2.1.1.
Generated by ./manage.py tom_setup on Jan. 9, 2019, 10:20 p.m.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import django_heroku

#reads all secret settings and apis, which will not be stored in git repo
try:
    from black_tom import local_settings as secret
except ImportError:
    pass

#this is required by Heroku, as they setup environment variables instead of using local_settings (not on github)
try:
    LCO_APIKEY = secret.LCO_APIKEY
except:
    LCO_APIKEY = os.environ['LCO_APIKEY']

try:
    ANTARES_KEY = secret.ANTARES_KEY
    ANTARES_SECRET = secret.ANTARES_SECRET
except:
    ANTARES_KEY = os.environ['ANTARES_KEY']
    ANTARES_SECRET = os.environ['ANTARES_SECRET']


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django_extensions',
    'guardian',
    'tom_common',
    'django_comments',
    'bootstrap4',
    'crispy_forms',
    'django_filters',
    'django_gravatar',
    'tom_targets',
    'tom_alerts',
    'tom_catalogs',
    'tom_observations',
    'tom_dataproducts',
    'custom_code',
    'saveobsapp.apps.SaveobsappConfig'
]

SITE_ID = 2

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'tom_common.middleware.ExternalServiceMiddleware',
     'tom_common.middleware.AuthStrategyMiddleware',
]

ROOT_URLCONF = 'black_tom.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

CRISPY_TEMPLATE_PACK = 'bootstrap4'

WSGI_APPLICATION = 'black_tom.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
if os.environ.get('black_tom_DB_BACKEND') == 'postgres':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'black_tom',
            'USER': os.environ['black_tom_DB_USER'],
            'PASSWORD': os.environ['black_tom_DB_PASSWORD'],
            'HOST': 'black_tom-db',
            'PORT': 5432,
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
)

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = False

USE_TZ = True

DATETIME_FORMAT = 'Y-m-d H:m:s'
DATE_FORMAT = 'Y-m-d'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

#STATIC_URL = '/static/'
#STATIC_ROOT = os.path.join(BASE_DIR, '_static')
#STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

#new from stackoverflow:
STATIC_URL = os.path.join(BASE_DIR, 'static').replace('\\','')+'/'
# Here you can add all the directories from where you want to use your js, css etc
STATICFILES_DIRS = [
  # This can be same as the static url
  os.path.join(BASE_DIR, "static"),
]
# This is the static root dir from where django uses the files from.
STATIC_ROOT = os.path.join(BASE_DIR, "static_root")


MEDIA_ROOT = os.path.join(BASE_DIR, 'data')
MEDIA_URL = '/data/'

# Using AWS - AMAZON account - disabling

#DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
#STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
#
#AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', '')
#AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRECT_ACCESS_KEY', '')
#AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME', '')
#AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME', '')
#AWS_DEFAULT_ACL = None

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO'
        }
    }
}

# TOM Specific configuration
TARGET_TYPE = 'SIDEREAL'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ['TOMEMAIL']
EMAIL_HOST_PASSWORD = os.environ['TOMEMAILPASSWORD']

#tns harvester reads it too, but SNEXBOT api key still needed - FIX?
SNEXBOT_APIKEY =  os.environ['TNSBOT_APIKEY']
TWITTER_APIKEY = 'dupablada'

#Not used:
SECRET_KEY = 'ks#e!w3m*y1g_=)%vmrdcyn*5dt0$)o^mq2f=vtj#myw#&amp;p3%i'

BROKER_CREDENTIALS = {
    'antares': {
        'api_key': ANTARES_KEY,
        'api_secret': ANTARES_SECRET
    }
}


FACILITIES = {
    'LCO': {
        'portal_url': 'https://observe.lco.global',
        'api_key': LCO_APIKEY,
    },
    'GEM': {
        'portal_url': {
            'GS': 'https://139.229.34.15:8443',
            'GN': 'https://128.171.88.221:8443',
        },
        'api_key': {
            'GS': '',
            'GN': '',
        },
        'user_email': '',
        'programs': {
            'GS-YYYYS-T-NNN': {
                'MM': 'Std: Some descriptive text',
                'NN': 'Rap: Some descriptive text'
            },
            'GN-YYYYS-T-NNN': {
                'QQ': 'Std: Some descriptive text',
                'PP': 'Rap: Some descriptive text',
            },
        },
    },
    'SNExGemini': {
        'portal_url': {
            'GS': 'https://139.229.34.15:8443',
            'GN': 'https://139.229.34.15:8443',
        },
        'api_key': {
            'GS': '',
            'GN': '',
        },
        'user_email': '',
        'programs': 'GS-2019A-Q-113' 
    }
}

# Define extra target fields here. Types can be any of "number", "st    ring", "boolean" or "datetime"
# See https://tomtoolkit.github.io/docs/target_fields for documentat    ion on this feature
# For example:
# EXTRA_FIELDS = [
#     {'name': 'redshift', 'type': 'number'},
#     {'name': 'discoverer', 'type': 'string'}
#     {'name': 'eligible', 'type': 'boolean'},
#     {'name': 'dicovery_date', 'type': 'datetime'}
# ]
EXTRA_FIELDS = [
    {'name': 'redshift', 'type': 'number'},
    {'name': 'classification', 'type': 'string'},
    {'name': 'tweet', 'type': 'boolean'},
]

# Authentication strategy can either be LOCKED (required login for all views)
# or READ_ONLY (read only access to views)
AUTH_STRATEGY = 'LOCKED'

# URLs that should be allowed access even with AUTH_STRATEGY = LOCKED
# for example: OPEN_URLS = ['/', '/about']
OPEN_URLS = ['/black_tom/tnstargets/']

HOOKS = {
    'target_post_save': 'custom_code.hooks.target_post_save',
    'observation_change_state': 'black_tom.hooks.observation_change_state'
}

TOM_ALERT_CLASSES = [
    'custom_code.brokers.mars.CustomMARSBroker',
    'tom_alerts.brokers.lasair.LasairBroker',
    'tom_antares.antares.AntaresBroker'
    ]

TOM_FACILITY_CLASSES = [
    #'tom_observations.facilities.gemini.GEMFacility',
    'custom_code.facilities.lco_facility.LCOFacility',
    'custom_code.facilities.gemini_facility.GeminiFacility',
    #'tom_observations.facilities.lco.LCOFacility',
    'tom_gemini_community.gemini_gsselect.GEMFacility',
    'black_tom.asvtelescope.ASVTelescope',
    'black_tom.opticonnetwork.OpticonNetwork',
    'black_tom.lcomultifilter.LCOMultiFilterFacility',
#    'tom_lt.lt.LTFacility',
    ]

TOM_HARVESTER_CLASSES = [
    'custom_code.harvesters.tns_harvester.TNSHarvester',
    'custom_code.harvesters.mars_harvester.MARSHarvester',
    'tom_catalogs.harvesters.simbad.SimbadHarvester',
    'tom_catalogs.harvesters.ned.NEDHarvester',
    #'tom_catalogs.harvesters.jplhorizons.JPLHorizonsHarvester',
    #'tom_catalogs.harvesters.mpc.MPCHarvester',
    ]

DATA_TYPES = (
    ('SPECTROSCOPY', 'Spectroscopy'),
    ('PHOTOMETRY', 'Photometry')
)

HINTS_ENABLED = False
HINT_LEVEL = 20

django_heroku.settings(locals())
