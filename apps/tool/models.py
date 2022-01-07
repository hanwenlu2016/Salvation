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


# 安全扫描表
class CheckTask(models.Model):
    STATE_CHOICE = (
        ('runing', 'runing'),  # 运行中
        ('finish', 'finish'),  # 已完成
        ('notstarted', 'notstarted'),)  # 未开始

    SCAN_TYPE_CHOICE = (
        ('webscan', 'webscan'),
        ('servicescan', 'servicescan'),)

    task_id = models.CharField(max_length=100, null=True, blank=True, verbose_name='任务id')
    check_name = models.CharField(max_length=100, verbose_name='扫描任务名称')  #
    xray_address = models.CharField(max_length=500, verbose_name='xray扫描地址')  # xray 扫描时才需要
    file = models.FileField(upload_to=get_photo_path, verbose_name='上传文件路径')
    task_state = models.CharField(max_length=60, choices=STATE_CHOICE, default='notstarted', verbose_name='任务状态')
    scan_type = models.CharField(max_length=60, choices=SCAN_TYPE_CHOICE, default='webscan', verbose_name='扫描类型')
    task_results = models.CharField(max_length=32, null=True, blank=True, verbose_name='任务结果')
    task_report = models.CharField(max_length=1000, null=True, blank=True, verbose_name='任务报告')
    task_msg = models.CharField(max_length=1000, null=True, blank=True, verbose_name='运行消息')
    task_start_time = models.DateTimeField(verbose_name='任务开始时间', null=True, blank=True)
    task_end_time = models.DateTimeField(verbose_name='任务结束时间', null=True, blank=True)
    tag = models.TextField(null=True, blank=True, verbose_name='说明备注')
    createtime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    creator = models.CharField(max_length=32, verbose_name='创建人')

    def save(self, *args, **kwargs):
        if not self.id:
            self.createtime = datetime.datetime.now()
        super(CheckTask, self).save(*args, **kwargs)

    def __str__(self):
        return self.check_name

    def get_absolute_url(self):
        if self.scan_type == 'webscan' or self.scan_type == 'servicescan':
            return reverse('xraylist')
        else:
            return reverse('checklist')

    class Meta:
        verbose_name = '扫描任务'
        verbose_name_plural = verbose_name
