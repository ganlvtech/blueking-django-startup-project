# A Django Startup Project For Tencent Blueking

A Simplified Django Settings For Tencent Blueking

[Tencent Blueking Cloud Campus Version Developer Center](https://bk.tencent.com/campus/developer-center/apps/)

You may find that Blueking's default Django project has too many unused things and difficult to learn.

The repo gives you a `settings.py`. It will make a pure django project runs on Blueking Cloud Platform.

You can also clone this repo as a startup project or demo project. But what you may need is only that `settings.py`.

## Getting started

1. Create a new django project

    ```bash
    django-admin startproject mysite
    cd mysite/
    ```

2. Get this `settings.py` script

    ```bash
    wget https://raw.githubusercontent.com/ganlvtech/blueking-django-startup-project/master/settings.py
    ```

3. Change `manage.py` `DJANGO_SETTINGS_MODULE`

    ```python
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
    ```

4. Change `settings.py` `mysite` to `yoursite`

    ```python
    from mysite.settings import *
    ```

5. Run server

    ```bash
    python manage.py migrate
    python manage.py runserver
    ```

6. You don't need to install `MySQL-python`. Try `PyMySQL`, which can be easily installed with pip.

    ```bash
    pip install PyMySQL
    ```

## Run This Demo Project

```bash
git clone https://github.com/ganlvtech/blueking-django-startup-project.git
pip install -r requirements.txt
pip install PyMySQL
```

Edit `mysite/settings.py` and `mysite/secrets.py`.

```bash
python manage.py migrate
python manage.py runserver
```

## About Blueking Platform

It's just a Django Docker container!

You can do everything you want.

There must be a `settings.py` in root directory, because `DJANGO_SETTINGS_MODULE` is set to `settings` from container's environment variables.

Blueking Django Framework provide lots of modules helping DevOps, such as traffic analyser, mailer, sms sender, logger, QQ login, permission control and Mako template engine. They are too heavy. A normal web application may not need them.

If your are new to Django, this simple `settings.py` won't make you confused. Just adding one file to your project makes Django official tutorial available for Blueking platform. Hope this could help you.

You can write them or migrate them by yourself when you are good enough in Django programming.

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
