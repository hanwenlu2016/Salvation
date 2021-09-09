# -*- coding: utf-8 -*-
# @File: permissions.py.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2021/9/9  14:51

from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    message = "您没有此权限!"

    def has_object_permission(self, request, view, obj):
        # 必须是超级管理员才能删除
        if request.user.is_superuser != 1:
            return False
        return True
