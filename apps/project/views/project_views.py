# -*- coding: utf-8 -*-
# @File: project_views.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2021/9/2  15:04

# 项目详情视图 类

from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.core.paginator import Paginator
from project.forms.project_from import ProjectUpdateForm, ProjectCreateForm
from project.models import Project

from util.loginmixin import LoginMixin


class ProjectListView(LoginMixin, ListView):
    """
    项目列表 视图
    """
    model = Project
    context_object_name = 'project'
    template_name = "project_manage/project/project_list.html"
    search_value = ""
    order_field = "-updatetime"  # 排序方式
    created_by = ''
    pagenum = 5  # 每页分页数据条数

    def get_queryset(self):
        search = self.request.GET.get("search")
        order_by = self.request.GET.get("orderby")
        filter_isenabled = self.request.GET.get("created_by")

        if order_by:
            all_pro = Project.objects.all().order_by(order_by)
            self.order_field = order_by
        else:
            all_pro = Project.objects.all().order_by(self.order_field)

        if filter_isenabled:
            self.created_by = filter_isenabled
            all_pro = Project.objects.filter(isenabled=self.created_by)

        if search:
            # 项目名称 、创建人、项目负责人、项目负责人姓名查询
            all_pro = all_pro.filter(
                Q(project_name__icontains=search) | Q(creator__icontains=search) | Q(
                    prjcet_personliable__username__icontains=search) | Q(
                    prjcet_personliable__name__icontains=search))
            self.search_value = search

        self.count_total = all_pro.count()
        paginator = Paginator(all_pro.order_by(self.order_field), self.pagenum)
        page = self.request.GET.get('page')
        project = paginator.get_page(page)
        return project

    def get_context_data(self, *args, **kwargs):
        context = super(ProjectListView, self).get_context_data(*args, **kwargs)
        context['count_total'] = self.count_total
        context['search'] = self.search_value
        context['orderby'] = self.order_field
        context['objects'] = self.get_queryset()
        context['created_by'] = self.created_by
        return context


class ProjectDetailView(LoginMixin, DetailView):
    """
    项目详情 视图
    """
    model = Project
    template_name = "project_manage/project/project_detail.html"

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        project_info = Project.objects.get(id=self.get_object().id)
        context['project_info'] = project_info
        return context


class ProjectParticpantDetailView(LoginMixin, DetailView):
    """
    项目的参加人员 详情
    """
    model = Project
    context_object_name = 'project_particpant'
    template_name = "project_manage/project/project_particpant_detail.html"

    def get_context_data(self, **kwargs):
        context = super(ProjectParticpantDetailView, self).get_context_data(**kwargs)
        related_member = Project.objects.get(id=self.get_object().id)
        context['project_particpant'] = related_member
        return context


class ProjectDevDetailView(LoginMixin, DetailView):
    """
    项目部署信息详情 视图
    """
    model = Project
    context_object_name = 'project_dev'
    template_name = "project_manage/project/project_dev_detail.html"

    def get_context_data(self, **kwargs):
        context = super(ProjectDevDetailView, self).get_context_data(**kwargs)
        dev = Project.objects.get(id=self.get_object().id)
        context['project_dev'] = dev
        return context


class ProjectCreateView(LoginMixin, CreateView):
    """
    添加项目 视图
    """
    model = Project
    form_class = ProjectCreateForm
    template_name = "project_manage/project/project_add.html"

    def get_form_kwargs(self):
        # Ensure the current `request` is provided to ProjectCreateForm.
        kwargs = super(ProjectCreateView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs


class ProjectUpdateView(LoginMixin, UpdateView):
    """
    更新项目 视图
    """
    model = Project
    form_class = ProjectUpdateForm
    template_name = "project_manage/project/project_update.html"

    def get_form_kwargs(self):
        # Ensure the current `request` is provided to ProjectCreateForm.
        kwargs = super(ProjectUpdateView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs


class ProjectDeleteView(LoginMixin, DeleteView):
    """
    删除项目 视图
    """
    # template_name_suffix='_delete'
    template_name = "project_manage/project/project_delete.html"
    model = Project
    success_url = reverse_lazy('prlist')
