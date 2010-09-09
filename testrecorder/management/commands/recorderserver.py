from django.core.management.base import BaseCommand
from django.conf import settings
from optparse import make_option
import sys
from testrecorder.settings import FIXTURES 

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--addrport', action='store', dest='addrport',
            type='string', default='',
            help='port number or ipaddr:port to run the server on'),          
    )
    help = 'Runs a test server with data from the given fixture(s) and testrecorder toolbar.'
    args = '[fixture ...]'

    requires_model_validation = False
    
    def __init__(self, *args, **kwargs):
        self._set_middlewares()
        super(Command, self).__init__(*args, **kwargs)
    
    def handle(self, *fixture_labels, **options):         
        from django.core.management import call_command
        from testrecorder.middleware import toolbar
        
        if not fixture_labels:
            fixture_labels = FIXTURES
        toolbar.fixtures = fixture_labels
        call_command('testserver', *fixture_labels, **options)
     
    def _set_middlewares(self):
        middleware_name = 'testrecorder.middleware.TestRecorderMiddleware'
        autologin_middleware_name = 'testrecorder.middleware.AutoLoginMiddleware'
        auth_middleware_name = 'django.contrib.auth.middleware.AuthenticationMiddleware'
        
        MWARES = list(settings.MIDDLEWARE_CLASSES)
        if not middleware_name in settings.MIDDLEWARE_CLASSES:
            MWARES.insert(0, middleware_name)
            
        if not autologin_middleware_name in settings.MIDDLEWARE_CLASSES:
            if auth_middleware_name in MWARES:
                ind = MWARES.index('django.contrib.auth.middleware.AuthenticationMiddleware')
                MWARES.insert(ind+1, autologin_middleware_name)
            else:
                MWARES.append(autologin_middleware_name)
        settings.MIDDLEWARE_CLASSES = MWARES                             