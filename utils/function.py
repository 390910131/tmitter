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
