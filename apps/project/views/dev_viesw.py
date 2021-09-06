# -*- coding: utf-8 -*-
# @File: dev_viesw.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2021/9/2  15:09

# 部署信息视图 类

from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.core.paginator import Paginator
from project.forms.dev_from import DevCreateForm,DevUpdateForm
from project.models import DeployInfo

from util.loginmixin import LoginMixin


class DevListView(LoginMixin, ListView):
    """
    项目部署信息列表 视图
    """
    model = DeployInfo
    context_object_name = 'project_dev'
    template_name = "project_manage/dev/dev_list.html"
    search_value = ""
    order_field = "-prjalias"
    created_by = ''
    pagenum = 5  # 每页分页数据条数

    def get_queryset(self):
        search = self.request.GET.get("search")
        order_by = self.request.GET.get("orderby")
        filter_isenabled = self.request.GET.get("created_by")

        if order_by:
            dev_pro = DeployInfo.objects.all().order_by(order_by)
            self.order_field = order_by
        else:
            dev_pro = DeployInfo.objects.all().order_by(self.order_field)

        if filter_isenabled:
            self.created_by = filter_isenabled
            dev_pro = DeployInfo.objects.filter(isenabled=self.created_by)

        if search:
            # 项目名称 、创建人、项目负责人、项目负责人姓名查询
            dev_pro = dev_pro.filter(
                Q(prjname__icontains=search) | Q(prjalias__icontains=search))
            self.search_value = search

        self.count_total = dev_pro.count()
        paginator = Paginator(dev_pro, self.pagenum)
        page = self.request.GET.get('page')
        project_dev = paginator.get_page(page)
        return project_dev

    def get_context_data(self, *args, **kwargs):
        context = super(DevListView, self).get_context_data(*args, **kwargs)
        context['count_total'] = self.count_total
        context['search'] = self.search_value
        context['orderby'] = self.order_field
        context['objects'] = self.get_queryset()
        context['created_by'] = self.created_by
        return context


class DevCreateView(LoginMixin, CreateView):
    """
    添加环境 视图
    """
    model = DeployInfo
    form_class = DevCreateForm
    template_name = "project_manage/dev/dev_add.html"

    def get_form_kwargs(self):
        # Ensure the current `request` is provided to ProjectCreateForm.
        kwargs = super(DevCreateView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

class DevUpdateView(LoginMixin, UpdateView):
    """
    更新项目
    """
    model = DeployInfo
    form_class = DevUpdateForm
    template_name = "project_manage/dev/dev_update.html"

    def get_form_kwargs(self):
        # Ensure the current `request` is provided to ProjectCreateForm.
        kwargs = super(DevUpdateView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs


class DevDeleteView(LoginMixin, DeleteView):
    """
    删除项目
    """
    #template_name_suffix='_delete'
    template_name = "project_manage/dev/dev_delete.html"
    model = DeployInfo
    success_url = reverse_lazy('devlist')
