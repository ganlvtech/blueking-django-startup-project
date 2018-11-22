from django.http import HttpResponse

from .models import Counter, VisitLog


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
            from site_stats.utils import get_client_ip
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
                else:
                    self.visit_log.response_length = -2
                self.visit_log.save()
        except Exception as e:
            print(e)

        return response
