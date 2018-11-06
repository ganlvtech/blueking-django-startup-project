from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^manage/createsuperuser/$', views.manage_createsuperuser),
    url(r'^manage/reset_db/$', views.manage_reset_db),
    url(r'^manage/$', views.index),
]
