from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^files/$', views.files),
    url(r'^pyinfo/$', views.pyinfo),
    url(r'^$', views.index),
]
