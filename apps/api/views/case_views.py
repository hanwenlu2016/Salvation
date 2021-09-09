# -*- coding: utf-8 -*-
# @File: case_views.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2021/9/7  16:04


from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..permissions import IsOwnerOrReadOnly
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from element.models import Case
from api.serializers import CaseListSerializer, CaseSerializer
from util.jsresponse import JsResponse


class CaseViewSet(viewsets.ModelViewSet):
    """
    用列信息接口
    """
    permission_classes = (IsAuthenticated,IsOwnerOrReadOnly)
    queryset = Case.objects.all()
    serializer_class = CaseSerializer

    # 设置三大常用过滤器之DjangoFilterBackend, SearchFilter

    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)

    # # 查询过滤

    search_fields = ('moduleid__module_name', 'title', 'casename', 'isdone', 'maintainer',)
    # 'moduleid__projcet__project_name', 项目名称
    # 外键上级 moduleid__projcet / moduleid外键

    # 选择过滤
    filter_fields = ('moduleid__projcet', 'moduleid', 'title', 'casename', 'isdone', 'maintainer',)

    # 重写 序列化返回类
    def get_serializer_class(self):

        if self.action == 'list':
            return CaseListSerializer
        else:
            return CaseSerializer

    def create(self, request, *args, **kwargs):

        # 判断用列是否重复
        is_title = Case.objects.filter(moduleid=request.data['moduleid'], title=request.data['title']).count()

        if is_title:
            print("用列已经存在")
            return JsResponse(data=[], msg="用列已经存在", code=300)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data = serializer.data
        print("新增用列成功")
        return JsResponse(data=data, msg="新增用列成功", headers=headers, code=200)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        print("删除成功")
        return JsResponse(data=[], msg="删除成功", code=200)
