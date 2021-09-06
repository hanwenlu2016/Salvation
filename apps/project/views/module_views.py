# -*- coding: utf-8 -*-
# @File: module_ciews.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2021/9/2  15:11

# 模块详情视图 类

from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView,UpdateView, DeleteView
from django.core.paginator import Paginator
from project.forms.module_from import ModuleCreateForm,ModuleUpdateForm
from project.models import Module

from util.loginmixin import LoginMixin

class ModuleListView(LoginMixin, ListView):
    """
    模块信息列表 视图
    """
    model = Module
    context_object_name = 'project_module'
    template_name = "project_manage/module/module_list.html"
    search_value = ""
    order_field = "-module_alias"
    created_by = ''
    pagenum = 5  # 每页分页数据条数

    def get_queryset(self):
        search = self.request.GET.get("search")
        order_by = self.request.GET.get("orderby")
        filter_isenabled = self.request.GET.get("created_by")

        if order_by:
            module_pro = Module.objects.all().order_by(order_by)
            self.order_field = order_by
        else:
            module_pro = Module.objects.all().order_by(self.order_field)

        if filter_isenabled:
            self.created_by = filter_isenabled
            module_pro = Module.objects.filter(isenabled=self.created_by)

        if search:
            # 项目名称 、创建人、项目负责人、项目负责人姓名查询
            module_pro = module_pro.filter(
                Q(prjname__icontains=search) | Q(prjalias__icontains=search))
            self.search_value = search

        self.count_total = module_pro.count()
        paginator = Paginator(module_pro, self.pagenum)
        page = self.request.GET.get('page')
        project_module = paginator.get_page(page)
        return project_module

    def get_context_data(self, *args, **kwargs):
        context = super(ModuleListView, self).get_context_data(*args, **kwargs)
        context['count_total'] = self.count_total
        context['search'] = self.search_value
        context['orderby'] = self.order_field
        context['objects'] = self.get_queryset()
        context['created_by'] = self.created_by
        return context

class ModuleCreateView(LoginMixin, CreateView):
    """
    添加环境 视图
    """
    model = Module
    form_class = ModuleCreateForm
    template_name = "project_manage/module/module_add.html"

    def get_form_kwargs(self):
        # Ensure the current `request` is provided to ProjectCreateForm.
        kwargs = super(ModuleCreateView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs


class ModuleUpdateView(LoginMixin, UpdateView):
    """
    更新项目
    """
    model = Module
    form_class = ModuleUpdateForm
    template_name = "project_manage/module/module_update.html"

    def get_form_kwargs(self):
        # Ensure the current `request` is provided to ProjectCreateForm.
        kwargs = super(ModuleUpdateView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs


class ModuleDeleteView(LoginMixin, DeleteView):
    """
    删除项目
    """
    #template_name_suffix='_delete'
    template_name = "project_manage/module/module_delete.html"
    model = Module
    success_url = reverse_lazy('modulelist')
