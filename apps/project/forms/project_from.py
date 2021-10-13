# -*- coding: utf-8 -*-
# @File: project_from.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2021/9/2  15:14

# 项目详情 表单

from django import forms
from ..models import Project
from oauth.models import Users


class ProjectCreateForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['createtime', 'updatetime', 'creator', 'updater']
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ProjectCreateForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = forms.ModelForm.save(self, False)
        if commit:
            instance.creator = self.request.user
            instance.updater = self.request.user
            instance.save()
            self.save_m2m()  # 多对多时 需要调用 save_m2m 方法
        return instance


class ProjectUpdateForm(ProjectCreateForm):
    # 重写父类方法
    def save(self, commit=True):
        obj = super(ProjectCreateForm, self).save(commit=False)
        if self.request:
            obj.updater = self.request.user.username
            obj.save()
            self.save_m2m()
        return obj
