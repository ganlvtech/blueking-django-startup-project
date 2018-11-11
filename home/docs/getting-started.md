1. 安装 Django

        pip install django==1.8.3

2. 创建 Django 项目，并进入项目文件夹

        django-admin startproject mysite
        cd mysite/

3. 下载 `settings.py`

        wget https://raw.githubusercontent.com/ganlvtech/blueking-django-startup-project/master/settings.py

4. 修改 `manage.py` 中的 `DJANGO_SETTINGS_MODULE`

    原来是

        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

    修改成

        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

5. 启动服务器

        python manage.py migrate
        python manage.py runserver

6. 访问 <http://127.0.0.1:8000/>