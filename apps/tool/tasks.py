# -*- coding: utf-8 -*-
import hashlib
import os
import datetime

from django_celery_results.models import TaskResult
from celery import shared_task

from util.loggers import logger
from Salvation import settings
from tool.models import CheckTask


def check_shell(check_path, check_name):
    """
    扫描脚本
    :param check_path:  项目扫描路径
    :param check_name: 扫描名称
    :return:
    """
    with open(check_path, 'rb') as f:
        fr = f.read()

    md5file = hashlib.md5(fr).hexdigest()
    result_path = os.path.abspath(os.path.join(check_path, ".."))  # 获取当前文件的上级目录
    output = result_path + os.sep + md5file + '.html'  # 输出结果路径

    try:
        logger.info('开始执行扫描任务!!!')
        shell = f'{settings.CHECK_SHELL_PATH} --project {check_name} --scan {check_path} -o {output}'
        os.system(shell)
    except Exception as e:
        logger.error('执行扫描任务失败！！！')
        logger.error(e)
        return 'Execution task exception !!!'
    return output


# 异步任务立刻执行脚本 任务
@shared_task
def check_shell_task(check_path, check_name):
    """
    执行扫描任务脚本任务
    :param check_path:  项目扫描路径
    :param check_name: 扫描名称
    :return:
    """
    return check_shell(check_path, check_name)


# 定时任务
@shared_task
def update_checktask_table_task():
    """
    更新 check 表状态定时任务
    :return:
    """
    try:
        # 查询 任务表不等于 finish的数据
        task_obj = CheckTask.objects.exclude(task_state='finish')

        # 如果 任务表查询出的数据不等于0 循环数据
        if task_obj.count() != 0:
            for task in task_obj:
                # 查询出 任务结果表 task_id 等于任务表的task_id
                task_result_obj = TaskResult.objects.filter(task_id=task.task_id)
                if task_result_obj.count()!= 0:
                    for result in task_result_obj:
                        task.task_state = 'finish'
                        task.task_results = result.status
                        task.task_report = result.result.replace('"', '')
                        task.task_end_time = result.date_done
                        task.task_msg = result.status
                    task.save()
                logger.info('执行 update_checktask_table_task 成功!')
                return 'update_checktask_table_task successfully!'
        else:
            logger.info('执行 update_checktask_table_task 成功! 无须更新数据!')
            return 'update_checktask_table_task no need to update data!'
    except Exception as e:
        logger.error(f'执行 update_checktask_table_task 任务失败！{e}')
        return 'update_checktask_table_task abnormal'


# # 定时任务
@shared_task
def delete_result_data_task():
    """
    删除 django_celery_results_taskresult表  每1小时清除一次 清除2小时之前的任务
    :return:
    """
    # 当前时间
    cur_date = datetime.datetime.now()
    # 前2小时
    yester_day = cur_date - datetime.timedelta(hours=2)

    try:
        task_result_obj = TaskResult.objects.filter(date_created__lt=yester_day)
        task_result_obj_num = task_result_obj.count()
        if task_result_obj_num != 0:
            task_result_obj.delete()
            logger.info('执行 delete_result_data_task 任务成功！共删除数据 {}条'.format(task_result_obj_num))
            return 'Delete success'
        else:
            logger.info('执行 delete_result_data_task 任务成功! 无删除数据！')
            return 'Not delete data'
    except Exception as e:
        logger.error('执行 delete_result_data_task 任务失败！{}'.format(e))
        return 'delete_result_data_task abnormal'



# Celery -A Salvation worker --loglevel=info --concurrency=10 异步任务
# celery -A celery_client worker --concurrency=10 --loglevel=info --logfile="/tmp/blackcat/blackcat.log" &


# Celery -A Salvation  beat -l ERROR --scheduler django_celery_beat.schedulers:DatabaseScheduler 定时任务