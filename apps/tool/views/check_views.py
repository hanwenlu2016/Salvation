# -*- coding: utf-8 -*-
# @File: check_views.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2021/10/13  11:35

import os.path
import shutil

from django.db.models import Q
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

from django.views.generic import CreateView, ListView, DeleteView
from django.core.paginator import Paginator
from tool.forms.check_from import CheckTaskForm
from tool.models import CheckTask

from util.loginmixin import LoginMixin
from util.loggers import logger
from tool import tasks

class CheckTaskListView(LoginMixin, ListView):
    """
    扫描信息信息列表 视图
    """
    model = CheckTask
    context_object_name = 'check'
    template_name = "tool/dependency_check/dependency_check_list.html"
    search_value = ""
    order_field = "-createtime"
    created_by = ''
    pagenum = 5  # 每页分页数据条数

    def get_queryset(self):
        search = self.request.GET.get("search")
        order_by = self.request.GET.get("orderby")
        filter_isenabled = self.request.GET.get("created_by")

        if order_by:
            check_pro = CheckTask.objects.all().order_by(order_by)
            self.order_field = order_by
        else:
            check_pro = CheckTask.objects.all().order_by(self.order_field)

        if filter_isenabled:
            self.created_by = filter_isenabled
            check_pro = CheckTask.objects.filter(isenabled=self.created_by)

        if search:
            # 任务名称 、创建人、
            check_pro = check_pro.filter(
                Q(check_name__icontains=search) | Q(creator__icontains=search))
            self.search_value = search

        self.count_total = check_pro.count()
        paginator = Paginator(check_pro, self.pagenum)
        page = self.request.GET.get('page')
        project_dev = paginator.get_page(page)
        return project_dev

    def get_context_data(self, *args, **kwargs):
        context = super(CheckTaskListView, self).get_context_data(*args, **kwargs)
        context['count_total'] = self.count_total
        context['search'] = self.search_value
        context['orderby'] = self.order_field
        context['objects'] = self.get_queryset()
        context['created_by'] = self.created_by
        return context


class CheckTaskCreateView(LoginMixin, CreateView):
    """
    添加扫描任务 视图
    """
    model = CheckTask
    form_class = CheckTaskForm
    template_name = "tool/dependency_check/dependency_check_add.html"

    def get_form_kwargs(self):
        # Ensure the current `request` is provided to ProjectCreateForm.
        kwargs = super(CheckTaskCreateView, self).get_form_kwargs()
        kwargs.update({'request': self.request})

        return kwargs


class CheckTaskDeleteView(LoginMixin, DeleteView):
    """
    删除扫描任务
    """
    # template_name_suffix='_delete'
    template_name = "tool/dependency_check/dependency_check_delete.html"
    model = CheckTask
    success_url = reverse_lazy('checklist')

    def delete(self, request, *args, **kwargs):

        """
        Call the delete() method on the fetched object and then redirect to the
        success URL.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()

        # 删除目录文件
        flie_path = self.object.file.file.name  # 获取文件路径
        flie_dir = os.path.abspath(os.path.join(flie_path, ".."))  # 获取当前文件的上级目录
        try:
            if os.path.exists(flie_dir):
                logger.info(f'{flie_dir} 删除目录文件成功!！')
                shutil.rmtree(flie_dir) # 删除目录下的文件
        except Exception as e:
            logger.error(e)

        return HttpResponseRedirect(success_url)
