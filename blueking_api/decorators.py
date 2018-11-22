# coding=utf-8
from django.http import HttpResponseRedirect

from .blueking_api import BlueKingApi
from .middlewares import CheckLogin, FetchUserPermission, MustLogin
from .models import Permission


def check_login_blue_king(next_):
    def wrap(request):
        middleware = CheckLogin()
        middleware.process_request(request)
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


def check_permission(permission_name):
    def decorator(next_):
        def wrap(request):
            middleware = FetchUserPermission()
            middleware.process_request(request)
            permission_role = request.session.get('permission_role')
            if permission_role == 2:
                return next_(request)
            else:
                permission = request.session.get('permission')
                permission = Permission(permission)
                if permission.can(permission_name):
                    return next_(request)
            bkapi = BlueKingApi()
            return HttpResponseRedirect(bkapi.check_failed_url())
        return wrap

    return decorator
