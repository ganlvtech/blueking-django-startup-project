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
            'about': path_info == '/about/',
            'license': path_info == '/license/',
            'utils': path_info in (
                '/pyinfo/',
                '/files/',
                '/hosts/',
                '/manage/createsuperuser/',
                '/manage/reset_db/',
            ),
        }
    }
