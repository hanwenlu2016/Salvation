# -*- coding: utf-8 -*-
# @File: project_from.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2021/9/2  15:14

# 项目详情 表单

from django import forms
from ..models import Project


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
        obj = super(ProjectCreateForm, self).save(commit=False) #重写父类方法
        if self.request:
            obj.updater = self.request.user.username
            obj.save()
        return obj
