import os

from django.conf.urls import url
from django.conf.urls.static import serve

from . import views


urlpatterns = [
    url(r'^files/$', views.files),
    url(r'^pyinfo/$', views.pyinfo),
    url(r'^docs/$', views.docs),
    url(r'^favicon.ico$', serve, {
        'path': 'favicon.ico',
        'document_root': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/home/images')
    }),
    url(r'^$', views.index),
]
