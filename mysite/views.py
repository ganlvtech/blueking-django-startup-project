import django
import os
import random
import string
from django.conf import settings
from django.core.management import execute_from_command_line
from django.db import connection
from django.http.response import HttpResponse
from django.utils.html import escape
from . import pyinfo as my_pyinfo
from . import secrets


def random_password():
    chars = string.letters + string.digits + string.punctuation
    return "".join(random.choice(chars) for i in range(random.randint(12, 16)))


def index(request):
    return HttpResponse("Hello, Django %s!" % (django.get_version()))


def pyinfo(request):
    return HttpResponse(my_pyinfo.pyinfo())


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
    if request.GET.get('password') != secrets.RESET_PASSWORD:
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
