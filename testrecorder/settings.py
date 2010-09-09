from django.conf import settings

FIXTURES = getattr(settings, 'RECORDER_FIXTURES', [])
AUTH = getattr(settings, 'RECORDER_AUTH', None)
IGNORE = getattr(settings, 'RECORDER_IGNORE', [])
AUTOLOGIN = getattr(settings, 'RECORDER_AUTOLOGIN', True)
FILES_PATH = getattr(settings, 'RECORDER_FILES_PATH', 'test/')