# -*- coding: utf-8 -*-
# @File: loginmixin.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2021/8/27  16:38


from django.contrib.auth.mixins import LoginRequiredMixin


class LoginMixin(LoginRequiredMixin):
    """
    没登录跳转到登录页面
    """
    login_url = 'login'
