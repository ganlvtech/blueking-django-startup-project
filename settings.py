"""A Django Startup Project For Tencent Blueking

The MIT License (MIT)
Copyright (c) 2018 Ganlv

```bash
django-admin startproject mysite
cd mysite/
wget https://raw.githubusercontent.com/ganlvtech/blueking-django-startup-project/master/settings.py
```

Change `manage.py`

```python
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
```
"""

import os
from mysite.settings import *

WSGI_ENV = os.environ.get('DJANGO_CONF_MODULE', '')
if WSGI_ENV.endswith('production'):
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
    STATIC_URL = os.environ.get('BK_STATIC_URL', '/static/')
    STATICFILES_DIRS = ()
elif WSGI_ENV.endswith('testing'):
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
    STATIC_URL = os.environ.get('BK_STATIC_URL', '/static/')
    STATICFILES_DIRS = ()
else:
    STATICFILES_DIRS = (
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "static"),
    )

    try:
        import MySQLdb
    except ImportError, e:
        print "MySQLdb not installed, use pymysql instead."
        import pymysql
        pymysql.install_as_MySQLdb()
