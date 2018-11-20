from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^get_app_access_token/$', views.get_app_access_token, name='get_app_access_token'),
    url(r'^get_user_access_token/$', views.get_user_access_token, name='get_user_access_token'),
    url(r'^refresh_user_access_token/$', views.refresh_user_access_token, name='refresh_user_access_token'),
    url(r'^get_user_info/$', views.get_user_info, name='get_user_info'),
    url(r'^get_openid_openkey/$', views.get_openid_openkey, name='get_openid_openkey'),
    url(r'^verify_openid_openkey/$', views.verify_openid_openkey, name='verify_openid_openkey'),
    url(r'^get_auth_token/$', views.get_auth_token, name='get_auth_token'),
    url(r'^send_email/$', views.send_email, name='send_email'),
    url(r'^send_sms/$', views.send_sms, name='send_sms'),
]
