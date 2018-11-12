from django.http.response import FileResponse, HttpResponseForbidden, HttpResponseNotFound, HttpResponseNotModified
from django.shortcuts import render


def index(request):
    import os
    from .utils import markdown_from_file

    getting_started_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'docs/getting-started.md')

    getting_started = markdown_from_file(getting_started_path)

    return render(request, 'home/index.html', {
        'getting_started': getting_started,
    })


def about(request):
    import os
    from .utils import markdown_from_file

    about_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'docs/about.md')
    about = markdown_from_file(about_path)

    return render(request, 'home/about.html', {
        'about': about
    })


def docs(request):
    import os
    from .utils import markdown_from_file

    docs_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'docs/docs.md')

    docs = markdown_from_file(docs_path)

    return render(request, 'home/docs.html', {
        'docs': docs
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


def license(request):
    import os

    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'LICENSE')

    if not os.path.isfile(path):
        content = ''
    else:
        with open(path, 'rb') as fh:
            data = fh.read()
        content = data.decode('utf-8')

    return render(request, 'home/plain_text.html', {
        'title': 'License',
        'heading': 'The MIT License',
        'content': content
    })


def pyinfo(request):
    import platform
    import re
    from mysite import secrets
    from .utils import my_pyinfo

    response = render(request, 'home/pyinfo.html', {
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
        import mimetypes
        import stat
        from django.utils.http import http_date
        from django.views.static import was_modified_since

        statobj = os.stat(path)
        if not was_modified_since(request.META.get('HTTP_IF_MODIFIED_SINCE'), statobj.st_mtime, statobj.st_size):
            return HttpResponseNotModified()

        content_type, encoding = mimetypes.guess_type(path)

        if not content_type:
            content_type = 'application/octet-stream'

            with open(path, 'rb') as fh:
                data = fh.read(4096)

            for i in range(0, 4):
                try:
                    if i == 0:
                        data.decode('utf-8')
                    else:
                        data[:-i].decode('utf-8')
                except UnicodeDecodeError:
                    pass
                else:
                    content_type = 'text/plain; charset=utf-8'
                    break

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

    return render(request, 'home/files.html', {'files': _files})
