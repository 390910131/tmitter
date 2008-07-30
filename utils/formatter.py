# -*- coding: utf-8 -*-
import re,urllib

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
    