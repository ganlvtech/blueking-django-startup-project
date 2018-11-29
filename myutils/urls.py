from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^pyinfo/$', views.pyinfo, name='pyinfo'),
    url(r'^process/$', views.process, name='process'),
    url(r'^debug/$', views.debug_, name='debug'),
    url(r'^files/$', views.files, name='files'),
    url(r'^hosts/$', views.hosts, name='hosts'),
    url(r'^users/$', views.users, name='users'),
    url(r'^createsuperuser/$', views.manage_createsuperuser, name='createsuperuser'),
    url(r'^reset_db/$', views.manage_reset_db, name='reset_db'),
    url(r'^500/$', views.raise_500, name='raise_500'),
]
