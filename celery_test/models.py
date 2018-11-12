from django.db import models


class Counter(models.Model):
    value = models.IntegerField(default=0)

    class Meta:
        app_label = 'celery_test'
