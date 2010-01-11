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
    help = 'Runs a development server with data from the given fixture(s).'
    args = '[fixture ...]'

    requires_model_validation = False

    def handle(self, *fixture_labels, **options):            
        from django.core.management import call_command

        settings.MIDDLEWARE_CLASSES += (
            'testrecorder.middleware.TestRecorderMiddleware',
        )
        if not fixture_labels:
            fixture_labels = settings.TEST_RUNNER_FIXTURES
        call_command('testserver', *fixture_labels, **options)
        