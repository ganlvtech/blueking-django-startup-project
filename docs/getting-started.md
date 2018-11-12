1. 安装 Django

        pip install django==1.8.3

2. 创建 Django 项目，并进入项目文件夹

        django-admin startproject mysite
        cd mysite/

3. 下载 `settings.py`

        wget https://django.qcloudapps.com/settings.py

4. 修改 `manage.py` 中的 `DJANGO_SETTINGS_MODULE`

    原来是

        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

    修改成

        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

5. 迁移数据库

        python manage.py migrate

6. 启动服务器，并访问 <http://127.0.0.1:8000/>

        python manage.py runserver

7. 提交到 SVN 服务器

8. 在开发者中心点击“一键部署”
