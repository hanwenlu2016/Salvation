# -*- coding: utf-8 -*-
# @File: urls.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2021/9/7  15:40

from rest_framework.routers import DefaultRouter
from api.views.case_views import CaseViewSet


router = DefaultRouter()

router.register(r'case', CaseViewSet, basename='case')
