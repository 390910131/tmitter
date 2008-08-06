# -*- coding: utf-8 -*-
from django.template import Library
from tmitter.mvc.models import *
from tmitter.settings import *

register = Library()

def get_face_url(size,content):
    return MEDIA_URL + '%s/' % size + content

def face16(content):
    return get_face_url(16,content)

def face24(content):
    return get_face_url(24,content)

def face32(content):
    return get_face_url(32,content)

def face(content):
    return get_face_url(64,content)

register.filter('face', face)
register.filter('face16', face16)
register.filter('face24', face24)
register.filter('face32', face32)

def user_url(username):
    return '%suser/%s' % (APP_DOMAIN,username)