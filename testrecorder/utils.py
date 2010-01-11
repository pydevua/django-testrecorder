class RequestRecord(object):
    
    def __init__(self, request, response):
        self.url = request.path_info
        self.method = request.method
        self.get = request.GET
        self.post = request.POST
        self.code = response.status_code
        self.redirect_url = ''
        
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