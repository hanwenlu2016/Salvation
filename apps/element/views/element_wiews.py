# -*- coding: utf-8 -*-
# @File: element_wiews.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2021/9/10  10:39


from util.loginmixin import LoginMixin
from django.views.generic import  ListView

from ..models import Case

class ElementListView(LoginMixin, ListView):
    """
    项目列表 视图
    """
    model = Case
    context_object_name = 'project'
    template_name = "element/element_list.html"
