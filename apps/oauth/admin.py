# -*- coding: utf-8 -*-
from django.contrib import admin
from oauth.models import Users, Department, Position
from django.contrib.auth.admin import UserAdmin

admin.site.site_title = "Salvation后台管理"
admin.site.site_header = "Salvation后台管理"


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    """
    部门展示类
    """
    ordering = ('id',)
    list_display = (id, 'dep_name',)
    search_fields = ('dep_name',)
    list_filter = ('dep_name',)
    list_per_page = 20


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    """
    职位展示类
    """
    ordering = ('id',)
    list_display = (id, 'post_name',)
    search_fields = ('post_name',)
    list_filter = ('post_name',)
    list_per_page = 20


@admin.register(Users)
class UsersAdmin(UserAdmin):
    """
    用户展示类
    """
    #model = Users
    list_display = ['username', 'name', 'gender', 'dep', 'post', 'birthday', 'mobile', 'email']
    search_fields = ('name', 'gender', 'dep', 'post',)
    list_filter = ( 'gender','dep',)
    list_per_page = 20

    # user 自定义字段
    fieldsets = UserAdmin.fieldsets + (
        ('个人详情', {'fields': ('name','gender','dep','mobile','birthday', )}),
    )






#
    # add_fieldsets = (
    #     (None, {u'fields': (
    #         'username', 'password1', 'password2', 'first_name', 'name', 'gender', 'dep', 'post', 'birthday', 'mobile',
    #         'email', 'is_superuser', 'is_staff',
    #         'is_active',)}),)
