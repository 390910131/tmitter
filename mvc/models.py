# -*- coding: utf-8 -*-
import time
from django.db import models
from django.utils import timesince

_list_per_page = 50

# category model
class Category(models.Model):
    name = models.CharField(maxlength=20)
    
    class Admin:
        list_display = ('id','name')
        list_display_links = ('id','name')
        list_per_page = _list_per_page
        pass

    
# User model
class User(models.Model):
    id = models.AutoField(
        primary_key = True,
        core = True,        
    )

    username = models.CharField(
        maxlength = 20
    )
    password = models.CharField(
        maxlength = 32
    )
    
    realname = models.CharField(
        maxlength = 20
    )
    
    email = models.EmailField()
    
    addtime = models.DateTimeField(
        auto_now = True
    )
    
    class Admin:       
        list_display = ('id','username','realname','email','addtime_format')
        list_display_links = ('username','realname','email')
        list_per_page = _list_per_page
        pass
    
    def addtime_format(self):
        return self.addtime.strftime('%Y-%m-%d %H:%M:%S')
    
        

# Note model
class Note(models.Model):
    
    id = models.AutoField(
        primary_key = True,core=True
    )
    message = models.TextField(core=True)
    addtime = models.DateTimeField(auto_now = True,core=True)
    category = models.ForeignKey(Category,core=True)
    user = models.ForeignKey(User,core = True)
    
    class Admin:
        list_display = ('id','user_name','message_short','addtime_format_admin','category_name')
        list_display_links = ('id','message_short')
        list_per_page = _list_per_page
        pass
    
    def message_short(self):
        return self.message
    #colored_first_name.admin_order_field = 'message'

    def addtime_format_admin(self):
        return self.addtime.strftime('%Y-%m-%d %H:%M:%S')
    #addtime_format.admin_order_field = 'addtime'
        
    def category_name(self):
        return self.category.name
    
    def user_name(self):
        return self.user.realname
    
    def timesince(self):
        return timesince.timesince(self.addtime,time.time())
