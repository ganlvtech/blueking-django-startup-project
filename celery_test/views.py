from django.shortcuts import render

from . import tasks
from .models import Counter


def index(request):
    counter = Counter.objects.first()
    value = counter.value
    return render(request, 'celery_test/index.html', {
        'count': value
    })


def add(request):
    result = tasks.add.delay()
    return render(request, 'celery_test/add.html', {
        'id': str(result)
    })
