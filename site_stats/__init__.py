try:
    from .models import Counter

    counter = Counter.objects.first()
    if not counter:
        counter = Counter()
        counter.save()
except:
    pass
