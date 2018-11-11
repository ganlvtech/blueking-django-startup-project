from django.http.response import HttpResponse, HttpResponseNotFound, HttpResponseForbidden
from django.shortcuts import render


def index(request):
    import markdown
    import os
    from io import open

    filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'docs/getting-started.md')
    with open(filename, 'r', encoding='utf-8') as f:
        data = f.read()
    getting_started = markdown.markdown(data, extensions=['fenced_code', 'tables'])

    filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'docs/faq.md')
    with open(filename, 'r', encoding='utf-8') as f:
        data = f.read()
    faq = markdown.markdown(data, extensions=['fenced_code', 'tables'])

    return render(request, 'home/index.html', {
        'getting_started': getting_started,
        'faq': faq,
    })


def docs(request):
    import markdown
    import os
    import re
    from io import open

    filename = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'README.md')
    with open(filename, 'r', encoding='utf-8') as f:
        data = f.read()
    html = markdown.markdown(data, extensions=['fenced_code', 'tables'])
    heading = re.match(r'<h1>(.*?)</h1>', html).group(1)
    html = re.sub(r'<h1>.*?</h1>', '', html)

    return render(request, 'home/docs.html', {
        'heading': heading,
        'html': html,
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
        html = re.sub(r'(BK_APP_PWD</td><td.*?>)(.*?)(</td>)', '\\1***\\3', html)
        html = re.sub(r'(amqp://.*?:)(.*?)(@)', '\\1***\\3', html)
        html = re.sub(r'(BK_SECRET_KEY</td><td.*?>)(.*?)(</td>)', '\\1***\\3', html)
    response.content = html

    return response


def files(request):
    import mimetypes
    import os
    from .utils import format_time

    path = request.GET.get('path', os.getcwd())

    if not os.path.exists(path):
        return HttpResponseNotFound()

    if 'secret' in path:
        return HttpResponseForbidden()

    if os.path.isfile(path):
        with open(path, 'rb') as fh:
            data = fh.read()
        response = HttpResponse(data)

        try:
            data.decode('utf-8')
            response['Content-Type'] = 'text/plain; charset=utf-8'
        except UnicodeDecodeError:
            mime = mimetypes.guess_type(path)
            if mime[0] is not None:
                response['Content-Type'] = mime[0]
            else:
                response['Content-Type'] = 'application/octet-stream'
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(path)
        return response

    _files = []

    full_path = path
    file_stat = os.stat(full_path)
    _files.append({
        'path': full_path,
        'is_dir': True,
        'name': '.',
        'size': file_stat.st_size,
        'date': format_time(file_stat.st_mtime)
    })

    full_path = os.path.dirname(path)
    file_stat = os.stat(full_path)
    _files.append({
        'path': full_path,
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
            'path': full_path,
            'is_dir': os.path.isdir(full_path),
            'name': filename,
            'size': file_stat.st_size,
            'date': format_time(file_stat.st_mtime)
        })

    return render(request, 'home/files.html', {'files': _files})
