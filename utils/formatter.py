# -*- coding: utf-8 -*-
import re,urllib
from tmitter.settings import *
from django.shortcuts import render_to_response
from django.template import context
from django.core.paginator import Paginator, InvalidPage

def tiny_url(url):
    u"""
    summary:
        将url转换成tinyurl
    author:
        Jason Lee <huacnlee@gmail.com>
    """
    apiurl = "http://tinyurl.com/api-create.php?url="
    tinyurl = urllib.urlopen(apiurl + url).read()
    return tinyurl

def content_tiny_url(content):
    u"""
    summary:
        让消息里面的连接转换成更短的Tinyurl
    author:
        Jason Lee <huacnlee@gmail.com>
    """
    
    regex_url = r'http:\/\/([\w.]+\/?)\S*'
    for match in re.finditer(regex_url, content):
        url = match.group(0)
        content = content.replace(url,tiny_url(url))
    
    return content

def substr(content, length,add_dot=True):
    u"""
    summary:
        字符串截取
    author:
        Jason Lee <huacnlee@gmail.com>
    """
    if(len(content) > length):
        content = content[:length]
        if(add_dot):
            content = content[:len(content)-3] + '...'
    return content

def pagebar(objects,page_index,username='',tempate='control/home_pagebar.html'):
    u"""
    summary:
        生成HTML分页控件,要使用tempate
    params:
        objects     数据列表
        page_index  当前页数
        username    目前被访问的空间的用户名，没有传空
        template    分页模板
    author:
        Jason Lee <huacnlee@gmail.com>
    """
    page_index = int(page_index)
    _paginator = Paginator(objects, PAGE_SIZE)
    
    if(username):
        tempate = 'control/user_pagebar.html'
    
    return render_to_response(tempate, { 
        'paginator': _paginator,
        'username' : username,
        'has_pages': _paginator.num_pages > 1,
        'has_next': _paginator.page(page_index).has_next(),
        'has_prev': _paginator.page(page_index).has_previous(),
        'page_index': page_index,
        'page_next': page_index + 1,
        'page_prev': page_index - 1,
        'page_count': _paginator.num_pages,
        'row_count' : _paginator.count,
        'page_nums': range(_paginator.num_pages+1)[1:],
    }).content

    
    