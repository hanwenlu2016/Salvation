# -*- coding: utf-8 -*-
# @File: forms.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2021/8/25  17:34

from django import forms
from .models import Project,DeployInfo


class ProjectCreateForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['createtime', 'updatetime', 'creator', 'updater']
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ProjectCreateForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        obj = super(ProjectCreateForm, self).save(commit=False)
        if self.request:
            print(self.request)
            obj.creator = self.request.user
            obj.updater = self.request.user
            obj.save()
        return obj


class ProjectUpdateForm(ProjectCreateForm):

    def save(self, *args, **kwargs):
        obj = super(ProjectCreateForm, self).save(commit=False)
        if self.request:
            obj.updater = self.request.user.username
            obj.save()
        return obj


class DevCreateForm(forms.ModelForm):
    """
    新增环境表单
    """
    class Meta:
        model = DeployInfo

        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(DevCreateForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        obj = super(DevCreateForm, self).save(commit=False)
        obj.save()
        return obj


class DevUpdateForm(forms.ModelForm):
    """
    更新环境表单
    """
    class Meta:
        model = DeployInfo
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(DevUpdateForm, self).__init__(*args, **kwargs)

    def clean_mobile(self):
        """
        验证手机号码合法性
        :return:
        """
        prjname = self.cleaned_data.get("prjname")
        prjname_old = self.initial.get("prjname")

        if prjname == prjname_old:  # 如果更新数据等于旧数据
            return prjname
        else:
            is_exist = DeployInfo.objects.filter(prjname=prjname).count()

            if is_exist >= 1:
                raise forms.ValidationError("项目名称已经存在")
        return prjname

    def save(self, *args, **kwargs):
        obj = super(DevUpdateForm, self).save(commit=False)
        obj.save()
        return obj