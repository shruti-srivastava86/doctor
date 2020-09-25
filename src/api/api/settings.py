"""
Django settings for api project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '0ff7b8508a4b7c40b98bc9f1f045cad7a6f01d1d7db0d9b49e6f6d51adf295fb599cda0ecaa8cb567a0e354cdc875bf690b82acd5e4139329f0cfb30c8e4339d' # noqa

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = (
    'adminpanel',
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'doctor',
    'doctor.user',
    'doctor.food_hydration',
    'doctor.mind',
    'doctor.motion',
    'doctor.sleep',
    'doctor.surrounding',
    'doctor.weight',
    'doctor.alerts',
    'doctor.badges',
    'doctor.stop_challenge_choose',
    'doctor.feedback',
    'doctor.video',
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'rest_framework_swagger',
    'scarface',
    'django_celery_beat',
    'django_celery_results',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'qinspect.middleware.QueryInspectMiddleware'
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, '/doctor/templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
            'debug': True
        },
    },
]

ROOT_URLCONF = 'api.urls'

WSGI_APPLICATION = 'api.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'doctordb',
        'USER': 'doctordbuser',
        'PASSWORD': 'doctor123!',
        'HOST': '127.0.0.1'
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        }
    },
}

QUERY_INSPECT_ENABLED = False

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = '/var/sites/doctor/shared/static/'

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = '/var/sites/doctor/shared/uploads/'

# REST Framework
# http://www.django-rest-framework.org/#installation

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DATETIME_FORMAT': "%Y-%m-%dT%H:%M:%SZ",
    'PAGE_SIZE': 10,

    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework_xml.parsers.XMLParser',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework_xml.renderers.XMLRenderer'
    ),
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    'EXCEPTION_HANDLER': 'api.generics.exception_handler.custom_exception_handler'
}

AUTH_USER_MODEL = 'user.User'

LOGIN_URL = "/admin/login"

BASE_URL = 'http://192.168.56.111'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ENVIRONMENT = None

USE_SENTRY = False

SENTRY_DSN = ""

# celery setup
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json', 'yaml']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_TIMEZONE = TIME_ZONE
CELERY_ENABLE_UTC = True
CELERY_DISABLE_RATE_LIMITS = True
CELERY_ALWAYS_EAGER = True

# django-scarface setup


try:
    from .settings_local import * # noqa
except ImportError:
    pass

if ENVIRONMENT in ['Local', 'Vagrant', 'Dev'] and DEBUG:
    INSTALLED_APPS += ('silk',)
    MIDDLEWARE_CLASSES += ('silk.middleware.SilkyMiddleware',)


if USE_SENTRY:
    import raven # noqa

    # Get the release number from deploy
    rno = os.path.abspath(os.path.realpath(__file__)).split('/')[5]
    RAVEN_CONFIG = {
        'dsn': SENTRY_DSN,
        'release': rno,
        'environment': ENVIRONMENT,
    }
    MIDDLEWARE_CLASSES += ('raven.contrib.django.middleware.SentryMiddleware',)
    INSTALLED_APPS += ('raven.contrib.django.raven_compat',)
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'root': {
            'level': 'WARNING',
            'handlers': ['sentry'],
        },
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s '
                          '%(process)d %(thread)d %(message)s'
            },
        },
        'handlers': {
            'sentry': {
                'level': 'ERROR',  # To capture more than ERROR, change to WARNING, INFO, etc.
                'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
                'tags': {},
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            }
        },
        'loggers': {
            'django.db.backends': {
                'level': 'ERROR',
                'handlers': ['console'],
                'propagate': False,
            },
            'raven': {
                'level': 'WARNING',
                'handlers': ['console'],
                'propagate': False,
            },
            'sentry.errors': {
                'level': 'WARNING',
                'handlers': ['console'],
                'propagate': False,
            },
            'doctor': {
                'level': 'WARNING',
                'handlers': ['console', 'sentry', ],
            },
        },
    }
