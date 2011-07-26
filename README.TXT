Documentation: http://django-testrecorder.readthedocs.org/en/latest/

====================
django-test-recorder
====================

Tool for generating tests for Django projects.

Статья о django-test-recorder: http://djbook.ru/examples/27/

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

NOTES:

1. If you have some middleware that changes request.path_info, maybe you should
add 'testrecorder.middleware.TestRecorderMiddleware' manually after you middleware.

2. **Use Firefox please**, because we have some problems with Chrome :( 

#More#

Tested with Django 1.1 - 1.2.5. 
The project code and bugtracker is hosted on http://github.com/pydevua/django-testrecorder.
Thanks for downloading. We are glad to hear your questions, comments or suggestions!
Thanks django-debug-toolbar for styles :)

Projects are very different so it is not so easy provide all situation. So if you 
get error create please issue. It will be good if you send js error or traceback 
from console. If your project is open, left please link to the repository.
Just settings.MIDDLEWARE_CLASSES can be good too. 
