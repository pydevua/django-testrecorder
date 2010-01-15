from django.core.urlresolvers import RegexURLResolver, RegexURLPattern, Resolver404, get_resolver
from django.utils.encoding import smart_str

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
        
    def is_data(self):
        return self.get or self.post
    
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
        #view, args, kwargs = resolver.resolve(self.url)
        args += tuple(kwargs.values())
        args = map(smart_str, args)
        output = ['"%s"' % name]
        if args:
            output.append(', args=["%s"]' % '", "'.join(args))
        return ''.join(output)       
        
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
                    sub_match_dict = dict([(smart_str(k), v) for k, v in match.groupdict().items()])
                    for k, v in sub_match[2].iteritems():
                        sub_match_dict[smart_str(k)] = v 
                    if hasattr(self, 'namespace') and self.namespace:
                        sub_match[0] = '%s:%s' % (self.namespace, sub_match[0])                                            
                    return sub_match[0], sub_match[1], sub_match_dict 
                tried.append(pattern.regex.pattern)
        raise Resolver404, {'tried': tried, 'path': new_path}

RegexURLPattern.resolve_to_name = _pattern_resolve_to_name
RegexURLResolver.resolve_to_name = _resolver_resolve_to_name