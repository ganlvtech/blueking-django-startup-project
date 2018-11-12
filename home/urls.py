from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^docs/$', views.docs),
    url(r'^about/$', views.about),
    url(r'^license/$', views.license),
]
