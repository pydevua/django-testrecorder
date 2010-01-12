import os
import django.views.static
from django.http import HttpResponse
from testrecorder.panels.classname import class_name_panel
from testrecorder.panels.functionname import function_name_panel
from testrecorder.panels.record import record_handler 
from django.shortcuts import render_to_response

def media(request, path):
    parent = os.path.abspath(os.path.dirname(__file__))
    root = os.path.join(parent, 'media', 'testrecorder')
    return django.views.static.serve(request, path, root)

def start(request):
    from testrecorder.middleware import toolbar
    toolbar.start_record = True
    return HttpResponse('{}')

def stop(request):
    from testrecorder.middleware import toolbar
    toolbar.start_record = False
    return HttpResponse('{}')

def class_name(request):
    name = request.POST.get('name', None)
    if name:
        class_name_panel.class_name = name
    return HttpResponse('{}')

def function_name(request):
    name = request.POST.get('name', None)
    if name:
        function_name_panel.function_name = name
    return HttpResponse('{}')

def code(request):
    from testrecorder.middleware import toolbar
    print toolbar.fixtures
    context = {
        'class_name': class_name_panel.class_name
    }
    
    return render_to_response('testrecorder/code.txt', context)
    
    