from django.template.loader import render_to_string
from testrecorder.urls import _PREFIX
from testrecorder.panels import Panel
from django.conf import settings
from testrecorder.panels.classname import ClassNamePanel
from testrecorder.panels.functionname import FunctionNamePanel
from testrecorder.panels.record import RecordPanel
from testrecorder.panels.code import CodePanel
import re

class Toolbar(object):
    
    def __init__(self):
        self.init = True
        self.start_record = False
        self.fixtures = []        
        self.cls_name_panel = ClassNamePanel()
        self.func_name_panel = FunctionNamePanel()
        self.record_panel = RecordPanel()
        self.code_panel = CodePanel()
        self._init_inore_patterns()
        
    def _init_inore_patterns(self):
        self.ignore = []
        patterns = settings.RECORDER_IGNORE
        for item in patterns:
            self.ignore.append(re.compile(item))
    
    def change_func_name(self, index, name):
        self.record_panel.change_func_name(index, name)
        if (len(self.record_panel.store) - 1) == index:
            self.func_name = name
             
    def delete(self, func_index, index):
        return self.record_panel.delete(func_index, index)
    
    def delete_func(self, index):
        return self.record_panel.delete_func(index)     
    
    @property
    def panels(self):
        return [
            self.cls_name_panel,
            self.func_name_panel,
            self.record_panel,
            self.code_panel,                
        ]
    
    def add_function(self, name):
        self.func_name = name
        self.record_panel.add_function(name)
    
    def get_class_name(self):
        return self.cls_name_panel.class_name
    
    def set_class_name(self, name):
        self.cls_name_panel.class_name = name
    
    class_name = property(get_class_name, set_class_name)
    
    def set_func_name(self, name):
        self.func_name_panel.function_name = name

    def get_func_name(self):
        return self.func_name_panel.function_name

    func_name = property(get_func_name, set_func_name)
    
    @property
    def records(self):
        return self.record_panel.store
    
    def is_valid_path(self, request):
        path = request.path_info
        for pattern in self.ignore:
            if pattern.match(path):
                return False
        return True
        
    def process_response(self, request, response):
        self.is_valid_path(request)
        if self.start_record and self.is_valid_path(request):
            if not self.record_panel.store:
                self.add_function(self.func_name)
            self.record_panel.process_response(request, response)
    
    def render(self):
        return render_to_string('testrecorder/base.html', {
            'panels': self.panels,
            'start': self.start_record,
            'init': self.init,
            'BASE_URL': '/%s' %  _PREFIX,
        })
        
toolbar = Toolbar()