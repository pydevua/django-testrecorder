from django.conf.urls.defaults import *
from django.conf import settings

_PREFIX = '__tr__'

urlpatterns = patterns('testrecorder.views',
    url(r'^%s/m/(.*)$' % _PREFIX, 'media'),
    url(r'^%s/class_name/$' % _PREFIX, 'class_name'),
    url(r'^%s/function_name/$' % _PREFIX, 'function_name'),
    url(r'^%s/start/$' % _PREFIX, 'start'),
    url(r'^%s/stop/$' % _PREFIX, 'stop'),
    url(r'^%s/code/$' % _PREFIX, 'code'),
)
