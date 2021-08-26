from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView,UpdateView,DeleteView
from django.core.paginator import Paginator
from django.contrib.messages.views import messages
from project.forms import ProjectCreateForm, ProjectUpdateForm
from project.models import Project


class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    context_object_name = 'project'
    template_name = "project/project_list.html"
    search_value = ""
    order_field = "-updater"
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
                    prjcet_personliable__project__project_name__icontains=search) | Q(
                    prjcet_personliable__username__icontains=search)
            )
            self.search_value = search

        self.count_total = all_pro.count()
        paginator = Paginator(all_pro, self.pagenum)
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


class ProjectDetailView(LoginRequiredMixin, DetailView):
    """
    项目详情
    """
    model = Project
    template_name = "project/project_detail.html"

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        project_info = Project.objects.get(id=self.get_object().id)
        context['project_info'] = project_info
        return context

class ProjectParticpantDetailView(LoginRequiredMixin, DetailView):
    """
    项目的参加人员 详情
    """
    model = Project
    context_object_name = 'project_particpant'
    template_name = "project/project_particpant_detail.html"

    def get_context_data(self, **kwargs):
        context = super(ProjectParticpantDetailView, self).get_context_data(**kwargs)
        related_member = Project.objects.get(id=self.get_object().id)
        context['project_particpant'] = related_member
        return context

class ProjectCreateView(LoginRequiredMixin, CreateView):
    """
    添加项目
    """
    model = Project
    form_class = ProjectCreateForm
    template_name = "project/project_add.html"

    def get_form_kwargs(self):
        # Ensure the current `request` is provided to ProjectCreateForm.
        kwargs = super(ProjectCreateView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    """
    更新项目
    """
    model = Project
    form_class = ProjectUpdateForm
    template_name = "project/project_update.html"

    def get_form_kwargs(self):
        # Ensure the current `request` is provided to ProjectCreateForm.
        kwargs = super(ProjectUpdateView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    """
    删除项目
    """
    model = Project
    success_url = reverse_lazy('prlist')
    #success_url = ""




