# -*- coding: utf-8 -*-
# @File: user_views.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2021/9/2  17:00

from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import  CreateView, ListView, UpdateView, DeleteView
from django.core.paginator import Paginator

from util.loginmixin import LoginMixin
from oauth.forms import UserCreateForm, UserUpdateForm
from oauth.models import Users


class UserListView(LoginMixin, ListView):
    """
    用户列表 视图
    """

    model = Users
    context_object_name = 'users'
    template_name = "oauth/user/user_list.html"
    search_value = ""
    order_field = "-id"
    created_by = ''
    pagenum = 5  # 每页分页数据条数

    def get_queryset(self):
        search = self.request.GET.get("search")
        order_by = self.request.GET.get("orderby")
        filter_gender = self.request.GET.get("created_by")

        if order_by:
            all_user = Users.objects.all().order_by(order_by)
            self.order_field = order_by
        else:
            all_user = Users.objects.all().order_by(self.order_field)

        if filter_gender:
            self.created_by = filter_gender
            all_user = Users.objects.filter(gender=self.created_by)

        if search:
            # 项目名称 、创建人、项目负责人、项目负责人姓名查询
            all_user = all_user.filter(
                Q(name__icontains=search) | Q(username__icontains=search) | Q(
                    mobile__icontains=search))
            self.search_value = search

        self.count_total = all_user.count()
        paginator = Paginator(all_user, self.pagenum)
        page = self.request.GET.get('page')
        users = paginator.get_page(page)
        return users

    def get_context_data(self, *args, **kwargs):
        context = super(UserListView, self).get_context_data(*args, **kwargs)
        context['count_total'] = self.count_total
        context['search'] = self.search_value
        context['orderby'] = self.order_field
        context['objects'] = self.get_queryset()
        context['created_by'] = self.created_by
        return context


class UserCreateView(LoginMixin, CreateView):
    """
    添加用户 视图
    """
    model = Users
    form_class = UserCreateForm
    template_name = "oauth/user/user_add.html"

    def get_form_kwargs(self):
        # Ensure the current `request` is provided to ProjectCreateForm.
        kwargs = super(UserCreateView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs


class UserUpdateView(LoginMixin, UpdateView):
    """
    更新用户
    """
    model = Users
    form_class = UserUpdateForm
    template_name = "oauth/user/user_update.html"

    def get_form_kwargs(self):
        # Ensure the current `request` is provided to ProjectCreateForm.
        kwargs = super(UserUpdateView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs


class UserDeleteView(LoginMixin, DeleteView):
    """
    删除用户
    """
    #template_name_suffix = '_user_delete'  # 删除模板默认 users（模型开头  /users_user_delete

    template_name = "oauth/user/user_delete.html"
    model = Users
    success_url = reverse_lazy('userlist')


