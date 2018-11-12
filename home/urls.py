from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^files/$', views.files),
    url(r'^pyinfo/$', views.pyinfo),
    url(r'^docs/$', views.docs),
    url(r'^about/$', views.about),
    url(r'^hosts/$', views.hosts),
    url(r'^license/$', views.license),
    url(r'^$', views.index),
]
