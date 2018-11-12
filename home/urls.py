import os

from django.conf.urls import url
from django.conf.urls.static import serve

from . import views

urlpatterns = [
    url(r'^files/$', views.files),
    url(r'^pyinfo/$', views.pyinfo),
    url(r'^docs/$', views.docs),
    url(r'^hosts/$', views.hosts),
    url(r'^license/$', views.license),
    url(r'^settings.py$', serve, {
        'path': 'settings.py',
        'document_root': os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    }),
    url(r'^favicon.ico$', serve, {
        'path': 'favicon.ico',
        'document_root': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
    }),
    url(r'^$', views.index),
]
