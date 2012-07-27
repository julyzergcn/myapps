import urlparse, urllib
from django.http import HttpResponseRedirect

class CsrfMiddleware(object):
    
    def process_request(self, request):
        if request.method=='GET' and request.GET.has_key('csrfmiddlewaretoken'):
            parse_result = list(urlparse.urlparse(request.get_full_path()))
            parse_result[4] = urllib.urlencode([tu for tu in urlparse.parse_qsl(parse_result[4]) if tu[0]!='csrfmiddlewaretoken'])
            new_full_path = urlparse.urlunparse(parse_result)
            return HttpResponseRedirect(new_full_path)
    