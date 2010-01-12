from django.core.management.base import BaseCommand
from django.conf import settings
from optparse import make_option
import sys

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--addrport', action='store', dest='addrport',
            type='string', default='',
            help='port number or ipaddr:port to run the server on'),          
    )
    help = 'Runs a test server with data from the given fixture(s) and testrecorder toolbar.'
    args = '[fixture ...]'

    requires_model_validation = False
    
    def handle(self, *fixture_labels, **options):         
        from django.core.management import call_command
        from testrecorder.middleware import toolbar
        
        middleware_name = 'testrecorder.middleware.TestRecorderMiddleware'
        if not middleware_name in settings.MIDDLEWARE_CLASSES:
            settings.MIDDLEWARE_CLASSES += (
                'testrecorder.middleware.TestRecorderMiddleware',
            )
        if not fixture_labels:
            try:
                fixture_labels = settings.RECORDER_SETTINGS['fixtures']
            except (AttributeError, KeyError):
                sys.exit('ERROR: Set fixtures in arguments or settings.TEST_RUNNER_FIXTURES')
        toolbar.fixtures = fixture_labels
        call_command('testserver', *fixture_labels, **options)
        