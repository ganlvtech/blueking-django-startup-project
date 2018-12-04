# coding=utf-8
import os
import sys

from django.core.exceptions import ValidationError
from django.http import FileResponse, HttpResponseForbidden, HttpResponseNotFound, HttpResponseNotModified
from django.shortcuts import render

from blueking_api.decorators import must_login_blue_king
from home.utils import render_plain_text_content
from .utils.debug import get_safe_request, get_safe_settings


@must_login_blue_king
def manage_createsuperuser(request):
    from django.contrib.auth import get_user_model

    User = get_user_model()

    if User.objects.filter(is_superuser=1).count() > 0:
        return render(request, 'myutils/manage_createsuperuser.html', {
            'superuser_exists': True
        })

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


@must_login_blue_king
def manage_reset_db(request):
    from django.db import connection
    from django.core.management import execute_from_command_line
    from django.contrib.auth import get_user_model
    from django.contrib.auth.hashers import check_password

    if request.method == 'GET':
        return render(request, 'myutils/manage_reset_db.html')

    username = request.POST.get('username')
    password = request.POST.get('password')
    confirm = request.POST.get('confirm')

    errors = []
    if not username:
        errors.append(ValidationError('username must be set'))
    if not password:
        errors.append(ValidationError('password must be set'))
    if not confirm:
        errors.append(ValidationError('confirm must be set'))
    if errors:
        raise ValidationError(errors)

    if confirm != 'Reset Database':
        return render(request, 'myutils/manage_reset_db.html', {
            'confirm_wrong': True
        })

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


@must_login_blue_king
def hosts(request):
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

    return render_plain_text_content(request, u'hosts', path.decode('utf-8'), content)


@must_login_blue_king
def users(request):
    if os.name == 'posix':
        users_path = '/etc/passwd'
        with open(users_path, 'rb') as fh:
            data = fh.read()
        users = data.decode('utf-8')

        groups_path = '/etc/group'
        with open(groups_path, 'rb') as fh:
            data = fh.read()
        groups = data.decode('utf-8')

        content = '{}\n\n{}\n\n\n{}\n\n{}'.format(users_path, users, groups_path, groups)
    else:
        content = 'Only available on Linux.'

    return render_plain_text_content(request, u'Users And Groups', u'用户和用户组', content)


@must_login_blue_king
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


@must_login_blue_king
def process(request):
    import subprocess

    if os.name == 'posix':
        args = ['ps', 'aux']
    else:
        args = ['tasklist', '/V']
    encoding = sys.getfilesystemencoding()
    output = subprocess.check_output(args).decode(encoding)

    return render_plain_text_content(request, u'Process List', u'进程列表', output)


@must_login_blue_king
def netstat(request):
    import subprocess

    if os.name == 'posix':
        args = ['netstat', '-anp']
    else:
        args = ['netstat', '-ano']
    encoding = sys.getfilesystemencoding()
    output = subprocess.check_output(args).decode(encoding)

    return render_plain_text_content(request, u'Network Statistics', u'网络统计', output)


@must_login_blue_king
def files(request):
    from six.moves import urllib
    from .utils import format_time

    path = request.GET.get('path', os.getcwd())
    abs_path = os.path.abspath(path)

    if not os.path.exists(abs_path):
        import base64
        try:
            path = base64.b64decode(path)
            abs_path = os.path.abspath(path)
            if not os.path.exists(abs_path):
                return HttpResponseNotFound()
        except TypeError:
            return HttpResponseNotFound()

    path = abs_path

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
        response['Content-Disposition'] = 'inline; filename=' + urllib.parse.quote(os.path.basename(path).encode('utf-8'))
        return response

    _files = []

    full_path = os.path.dirname(path)
    file_stat = os.stat(full_path)

    _files.append({
        'path': urllib.parse.quote(full_path.encode('utf-8')),
        'is_dir': True,
        'name': '..',
        'uid': file_stat.st_uid,
        'gid': file_stat.st_gid,
        'mode': oct(file_stat.st_mode & 0o777),
        'size': file_stat.st_size,
        'date': format_time(file_stat.st_mtime)
    })

    file_names = os.listdir(path)
    for filename in file_names:
        full_path = os.path.join(path, filename)
        file_stat = os.stat(full_path)
        _files.append({
            'path': urllib.parse.quote(full_path.encode('utf-8')),
            'is_dir': os.path.isdir(full_path),
            'name': filename,
            'uid': file_stat.st_uid,
            'gid': file_stat.st_gid,
            'mode': oct(file_stat.st_mode & 0o777),
            'size': file_stat.st_size,
            'date': format_time(file_stat.st_mtime)
        })

    return render(request, 'myutils/files.html', {
        'files': _files
    })


@must_login_blue_king
def debug_(request):
    import pprint

    content = 'request =\n' + pprint.pformat(get_safe_request(request)) + \
              '\n\n\nsettings =\n' + pprint.pformat(get_safe_settings())
    return render_plain_text_content(request, u'Debug Info', u'调试信息', content)


def raise_500(request):
    raise Exception('Self raised 500 exception')
