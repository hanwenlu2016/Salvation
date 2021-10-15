# -*- coding: utf-8 -*-

import os

from celery import Celery, platforms
from django.conf import settings

# 支持root启动
platforms.C_FORCE_ROOT=True

# 指定Django默认配置文件模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Salvation.settings')

# 为我们的项目myproject创建一个Celery实例。这里不指定broker backend 容易出现错误。
app = Celery('Salvation')

# 这里指定从django的settings.py里读取celery配置
app.config_from_object('django.conf:settings',namespace='CELERY')

# 发现任务文件每个app下的task.py
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

