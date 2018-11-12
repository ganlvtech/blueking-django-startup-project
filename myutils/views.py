from django.core.exceptions import ValidationError
from django.http import FileResponse, HttpResponseForbidden, HttpResponseNotFound, HttpResponseNotModified
from django.shortcuts import render


def index(request):
    return render(request, 'myutils/index.html')


def manage_createsuperuser(request):
    from django.contrib.auth import get_user_model

    User = get_user_model()

    if User.objects.filter(is_superuser=1).count() > 0:
        return render(request, 'myutils/manage_createsuperuser.html', {
            'superuser_exists': True
        })
        # return HttpResponse("Superuser already exists!")

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

    return render(request, 'myutils/manage_createsuperuser.html', {
        'ok': True
    })


def manage_reset_db(request):
    from django.db import connection
    from django.core.management import execute_from_command_line
    from django.contrib.auth import get_user_model
    from mysite import secrets
    from django.contrib.auth.hashers import check_password

    if request.method == 'GET':
        return render(request, 'myutils/manage_reset_db.html')

    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')

    errors = []
    if not username:
        errors.append(ValidationError('username must be set'))
    if not password:
        errors.append(ValidationError('password must be set'))
    if errors:
        raise ValidationError(errors)

    User = get_user_model()

    user = User.objects.filter(is_superuser=1, username=username).first()
    if not user or not check_password(password, user.password):
        return render(request, 'myutils/manage_reset_db.html', {
            'password_wrong': True
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
        'ok': True
    })


def hosts(request):
    import os

    if os.name == 'nt':
        path = os.path.join(os.getenv('SYSTEMROOT', r'C:\Windows'), r'System32\drivers\etc\hosts')
    elif os.name == 'posix':
        path = '/etc/hosts'
    else:
        path = None

    if path is None or not os.path.isfile(path):
        content = ''
    else:
        with open(path, 'rb') as fh:
            data = fh.read()
        content = data.decode('utf-8')

    return render(request, 'home/plain_text.html', {
        'title': 'hosts',
        'heading': path,
        'content': content
    })


def pyinfo(request):
    import platform
    import re
    from mysite import secrets
    from .utils import my_pyinfo

    response = render(request, 'myutils/pyinfo.html', {
        'py_version': platform.python_version(),
        'tables': my_pyinfo()
    })

    html = response.content
    if request.GET.get('password') != secrets.PYINFO_PASSWORD:
        html = re.sub(r'(BK_APP_PWD</td>\s*?<td.*?>)(.*?)(</td>)', '\\1***\\3', html)
        html = re.sub(r'(amqp://.*?:)(.*?)(@)', '\\1***\\3', html)
        html = re.sub(r'(BK_SECRET_KEY</td>\s*?<td.*?>)(.*?)(</td>)', '\\1***\\3', html)
    response.content = html

    return response


def files(request):
    import os
    import urllib
    from .utils import format_time

    path = request.GET.get('path', os.getcwd())
    path = os.path.abspath(path)

    if not os.path.exists(path):
        return HttpResponseNotFound()

    if 'secret' in path:
        return HttpResponseForbidden()

    if os.path.isfile(path):
        import stat
        from django.utils.http import http_date
        from django.views.static import was_modified_since
        from .utils import guess_type

        statobj = os.stat(path)
        if not was_modified_since(request.META.get('HTTP_IF_MODIFIED_SINCE'), statobj.st_mtime, statobj.st_size):
            return HttpResponseNotModified()

        content_type, encoding = guess_type(path)

        response = FileResponse(open(path, 'rb'), content_type=content_type)
        response["Last-Modified"] = http_date(statobj.st_mtime)
        if stat.S_ISREG(statobj.st_mode):
            response["Content-Length"] = statobj.st_size
        if encoding:
            response["Content-Encoding"] = encoding
        response['Content-Disposition'] = 'inline; filename=' + urllib.quote(os.path.basename(path).encode('utf-8'))
        return response

    _files = []

    full_path = os.path.dirname(path)
    file_stat = os.stat(full_path)
    _files.append({
        'path': urllib.quote(full_path.encode('utf-8')),
        'is_dir': True,
        'name': '..',
        'size': file_stat.st_size,
        'date': format_time(file_stat.st_mtime)
    })

    file_names = os.listdir(path)
    for filename in file_names:
        full_path = os.path.join(path, filename)
        file_stat = os.stat(full_path)
        _files.append({
            'path': urllib.quote(full_path.encode('utf-8')),
            'is_dir': os.path.isdir(full_path),
            'name': filename,
            'size': file_stat.st_size,
            'date': format_time(file_stat.st_mtime)
        })

    return render(request, 'myutils/files.html', {
        'files': _files
    })
