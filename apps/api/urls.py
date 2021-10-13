# -*- coding: utf-8 -*-
# @File: urls.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2021/9/7  15:40

from rest_framework.routers import DefaultRouter
from api.views.case_views import CaseViewSet
from api.views.location_views import LocationTypeViewSet
from api.views.operate_views import OperateTypeViewSet
from api.views.project_views import ProjectViewSet
from api.views.moudle_views import ModuleViewSet

# app_name='api'

router = DefaultRouter()

router.register(r'case', CaseViewSet, basename='case',)

router.register(r'locatype', LocationTypeViewSet, basename='locatype')

router.register(r'opertype', OperateTypeViewSet, basename='opertype')

router.register(r'project', ProjectViewSet, basename='project')

router.register(r'module', ModuleViewSet, basename='module')

