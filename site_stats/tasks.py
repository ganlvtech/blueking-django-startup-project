from celery import shared_task

from site_stats.models import VisitLog


@shared_task
def clear_visit_log(limit=10000):
    count = VisitLog.objects.count()
    if limit < count:
        limit = count
    min_id = VisitLog.objects.order_by('-id').all()[limit].id
    to_be_deleted = VisitLog.objects.filter(id__lt=min_id)
    count = to_be_deleted.count()
    to_be_deleted.delete()
    return count
