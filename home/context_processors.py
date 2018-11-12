from django.conf import settings

def blueking(request):
    result = {}

    try:
        result['REMOTE_STATIC_URL'] = settings.REMOTE_STATIC_URL
    except AttributeError:
        pass

    return result

