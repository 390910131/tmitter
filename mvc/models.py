# -*- coding: utf-8 -*-
import time
from django.db import models
from django.contrib import admin
from django.utils import timesince,html
from tmitter.utils import formatter
from tmitter.settings import *

_list_per_page = 50

# category model
class Category(models.Model):
    name = models.CharField('名称',max_length=20)
    
    def __unicode__(self):
        return self.name
    
    
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name')
    list_display_links = ('id','name')
    list_per_page = _list_per_page

    
# User model
class User(models.Model):
    id = models.AutoField(primary_key = True,core = True)

    username = models.CharField('用户名',max_length = 20)
    password = models.CharField('密码',max_length = 32)    
    realname = models.CharField('姓名',max_length = 20)    
    email = models.EmailField('Email')    
    addtime = models.DateTimeField('注册时间',auto_now = True)
    
    def __unicode__(self):
        return self.realname
    
    def addtime_format(self):
        return self.addtime.strftime('%Y-%m-%d %H:%M:%S')
    
    def get_user_url(self):
        return '%suser/%s' % (APP_DOMAIN,self.username)
    
class UserAdmin(admin.ModelAdmin):       
    list_display = ('id','username','realname','email','addtime_format')
    list_display_links = ('username','realname','email')
    list_per_page = _list_per_page


# Note model
class Note(models.Model):
    
    id = models.AutoField(
        primary_key = True,core=True
    )
    message = models.TextField('消息',core=True)
    addtime = models.DateTimeField('发布时间',auto_now = True,core=True)
    category = models.ForeignKey(Category,core=True)
    user = models.ForeignKey(User,core = True)
    
    def __unicode__(self):
        return self.message
    
    def message_short(self):
        return formatter.substr(self.message,30)

    def addtime_format_admin(self):
        return self.addtime.strftime('%Y-%m-%d %H:%M:%S')
        
    def category_name(self):
        """分类名称"""
        return self.category.name
    
    def user_name(self):
        return self.user.realname
    
    def save(self):
        self.message = formatter.content_tiny_url(self.message)
        self.message = html.escape(self.message)
        self.message = formatter.substr(self.message,140)
        super(Note, self).save()
    
    def get_absolute_url(self):
        return APP_DOMAIN + 'message/%s/' % self.id
    

class NoteAdmin(admin.ModelAdmin):
    list_display = ('id','user_name','message_short','addtime_format_admin','category_name')
    list_display_links = ('id','message_short')
    search_fields = ['message']
    list_per_page = _list_per_page


admin.site.register(Note, NoteAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(User,UserAdmin)
