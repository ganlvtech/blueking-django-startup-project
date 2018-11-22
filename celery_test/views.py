from django.shortcuts import render
from djcelery.models import TaskMeta

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
        'task_id': str(result)
    })


def status(request):
    task_id = request.GET.get('task_id')
    task_meta = TaskMeta.objects.filter(task_id=task_id).first()
    return render(request, 'celery_test/status.html', {
        'task_id': task_id,
        'task_meta': task_meta,
    })
