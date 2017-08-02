# -*- coding:utf8 -*-
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
from users import views

urlpatterns = (
    url(r'user_detail/$', views.UserDetail.as_view()),
    url(r'user_list/$', views.UserList.as_view()),

    url(r'logout/$', views.AuthLogout.as_view()),
)

urlpatterns = format_suffix_patterns(urlpatterns)


