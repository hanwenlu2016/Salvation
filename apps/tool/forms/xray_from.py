# -*- coding: utf-8 -*-
import os
import re

from django import forms

from .. import tasks
from ..models import CheckTask
from util.loggers import logger

from util.time_processing import plus_seconds


class XrayTaskForm(forms.ModelForm):
    """
    新增扫描任务 表单
    """

    class Meta:
        model = CheckTask
        # exclude = ['task_state', 'task_results', 'task_report', 'createtime', 'creator']
        fields = ('check_name', 'xray_address', 'scan_type', 'tag')
        # fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(XrayTaskForm, self).__init__(*args, **kwargs)


    def clean_scan_type(self, ):
        """
        验证类型
        """
        scan_type = self.cleaned_data.get("scan_type")
        SCAN_TYPE_CHOICE = ['webscan', 'servicescan', 'check', 'other']  # 必须和 model SCAN_TYPE_CHOICE一直

        if scan_type not in SCAN_TYPE_CHOICE:
            logger.error('新增扫描任务失败！扫描类型不支持！')
            raise forms.ValidationError("新增扫描任务失败！扫描类型不支持！")
        else:
            return scan_type

    def save(self, commit=True):
        instance = forms.ModelForm.save(self, False)

        if commit:
            instance.creator = self.request.user
            instance.updater = self.request.user
            instance.task_state = 'runing'  # 上传时修改任务状态
            instance.task_start_time = plus_seconds(5)  # 当前时间+5秒 大约任务开始时间
            url = self.cleaned_data.get("xray_address")
            types = self.cleaned_data.get("scan_type")
            instance.task_id = tasks.xray_shell_task.delay(url, types)  # 执行异步任务
            instance.save()
            logger.info(f'新增扫描任务成功！{instance.check_name}')

        return instance
