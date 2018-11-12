from celery import shared_task

from .models import Counter


@shared_task
def add():
    counter = Counter.objects.first()
    counter.value += 1
    counter.save()
    return counter.value
