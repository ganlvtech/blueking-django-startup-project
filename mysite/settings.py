"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 1.8.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

from . import secrets

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = secrets.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'appdev.o.qcloud.com',
    'django.qcloudapps.com',
    'django.test.qcloudapps.com',
]

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'mysite.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django',
        'USER': 'django',
        'PASSWORD': secrets.DATABASES['default']['PASSWORD'],
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

# Content Security Policy
# https://django-csp.readthedocs.io/en/latest/configuration.html
MIDDLEWARE_CLASSES += ('csp.middleware.CSPMiddleware',)
CSP_FRAME_ANCESTORS = 'bk.tencent.com'
CSP_DEFAULT_SRC = (
    "'self'",
    'data:',
)
CSP_SCRIPT_SRC = (
    "'self'",
    "'unsafe-inline'",
    'o.qcloud.com',
)
CSP_STYLE_SRC = (
    "'self'",
    "'unsafe-inline'",
)
CSP_IMG_SRC = (
    "'self'",
    'data:',
    'q1.qlogo.cn',
)
CSP_CONNECT_SRC = (
    'ws://appdev.o.qcloud.com:8000',
    'ws://django.qcloudapps.com',
    'ws://django.test.qcloudapps.com',
)

# my site settings
INSTALLED_APPS += (
    'home',
    'myutils',
    'golang',
)
TEMPLATES[0]['OPTIONS']['context_processors'] += (
    'home.context_processors.blueking',
    'home.context_processors.navbar',
)

# site_stats
INSTALLED_APPS += ('site_stats',)
MIDDLEWARE_CLASSES += ('site_stats.middlewares.SiteStatistics',)
TEMPLATES[0]['OPTIONS']['context_processors'] += ('site_stats.context_processors.visit_count',)

# blueking_api
INSTALLED_APPS += ('blueking_api',)
MIDDLEWARE_CLASSES += ('blueking_api.middlewares.CheckLogin',)

# celery_test
INSTALLED_APPS += ('celery_test',)
MIDDLEWARE_CLASSES += ('blueking_api.middlewares.CheckLogin',)
# http://docs.celeryproject.org/en/3.1/django/first-steps-with-django.html
import djcelery

djcelery.setup_loader()
INSTALLED_APPS += ('djcelery',)
# Django DB broker
BROKER_URL = 'django://'
INSTALLED_APPS += ('kombu.transport.django',)
# Redis broker
# BROKER_URL = 'redis://localhost'
# Celery beat periodic tasks
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

# file_upload
INSTALLED_APPS += ('file_upload',)
# https://docs.djangoproject.com/en/1.8/topics/http/file-uploads/
# https://docs.djangoproject.com/en/1.8/ref/settings/#media-root
# https://docs.djangoproject.com/en/1.8/ref/settings/#media-url
MEDIA_ROOT = os.path.join(BASE_DIR, 'USERRES')
MEDIA_URL = '/upload/'

# send_email
INSTALLED_APPS += ('send_email',)
# https://docs.djangoproject.com/en/1.8/topics/email/
EMAIL_USE_TLS = True

# websocket_test
INSTALLED_APPS += ('websocket_test',)
try:
    import uwsgi
    WEBSOCKET_FACTORY_CLASS = 'dwebsocket.backends.uwsgi.factory.uWsgiWebSocketFactory'
except ImportError:
    pass
