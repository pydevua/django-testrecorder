from django.core.urlresolvers import RegexURLResolver, RegexURLPattern, Resolver404, get_resolver
from django.utils.encoding import smart_str
from django.utils.http import urlencode
from testrecorder.settings import FILES_PATH
from django.core.files.storage import FileSystemStorage
from django.http import Http404
from django.forms import BaseForm

class CodeNode(object):
    
    def __init__(self, level=0, tab='    '):
        self.code = []
        self.level = level
        self.tab = tab
        self.markers = {}
    
    def child_node(self):
        return CodeNode(self.level, self.tab)
    
    def marker(self, name):
        self.markers[name] = (len(self.code), self.level)
    
    def insert(self, name, string):
        index, level = self.markers[name]
        self.code.insert(index, self.tab * level + string+'\n')
        return self
        
    def add(self, string):
        if string is None:
            return self
        if isinstance(string, CodeNode):
            self.code.append(str(string))
        else:
            self.code.append(self.tab * self.level + string+'\n')
        return self

    def indent(self):
        self.level += 1
        return self
        
    def dedent(self):
        if self.level == 0:
            raise SyntaxError, "internal error in code generator"
        self.level -= 1
        return self
    
    def blank(self):
        return self.add('')
    
    def render(self):
        return ''.join(self.code)

    def __str__(self):
        return self.render()
    
class TestGenerator(object):
    
    def __init__(self, class_name, fixtures, auth, store):
        self.class_name = class_name
        self.fixtures = fixtures
        self.auth = auth
        self.store = store
    
    def add_imports(self, node):
        node.add('# -*- coding: utf-8 -*-')
        node.add('from django.test import TestCase')
        node.add('from django.core.urlresolvers import reverse')
        node.marker('import')
        return node        
    
    def add_fixtures(self, node):
        if not self.fixtures:
            return node 
        
        fixtures_str = '", "'.join(self.fixtures)
        
        if len(fixtures_str) < 80:
            node.add('fixtures = ["%s"]' % fixtures_str)
        else:
            node.add('fixtures = [')
            node.indent()
            for item in self.fixtures[:-1]:
                node.add('"%s",' % item)   
            node.add('"%s"' % self.fixtures[-1])                 
            node.dedent()
            node.add(']')
    
    def dict_values(self, values):
        
        def get_value(val):
            if len(unicode(val).splitlines()) > 1:
                return 'u"""%s"""' % val
            if isinstance(val, FileProxy):
                return 'open(path.join(settings.MEDIA_ROOT, "%s"), "rb")' % val.path
            if isinstance(val, list):
                if len(val) > 1:
                    return '[%s]' % ', '.join(map(get_value, val))
                elif len(val) == 1:
                    return get_value(val[0])
                else:
                    return ''
            return 'u"%s"' % unicode(val)                
        
        values_length = len(values)
        for i, item in enumerate(values):
            string = '"%s": %s' % (item[0], get_value(item[1]))
            if not i == (values_length - 1): string += ','
            yield string
                
    def add_auth(self, node):
        node.add('self.auth = {').indent()
        for item in self.dict_values(self.auth.items()):
            node.add(item)
        node.dedent().add('}')
        return node        
    
    def add_setup(self, node):
        if not self.auth:
            return
        node.add('def setUp(self):').indent()
        auth_node = self.add_auth(node.child_node())
        return node.add(auth_node).dedent()   
    
    def add_request(self, request, node):
        if request.files and not hasattr(self, '_import_for_files'):
            setattr(self, '_import_for_files', True)
            node.insert('import', 'from django.conf import settings')
            node.insert('import', 'from os import path')
        if request.is_data() and not request.is_data_short():
            node.add('data = {').indent()
            for item in self.dict_values(request.data):
                node.add(item)
            node.dedent().add('}')
        if request.is_url_short():
            url = request.url_reverse
        else:
            url = 'url'
            node.add('url = %s%s' % (request.url_reverse, request.get_param()))
        if request.is_data():
            if request.is_data_short():
                data = ', %s' % request.short_data
            else:
                data = ', data'
        else:
            data = ''
        node.add('response = self.client.%s(%s%s)' % (request.method.lower(), url, data))
        node.add('self.failUnlessEqual(response.status_code, %s)' % request.code)
        if request.redirect_url:
            node.add('self.failUnlessEqual(response["Location"], "http://testserver%s")' % request.redirect_url)
        for assertion in request.assertions:
            node.add(assertion)
        for context_name, form in request.forms.items():
            if form.is_valid():
                node.add('self.failUnless(response.context["%s"].is_valid())' % context_name)
            else:
                #for fname, errors in form.errors.items():
                #    node.add('self.assertFormError(response, "%s", "%s", %s)' % (context_name, fname, list(errors)))
                node.add('self.failIf(response.context["%s"].is_valid())' % context_name)
        return node.blank()
    
    def add_func(self, func, node):
        node.add('def %s(self):' % func.name).indent()
        if self.auth:
            node.add('self.client.login(**self.auth)').blank()
        for item in func.records:
            self.add_request(item, node)
        node.dedent()
    
    def render(self):
        node = CodeNode()
        self.add_imports(node)
        node.blank().add('class %s(TestCase):' % self.class_name).indent()
        self.add_fixtures(node)
        self.add_setup(node)
        node.blank()
        for item in self.store:
            self.add_func(item, node)
        return node.render()
        
    def __unicode__(self):
        return self.render()

class ActionStorage(object):
    
    def __init__(self):
        self.data = []
        
    def rename_func(self, index, name):
        self.data[index].name = name
        
    def add_function(self, name):
        self.data.append(TestFunctionRecord(name))
        
    def delete_request(self, func_index, index):
        self.data[func_index].delete(index)
    
    def add_request(self, request, response, ignore_csrf_token=True):
        self.data[-1].add(RequestRecord(request, response, ignore_csrf_token))        
    
    def remove_assertion(self, func_index, index):
        self.data[func_index].records[index].remove_assertion()
        
    def add_assertion(self, value, func_index=None, index=None):
        if func_index is None:
            func_index = len(self.data) - 1
        if index is None:
            index = len(self.data[func_index].records) - 1
        self.data[func_index].records[index].add_assertion(value)
        
    def delete_func(self, index):
        del self.data[index]
        
    def get_data(self):
        return self.data
    
    def __len__(self):
        return len(self.data)
    
    def __iter__(self):
        return iter(self.data)
    
    def __nonzero__(self):
        return bool(self.data)
        
class TestFunctionRecord(object):
    
    def __init__(self, name, *args, **kwargs):
        self.name = name
        self.records = []
    
    def add(self, item):
        self.records.append(item)
        
    def delete(self, index):
        try:
            del self.records[index]
            return True
        except IndexError:
            return False
        
class FileProxy(object):

    def __init__(self, path, store):
        self.path = path
        self.store = store
        
    def __del__(self):
        self.store.delete(self.path)
    
class RequestRecord(object):
    
    file_store = FileSystemStorage()
    
    def __init__(self, request, response, ignore_csrf_token=True):
        self.url = request.path_info
        self.method = request.method
        self.get = [(k, request.GET.getlist(k)) for k in request.GET]
        self.forms = {}
        
        if hasattr(request, '_djtr_context'):
            context = {}
            for d in request._djtr_context.dicts:
                context.update(d)
                
            for context_name, item in context.items():
                if isinstance(item, BaseForm) and item.is_bound:
                    self.forms[context_name] = item
                    
        icf, tn = ignore_csrf_token, 'csrfmiddlewaretoken'
        self.post = [(k, request.POST.getlist(k)) for k in request.POST if not icf or k != tn]
        
        self.files = []
        for field_name, file in request.FILES.items():
            file_path = self.file_store.save(FILES_PATH+file.name, file)
            self.files.append((field_name, FileProxy(file_path, self.file_store)))
        self.code = response.status_code
        self.redirect_url = response.get('Location', '') 
        if self.redirect_url and not self.redirect_url.startswith('/'):
            self.redirect_url = '/'+self.redirect_url
        self.assertions = []
    
    def remove_assertion(self):
        self.assertions = []
    
    def add_assertion(self, value):
        self.assertions.append(value)
        
    def is_data(self):
        return self.get or self.post
    
    def get_param(self):
        if self.method == 'POST' and self.get:
            return '+"?%s"' % urlencode(self.get, 1)
        return ''
    
    @property
    def data(self):
        if self.method == 'GET':
            return self.get
        if self.method == 'POST':
            return self.post+self.files
        return []
    
    def render_data(self):
        rows = []
        for key, value in self.data:
            value_str = '"'
            rows.append('"%s": ')
    
    @property
    def url_reverse(self):
        resolver = get_resolver(None)
        try:
            name, args, kwargs = resolver.resolve_to_name(self.url)
            output = ['"%s"' % name]
            if kwargs:
                output.append(', kwargs=%s' % self.to_short_dict(kwargs))
            if args:
                output.append(', args=%s' % str(list(args)))
            return 'reverse(%s)' % ''.join(output)
        except Http404:
            return '"%s"' % self.url
    
    def is_url_short(self):
        resolver = get_resolver(None)
        try:
            name, args, kwargs = resolver.resolve_to_name(self.url)
            args += tuple(kwargs.values())
            return not (args or self.get_param())
        except Http404:
            return True
    
    def is_data_short(self):
        if len(self.data) <= 1 and not self.files:
            for value in self.data:
                if self.is_multiline(value):
                    return False
            return True
        return False
    
    def is_multiline(self, value):
        return len(str(value).splitlines()) > 1
    
    def to_short_dict(self, data):
        output = []
        for key, value in data.items():
            s = '"%s": "%s"' % (key, value)
            output.append(s)
        return '{%s}' % ', '.join(output)
        
    @property
    def short_data(self):
        output = []
        for key, value in self.data:
            s = "'%s': '%s'" % (key, ', '.join(value))
            output.append(s)
        return '{%s}' % ', '.join(output)
            
def replace_insensitive(string, target, replacement):
    """
    Similar to string.replace() but is case insensitive
    Code borrowed from: http://forums.devshed.com/python-programming-11/case-insensitive-string-replace-490921.html
    """
    no_case = string.lower()
    index = no_case.rfind(target.lower())
    if index >= 0:
        return string[:index] + replacement + string[index + len(target):]
    else: # no results so return the original string
        return string

#Patched snippet #1378
#http://www.djangosnippets.org/snippets/1378/   
def _pattern_resolve_to_name(self, path):
    match = self.regex.search(path)
    if match:
        name = ""
        if self.name:
            name = self.name
        elif hasattr(self, '_callback_str'):
            name = self._callback_str
        else:
            name = "%s.%s" % (self.callback.__module__, self.callback.func_name)
        kwargs = match.groupdict()
        if kwargs:
            args = ()
        else:
            args = match.groups()         
        return name, args, kwargs

def _resolver_resolve_to_name(self, path):
    tried = []
    match = self.regex.search(path)
    if match:
        new_path = path[match.end():]
        for pattern in self.url_patterns:
            try:
                sub_match = pattern.resolve_to_name(new_path)
            except Resolver404, e:
                tried.extend([(pattern.regex.pattern + '   ' + t) for t in e.args[0]['tried']])
            else:
                if sub_match:
                    name = sub_match[0]
                    sub_match_dict = dict([(smart_str(k), v) for k, v in match.groupdict().items()])
                    for k, v in sub_match[2].iteritems():
                        sub_match_dict[smart_str(k)] = v 
                    if hasattr(self, 'namespace') and self.namespace:
                        name = '%s:%s' % (self.namespace, name)                                            
                    return name, sub_match[1], sub_match_dict 
                tried.append(pattern.regex.pattern)
        raise Resolver404, {'tried': tried, 'path': new_path}

RegexURLPattern.resolve_to_name = _pattern_resolve_to_name
RegexURLResolver.resolve_to_name = _resolver_resolve_to_name