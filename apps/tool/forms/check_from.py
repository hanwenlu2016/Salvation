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

    def illegalFileName(self, filename):
        """
        验证文件名
        """
        dangerChars = [';', '|', '"', "'", '&', '^', '%', '$', '@',' ']
        for c in dangerChars:
            if c in filename:
                return True
        return False

    def clean_file(self):
        """
        验证手机号码合法性
        :return:
        """

        f = self.cleaned_data.get("file")
        if f:
            # 支持的格式
            allow_suffix = ['tar', '7z', 'zip', 'gz', 'war', 'so', 'rar', 'bz2', 'arj', 'cab', 'lzh', 'iso', 'UUE',
                            'jar', 'rpm']

            file_suffix = f.name.split(".")[-1].lower()

            if file_suffix not in allow_suffix:
                raise forms.ValidationError("文件格式错误，请重新上传!")
            if self.illegalFileName(f.name):
                raise forms.ValidationError("文件名非法，请重新上传!")
        return f

    def save(self, commit=True):
        instance = forms.ModelForm.save(self, False)
        if commit:
            instance.creator = self.request.user
            instance.updater = self.request.user
            instance.save()
        return instance
