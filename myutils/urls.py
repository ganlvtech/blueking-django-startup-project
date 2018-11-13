from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^pyinfo/$', views.pyinfo, name='pyinfo'),
    url(r'^files/$', views.files, name='files'),
    url(r'^hosts/$', views.hosts, name='hosts'),
    url(r'^createsuperuser/$', views.manage_createsuperuser, name='createsuperuser'),
    url(r'^reset_db/$', views.manage_reset_db, name='reset_db'),
]
