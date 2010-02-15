from testrecorder.panels import Panel
from django.template.loader import render_to_string
from testrecorder.urls import _PREFIX
from django.utils.safestring import mark_safe

class AssertionPanel(Panel):
    
    name = 'Assertion'
    has_content = True
    
    def nav_title(self):
        return mark_safe('Add assertion')

    def title(self):
        return 'Add assertion'

    def url(self):
        return ''

    def content(self):
        context = {
            'BASE_URL': '/%s' %  _PREFIX
        }
        return render_to_string('testrecorder/panels/assertion.html', context)  