from django.db import models


class Counter(models.Model):
    value = models.IntegerField(default=0)

    class Meta:
        app_label = 'site_stats'


class VisitLog(models.Model):
    user_id = models.CharField(max_length=128, default='')
    user_info = models.CharField(max_length=255, default='')
    path = models.CharField(max_length=1024, default='')
    method = models.CharField(max_length=20, default='')
    ip = models.CharField(max_length=40, default='')
    user_agent = models.CharField(max_length=1024, default='')
    query = models.CharField(max_length=1024, default='')
    body = models.CharField(max_length=4096, default='')
    response_code = models.IntegerField(default=0)
    response_length = models.IntegerField(default=0)
    response_body = models.CharField(max_length=4096, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'site_stats'
