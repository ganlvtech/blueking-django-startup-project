import os

from django.conf.urls import url
from django.views.static import serve

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^docs/$', views.docs, name='docs'),
    url(r'^about/$', views.about, name='about'),
    url(r'^license/$', views.license, name='license'),
    url(r'^favicon.ico$', serve, {
        'path': 'favicon.ico',
        'document_root': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
    }, name='favicon.ico'),
]
