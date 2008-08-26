# -*- coding: utf-8 -*-
from django.template import Library
from tmitter.mvc.models import *
from tmitter.settings import *

register = Library()

def in_list(val,lst):
    """
    summary:
        检查只时候在列表中
    author:
        Jason Lee
    """
    return val in lst

register.filter("in_list", in_list)