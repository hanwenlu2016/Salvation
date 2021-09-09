# -*- coding: utf-8 -*-
# @File: project_views.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2021/9/9  11:56

from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from ..serializers import ProjectSerializer
from project.models import Project


class ProjectViewSet(mixins.ListModelMixin,viewsets.GenericViewSet):
    """
    项目信息接口
    """
    permission_classes = (IsAuthenticated,)
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)

    ## 选择过滤
    filter_fields = ('id','project_name','isenabled','version')
