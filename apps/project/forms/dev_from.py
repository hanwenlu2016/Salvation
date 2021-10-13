# -*- coding: utf-8 -*-
# @File: dev_from.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2021/9/2  15:14

from django import forms
from ..models import DeployInfo


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

    def save(self, commit=True):
        instance = forms.ModelForm.save(self, False)
        if commit:
            instance.save()
        return instance



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

    def clean_prjalias(self):
        """
        验证项目别名合法性
        :return:
        """
        prjalias = self.cleaned_data.get("prjalias")
        prjalias_old = self.initial.get("prjalias")

        if prjalias == prjalias_old:  # 如果更新数据等于旧数据
            return prjalias
        else:
            is_exist = DeployInfo.objects.filter(prjalias=prjalias).count()

            if is_exist >= 1:
                raise forms.ValidationError("项目别名已经存在")
        return prjalias

    def save(self, *args, **kwargs):
        obj = super(DevUpdateForm, self).save(commit=False)
        obj.save()
        return obj