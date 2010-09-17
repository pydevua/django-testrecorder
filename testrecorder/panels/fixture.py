from testrecorder.panels import Panel
from django.template.loader import render_to_string
from testrecorder.urls import _PREFIX
from django.db import models
from django.utils.text import capfirst

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
        model_dict = []
        for app in models.get_apps():
            obj = {
                'app': app.__name__.split('.')[-2],
                'models': []   
            } 
            for model in models.get_models(app, include_auto_created=True):
                if not model.objects.exists():
                    continue
                
                d = {
                    'name': capfirst(model._meta.verbose_name_plural),
                    'model': model
                }
                obj['models'].append(d)
            
            if obj['models']:
                model_dict.append(obj)
            
        context = {
            'BASE_URL': '/%s' %  _PREFIX,
            'model_dict': model_dict
        }
        return render_to_string('testrecorder/panels/fixture.html', context) 
