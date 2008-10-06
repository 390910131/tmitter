# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.contrib import admin
from tmitter.mvc.feed import RSSRecentNotes,RSSUserRecentNotes

admin.autodiscover()

rss_feeds = {
    'recent': RSSRecentNotes,
}

rss_user_feeds = {
    'recent': RSSUserRecentNotes,
}

urlpatterns = patterns('',
    # Example:
    # (r'^note/', include('note.foo.urls')),
    (r'^$','tmitter.mvc.views.index'),
    (r'^p/(?P<_page_index>\d+)/$','tmitter.mvc.views.index_page'),
    (r'^user/$','tmitter.mvc.views.index_user_self'),
    (r'^user/(?P<_username>[a-zA-Z\-_\d]+)/$','tmitter.mvc.views.index_user'),
    (r'^user/(?P<_username>[a-zA-Z\-_\d]+)/(?P<_page_index>\d+)/$','tmitter.mvc.views.index_user_page'),
    (r'^users/$','tmitter.mvc.views.users_index'),
    (r'^users/(?P<_page_index>\d+)/$','tmitter.mvc.views.users_list'),
    (r'^signin/$','tmitter.mvc.views.signin'),
    (r'^signout/$','tmitter.mvc.views.signout'),
    (r'^signup/$','tmitter.mvc.views.signup'),
    (r'^settings/$','tmitter.mvc.views.settings'),
    (r'^message/(?P<_id>\d+)/$','tmitter.mvc.views.detail'),
    (r'^message/(?P<_id>\d+)/delete/$','tmitter.mvc.views.detail_delete'),
    (r'^friend/add/(?P<_username>[a-zA-Z\-_\d]+)','tmitter.mvc.views.friend_add'),
    (r'^friend/remove/(?P<_username>[a-zA-Z\-_\d]+)','tmitter.mvc.views.friend_remove'),
    (r'^api/note/add/','tmitter.mvc.views.api_note_add'),
    # Uncomment this for admin:
    (r'^admin/(.*)',admin.site.root),
    (r'^feed/rss/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': rss_feeds}),
    (r'^user/feed/rss/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': rss_user_feeds}),	
    (r'^statics/(?P<path>.*)$', 'django.views.static.serve', {'document_root': './statics'}),
    (r'^i18n/', include('django.conf.urls.i18n')),

)
