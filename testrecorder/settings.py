from django.conf import settings

#fixtures loaded with recorder server and used for testing
FIXTURES = getattr(settings, 'RECORDER_FIXTURES', [])

#authentication data. For example: 
#{'username': 'test', 'password': 'test'}
#sended to django.contrib.auth.authenticate like **AUTH 
AUTH = getattr(settings, 'RECORDER_AUTH', None)

#If AUTOLOGIN - AutoLoginMiddleware try to authenticate user using AUTH option
AUTOLOGIN = getattr(settings, 'RECORDER_AUTOLOGIN', True)

#patterns for ignoring some request.  For example:
#('^/admin.*',)
#if pattern.match(request.path_info) it is not recorded
IGNORE = getattr(settings, 'RECORDER_IGNORE', [])

#path to save request.FILES related to settings.MEDIA_ROOT
FILES_PATH = getattr(settings, 'RECORDER_FILES_PATH', 'test/')

#Show auto-start initial window or not?
INIT_ON_START = getattr(settings, 'RECORDER_INIT_ON_START', True)