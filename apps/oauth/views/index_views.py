# -*- coding: utf-8 -*-
# @File: index_ciews.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2021/9/2  16:52

from django.shortcuts import render
from django.views.generic import TemplateView
from util.loginmixin import LoginMixin

from oauth.models import Users


class IndexView(LoginMixin, TemplateView):
    """
    首页 视图
    """
    template_name = "accounts/index.html"
    context = {}

    def get(self, request, *args, **kwargs):
        data_count = {
            "userlist": Users.objects.all().order_by('-last_login')[:5],  # 只取登录时间的默认5
            "member": Users.objects.all().count(),
        }
        self.context['data_count'] = data_count
        return render(request, self.template_name, self.context)
