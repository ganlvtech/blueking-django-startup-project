## 在服务器上通过 pip 安装包

把需要的包和版本号写在 `requirements.txt` 中

服务器会自动运行 `pip install -r requirements.txt`

**注意：服务器的 setuptools 并不是最新版的，部分 pip 包安装时对 setuptools 的版本有要求，这些包不能被安装。**

## 关于 MySQL

在本地开发环境中，你不必使用原生的 `MySQL-python`，试试 `PyMySQL` 吧！

```bash
pip install PyMySQL
```

你不必将 `PyMySQL` 添加到 `requirements.txt` 中，因为服务器已经自带了 `MySQL-python`。

## 静态文件

服务器中并不通过 Django 提供静态文件，而是通过 Nginx 直接提供，所以 SVN Commit 必须包含 `/static/` 文件夹。

如果你把静态文件存放在每个子应用的 `static/` 文件夹下，那么你可以使用 Django `collectstatic` 将他们自动复制到 `/static/` 文件夹，然后执行 SVN Commit。

```bash
python manage.py collectstatic
```

## 使用 Celery

安装 Celery 和 Django Celery

```bash
pip install celery==3.1.18
pip install django-celery==3.2.1
```

在 `mysite/settings.py` 的最后添加导入 `djcelery`

```python
import djcelery  # NOQA
djcelery.setup_loader()
INSTALLED_APPS += ('djcelery',)
BROKER_URL = 'django://'
INSTALLED_APPS += ('kombu.transport.django',)
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
```

执行数据库迁移

```bash
python manage.py migrate
```

启动 Celery Worker 和 Celery Beat

```bash
python manage.py celery worker
python manage.py celery beat
```

> `celery beat` 按照数据库中的 Period Tasks，定期把任务交给 worker 去做。
>
> 他本身并不处理任务，所以即使你仅使用周期性任务，也需要启动 worker。
>
> 如果您你只需要普通后台任务，并不需要周期性任务的话，可以从 `mysite/settings.py` 中移除 `CELERYBEAT_SCHEDULER`。

## 运行这个项目

下载并解压这个项目

安装所需的包

```bash
pip install django==1.8.3
pip install PyMySQL
```

复制一份 `mysite/settings.py` 和 `mysite/secrets.py`，并修改其中的一些配置项目

然后迁移并运行数据库

```bash
python manage.py migrate
python manage.py runserver
```

访问 <http://127.0.0.1:8000/>

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
