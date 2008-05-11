from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    # (r'^note/', include('note.foo.urls')),
    (r'^$','tmitter.mvc.views.index'),
    (r'^p/(?P<_page_index>\d+)/$','tmitter.mvc.views.index_page'),
    (r'^user/(?P<_username>[a-zA-Z\-_\d]+)/$','tmitter.mvc.views.index_user'),
    (r'^signin/$','tmitter.mvc.views.signin'),
    (r'^signout/$','tmitter.mvc.views.signout'),
    
    (r'^message/(?P<_id>\d+)/$','tmitter.mvc.views.detail'),
    (r'^message/(?P<_id>\d+)/delete/$','tmitter.mvc.views.detail_delete'),
    # Uncomment this for admin:
    (r'^admin/', include('django.contrib.admin.urls')),
)
