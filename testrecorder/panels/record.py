from testrecorder.panels import Panel
from django.template.loader import render_to_string
from testrecorder.urls import _PREFIX
from django.core.urlresolvers import reverse
from testrecorder.utils import RequestRecord, TestFunctionRecord

class RecordPanel(Panel):
    
    name = 'RecordRequests'
    has_content = True
    
    def __init__(self):
        self.data = []
    
    def change_func_name(self, index, name):
        try:
            self.data[index].name = name
            return True
        except IndexError:
            return False        
    
    def add_function(self, name):
        self.data.append(TestFunctionRecord(name))
    
    def nav_title(self):
        return 'Requests'

    def title(self):
        return 'Requests'

    def url(self):
        return ''
    
    def delete(self, func_index, index):
        try:
            return self.data[func_index].delete(index)
        except IndexError:
            return False

    def delete_func(self, index):
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
        self.data[-1].add(item)

#record_handler = RecordPanel()