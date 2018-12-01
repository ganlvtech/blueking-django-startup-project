# coding=utf-8
import re

from django.http.response import HttpResponseRedirect

from .blueking_api import BlueKingApi


class CheckLogin(object):
    def process_request(self, request):
        bkapi = BlueKingApi()
        openid = request.session.get('openid')
        openkey = request.session.get('openkey')
        if not openid or not openkey:
            openid = request.GET.get('openid')
            openkey = request.GET.get('openkey')
            if not openid or not openkey:
                uin = request.COOKIES.get('uin')
                skey = request.COOKIES.get('skey')
                if not uin or not skey:
                    return
                api_response = bkapi.get_openid_openkey(uin, skey)
                openid = api_response['data']['openid']
                openkey = api_response['data']['openkey']
            request.session['openid'] = openid
            request.session['openkey'] = openkey
        nick_name = request.session.get('nick_name')
        avatar_url = request.session.get('avatar_url')
        if not nick_name or not avatar_url:
            api_response = bkapi.get_user_info(openid, openkey)
            request.session['nick_name'] = api_response['data']['nick_name']
            request.session['avatar_url'] = api_response['data']['avatar_url']
            if request.is_secure():
                request.session['avatar_url'] = re.sub(r'^http://', 'https://', request.session['avatar_url'])


class MustLogin(object):
    def process_request(self, request):
        bkapi = BlueKingApi()
        openid = request.session.get('openid')
        openkey = request.session.get('openkey')
        if not openid or not openkey:
            openid = request.GET.get('openid')
            openkey = request.GET.get('openkey')
            if not openid or not openkey:
                uin = request.COOKIES.get('uin')
                skey = request.COOKIES.get('skey')
                if not uin or not skey:
                    return HttpResponseRedirect(bkapi.develop_login_url(request.build_absolute_uri()))
                api_response = bkapi.get_openid_openkey(uin, skey)
                openid = api_response['data']['openid']
                openkey = api_response['data']['openkey']
            request.session['openid'] = openid
            request.session['openkey'] = openkey
        nick_name = request.session.get('nick_name')
        avatar_url = request.session.get('avatar_url')
        if not nick_name or not avatar_url:
            api_response = bkapi.get_user_info(openid, openkey)
            request.session['nick_name'] = api_response['data']['nick_name']
            request.session['avatar_url'] = api_response['data']['avatar_url']
            if request.is_secure():
                request.session['avatar_url'] = re.sub(r'^http://', 'https://', request.session['avatar_url'])


class FetchUserPermission(object):
    """获取用户拥有权限

    必须放在 CheckLogin 或 MustLogin 之后
    """

    def process_request(self, request):
        permission = request.session.get('permission')
        permission_role = request.session.get('permission_role')
        if not permission or not permission_role:
            openid = request.session.get('openid')
            if not openid:
                return
            bkapi = BlueKingApi()
            api_response = bkapi.get_permissions(openid)
            request.session['permission'] = api_response['permission']
            request.session['permission_role'] = api_response['permission_role']
