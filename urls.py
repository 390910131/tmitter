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
    (r'^signin/$','tmitter.mvc.views.signin'),
    (r'^signout/$','tmitter.mvc.views.signout'),
    (r'^signup/$','tmitter.mvc.views.signup'),
    (r'^settings/$','tmitter.mvc.views.settings'),
    (r'^message/(?P<_id>\d+)/$','tmitter.mvc.views.detail'),
    (r'^message/(?P<_id>\d+)/delete/$','tmitter.mvc.views.detail_delete'),
    (r'^mail/$','tmitter.utils.mailer.test'),
    # Uncomment this for admin:
    (r'^admin/(.*)',admin.site.root),
    (r'^feed/rss/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': rss_feeds}),
    (r'^user/feed/rss/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': rss_user_feeds}),
    (r'^styles/(?P<path>.*)$', 'django.views.static.serve', {'document_root': './statics/styles'}),
    (r'^scripts/(?P<path>.*)$', 'django.views.static.serve', {'document_root': './statics/scripts'}),
    (r'^images/(?P<path>.*)$', 'django.views.static.serve', {'document_root': './statics/images'}),
    (r'^uploads/(?P<path>.*)$', 'django.views.static.serve', {'document_root': './statics/uploads'}),

)
