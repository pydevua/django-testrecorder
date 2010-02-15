import os
import django.views.static
from django.http import HttpResponse
from django.shortcuts import render_to_response
from testrecorder.middleware import toolbar
from django.conf import settings
from django.core.management import call_command

def media(request, path):
    parent = os.path.abspath(os.path.dirname(__file__))
    root = os.path.join(parent, 'media', 'testrecorder')
    return django.views.static.serve(request, path, root)

def init(request):
    class_name = request.POST.get('class_name', None)
    func_name = request.POST.get('func_name', None)
    if class_name:
        toolbar.class_name = class_name
    if func_name:
        toolbar.add_function(func_name)
    toolbar.init = False
    toolbar.start_record = True            
    return HttpResponse('{}')

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

def change_func_name(request):
    id = request.POST.get('id', None)
    value = request.POST.get('value', None)
    if id and value:
        toolbar.change_func_name(int(id[4:]), value)
    return HttpResponse(value)

def add_function(request):
    name = request.POST.get('name', None)
    if name:
        toolbar.add_function(name)
    call_command('flush', interactive=False)
    call_command('loaddata', *toolbar.fixtures)    
    return HttpResponse('{}')

def delete(request):
    index = request.GET.get('index', None)
    func_index = request.GET.get('func_index', None)
    index and func_index and toolbar.delete(int(func_index), int(index))
    return HttpResponse(toolbar.record_panel.content())

def func_delete(request):
    index = request.GET.get('index', None)
    index and toolbar.delete_func(int(index))
    return HttpResponse(toolbar.record_panel.content())

def code(request):
    return HttpResponse(toolbar.get_code())

def assertion(request):
    index = request.GET.get('index', None)
    func_index = request.GET.get('func_index', None)
    value = request.POST.get('value', None)
    if not index is None:
        index = int(index)
    if not func_index is None:
        func_index = int(func_index)        
    value and toolbar.add_assertion(value, func_index, index)    
    return HttpResponse('{}')    
    