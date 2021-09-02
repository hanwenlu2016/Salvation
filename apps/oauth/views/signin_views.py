# -*- coding: utf-8 -*-
# @File: signin_views.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2021/9/2  16:57

from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from oauth.forms import SignUpForm


class SignInView(LoginView):
    """
    登录视图
    """
    template_name = 'accounts/login.html'


class SignOutView(LogoutView):
    """
    登出视图
    """
    template_name = 'accounts/login.html'


class SignUpView(CreateView):
    """
    注册视图
    """

    template_name = 'accounts/register.html'
    form_class = SignUpForm
    success_url = reverse_lazy('login')

    def form_invalid(self, form):
        """
        验证失败时触发
        :param form:
        :return:
        """
        return self.render_to_response({'form': form, })