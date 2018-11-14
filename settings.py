"""A Django Startup Project For Tencent Blueking

The MIT License (MIT)
Copyright (c) 2018 Ganlv

Usage

```bash
django-admin startproject mysite
cd mysite/
wget https://raw.githubusercontent.com/ganlvtech/blueking-django-startup-project/master/settings.py
```

Change `manage.py` `DJANGO_SETTINGS_MODULE` value `mysite.settings` to `settings`

Change `from mysite.settings import *` `mysite` to `yoursite`
"""

import os

from mysite.settings import *

WSGI_ENV = os.environ.get('DJANGO_CONF_MODULE', '')
if WSGI_ENV.endswith('production'):
    RUN_MODE = 'PRODUCT'
    SECRET_KEY = os.environ.get('BK_SECRET_KEY', '')
    DEBUG = False
    ALLOWED_HOSTS = ['*']
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': os.environ.get('BK_DB_HOST', 'appdb.bk.tencentyun.com'),
            'PORT': os.environ.get('BK_DB_PORT', '3337'),
            'USER': os.environ.get('BK_APP_CODE', ''),
            'PASSWORD': os.environ.get('BK_APP_PWD', ''),
            'NAME': os.environ.get('BK_APP_CODE', ''),
        },
    }
    BROKER_URL = os.environ.get('BK_BROKER_URL', '')
    STATIC_URL = os.environ.get('BK_STATIC_URL', '/static/')
    MEDIA_ROOT = os.path.join(BASE_DIR, 'USERRES')
    REMOTE_STATIC_URL = os.environ.get('BK_REMOTE_STATIC_URL', 'http://o.qcloud.com/static_api/')
elif WSGI_ENV.endswith('testing'):
    RUN_MODE = 'TEST'
    SECRET_KEY = os.environ.get('BK_SECRET_KEY', '')
    DEBUG = False
    ALLOWED_HOSTS = ['*']
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': os.environ.get('BK_DB_HOST', 'test.appdb.bk.tencentyun.com'),
            'PORT': os.environ.get('BK_DB_PORT', '3340'),
            'USER': os.environ.get('BK_APP_CODE', ''),
            'PASSWORD': os.environ.get('BK_APP_PWD', ''),
            'NAME': os.environ.get('BK_APP_CODE', ''),
        },
    }
    BROKER_URL = os.environ.get('BK_BROKER_URL', '')
    STATIC_URL = os.environ.get('BK_STATIC_URL', '/static/')
    MEDIA_ROOT = os.path.join(BASE_DIR, 'USERRES')
    REMOTE_STATIC_URL = os.environ.get('BK_REMOTE_STATIC_URL', 'http://o.qcloud.com/static_api/')
else:
    RUN_MODE = 'DEVELOP'
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    try:
        import MySQLdb
    except ImportError, e:
        print "MySQLdb not installed, use PyMySQL instead."
        import pymysql

        pymysql.install_as_MySQLdb()

if BROKER_URL.startswith('django://'):
    if 'kombu.transport.django' not in INSTALLED_APPS:
        INSTALLED_APPS += ('kombu.transport.django',)
else:
    if 'kombu.transport.django' in INSTALLED_APPS:
        INSTALLED_APPS = tuple([item for item in INSTALLED_APPS if item != 'kombu.transport.django'])
