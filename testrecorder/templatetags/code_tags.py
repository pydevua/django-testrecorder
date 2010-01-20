# -*- coding: utf-8 -*-
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

def data_value(value):
    if len(str(value).splitlines()) > 1:
        output = "'''%s'''" % value
    else:
        output = "'%s'" % value
    return mark_safe(output)

register.filter('data_value', data_value)