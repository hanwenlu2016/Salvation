from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.views.generic import TemplateView, CreateView

from .models import Users

from oauth.forms import SignUpForm


class HomeView(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    template_name = "index.html"
    context = {}

    def get(self, request, *args, **kwargs):
        data_count = {
            "userlist": Users.objects.all().order_by('last_login')[:5], # 只取登录时间的默认5
            "member": Users.objects.all().count(),
        }
        self.context['data_count'] = data_count
        return render(request, self.template_name, self.context)


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
    success_url = '/auth/login'

    def form_invalid(self, form):
        """
        验证失败时触发
        :param form:
        :return:
        """
        return self.render_to_response({'form': form, })
