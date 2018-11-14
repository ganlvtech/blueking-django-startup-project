from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^stream/$', views.stream, name='stream'),
    url(r'^nowait/$', views.nowait, name='nowait'),
]
