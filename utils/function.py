# -*- coding: utf-8 -*-
import md5

def md5_encode(str):
    u"""
    summary:
        MD5 encode
    author:
        Jason Lee <huacnlee@gmail.com>
    """
    return md5.new(str).hexdigest()

def get_referer_url(request):
    """
    summary:
        get request referer url address,default /
    author:
        Jason Lee <huacnlee@gmail.com>
    """
    return request.META.get('HTTP_REFERER', '/')