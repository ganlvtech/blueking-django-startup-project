from celery import shared_task

from .models import Counter


@shared_task
def add():
    counter = Counter.objects.get(pk=1)
    counter.value += 1
    counter.save()
    return counter.value
