from django.http.response import HttpResponse

from . import tasks
from .models import Counter


def index(request):
    counter = Counter.objects.first()
    value = counter.value
    return HttpResponse(value)


def add(request):
    result = tasks.add.delay()
    return HttpResponse(result)
