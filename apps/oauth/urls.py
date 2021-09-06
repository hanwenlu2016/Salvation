# -*- coding: utf-8 -*-
# @File: urls.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2021/8/10  11:28

from django.urls import path

from oauth.views.index_views import *
from oauth.views.signin_views import *
from oauth.views.user_views import *


urlpatterns = [
    path('', SignInView.as_view(), name='login'),
    path('register/', SignUpView.as_view(), name='register'),
    path('logout/', SignOutView.as_view(), name='logout'),
    path('index/', IndexView.as_view(), name='index'),
    path('userlist/', UserListView.as_view(), name='userlist'),
    path('user-add', UserCreateView.as_view(), name='user_add'),  # 新增用户
    path('user-update/<int:pk>/', UserUpdateView.as_view(), name="user_update"),  # 更新用户
    path('user-delete/<int:pk>/', UserDeleteView.as_view(), name="user_delete"),  # 删除用户

]
