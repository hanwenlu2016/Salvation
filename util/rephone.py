# -*- coding: utf-8 -*-
# @File: rephone.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2021/8/10  13:33

import re


def is_phone(tel):
    """
    匹配手机号码合法性
    :param tel:
    :return:
    """
    ret = re.match(r"^1[3456789]\d{9}$", str(tel))
    if ret:
        return True
    else:
        return False
