# -*- coding: utf-8 -*-
# @File: location_views.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2021/9/9  11:40

from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from ..serializers import LocationTypeSerializer
from element.models import LocationType


class LocationTypeViewSet(viewsets.ModelViewSet):
    """
    定位类型接口
    """

    # permission_classes = (IsAuthenticated,)

    queryset = LocationType.objects.all()
    serializer_class = LocationTypeSerializer


    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)

    ## 选择过滤
    filter_fields = ('id','location_type')

