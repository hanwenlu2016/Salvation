# -*- coding: utf-8 -*-


import six

from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import Serializer

class JsResponse(Response):
    """
    自定义返回 函数
    JsResponse(data=[],code=200,msg="初始化成功",status=status.HTTP_200_OK)
     JsResponse(data=[],msg="初始化成功")
    """

    # code 默认200  状态200
    def __init__(self, data=None, code=200, msg=None,
                 status=status.HTTP_200_OK,
                 template_name=None, headers=None,
                 exception=False, content_type=None):

        super(Response, self).__init__(None, status=status)

        if isinstance(data, Serializer):
            msg = (
                'You passed a Serializer instance as data, but '
                'probably meant to pass serialized `.data` or '
                '`.error`. representation.'
            )
            # logger.error('You passed a Serializer instance as data, but '
            #              'probably meant to pass serialized `.data` or '
            #              '`.error`. representation.')
            raise AssertionError(msg)

        self.data = {"code": code, "msg": msg, "data": data}
        self.template_name = template_name
        self.exception = exception
        self.content_type = content_type

        if headers:
            for name, value in six.iteritems(headers):
                self[name] = value
