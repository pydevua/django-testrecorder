from django.conf import settings
from django.conf.urls.defaults import include, patterns
from testrecorder.utils import RequestRecorder, replace_insensitive
from testrecorder.toolbar import Toolbar
import os
import testrecorder.urls
from django.utils.encoding import smart_unicode

_HTML_TYPES = ('text/html', 'application/xhtml+xml')
start_record = False
toolbar = Toolbar()

class TestRecorderMiddleware(object):
    _cache = RequestRecorder()
    _toolbar = toolbar
    
    def __init__(self):
        self.override_url = True
        self.original_urlconf = settings.ROOT_URLCONF
        self.original_pattern = patterns('', ('', include(self.original_urlconf)),)        
    
    def process_request(self, request):
        if self.override_url:
            testrecorder.urls.urlpatterns += self.original_pattern
            self.override_url = False
        request.urlconf = 'testrecorder.urls'
        for panel in self.toolbar.panels:
            panel.process_request(request)
        
    def process_view(self, request, view_func, view_args, view_kwargs):
        pass
        
    def process_response(self, request, response):
        print start_record  
        if response['Content-Type'].split(';')[0] in _HTML_TYPES:
            self._cache.add_request(response.status_code)
            print self._cache._requests
            response.content = replace_insensitive(smart_unicode(response.content), u'</body>', smart_unicode(self._toolbar.render() + u'</body>'))
        return response                               
    
    def _show_toolbar(self, request):
        return True  