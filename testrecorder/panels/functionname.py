from testrecorder.panels import Panel
from django.template.loader import render_to_string
from testrecorder.urls import _PREFIX

class FunctionNamePanel(Panel):
    
    name = 'FunctionName'
    has_content = True
    function_name = 'test_func'
    
    def nav_title(self):
        return 'Function name: %s' % self.function_name

    def title(self):
        return 'Function name'

    def url(self):
        return ''

    def content(self):
        context = {
            'BASE_URL': '/%s' %  _PREFIX
        }
        return render_to_string('testrecorder/panels/function_name.html', context)    

#function_name_panel = FunctionNamePanel()