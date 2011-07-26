Installation
============

For installation get source code from `repo <https://github.com/pydevua/django-testrecorder>`_,
and use ``python setup.py install``. Or you can install with ``pip install django-testrecorder``,
but it can contain not up-to-date version.

Edit ``settings.py`` to add ``'testrecorder'`` to ``INSTALLED_APPS``.

Usage
=====

To start server use command ``python manage.py recorderserver``. This is just 
wrapper for django ``testserver`` command, so any data in current database will
not be affected. 

Now you can visit ``http://127.0.0.1:8000/`` and all your actions will be recorded
and then you can get tests for this actions.

Settings
========

You can add fixtures that will be loaded automatically. 

::

    RECORDER_FIXTURES = [
        'test1.json', 
        'test2.json', 
        'test3.json',
        'test4.json'
    ]
    
You can set URLS that will not be recorded. 

::

    RECORDER_IGNORE = (
        '^/favicon.ico',
        '^/admin.*',      
    )
    
Also you can set auto-login. For default auth-backend this looks like this:

::

    RECORDER_AUTOLOGIN = True
    RECORDER_AUTH = {
        'username': 'admin',
        'password': 'admin'
    }
    
If you upload some files during test recording they will be saved in ``MEDIA_ROOT/test/``
and used in tests. You can change path with ``RECORDER_FILES_PATH`` setting:

::

    RECORDER_FILES_PATH = 'files_to_test/'
    
You can turn on testing form validation with ``RECORDER_TEST_FORM_VALIDATION``.
It is turned off by default, because is experimental feauture. 
his does not call any lazy objects in context or form validation before request finished
and just check in test if form have same validation state that was recorded. 

You can turn on testing of emails sending with ``RECORDER_TEST_EMAIL_SENDING``.
In this case ``django.core.mail.backends.locmem.EmailBackend`` will be set as
``EMAIL_BACKEND`` and testrecorder will save number of sent emails.