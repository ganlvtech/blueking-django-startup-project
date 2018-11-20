from .middlewares import MustLoginBlueKing


def must_login_blue_king(next_):
    def wrap(request):
        must_login = MustLoginBlueKing()
        must_login.process_request(request)
        return next_(request)

    return wrap
