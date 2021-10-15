import datetime
import os

from django.db import models

# Create your models here.
from django.urls import reverse


def get_photo_path(instance, filename):
    """
    动态生成文件目录
    :param instance:
    :param filename:
    :return:
    """

    productionName = instance.check_name  # 获取文件名称
    check_files = 'upload/checkfiles'    # 固定路径
    today = datetime.datetime.today()
    year = today.year
    month = today.month
    day = today.day

    return f'{check_files}/{year}/{month}/{day}/{productionName}/{filename}'


class CheckTask(models.Model):
    STATE_CHOICE = (
        ('runing', 'runing'),  # 运行中
        ('finish', 'finish'),  # 已完成
        ('notstarted', 'notstarted'),)  # 未开始

    check_name = models.CharField(max_length=100, verbose_name='扫描任务名称')
    file = models.FileField(upload_to=get_photo_path, verbose_name='上传文件路径')
    task_state = models.CharField(max_length=32, choices=STATE_CHOICE, default='notstarted', verbose_name='任务状态')
    task_results = models.CharField(max_length=32, null=True, blank=True, verbose_name='任务结果')
    task_report = models.CharField(max_length=1000, null=True, blank=True, verbose_name='任务报告')
    task_msg = models.CharField(max_length=1000, null=True, blank=True, verbose_name='运行消息')
    task_start_time = models.DateTimeField(verbose_name='任务开始时间', null=True, blank=True)
    task_end_time = models.DateTimeField(verbose_name='任务结束时间', null=True, blank=True)
    createtime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    creator = models.CharField(max_length=32, verbose_name='创建人')

    def save(self, *args, **kwargs):
        if not self.id:
            self.createtime = datetime.datetime.now()
        super(CheckTask, self).save(*args, **kwargs)

    def __str__(self):
        return self.check_name

    def get_absolute_url(self):
        return reverse('checklist')

    class Meta:
        verbose_name = '扫描任务'
        verbose_name_plural = verbose_name
