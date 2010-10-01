from testrecorder.panels import Panel
from django.template.loader import render_to_string
from testrecorder.urls import _PREFIX
from django.db import models
from django.utils.text import capfirst
from testrecorder import settings

class FixturePanel(Panel):
    
    name = 'Fixtures'
    has_content = True
    
    def __init__(self):
        self.ignore_apps = []
        self.ignore_models = []
        for item in settings.EXCLUDE_MODELS:
            if '.' in item:
                self.ignore_models.append(item)
            else:
                self.ignore_apps.append(item)
    
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
                opt = model._meta
                
                if opt.app_label in self.ignore_apps:
                    continue
                if '%s.%s' % (opt.app_label, opt.object_name) in self.ignore_models:
                    continue
                if not model.objects.exists():
                    continue
                
                d = {
                    'verbose_name': capfirst(opt.verbose_name_plural),
                    'model': model,
                    'model_name': '%s.%s' % (opt.app_label, opt.object_name)
                }
                obj['models'].append(d)
            
            if obj['models']:
                model_dict.append(obj)
            
        context = {
            'BASE_URL': '/%s' %  _PREFIX,
            'model_dict': model_dict
        }
        return render_to_string('testrecorder/panels/fixture.html', context) 
