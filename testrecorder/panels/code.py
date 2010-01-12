from testrecorder.panels import Panel
from django.template.loader import render_to_string
from testrecorder.urls import _PREFIX

class CodePanel(Panel):
    
    name = 'Code'
    has_content = True
    
    def nav_title(self):
        return 'Get Code'

    def title(self):
        return 'Get Code'

    def url(self):
        return '/%s/code/' % _PREFIX

    def content(self):
        context = {
            'BASE_URL': '/%s' %  _PREFIX
        }
        return render_to_string('testrecorder/panels/code.html', context)    

#class_name_panel = CodePanel()