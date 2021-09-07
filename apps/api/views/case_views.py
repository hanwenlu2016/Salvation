# -*- coding: utf-8 -*-
# @File: case_views.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2021/9/7  16:04

from rest_framework import viewsets

from element.models import Case
from api.serializers import CaseListSerializer, CaseSerializer
from util.jsresponse import JsResponse


class CaseViewSet(viewsets.ModelViewSet):
    """
    用列信息接口
    """
    queryset = Case.objects.all()
    serializer_class = CaseSerializer

    # 重写 序列化返回类
    def get_serializer_class(self):

        if self.action == 'list':
            return CaseListSerializer
        else:
            return CaseSerializer

    def create(self, request, *args, **kwargs):
        if Case.objects.filter(title=request.data['title']).count():
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
