from django.test import TestCase

# Create your tests here.
# import os
# import datetime as dt
# pwd = os.path.abspath(os.path.join(os.getcwd(), "../../upload"))
# uploaddir = pwd+ os.sep + 'check/files'
# today = dt.datetime.today()
# dir_name = uploaddir + f'/{today.year}/{today.month}/{today.day}/'
# print(dir_name)
import datetime

x = datetime.datetime.now()


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

