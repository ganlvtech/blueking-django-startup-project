from django.http.response import HttpResponse
from django.shortcuts import render


def index(request):
    import markdown
    import os

    filename = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'README.md')
    with open(filename, 'r') as f:
        data = f.read()

    html = markdown.markdown(data, extensions=['fenced_code', 'tables'])
    return render(request, 'home/index.html', {'html': html})


def pyinfo(request):
    import re
    from mysite import secrets
    from .utils.pyinfo import pyinfo as my_pyinfo

    html = my_pyinfo()

    if request.GET.get('password') != secrets.PYINFO_PASSWORD:
        html = re.sub(r'(BK_APP_PWD</td><td.*?>)(.*?)(</td>)', '\\1***\\3', html)
        html = re.sub(r'(amqp://.*?:)(.*?)(@)', '\\1***\\3', html)
        html = re.sub(r'(BK_SECRET_KEY</td><td.*?>)(.*?)(</td>)', '\\1***\\3', html)

    return HttpResponse(html)


def admin_init(request):
    from django.contrib.auth import get_user_model
    from .utils.helpers import random_password
    User = get_user_model()

    if User.objects.filter(username='admin').count() > 0:
        return HttpResponse("admin already exists!")

    password = random_password()
    User.objects.create_superuser('admin', 'admin@example.com', password)

    return render(request, 'home/admin_init.html', {'password': password})


def admin_db_reset(request):
    from django.db import connection
    from django.core.management import execute_from_command_line
    from mysite import secrets

    if request.method == 'GET':
        return render(request, 'home/admin_db_reset.html')

    if request.POST.get('password') != secrets.RESET_PASSWORD:
        return render(request, 'home/admin_db_reset.html', {
            'message': "Password wrong!"
        })

    with connection.cursor() as cursor:
        cursor.execute("SHOW TABLES")
        tables = [cols[0] for cols in cursor.fetchall()]

        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        for table in tables:
            cursor.execute("DROP TABLE `%s`" % (table))
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

    execute_from_command_line(['manage.py', 'migrate'])

    return render(request, 'home/admin_db_reset.html', {
        'message': "All tables dropped. New tables migrated."
    })
