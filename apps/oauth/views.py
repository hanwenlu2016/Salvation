from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, ListView
from django.core.paginator import Paginator
from .models import Position

from .models import Users

from oauth.forms import SignUpForm


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "index.html"
    context = {}

    def get(self, request, *args, **kwargs):
        data_count = {
            "userlist": Users.objects.all().order_by('-last_login')[:5],  # 只取登录时间的默认5
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



class UserListView(LoginRequiredMixin,ListView):
    model = Users
    context_object_name = 'users'
    template_name = "oauth/user_list.html"
    search_value = ""
    order_field = "-id"
    created_by = ''
    pagenum = 5  # 每页分页数据条数

    def get_queryset(self):
        search = self.request.GET.get("search")
        order_by = self.request.GET.get("orderby")
        filter_isenabled = self.request.GET.get("created_by")

        if order_by:
            all_user = Users.objects.all().order_by(order_by)
            self.order_field = order_by
        else:
            all_user = Users.objects.all().order_by(self.order_field)

        # if filter_isenabled:
        #     self.created_by = filter_isenabled
        #     all_user = Users.objects.filter(isenabled=self.created_by)

        # if search:
        #     # 项目名称 、创建人、项目负责人、项目负责人姓名查询
        #     all_user = all_user.filter(
        #         Q(project_name__icontains=search) | Q(creator__icontains=search) | Q(
        #             prjcet_personliable__project__project_name__icontains=search) | Q(
        #             prjcet_personliable__username__icontains=search)
        #     )
        #     self.search_value = search

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
# Handle Errors

def page_not_found(request, exception):
    context = {}
    response = render(request, "errors/404.html", context=context)
    response.status_code = 404
    return response


def server_error(request, exception=None):
    context = {}
    response = render(request, "errors/500.html", context=context)
    response.status_code = 500
    return response


def permission_denied(request, exception=None):
    context = {}
    response = render(request, "errors/403.html", context=context)
    response.status_code = 403
    return response


def bad_request(request, exception=None):
    context = {}
    response = render(request, "errors/400.html", context=context)
    response.status_code = 400
    return response
