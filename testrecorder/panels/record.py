from testrecorder.panels import Panel
from django.template.loader import render_to_string
from testrecorder.urls import _PREFIX
from django.core.urlresolvers import reverse
from testrecorder.utils import RequestRecord

class RecordPanel(Panel):
    
    name = 'RecordRequests'
    has_content = True
    
    def __init__(self):
        self.data = []
    
    def nav_title(self):
        return 'Reuqests'

    def title(self):
        return 'Reuqests'

    def url(self):
        return ''
    
    def delete(self, index):
        try:
            del self.data[index]
            return True
        except IndexError:
            return False
    
    def content(self):
        context = {
            'BASE_URL': '/%s' %  _PREFIX,
            'records': self.data
        }
        return render_to_string('testrecorder/panels/record.html', context)    

    def process_response(self, request, response):
        item = RequestRecord(request, response)
        self.data.append(item)

#record_handler = RecordPanel()