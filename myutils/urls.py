from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^pyinfo/$', views.pyinfo, name='pyinfo'),
    url(r'^process/$', views.process, name='process'),
    url(r'^request/$', views.request_, name='request'),
    url(r'^files/$', views.files, name='files'),
    url(r'^hosts/$', views.hosts, name='hosts'),
    url(r'^users/$', views.users, name='users'),
    url(r'^createsuperuser/$', views.manage_createsuperuser, name='createsuperuser'),
    url(r'^reset_db/$', views.manage_reset_db, name='reset_db'),
]
