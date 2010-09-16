from testrecorder.panels import Panel
from django.template.loader import render_to_string
from testrecorder.urls import _PREFIX
from django.db import models

class FixturePanel(Panel):
    
    name = 'Fixtures'
    has_content = True
    
    def nav_title(self):
        return 'Fixtures'

    def title(self):
        return 'Fixtures builder'

    def url(self):
        return ''

    def content(self):
        all_models = [
            (app.__name__.split('.')[-2],
                [m for m in models.get_models(app, include_auto_created=True)])
            for app in models.get_apps()
        ]
        context = {
            'BASE_URL': '/%s' %  _PREFIX
        }
        return render_to_string('testrecorder/panels/fixture.html', context) 
