from django.http.response import HttpResponse
from .models import Counter
from . import tasks


def index(request):
    value = Counter.objects.get(pk=1).value
    return HttpResponse(value)


def add(request):
    result = tasks.add.delay()
    return HttpResponse(result)

