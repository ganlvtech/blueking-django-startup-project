from django.conf.urls import url
from django.views.static import serve

from mysite import settings
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^delete/$', views.delete, name='delete'),
    url(r'^files/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    }, name='serve'),
]
