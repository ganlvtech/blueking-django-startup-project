# A Django Startup Project For Tencent Blueking

A Simplified Django Settings For [Tencent Blueking](https://bk.tencent.com/campus/)

[Home Page](https://django.qcloudapps.com/)

## [中文文档](docs/README.md)

## Online Demos

See [demos](https://django.qcloudapps.com/demos/)


* `upload` module

    * [File Upload](https://django.qcloudapps.com/upload/)

* `myutils` module

    * [System Infomation](https://django.qcloudapps.com/utils/pyinfo/)
    * [Process Infomation](https://django.qcloudapps.com/utils/process/)
    * [Files Explorer](https://django.qcloudapps.com/utils/files/)
    * [`/etc/hosts`](https://django.qcloudapps.com/utils/hosts/)
    * [`/etc/passwd` and `/etc/group`](https://django.qcloudapps.com/utils/user/)
    * [Django manage create superuser](https://django.qcloudapps.com/utils/createsuperuser/)
    * [Reset database](https://django.qcloudapps.com/utils/reset_db/)

* `site_stats` module

    * [Visit log](http://django.qcloudapps.com/stats/)

* `golang` module

    * [Run golang program](https://django.qcloudapps.com/go/)
    * [Return with event-stream](https://django.qcloudapps.com/go/stream)
    * [Run async and return PID](https://django.qcloudapps.com/go/nowait/)

* `celery_test` module

    * [A counter using django celery that increases every minutes](https://django.qcloudapps.com/celery/)
    * [Increase the counter manually](https://django.qcloudapps.com/celery/add/)

* `send_mail` module

    * [Send E-mail via SMTP](https://django.qcloudapps.com/mail/)

* `django.contrib.admin` module

    * [Django Admin Site](https://django.qcloudapps.com/admin/)

You may find that Blueking's default Django project has too many unused things and difficult to learn.

The repo gives you a `settings.py`. It will make a pure django project runs on Blueking Cloud Platform.
[Tencent Blueking Cloud Campus Version Developer Center](https://bk.tencent.com/campus/developer-center/)


You can also clone this repo as a startup project or demo project. But what you may need is only that `settings.py`.

## Getting Started

1. Create a new django project

        django-admin startproject mysite
        cd mysite/

2. Get this `settings.py` script

        wget https://django.qcloudapps.com/settings.py

3. Change `manage.py` `DJANGO_SETTINGS_MODULE`

        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

4. Run server

        python manage.py migrate
        python manage.py runserver

5. You don't need to install `MySQL-python` locally. Try `PyMySQL`, which can be easily installed with pip.

        pip install PyMySQL

6. If you need to install some other packages with pip on the server, just add them to `requirements.txt`. The auto deploy script will do `pip install -r requirements.txt` before running the application.

7. You must put static files under `/static/` and upload `/static/` to the server. Put them under each app's `static/` dir and only use it in development environment. And use `collectstatic` to move static files of each apps to `/static/` dir.

        python manage.py collectstatic

## Run This Demo Project

**This instruction only enable the `home` module. If you want to enable others, you need to install some other packages listed in `requirements.txt`.**

First, clone this repo or download the zip of this project.

Then, install `django` and `PyMySQL`.

```bash
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
import djcelery
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

See [pyinfo](https://django.qcloudapps.com/utils/pyinfo/).

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
