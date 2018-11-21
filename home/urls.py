import os

from django.conf.urls import url
from django.views.static import serve

from . import views

urlpatterns = [
    url(r'^settings.py$', serve, {
        'path': 'settings.py',
        'document_root': os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    }, name='settings.py'),
    url(r'^$', views.index, name='index'),
    url(r'^docs/$', views.docs, name='docs'),
    url(r'^demos/$', views.demos, name='demos'),
    url(r'^about/$', views.about, name='about'),
    url(r'^license/$', views.license, name='license'),
    url(r'^favicon.ico$', serve, {
        'path': 'favicon.ico',
        'document_root': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
    }, name='favicon.ico'),
]
