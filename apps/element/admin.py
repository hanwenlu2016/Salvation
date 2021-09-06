from django.contrib import admin

from element.models import Case,LocationType,OperateType,CaseSte


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    """
    用例展示类
    """
    ordering = ('id',)
    exclude = ['maintainer', ]
    list_display = ('moduleid', 'casename','title', 'precondition','isdone','createtime', 'updatetime', 'maintainer')
    search_fields = ('title','isdone')
    list_filter = ('title','isdone')
    list_per_page = 50

    def save_model(self, request, obj, form, change):
        if not change:
            obj.maintainer = request.user
        obj.save()

@admin.register(CaseSte)
class CaseSteAdmin(admin.ModelAdmin):
    """
    用例步骤展示类
    """
    ordering = ('id',)
    list_display = ('casesteid', 'info', 'ope_type', 'locat_type',  'locate','expect', )
    search_fields = ('info', 'ope_type', 'locat_type', 'locate', 'expect')
    list_filter = ('info', )
    list_per_page = 50

    def save_model(self, request, obj, form, change):
        if not change:
            obj.maintainer = request.user
        obj.save()

@admin.register(LocationType)
class LocationTypeAdmin(admin.ModelAdmin):
    """
    定位类型类
    """
    ordering = ('id',)
    list_display = ('location_type',)
    search_fields = ('location_type',)
    list_filter = ('location_type',)
    list_per_page = 50

@admin.register(OperateType)
class OperateTypeAdmin(admin.ModelAdmin):
    """
    执行类型类
    """
    ordering = ('id',)
    list_display = ('operate_type',)
    search_fields = ('operate_type',)
    list_filter = ('operate_type',)
    list_per_page = 50

