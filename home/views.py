from django.http.response import HttpResponse, Http404
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


def files(request):
    import os
    import datetime
    from mysite import secrets

    path = request.GET.get('path', os.getcwd())

    if not os.path.exists(path):
        raise Http404

    if os.path.isfile(path):
        if request.GET.get('password') != secrets.DOWNLOAD_PASSWORD:
            return HttpResponse('Password wrong! File downloading is not allowed.')
        with open(path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type='application/force-download')
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(path)
            return response

    file_names = os.listdir(path)
    _files = []
    for filename in file_names:
        full_path = os.path.join(path, filename)
        file_stat = os.stat(full_path)
        _files.append({
            'full_path': full_path,
            'is_dir': os.path.isdir(full_path),
            'name': filename,
            'size': file_stat.st_size,
            'date': str(datetime.datetime.utcfromtimestamp(file_stat.st_mtime))
        })
    return render(request, 'home/files.html', {'files': _files})
