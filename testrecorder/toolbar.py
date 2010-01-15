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
    
    start_record = False
    fixtures = []
    
    def __init__(self):
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
             
    def delete(self, index):
        self.record_panel.delete(index)
    
    @property
    def panels(self):
        return [
            self.cls_name_panel,
            self.func_name_panel,
            self.record_panel,
            self.code_panel,                
        ]
    
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
    def requests(self):
        return self.record_panel.data
    
    def is_valid_path(self, request):
        path = request.path_info
        for pattern in self.ignore:
            if pattern.match(path):
                return False
        return True
        
    def process_response(self, request, response):
        self.is_valid_path(request)
        if self.start_record and self.is_valid_path(request):
            self.record_panel.process_response(request, response)
    
    def render(self):
        return render_to_string('testrecorder/base.html', {
            'panels': self.panels,
            'start': self.start_record,
            'BASE_URL': '/%s' %  _PREFIX,
        })
        
toolbar = Toolbar()