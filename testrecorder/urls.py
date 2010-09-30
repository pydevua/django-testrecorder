from django.conf.urls.defaults import *
from django.conf import settings

_PREFIX = '__tr__'

rec_urlpatterns = patterns('testrecorder.views',
    url(r'^%s/m/(.*)$' % _PREFIX, 'media'),
    url(r'^%s/class_name/$' % _PREFIX, 'class_name'),
    url(r'^%s/add_function/$' % _PREFIX, 'add_function'),
    url(r'^%s/start/$' % _PREFIX, 'start'),
    url(r'^%s/stop/$' % _PREFIX, 'stop'),
    url(r'^%s/code/$' % _PREFIX, 'code'),
    url(r'^%s/init/$' % _PREFIX, 'init'),
    url(r'^%s/delete/$' % _PREFIX, 'delete', name='delete'),
    url(r'^%s/func_delete/$' % _PREFIX, 'func_delete'),
    url(r'^%s/change_func_name/$' % _PREFIX, 'change_func_name'),
    url(r'^%s/assertion/$' % _PREFIX, 'assertion', name='add_assertion'),
    url(r'^%s/assertion/remove/(\d+)/(\d+)/$' % _PREFIX, 'remove_assertions', name='remove_assertions'),
    url(r'^%s/load_requests/$' % _PREFIX, 'load_requests'),    
)

urlpatterns = patterns('',
    ('', include(rec_urlpatterns, 'test-recorder')),                       
)