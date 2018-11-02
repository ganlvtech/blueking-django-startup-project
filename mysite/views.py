import django
import markdown
import os
import random
import re
import string
from django.conf import settings
from django.core.management import execute_from_command_line
from django.middleware.csrf import get_token
from django.db import connection
from django.http.response import HttpResponse
from django.utils.html import escape
from . import pyinfo as my_pyinfo
from . import secrets


def random_password():
    chars = string.letters + string.digits + string.punctuation
    return "".join(random.choice(chars) for i in range(random.randint(12, 16)))


def index(request):
    filename = os.path.join(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))), 'README.md')
    with open(filename, 'r') as f:
        data = f.read()
    print(data)
    html = markdown.markdown(data, extensions=['fenced_code', 'tables'])
    html = r"""
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/sindresorhus/github-markdown-css/github-markdown.css">
    <style>
        .markdown-body {
            margin: 0 auto;
            width: 980px;
            max-width: 100%;
        }
    </style>
    <div class="markdown-body">""" + html + '</div>'
    return HttpResponse(html)


def version(request):
    return HttpResponse("Hello, Django %s!" % (django.get_version()))


def pyinfo(request):
    html = my_pyinfo.pyinfo()

    if request.GET.get('password') != secrets.PYINFO_PASSWORD:
        html = re.sub(r'(BK_APP_PWD</td><td.*?>)(.*?)(</td>)', '\\1***\\3', html)
        html = re.sub(r'(amqp://.*?:)(.*?)(@)', '\\1***\\3', html)
        html = re.sub(r'(BK_SECRET_KEY</td><td.*?>)(.*?)(</td>)', '\\1***\\3', html)

    return HttpResponse(html)


def admin_init(request):
    from django.contrib.auth import get_user_model
    User = get_user_model()

    if User.objects.filter(username='admin').count() > 0:
        return HttpResponse("admin already exists!")

    password = random_password()
    User.objects.create_superuser('admin', 'admin@example.com', password)

    html = """
    Superuser created.<br>
    Username <input type="text" readonly value="admin">.<br>
    Password <input type="text" readonly value=\"%s\">.<br>
    This operation can't be done twice.
    """ % (escape(password))
    return HttpResponse(html)


def clear_db(request):
    if request.method == 'GET':
        return HttpResponse("""
        <form method="POST">
            <input type="hidden" name="csrfmiddlewaretoken" value="%s">
            <input type="text" name="password">
            <input type="submit">
        </form>
        """ % (get_token(request)))

    if request.POST.get('password') != secrets.RESET_PASSWORD:
        return HttpResponse("Password wrong!")

    with connection.cursor() as cursor:
        cursor.execute("SHOW TABLES")
        tables = [cols[0] for cols in cursor.fetchall()]

        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        for table in tables:
            cursor.execute("DROP TABLE `%s`" % (table))
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

    execute_from_command_line(['manage.py', 'migrate'])

    return HttpResponse("All tables dropped. New tables migrated.")
