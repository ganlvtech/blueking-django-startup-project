from .models import Counter


def visit_count(request):
    counter = Counter.objects.first()
    count = counter.value
    return {
        'visit_count': count
    }
