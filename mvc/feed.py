# -*- coding: utf-8 -*-
from django.contrib.syndication.feeds import Feed,FeedDoesNotExist
from django.core.exceptions import ObjectDoesNotExist
from tmitter.mvc.models import Note,User
from tmitter.utils import formatter
from tmitter.settings import *
from tmitter.mvc.templatetags import user_tags

_global_title_template = 'feed/title.html'
_global_description_template = 'feed/description.html'

class RSSRecentNotes(Feed):
    """所有用户最新文章列表"""
    title = u'%s 网友最近消息' % APP_NAME
    link = APP_DOMAIN
    description = u'%s上面网友最近发布的消息' % APP_NAME
    author = "%s RSS generator" % APP_NAME
    title_template = _global_title_template
    description_template = _global_description_template
    
    def items(self):
        return Note.objects.order_by('-addtime')[:FEED_ITEM_MAX]
    
    def item_author_name(self, item):
        return item.user.realname
    
    def item_author_link(self, item):
        return user_tags.user_url(item.user.username)
    
    def item_link(self, item):
        return item.get_absolute_url()

    def item_pubdate(self, item):
        return item.addtime
    
class RSSUserRecentNotes(Feed):
    """用户最新文章列表"""
    def title(self,obj):
        return u'%s %s 最近消息' % (APP_NAME,obj.realname)
    
    def link(self,obj):
        return '%suser/%s' % (APP_DOMAIN,obj.username)
    
    def description(self,obj):
        return u'%s 在 %s 上面最近发布的消息' % (APP_NAME,obj.realname)
    
    def author(self,obj):
        return "%s" % obj.realname
    
    def get_object(self, bits):
        # In case of "/rss/beats/0613/foo/bar/baz/", or other such clutter,
        # check that bits has only one member.
        if len(bits) != 1:
            raise ObjectDoesNotExist
        return User.objects.get(username=bits[0])
    
    title_template = _global_title_template
    description_template = _global_description_template
    
    def items(self,obj):
        return Note.objects.filter(user=obj).order_by('-addtime')[:FEED_ITEM_MAX]
    
    def item_author_name(self, item):
        return item.user.realname
    
    def item_author_link(self, item):
        return user_tags.user_url(item.user.username)
    
    def item_link(self, item):
        return item.get_absolute_url()

    def item_pubdate(self, item):
        return item.addtime
    

    