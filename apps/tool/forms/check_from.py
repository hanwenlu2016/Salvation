# -*- coding: utf-8 -*-
import os
import re

from django import forms

from ..models import CheckTask
from util.loggers import logger
import datetime
from util.time_processing import plus_seconds
from tool import tasks


class CheckTaskForm(forms.ModelForm):
    """
    新增扫描任务 表单
    """

    class Meta:
        model = CheckTask
        # exclude = ['task_state', 'task_results', 'task_report', 'createtime', 'creator']
        fields = ('check_name', 'file','tag')
        # fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CheckTaskForm, self).__init__(*args, **kwargs)

    def illegalFileName(self, filename):
        """
        验证文件名
        """
        dangerChars = [';', '|', '"', "'", '&', '^', '%', '$', '@', ' ']
        for c in dangerChars:
            if c in filename:
                return True
        return False

    def clean_check_name(self):
        """
        检查扫描任
        :return:
        """
        check_name = self.cleaned_data.get("check_name")
        zhmodel = re.compile(u'[\u4e00-\u9fa5]')
        match = zhmodel.search(check_name)

        if CheckTask.objects.filter(check_name=check_name).count() != 0:
            logger.error('新增扫描任务失败！扫描任务已经存在！')
            raise forms.ValidationError("新增扫描任务失败！扫描任务已经存在！")

        if match:
            logger.error('新增扫描任务失败！请勿输入中文命名')
            raise forms.ValidationError("新增扫描任务失败！请勿输入中文命名！")
        else:
            return check_name

    def clean_file(self):
        """
        验证文件合法合法性
        :return:
        """

        f = self.cleaned_data.get("file")

        if f:
            # 支持的格式
            allow_suffix = ['tar', '7z', 'zip', 'gz', 'war', 'so', 'rar', 'bz2', 'arj', 'cab', 'lzh', 'iso', 'UUE',
                            'jar', 'rpm']

            file_suffix = f.name.split(".")[-1].lower()

            if file_suffix not in allow_suffix:
                logger.error(f'新增扫描任务失败！文件格式错误，请重新上传!')
                raise forms.ValidationError("文件格式错误，请重新上传!")

            if f.size > 524288000:  # 500*1024*1024 限制大于500m的文件
                logger.error(f'新增扫描任务失败！文件不能大于500M，请重新上传!')
                raise forms.ValidationError("文件不能大于500M，请重新上传!")

            if self.illegalFileName(f.name):
                logger.error(f'新增扫描任务失败！文件名非法，请重新上传!')
                raise forms.ValidationError("文件名非法，请重新上传!")
        return f

    def save(self, commit=True):
        instance = forms.ModelForm.save(self, False)

        if commit:
            instance.creator = self.request.user
            instance.updater = self.request.user
            instance.task_state = 'runing'  # 上传时修改任务状态
            instance.task_start_time = plus_seconds(5)  # 当前时间+5秒 大约任务开始时间

            check_path = self.get_photo_path(instance)  # 处理扫描路径
            instance.task_id = tasks.check_shell_task.delay(check_path, instance.check_name)  # 执行异步任务
            instance.save()
            logger.info(f'新增扫描任务成功！{instance.check_name}')

        return instance

    def get_photo_path(self, instance):
        """
        拼接处理扫描路径
        :param filename: 文件名称
        :param file: 文件
        :return:
        """
        object_path = instance.file.path        # 项目路径
        productionName = instance.check_name  # 获取任务名称
        file =  instance.file.name          # 获取文件

        check_files = 'upload/checkfiles'  # 固定路径
        today = datetime.datetime.today()
        year = today.year
        month = today.month
        day = today.day
        flie_dir = os.path.abspath(os.path.join(object_path, ".."))  # 获取当前文件的上上个级目录
        return f'{flie_dir}/{check_files}/{year}/{month}/{day}/{productionName}/{file}'
