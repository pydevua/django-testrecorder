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
        self.existed_objects = {}
        for item in settings.EXCLUDE_MODELS:
            if '.' in item:
                self.ignore_models.append(item)
            else:
                self.ignore_apps.append(item)
        
        self._init_existed_objects()
    
    def _init_existed_objects(self):
        for model in models.get_models():
            opt = model._meta
            name = '%s.%s' % (opt.app_label, opt.object_name)
            
            if self.ignore_model(opt.app_label, opt.object_name):
                self.existed_objects[name] = []          
            else:
                self.existed_objects[name] = list(model.objects.values_list('pk', flat=True))
    
    def get_objects(self, name, ids, includ_existed=False):
        model = models.get_model(*name.split('.'))
        qs = model._default_manager.filter(pk__in=ids)
        if not includ_existed:
            print self.existed_objects[name]
            qs = qs.exclude(pk__in=self.existed_objects[name])
        return qs
    
    def nav_title(self):
        return 'Fixtures'

    def title(self):
        return 'Fixtures builder(Beta)'

    def url(self):
        return ''
    
    def ignore_model(self, app_label, model_name):
        if app_label in self.ignore_apps:
            return True
        if '%s.%s' % (app_label, model_name) in self.ignore_models:
            return True
        return False      
    
    def content(self):
        model_dict = []
        for app in models.get_apps():
            obj = {
                'app': app.__name__.split('.')[-2],
                'models': []   
            } 
            for model in models.get_models(app, include_auto_created=True):
                opt = model._meta
                
                if self.ignore_model(opt.app_label, opt.object_name):
                    continue
                if not model.objects.exists():
                    continue
                
                d = {
                    'verbose_name': capfirst(opt.verbose_name_plural),
                    'model': model,
                    'model_name': '%s.%s' % (opt.app_label, opt.object_name)
                }
                d['existed_objects'] = self.existed_objects[d['model_name']]
                obj['models'].append(d)
            
            if obj['models']:
                model_dict.append(obj)
            
        context = {
            'BASE_URL': '/%s' %  _PREFIX,
            'model_dict': model_dict
        }
        return render_to_string('testrecorder/panels/fixture.html', context) 
