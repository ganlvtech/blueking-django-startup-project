from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^wait/$', views.wait, name='wait'),
    url(r'^nowait/$', views.nowait, name='nowait'),
]
