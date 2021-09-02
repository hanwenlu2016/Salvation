# -*- coding: utf-8 -*-
from django.contrib import admin
from project.models import DeployInfo, Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """
    项目展示类
    """
    ordering = ('id',)

    # 表单字段隐藏
    exclude = ['creator', 'updater']

    list_display = (
        id, 'project_name', 'isenabled', 'descr', 'version', 'deployinfos', 'prjcet_personliable',
        'createtime', 'updatetime', 'creator', 'updater')
    search_fields = ('project_name', 'isenabled', 'version','creator')
    list_filter = ('project_name', 'isenabled', 'version','creator')
    list_per_page = 20

    def save_model(self, request, obj, form, change):
        if not change:
            obj.creator = request.user
            obj.updater = request.user
        obj.save()

@admin.register(DeployInfo)
class DeployInfoAdmin(admin.ModelAdmin):
    """
    部署展示类
    """
    ordering = ('id',)
    list_display = (id, 'prjname', 'prjalias', 'deploypath', 'depldescr')
    search_fields = ('prjname', 'prjalias',)
    list_filter = ( 'prjname', 'prjalias')
    list_per_page = 20
