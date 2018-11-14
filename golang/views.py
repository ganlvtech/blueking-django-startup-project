import os
import subprocess

from django.http import HttpResponse

from .helpers import get_go_program_path


def index(request):
    path = get_go_program_path()
    os.chmod(path, 0o755)
    exit_status = os.system(path)
    return HttpResponse(exit_status)


def wait(request):
    path = get_go_program_path()
    os.chmod(path, 0o755)
    proc = subprocess.Popen([path], stdout=subprocess.PIPE)
    (out, err) = proc.communicate()
    return HttpResponse(out)


def nowait(request):
    path = get_go_program_path()
    os.chmod(path, 0o755)
    proc = subprocess.Popen([path])
    return HttpResponse(proc.pid)
