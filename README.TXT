./manage.py recorderserver [fixture.json]

#local_settings.py example
from settings import INSTALLED_APPS
import sys
sys.path.insert(0, '/some_path/test-recorder')

RECORDER_SETTINGS = {
    'fixtures': ['fixture.json'],
    'ignore': (
         '^/admin.*',      
    ),
    'auth': {
        'username': 'admin',
        'password': '123'     
    },    
}
INSTALLED_APPS += (
    'testrecorder',
)
