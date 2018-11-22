import subprocess

from django.http import StreamingHttpResponse
from django.shortcuts import render

from .helpers import get_go_program_path


def index(request):
    path = get_go_program_path()
    output = subprocess.check_output([path])
    return render(request, 'golang/index.html', {
        'content': output
    })


def stream(request):
    if not request.GET.get('stream'):
        return render(request, 'golang/stream.html')

    path = get_go_program_path()
    proc = subprocess.Popen([path], stdout=subprocess.PIPE)

    def iterator():
        while True:
            line = proc.stdout.readline()
            if line != '':
                yield 'data: {}\n\n'.format(line)
            else:
                break

    response = StreamingHttpResponse(iterator(), content_type="text/event-stream")
    response['Cache-Control'] = 'no-cache'

    return response


def nowait(request):
    path = get_go_program_path()
    proc = subprocess.Popen([path], close_fds=True)
    return render(request, 'golang/nowait.html', {
        'pid': proc.pid
    })
