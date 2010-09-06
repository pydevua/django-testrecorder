from django.core.urlresolvers import RegexURLResolver, RegexURLPattern, Resolver404, get_resolver
from django.utils.encoding import smart_str
from django.utils.http import urlencode

class CodeNode(object):
    
    def __init__(self, level=0, tab='    '):
        self.code = []
        self.level = level
        self.tab = tab
    
    def child_node(self):
        return CodeNode(self.level, self.tab)
        
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
        node.add('from django.test import TestCase')
        node.add('from django.core.urlresolvers import reverse')
        return node        
    
    def add_fixtures(self, node):
        if self.fixtures:
            node.add('fixtures = ["%s"]' % '", "'.join(self.fixtures)).blank()
        return node
    
    def dict_values(self, values):
        
        def get_value(val):
            if len(str(val).splitlines()) > 1:
                return '"""%s"""' % val
            if isinstance(val, list):
                if len(val) > 1:
                    return '[%s]' % ', '.join(map(get_value, val))
                elif len(val) == 1:
                    return get_value(val[0])
                else:
                    return ''
            return '"%s"' % str(val)                
        
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
        if request.is_data() and not request.is_data_short():
            node.add('data = {').indent()
            for item in self.dict_values(request.data):
                node.add(item)
            node.dedent().add('}')
        if request.is_url_short():
            url = 'reverse(%s)' % request.url_reverse
        else:
            url = 'url'
            node.add('url = reverse(%s)%s' % (request.url_reverse, request.get_param()))
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
        return node.blank()
    
    def add_func(self, func, node):
        node.blank().add('def %s(self):' % func.name).indent()
        if self.auth:
            node.add('self.client.login(**self.auth)').blank()
        for item in func.records:
            self.add_request(item, node)
    
    def render(self):
        node = CodeNode()
        self.add_imports(node)
        node.blank().add('class %s(TestCase):' % self.class_name).indent()
        self.add_fixtures(node)
        self.add_setup(node)
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
    
    def add_request(self, request, response):
        self.data[-1].add(RequestRecord(request, response))        
    
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
        
    
class RequestRecord(object):
    
    def __init__(self, request, response):
        self.url = request.path_info
        self.method = request.method
        self.get = [(k, request.GET.getlist(k)) for k in request.GET]
        self.post = [(k, request.POST.getlist(k)) for k in request.POST]
        self.code = response.status_code
        self.redirect_url = response.get('Location', '') 
        if self.redirect_url and not self.redirect_url.startswith('/'):
            self.redirect_url = '/'+self.redirect_url
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
            return self.post
        return []
    
    def render_data(self):
        rows = []
        for key, value in self.data:
            value_str = '"'
            rows.append('"%s": ')
    
    @property
    def url_reverse(self):
        resolver = get_resolver(None)
        name, args, kwargs = resolver.resolve_to_name(self.url)
        output = ['"%s"' % name]
        if kwargs:
            output.append(', kwargs=%s' % self.to_short_dict(kwargs))
        return ''.join(output)
    
    def is_url_short(self):
        resolver = get_resolver(None)
        name, args, kwargs = resolver.resolve_to_name(self.url)
        args += tuple(kwargs.values())
        return not (args or self.get_param())               
    
    def is_data_short(self):
        if len(self.data) <= 1:
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