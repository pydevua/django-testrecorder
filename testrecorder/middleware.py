from django.conf import settings
from django.conf.urls.defaults import include, patterns
from testrecorder.utils import replace_insensitive
from testrecorder.toolbar import toolbar
import os
import testrecorder.urls
from django.utils.encoding import smart_unicode

_HTML_TYPES = ('text/html', 'application/xhtml+xml')
_STATUS_CODES = (200, 302)

class TestRecorderMiddleware(object):
    
    def __init__(self):
        self.override_url = True
        self.original_urlconf = settings.ROOT_URLCONF
        self.original_pattern = patterns('', ('', include(self.original_urlconf)),)        
    
    def process_request(self, request):
        if self.override_url:
            testrecorder.urls.urlpatterns += self.original_pattern
            self.override_url = False
        request.urlconf = 'testrecorder.urls'
        
    def process_view(self, request, view_func, view_args, view_kwargs):
        pass
        
    def process_response(self, request, response):
        if self._save_request(request, response):
            for panel in toolbar.panels:
                panel.process_response(request, response)
            if response.status_code == 200:            
                response.content = replace_insensitive(smart_unicode(response.content), u'</body>', smart_unicode(toolbar.render() + u'</body>'))
        return response
    
    def _save_request(self, request, response):
        if not response['Content-Type'].split(';')[0] in _HTML_TYPES:
            return False
        #This response has 'text/html' type
        if response.status_code == 304:
            return False
        if request.path.startswith(os.path.join('/', testrecorder.urls._PREFIX)):
            return False
        return True