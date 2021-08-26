# -*- coding: utf-8 -*-
# @File: project_extras.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2021/8/18  17:03

from django import template

register = template.Library()

@register.inclusion_tag('oauth/inclusions/_pagination.html', takes_context=True)
def show_pagination(context):
    return {
        'page_objects':context['objects'],
        'search':context['search'],
        'orderby':context['orderby'],}
