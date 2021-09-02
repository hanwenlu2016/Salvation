# -*- coding: utf-8 -*-
# @File: dep_views.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2021/9/2  17:35

# 部门视图类
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import  CreateView, ListView, UpdateView, DeleteView

from mixins.loginmixin import LoginMixin
from ..models import Department

class DepListView(LoginMixin, ListView):
    """
    部门列表 视图
    """

    model = Department
    context_object_name = 'dep'
    template_name = "oauth/dep/dep_list.html"
    search_value = ""
    order_field = "-id"
    created_by = ''
    pagenum = 5  # 每页分页数据条数

    def get_queryset(self):
        search = self.request.GET.get("search")
        order_by = self.request.GET.get("orderby")
        filter_gender = self.request.GET.get("created_by")

        if order_by:
            all_dep = Department.objects.all().order_by(order_by)
            self.order_field = order_by
        else:
            all_dep = Department.objects.all().order_by(self.order_field)

        if filter_gender:
            self.created_by = filter_gender
            all_dep = Department.objects.filter(gender=self.created_by)

        if search:
            # 项目名称 、创建人、项目负责人、项目负责人姓名查询
            all_dep = all_dep.filter(
                Q(name__icontains=search) | Q(username__icontains=search) | Q(
                    mobile__icontains=search))
            self.search_value = search

        self.count_total = all_dep.count()
        paginator = Paginator(all_dep, self.pagenum)
        page = self.request.GET.get('page')
        dep = paginator.get_page(page)
        return dep

    def get_context_data(self, *args, **kwargs):
        context = super(DepListView, self).get_context_data(*args, **kwargs)
        context['count_total'] = self.count_total
        context['search'] = self.search_value
        context['orderby'] = self.order_field
        context['objects'] = self.get_queryset()
        context['created_by'] = self.created_by
        return context
