# -*- coding: utf-8 -*-
from django import forms

from ..models import CheckTask


class CheckTaskForm(forms.ModelForm):
    """
    新增扫描任务 表单
    """

    class Meta:
        model = CheckTask
        exclude = ['task_state', 'task_results', 'task_report', 'createtime', 'creator']
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CheckTaskForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = forms.ModelForm.save(self, False)
        if commit:
            instance.creator = self.request.user
            instance.updater = self.request.user
            instance.save()
        return instance

