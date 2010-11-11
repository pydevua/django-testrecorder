from testrecorder.panels import Panel
from django.template.loader import render_to_string
from testrecorder.urls import _PREFIX
from django.utils.safestring import mark_safe
from testrecorder.settings import DEFAULT_FUNC_NAME 

class FunctionNamePanel(Panel):
    
    name = 'FunctionName'
    has_content = True
    function_name = DEFAULT_FUNC_NAME 
    
    def nav_title(self):
        mark_safe
        return mark_safe('Function: <span class="small">%s</span>' % self.function_name)

    def title(self):
        return 'Add function'

    def url(self):
        return ''

    def content(self):
        context = {
            'BASE_URL': '/%s' %  _PREFIX
        }
        return render_to_string('testrecorder/panels/function_name.html', context)    

#function_name_panel = FunctionNamePanel()