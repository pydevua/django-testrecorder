from testrecorder.panels import Panel
from django.template.loader import render_to_string
from testrecorder.urls import _PREFIX
from django.utils.safestring import mark_safe
from testrecorder.settings import DEFAULT_CLASS_NAME

class ClassNamePanel(Panel):
    
    name = 'TestcaseName'
    has_content = True
    class_name = DEFAULT_CLASS_NAME
    
    def nav_title(self):
        return mark_safe('Class name: <span>%s</span>' % self.class_name)

    def title(self):
        return 'Class name'

    def url(self):
        return ''

    def content(self):
        context = {
            'class_name': self.class_name,
            'BASE_URL': '/%s' %  _PREFIX
        }
        return render_to_string('testrecorder/panels/class_name.html', context)    

#class_name_panel = ClassNamePanel()