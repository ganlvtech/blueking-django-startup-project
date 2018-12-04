from django.http.response import HttpResponseForbidden

from .models import Counter, VisitLog
from .utils import get_client_ip


class SiteStatistics(object):
    visit_log = None

    def process_request(self, request):
        if request.path_info.startswith('/admin/'):
            return

        counter = Counter.objects.first()
        counter.value += 1
        counter.save()

        try:
            self.visit_log = VisitLog()
            self.visit_log.user_id = request.session.get('openid', '')[:128]
            user_info = ''
            openkey = request.session.get('openkey', '')
            nick_name = request.session.get('nick_name', '')
            if openkey or nick_name:
                user_info = nick_name + ' ' + openkey
            self.visit_log.user_info = user_info[:255]
            self.visit_log.path = request.path[:1024]
            self.visit_log.method = request.method
            self.visit_log.ip = get_client_ip(request)
            self.visit_log.user_agent = request.META['HTTP_USER_AGENT'][:1024]
            self.visit_log.query = request.META['QUERY_STRING'][:1024]
            self.visit_log.body = request.body[:4096]
            self.visit_log.response_length = -1
            self.visit_log.save()
        except Exception as e:
            print(e)

    def process_response(self, request, response):
        try:
            if self.visit_log:
                self.visit_log.response_code = response.status_code
                if hasattr(response, 'content'):
                    self.visit_log.response_length = len(response.content)
                    self.visit_log.response_body = response.content[:4096]
                elif 'Content-Length' in response:
                    self.visit_log.response_length = response['Content-Length']
                else:
                    self.visit_log.response_length = -2
                self.visit_log.save()
        except Exception as e:
            print(e)

        return response


class BanUser(object):
    ban_openid_list = (
        "144115212352913603",
    )
    ban_nick_name_list = (
        "453413024",
    )
    ban_ip_list = (
        "116.228.88.252",
    )

    def process_request(self, request):
        ip = get_client_ip(request)
        if ip in self.ban_ip_list:
            return HttpResponseForbidden('Banned IP')
        openid = request.session.get('openid')
        if openid and openid in self.ban_openid_list:
            return HttpResponseForbidden('Banned openid')
        nick_name = request.session.get('nick_name')
        if nick_name and nick_name in self.ban_nick_name_list:
            return HttpResponseForbidden('Banned QQ')
