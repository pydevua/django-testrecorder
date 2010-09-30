from testrecorder.panels import Panel
from django.template.loader import render_to_string
from testrecorder.urls import _PREFIX
from testrecorder.utils import ActionStorage

class RecordPanel(Panel):
    
    name = 'RecordRequests'
    has_content = True
    
    def __init__(self):
        self.store = ActionStorage()
    
    def change_func_name(self, index, name):
        try:
            self.store.rename_func(index, name)
            return True
        except IndexError:
            return False        
    
    def add_function(self, name):
        self.store.add_function(name)
    
    def nav_title(self):
        return 'Requests'

    def title(self):
        return 'Requests'

    def url(self):
        return ''
    
    def remove_assertion(self, func_index, index):
        try:
            self.store.remove_assertion(func_index, index)
            return True
        except IndexError:
            return False
    
    def add_assertion(self, value, func_index=None, index=None):
        try:
            self.store.add_assertion(value, func_index, index)
            return True
        except IndexError:
            return False
        
    
    def delete(self, func_index, index):
        try:
            self.store.delete_request(func_index, index)
            return True
        except IndexError:
            return False

    def delete_func(self, index):
        try:
            self.store.delete_func(index)
            return True
        except IndexError:
            return False
    
    def content(self):
        context = {
            'BASE_URL': '/%s' %  _PREFIX,
            'records': self.store
        }
        return render_to_string('testrecorder/panels/record.html', context)    

    def process_response(self, request, response):
        self.store.add_request(request, response)