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
import home.urls
import myutils.urls

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^celery/', include(celery_test.urls)),
    url(r'^settings.py$', serve, {
        'path': 'settings.py',
        'document_root': os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    }),
    url(r'^favicon.ico$', serve, {
        'path': 'favicon.ico',
        'document_root': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
    }),
    url(r'^', include(myutils.urls)),
    url(r'^', include(home.urls)),
]
