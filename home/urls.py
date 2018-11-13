from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^docs/$', views.docs, name='docs'),
    url(r'^about/$', views.about, name='about'),
    url(r'^license/$', views.license, name='license'),
]
