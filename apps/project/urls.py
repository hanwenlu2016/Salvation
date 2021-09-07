# -*- coding: utf-8 -*-
# @File: urls.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2021/8/12  17:17

from django.urls import path

from project.views.project_views import *
from project.views.dev_views import *
from project.views.module_views import *

urlpatterns = [
    path('prlist/', ProjectListView.as_view(), name='prlist'),  # 项目列表
    path('project-particpant/<int:pk>/', ProjectParticpantDetailView.as_view(), name='project_particpant'),  # 参与项目列表
    path('project-dev/<int:pk>/', ProjectDevDetailView.as_view(), name='project_dev'),  # 项目部署信息详情
    path('project-add/', ProjectCreateView.as_view(), name='project_add'),  # 新增项目
    path('project-update/<int:pk>/', ProjectUpdateView.as_view(), name="project_update"),  # 更新项目
    path('project-delete/<int:pk>/', ProjectDeleteView.as_view(), name="prlist_delete"),  # 删除项目
    path('prldetai/<int:pk>/', ProjectDetailView.as_view(), name='prldetai'),  # 项目详情
    path('devlist/', DevListView.as_view(), name='devlist'),  # 项目部署列表
    path('dev-add/', DevCreateView.as_view(), name='dev_add'),  # 项目部署新增
    path('dev-update/<int:pk>/', DevUpdateView.as_view(), name="dev_update"),  # 更新项目
    path('dev-delete/<int:pk>/', DevDeleteView.as_view(), name="dev_delete"),  # 删除项目
    path('modulelist/', ModuleListView.as_view(), name='modulelist'),  # 模块列表
    path('module-add/', ModuleCreateView.as_view(), name='module_add'),  # 项目部署新增
    path('module-update/<int:pk>/', ModuleUpdateView.as_view(), name="module_update"),  # 更新项目
    path('module-delete/<int:pk>/', ModuleDeleteView.as_view(), name="module_delete"),  # 删除项目
]
