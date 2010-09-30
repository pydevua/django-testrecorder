====================
django-test-recorder
====================

Tool for generating tests for Django projects.

#Using:#

Run ./manage.py recorderserver <fixture fixture ...> and visit http://127.0.0.1:8000.
This command support same options like "testserver" command.

#Examples of settings:#

import sys
sys.path.insert(0, '/some_path/test-recorder') #or just copy it to PYTHONPATH

INSTALLED_APPS += (
    'testrecorder',
)

RECORDER_AUTOLOGIN = True
RECORDER_AUTH = {
    'username': 'admin',
    'password': 'admin'
}
RECORDER_FIXTURES = ['test.json']
RECORDER_IGNORE = (
    '^/admin.*',      
)

For all available settings see testrecorder.settings.py

#More#

Tested with Django 1.1+. 
The project code and bugtracker is hosted on http://github.com/pydevua/django-testrecorder.
Thanks for downloading. We are glad to hear your questions, comments or suggestions!
Thanks django-debug-toolbar for styles :)