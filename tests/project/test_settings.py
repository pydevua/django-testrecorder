from settings import *

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'main',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware', 
    'django.contrib.sessions.middleware.SessionMiddleware', 
    'django.middleware.locale.LocaleMiddleware', 
    'django.middleware.csrf.CsrfViewMiddleware', 
    'django.contrib.auth.middleware.AuthenticationMiddleware', 
    'testrecorder.middleware.AutoLoginMiddleware'
)