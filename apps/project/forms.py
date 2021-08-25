# -*- coding: utf-8 -*-
# @File: forms.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2021/8/25  17:34

from django import forms
from .models import Project


class ProjectCreateForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude=['createtime','updatetime','creator','updater']
        # fields = ('project_name,isenabled,descr,version,deployinfos,creator,updater,')
        fields = '__all__'

    def save(self, commit=True):
        pass
