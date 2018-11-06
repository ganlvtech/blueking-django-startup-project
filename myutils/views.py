from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, 'myutils/index.html')


def manage_createsuperuser(request):
    from django.contrib.auth import get_user_model

    User = get_user_model()

    if User.objects.filter(is_superuser=1).count() > 0:
        return HttpResponse("Superuser already exists!")

    if request.method != 'POST':
        return render(request, 'myutils/manage_createsuperuser.html')

    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')

    errors = []
    if not username:
        errors.append(ValidationError('username must be set'))
    if not email:
        errors.append(ValidationError('email must be set'))
    if not password:
        errors.append(ValidationError('password must be set'))
    if errors:
        raise ValidationError(errors)

    User.objects.create_superuser(username, email, password)

    return HttpResponse('OK')


def manage_collectstatic(request):
    from django.core.management import execute_from_command_line

    if request.GET.get('clear'):
        execute_from_command_line(['manage.py', 'collectstatic', '--clear', '--noinput'])
    else:
        execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])

    return HttpResponse('OK')


def manage_reset_db(request):
    from django.db import connection
    from django.core.management import execute_from_command_line
    from mysite import secrets

    if request.method == 'GET':
        return render(request, 'myutils/manage_reset_db.html')

    if request.POST.get('password') != secrets.RESET_PASSWORD:
        return render(request, 'myutils/manage_reset_db.html', {
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

    return render(request, 'myutils/manage_reset_db.html', {
        'message': "All tables dropped. New tables migrated."
    })
