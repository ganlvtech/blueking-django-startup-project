# A Django Startup Project For Tencent Blueking

A Simplified Django Settings For Tencent Blueking

[Tencent Blueking Cloud Campus Version Developer Center][blueking-campus]

Online demos:

* [Home Page][home]
* [System Infomation][pyinfo]
* [A files explorer][files]
* [Static files][static-files]
* [A counter using django celery that increases every minutes][celery]
* [Increase the counter manually][celery-add]
* [Django Admin Site][admin]
* [Django manage][manage]
* [Django manage create superuser][create-superuser]
* [Reset database][reset-db]

You may find that Blueking's default Django project has too many unused things and difficult to learn.

The repo gives you a `settings.py`. It will make a pure django project runs on Blueking Cloud Platform.

You can also clone this repo as a startup project or demo project. But what you may need is only that `settings.py`.

## Getting Started

1. Create a new django project

        django-admin startproject mysite
        cd mysite/

2. Get this `settings.py` script

        wget https://raw.githubusercontent.com/ganlvtech/blueking-django-startup-project/master/settings.py


3. Change `manage.py` `DJANGO_SETTINGS_MODULE`

        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

4. Change `settings.py` `mysite` to `yoursite`

        from mysite.settings import *

5. Run server

        python manage.py migrate
        python manage.py runserver

6. You don't need to install `MySQL-python` locally. Try `PyMySQL`, which can be easily installed with pip.

        pip install PyMySQL

7. If you need to install some other packages with pip on the server, just add them to `requirements.txt`. The auto deploy script will do `pip install -r requirements.txt` before running the application.

8. You must put static files under `/static/` and upload `/static/` to the server. Put them under each app's `static/` dir and only use it in development environment. And use `collectstatic` to move static files of each apps to `/static/` dir.

        python manage.py collectstatic

## Run This Demo Project

```bash
git clone https://github.com/ganlvtech/blueking-django-startup-project.git
pip install django==1.8.3
pip install PyMySQL
```

Edit `mysite/settings.py` and `mysite/secrets.py`.

```bash
python manage.py migrate
python manage.py runserver
```

### Use Celery

```bash
pip install celery==3.1.18
pip install django-celery==3.2.1
```

You can see the following lines at the end of `mysite/settings.py`.

```python
import djcelery  # NOQA
djcelery.setup_loader()
INSTALLED_APPS += ('djcelery',)
BROKER_URL = 'django://'
INSTALLED_APPS += ('kombu.transport.django',)
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
```

And then run migration.

```bash
python manage.py migrate
```

Start celery workers and celery beat

```bash
python manage.py celery worker
python manage.py celery beat
```

> `celery beat` loads periodic tasks from database and sends the tasks to worker.
>
> Celery beat doesn't do the work itself. So even if you only need periodic task, you must start one worker at least.
>
> If you don't need periodic task, remove `CELERYBEAT_SCHEDULER` from `settings.py`.

## About Blueking Platform

It's just a Django Docker container!

You can do everything you want.

There must be a `settings.py` in root directory, because `DJANGO_SETTINGS_MODULE` is set to `settings` from container's environment variables.

Static files are served outside the container. So you must put static files under `/static/` and upload `/static/` to the server. Putting them under each app's dir and serve them by Django is not available.

Blueking Django Framework provide lots of modules helping DevOps, such as traffic analyser, mailer, sms sender, logger, QQ login, permission control and Mako template engine. They are too heavy. A normal web application may not need them.

If your are new to Django, this simple `settings.py` won't make you confused. Just adding one file to your project makes Django official tutorial available for Blueking platform. Hope this could help you.

You can write them or migrate them by yourself when you are good enough in Django programming.

## System Infomation

See [pyinfo].

### Pre-Installed Modules (Site Packages)

| Package Name              | Version     |
| :------------------------ | :---------- |
| amqp                      | 1.4.9       |
| anyjson                   | 0.3.3       |
| billiard                  | 3.3.0.23    |
| blueking.component.qcloud | 0.1.4       |
| celery                    | 3.1.18      |
| Django                    | 1.8.3       |
| django-celery             | 3.2.1       |
| eventlet                  | 0.14.0      |
| gevent                    | 1.1.0       |
| greenlet                  | 0.4.9       |
| gunicorn                  | 19.1.1      |
| httplib2                  | 0.9.1       |
| kombu                     | 3.0.35      |
| Mako                      | 1.0.1       |
| MarkupSafe                | 0.23        |
| meld3                     | 1.0.2       |
| MySQL-python              | 1.2.3       |
| mysqlclient               | 1.3.4       |
| pip                       | 6.1.1       |
| Python                    | 2.7.6.post3 |
| python-memcached          | 1.48        |
| pytz                      | 2016.6.1    |
| requests                  | 2.10.0      |
| setuptools                | 11.3.1      |
| supervisor                | 3.0         |
| uWSGI                     | 2.0.8       |
| wsgiref                   | 0.1.2       |

### Notes

`setuptools` is at version `11`. Some packages (e.g. `PyMySQL`) require `setuptools` version `30`. But the auto deploy script won't update `setuptools`. So PyMySQL cannot be easily installed.

## LICENSE

The MIT License (MIT)

Copyright (c) 2018 Ganlv

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

[home]: https://django.test.qcloudapps.com/
[pyinfo]: https://django.test.qcloudapps.com/pyinfo/
[files]: https://django.test.qcloudapps.com/files/
[static-files]: https://django.test.qcloudapps.com/static/index.html
[celery]: https://django.test.qcloudapps.com/celery/
[celery-add]: https://django.test.qcloudapps.com/celery/add/
[admin]: https://django.test.qcloudapps.com/admin/
[manage]: https://django.test.qcloudapps.com/manage/
[create-superuser]: https://django.test.qcloudapps.com/manage/createsuperuser/
[reset-db]: https://django.test.qcloudapps.com/manage/reset_db/
[blueking-campus]: https://bk.tencent.com/campus/developer-center/apps/
