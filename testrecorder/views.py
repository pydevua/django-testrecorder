import os
import django.views.static
from django.http import HttpResponse
from django.shortcuts import render_to_response
from testrecorder.middleware import toolbar
from django.conf import settings
    
def media(request, path):
    parent = os.path.abspath(os.path.dirname(__file__))
    root = os.path.join(parent, 'media', 'testrecorder')
    return django.views.static.serve(request, path, root)

def start(request):
    toolbar.start_record = True
    return HttpResponse('{}')

def stop(request):
    toolbar.start_record = False
    return HttpResponse('{}')

def class_name(request):
    name = request.POST.get('name', None)
    if name:
        toolbar.class_name = name
    return HttpResponse('{}')

def function_name(request):
    name = request.POST.get('name', None)
    if name:
        toolbar.func_name = name
    return HttpResponse('{}')

def code(request):
    try:
        auth = settings.RECORDER_SETTINGS['auth']
    except (AttributeError, KeyError):
        auth = None
    context = {
        'class_name': toolbar.class_name,
        'fixtures': toolbar.fixtures,
        'func_name': toolbar.func_name,
        'requests': toolbar.requests,
        'auth': auth
    }
    
    return render_to_response('testrecorder/code.txt', context)
    
    