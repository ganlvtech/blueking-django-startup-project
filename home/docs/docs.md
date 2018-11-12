### 使用 Celery

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

### 运行这个项目

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

### LICENSE

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
