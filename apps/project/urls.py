# -*- coding: utf-8 -*-
# @File: urls.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2021/8/12  17:17

from django.urls import path

from .views import ProjectListView

urlpatterns = [
    path('prlist/', ProjectListView.as_view(), name='prlist'),
 ]