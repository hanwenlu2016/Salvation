# -*- coding: utf-8 -*-
# @File: urls.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2021/8/12  17:17

from django.urls import path

from .views import ProjectListView, ProjectDetailView,ProjectParticpantDetailView,ProjectCreateView

urlpatterns = [
    path('prlist/', ProjectListView.as_view(), name='prlist'), #项目列表
    path('project_particpant/<int:pk>/', ProjectParticpantDetailView.as_view(), name='project_particpant'), # 参与项目
    path('project_add', ProjectCreateView.as_view(), name='project_add'),  # 新增项目
    path('prldetai/<int:pk>/', ProjectDetailView.as_view(), name='prldetai'), # 项目详情
]
