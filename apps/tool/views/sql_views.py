# -*- coding: utf-8 -*-

import os.path
import shutil

from django.db.models import Q
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect


from django.views.generic import CreateView, ListView, DeleteView
from django.core.paginator import Paginator
from tool.forms.xray_from import XrayTaskForm
from ..models import CheckTask
from util.loggers import logger
from util.loginmixin import LoginMixin

class XrayTaskListView(ListView):
    """
    扫描信息信息列表 视图
    """
    model = CheckTask
    context_object_name = 'check'
    template_name = "tool/xray_injection/xray_list.html"
    search_value = ""
    order_field = "-createtime"
    created_by = ''
    pagenum = 5  # 每页分页数据条数

    def get_queryset(self):
        search = self.request.GET.get("search")
        order_by = self.request.GET.get("orderby")
        filter_state = self.request.GET.get("created_by")

        if order_by:
            #check_pro = CheckTask.objects.all().order_by(order_by)
            check_pro = CheckTask.objects.exclude(scan_type='check').order_by(order_by)
            self.order_field = order_by
        else:
            #check_pro = CheckTask.objects.all().order_by(self.order_field)
            check_pro = CheckTask.objects.exclude(scan_type='check').order_by(self.order_field)

        if filter_state:

            if filter_state == '有注入':
                # 查询不等于 空并且  task_report 不为 NO
                check_pro = CheckTask.objects.exclude(scan_type='check',).filter(~Q(task_report='') & ~Q(task_report='NO'))
            else:
                check_pro = CheckTask.objects.exclude(scan_type='check',).filter(Q(task_report='NO') | Q(task_report=''))

            self.created_by = filter_state
            check_pro = check_pro

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
        context = super(XrayTaskListView, self).get_context_data(*args, **kwargs)
        context['count_total'] = self.count_total
        context['search'] = self.search_value
        context['orderby'] = self.order_field
        context['objects'] = self.get_queryset()
        context['created_by'] = self.created_by
        return context


class XrayTaskCreateView(LoginMixin,CreateView):
    """
    添加扫描任务 视图
    """
    model = CheckTask
    form_class = XrayTaskForm
    template_name = "tool/xray_injection/xray_add.html"

    def get_form_kwargs(self):
        # Ensure the current `request` is provided to ProjectCreateForm.
        kwargs = super(XrayTaskCreateView, self).get_form_kwargs()
        kwargs.update({'request': self.request})

        return kwargs

class XrayTaskDeleteView(LoginMixin,DeleteView):
    """
    删除扫描任务
    """
    # template_name_suffix='_delete'
    template_name = "tool/xray_injection/xray_delete.html"
    model = CheckTask
    success_url = reverse_lazy('xraylist')

    def delete(self, request, *args, **kwargs):

        """
        Call the delete() method on the fetched object and then redirect to the
        success URL.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        flie_dir = self.object.task_report
        self.object.delete()


        # 删除目录文件

        try:
            if os.path.exists(flie_dir):
                logger.info(f'{flie_dir} 删除目录文件成功!！')
                #shutil.rmtree(flie_dir)  # 删除目录下的文件
                os.remove(flie_dir)
        except Exception as e:
            logger.error(e)
            return HttpResponseRedirect(success_url)

        return HttpResponseRedirect(success_url)

