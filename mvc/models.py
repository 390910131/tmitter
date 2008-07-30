# -*- coding: utf-8 -*-
import time
from django.db import models
from django.contrib import admin
from django.utils import timesince,html
from tmitter.utils import formatter

_list_per_page = 50

# category model
class Category(models.Model):
    name = models.CharField(max_length=20)
    
    
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name')
    list_display_links = ('id','name')
    list_per_page = _list_per_page

    
# User model
class User(models.Model):
    id = models.AutoField(
        primary_key = True,
        core = True,        
    )

    username = models.CharField(
        max_length = 20
    )
    password = models.CharField(
        max_length = 32
    )
    
    realname = models.CharField(
        max_length = 20
    )
    
    email = models.EmailField()
    
    addtime = models.DateTimeField(
        auto_now = True
    )
    
    def addtime_format(self):
        return self.addtime.strftime('%Y-%m-%d %H:%M:%S')
    
class UserAdmin(admin.ModelAdmin):       
    list_display = ('id','username','realname','email','addtime_format')
    list_display_links = ('username','realname','email')
    list_per_page = _list_per_page


# Note model
class Note(models.Model):
    
    id = models.AutoField(
        primary_key = True,core=True
    )
    message = models.TextField(core=True)
    addtime = models.DateTimeField(auto_now = True,core=True)
    category = models.ForeignKey(Category,core=True)
    user = models.ForeignKey(User,core = True)
    
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
    
    def save(self):
        self.message = formatter.content_tiny_url(self.message)
        self.message = html.escape(self.message)
        self.message = formatter.substr(self.message,140)
        super(Note, self).save()
    

class NoteAdmin(admin.ModelAdmin):
    list_display = ('id','user_name','message_short','addtime_format_admin','category_name')
    list_display_links = ('id','message_short')
    list_per_page = _list_per_page


admin.site.register(Note, NoteAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(User,UserAdmin)
