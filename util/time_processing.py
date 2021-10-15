# -*- coding: utf-8 -*-
import datetime

def plus_seconds(s):
    """
    当前时间加秒
    :param s:  秒数
    :return:
    """
    today = datetime.datetime.now()
    # 计算偏移量
    offset = datetime.timedelta(seconds=float(s))
    # 获取修改后的时间并格式化
    newdate = (today + offset).strftime('%Y-%m-%d %H:%M:%S')
    return newdate

'''
#时间加0.5天
offset = datetime.timedelta(days=0.5)
#时间加0.5小时
offset = datetime.timedelta(hours=0.5)
#时间加1分钟
offset = datetime.timedelta(minutes=1)
#时间加1秒钟
offset = datetime.timedelta(seconds=1)
'''
