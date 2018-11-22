from django.conf import settings


def blueking(request):
    result = {}

    try:
        result['REMOTE_STATIC_URL'] = settings.REMOTE_STATIC_URL
    except AttributeError:
        pass

    return result


def navbar(request):
    path_info = request.path_info
    return {
        'navbar': {
            'index': path_info == '/',
            'docs': path_info == '/docs/',
            'bkapi': path_info.startswith('/bkapi/'),
            'demos': path_info == '/demos/'
                     or path_info.startswith('/utils/')
                     or path_info.startswith('/stats/')
                     or path_info.startswith('/celery/')
                     or path_info.startswith('/upload/')
                     or path_info.startswith('/go/')
                     or path_info.startswith('/mail/'),
            'about': path_info == '/about/',
            'license': path_info == '/license/',
        }
    }
