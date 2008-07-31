# -*- coding: utf-8 -*-
import re,urllib
from tmitter.settings import *
from django.shortcuts import render_to_response
from django.template import context
from django.core.paginator import ObjectPaginator, InvalidPage

def tiny_url(url):
    """将url转换成tinyurl"""
    apiurl = "http://tinyurl.com/api-create.php?url="
    tinyurl = urllib.urlopen(apiurl + url).read()
    return tinyurl

def content_tiny_url(content):
    """让消息里面的连接转换成更短的Tinyurl"""
    
    regex_url = r'http:\/\/([\w.]+\/?)\S*'
    for match in re.finditer(regex_url, content):
        url = match.group(0)
        content = content.replace(url,tiny_url(url))
    
    return content

def substr(content, length,add_dot=True):
    """字符串截取"""
    if(len(content) > length):
        content = content[:length]
        if(add_dot):
            content = content[:len(content)-3] + '...'
    return content

def pagebar(objects,page_index,username,tempate='control/home_pagebar.html'):
    """生成HTML分页控件,要使用tempate"""
    page_index = int(page_index)
    _paginator = ObjectPaginator(objects, PAGE_SIZE)
    
    if(username):
        tempate = 'control/user_pagebar.html'
    
    return render_to_response(tempate, { 
        'paginator': _paginator,
        'username' : username,
        'has_pages': _paginator.pages > 1,
        'has_next': _paginator.has_next_page(page_index - 1),
        'has_prev': _paginator.has_previous_page(page_index - 1),
        'page_index': page_index,
        'page_next': page_index + 1,
        'page_prev': page_index - 1,
        'page_count': _paginator.pages,
        'row_count' : _paginator.hits,
        'page_nums': range(_paginator.pages+1)[1:],
    }).content

    
    