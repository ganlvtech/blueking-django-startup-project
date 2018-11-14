"""djangotest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
import os

from django.conf.urls import include, url
from django.contrib import admin
from django.views.static import serve

import celery_test.urls
import file_upload.urls
import golang.urls
import home.urls
import myutils.urls

urlpatterns = [
    url(r'^settings.py$', serve, {
        'path': 'settings.py',
        'document_root': os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    }, name='settings.py'),
    url(r'^', include(home.urls, namespace='home')),
    url(r'^utils/', include(myutils.urls, namespace='utils')),
    url(r'^celery/', include(celery_test.urls, namespace='celery')),
    url(r'^upload/', include(file_upload.urls, namespace='upload')),
    url(r'^go/', include(golang.urls, namespace='golang')),
    url(r'^admin/', include(admin.site.urls)),
]
