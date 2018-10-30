import django
from django.http.response import HttpResponse
import mysite.pyinfo

def pyinfo(request):
    return HttpResponse(mysite.pyinfo.pyinfo())

def index(request):
    return HttpResponse("Hello, Django %s!" % (django.get_version()))
