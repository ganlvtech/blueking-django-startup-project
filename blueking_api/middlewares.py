from django.http import HttpResponseRedirect

from .blueking_api import BlueKingApi


class SaveOpenIdOpenKeyToSession(object):
    def process_request(self, request):
        openid = request.GET.get('openid')
        openkey = request.GET.get('openkey')
        if openid and openkey:
            request.session['openid'] = openid
            request.session['openkey'] = openkey


class MustLoginBlueKing(object):
    def process_request(self, request):
        bkapi = BlueKingApi()

        openid = request.session.get('openid')
        openkey = request.session.get('openkey')
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