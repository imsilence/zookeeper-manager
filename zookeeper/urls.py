#!/usr/bin/env python
#encoding: utf-8

from django.conf.urls import url

import views

urlpatterns = [
    url(r'^$|^index/', views.index, name='index'),
    url(r'^detail/', views.detail, name='detail'),
    url(r'^update/', views.update, name='update'),
    url(r'^create/', views.create, name='create'),
    url(r'^delete/', views.delete, name='delete'),
]
