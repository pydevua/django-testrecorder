from django.template.loader import render_to_string
from testrecorder.urls import _PREFIX
from testrecorder.panels import Panel

class Toolbar(object):
    
    start_record = False
    
    def __init__(self):
        from testrecorder.panels.classname import class_name_panel
        from testrecorder.panels.functionname import function_name_panel
        from testrecorder.panels.record import record_handler         
        self.default_panels = (
            class_name_panel,
            function_name_panel,
            record_handler                   
        )      
        self.panels = []
        self.init_panels()       

    def init_panels(self):
        for panel in self.default_panels:
            if isinstance(panel, Panel):
                self.panels.append(panel)
            else:
                self.panels.append(panel())
    
    def render(self):
        return render_to_string('testrecorder/base.html', {
            'panels': self.panels,
            'start': self.start_record,
            'BASE_URL': '/%s' %  _PREFIX,
        })