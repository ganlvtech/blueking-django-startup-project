from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render

from .models import VisitLog


def index(request):
    paginator = Paginator(VisitLog.objects.order_by('-id').all(), 25)
    page = request.GET.get('page')
    try:
        logs = paginator.page(page)
    except PageNotAnInteger:
        logs = paginator.page(1)
    except EmptyPage:
        logs = paginator.page(paginator.num_pages)

    limit = 4
    current_page = logs.number
    num_pages = paginator.num_pages
    paginator_pages = []
    for p in range(1, num_pages + 1):
        if 1 <= p < 1 + limit or current_page - limit <= p <= current_page + limit or num_pages - limit < p <= num_pages:
            paginator_pages.append(p)
        else:
            if paginator_pages[-1] > 0:
                paginator_pages.append(-1)

    return render(request, 'site_stats/index.html', {
        'logs': logs,
        'paginator_pages': paginator_pages,
    })
