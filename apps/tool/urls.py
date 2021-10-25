# -*- coding: utf-8 -*-
# @File: urls.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2021/8/12  17:17

from django.urls import path, re_path

from tool.views.check_views import *
from tool.views.aes_views import *
from tool.views.ftp_views import *

urlpatterns = [
    path('checklist/', CheckTaskListView.as_view(), name='checklist'),  # 扫描任务列表
    path('checkadd/', CheckTaskCreateView.as_view(), name='checkadd'),  # 新增扫描任务
    path('check-delete/<int:pk>/', CheckTaskDeleteView.as_view(), name="check_delete"),  # 删除扫描任务
    re_path('check-download/(\d+)', CheckDownloadView.as_view(), name="check_download"),  # 下载报告
    path('aes/', AesView.as_view(), name='aes'),  # 加解密
    path('ftp/', FtpView.as_view(), name='ftp'),  # ftp下载
    path('ftp_tool/', FtpToolView.as_view(), name='ftp_tool'),  # ftp工具下载
]
