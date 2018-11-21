from .middlewares import CheckLogin, MustLogin


def check_login_blue_king(next_):
    def wrap(request):
        middleware = CheckLogin()
        response = middleware.process_request(request)
        if response:
            return response
        return next_(request)

    return wrap


def must_login_blue_king(next_):
    def wrap(request):
        middleware = MustLogin()
        response = middleware.process_request(request)
        if response:
            return response
        return next_(request)

    return wrap
