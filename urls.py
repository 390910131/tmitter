from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    # (r'^note/', include('note.foo.urls')),
    (r'^$','tmitter.mvc.views.index'),
    (r'^user/(?P<_username>[a-zA-Z\-_\d]+)/$','tmitter.mvc.views.index_param'),
    (r'^signin/$','tmitter.mvc.views.signin'),
    (r'^signout/$','tmitter.mvc.views.signout'),
    
    (r'^message/(?P<_id>\d+)/$','tmitter.mvc.views.detail'),
    # Uncomment this for admin:
    (r'^admin/', include('django.contrib.admin.urls')),
)
