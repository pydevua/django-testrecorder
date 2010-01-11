from testrecorder.panels import Panel
from django.template.loader import render_to_string
from testrecorder.urls import _PREFIX
from django.core.urlresolvers import reverse
from testrecorder.utils import RequestRecord

class RecordPanel(Panel):
    
    name = 'RecordRequests'
    has_content = True
    
    def __init__(self):
        self._data = []
    
    def nav_title(self):
        from testrecorder.middleware import toolbar 
        return toolbar.start_record and 'Logs(started)' or 'Logs(stoped)'

    def title(self):
        from testrecorder.middleware import toolbar 
        return toolbar.start_record and 'Logs(started)' or 'Logs(stoped)'

    def url(self):
        return ''

    def content(self):
        context = {
            'BASE_URL': '/%s' %  _PREFIX,
            'records': self._data
        }
        return render_to_string('testrecorder/panels/record.html', context)    

    def process_response(self, request, response):
        from testrecorder.middleware import toolbar
        
        if (toolbar.start_record):
            item = RequestRecord(request, response)
            self._data.append(item)

record_handler = RecordPanel()