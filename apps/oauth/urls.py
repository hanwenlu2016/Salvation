# -*- coding: utf-8 -*-
# @File: urls.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2021/8/10  11:28

from django.urls import path

from oauth.views import SignInView, SignOutView, SignUpView, HomeView, UserListView

urlpatterns = [
    path('login/', SignInView.as_view(), name='login'),
    path('register/', SignUpView.as_view(), name='register'),
    path('logout/', SignOutView.as_view(), name='logout'),
    path('index/', HomeView.as_view(), name='index'),
    path('userlist/', UserListView.as_view(), name='userlist'),
]
