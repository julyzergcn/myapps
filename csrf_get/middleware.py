import urlparse, urllib
from django.http import HttpResponseRedirect

class CsrfMiddleware(object):
    '''
    Detect "csrfmiddlewaretoken" in the request string, and if it is there then remove it and redirect to the new version without that parameter. For example:

    /foo?a=1&b=2&csrfmiddlewaretoken=foo&d=4

    should redirect to

    /foo?a=1&b=2&d=4
    '''
    def process_request(self, request):
        if request.method=='GET' and \
            request.GET.has_key('csrfmiddlewaretoken'):
            request_full_path = request.get_full_path()
            parse_result = urlparse.urlparse(request_full_path)
            
            # parse_result is a tuple ParseResult(scheme, netloc, path, params, query, fragment)
            # convert the tuple to a list
            parse_result = list(parse_result)
            
            # the 4th of the list should be the query string, 
            # e.g. "a=1&b=2&csrfmiddlewaretoken=foo&d=4"
            query_string = parse_result[4]
            
            # parse the query string to a tuple list of (key, value),
            # e.g. [('a', '1'), ('b', '2'), ('csrfmiddlewaretoken', 'foo'), ('d', '4')]
            query_list = urlparse.parse_qsl(query_string)
            
            # filter out the 'csrfmiddlewaretoken' tuple from the list
            query_list = [tu for tu in query_list if tu[0]!='csrfmiddlewaretoken']
            
            # convert the new tuple list to a query string
            query_string = urllib.urlencode(query_list)
            
            parse_result[4] = query_string
            
            # conver the ParseResult tuple to a new path
            new_full_path = urlparse.urlunparse(parse_result)
            
            return HttpResponseRedirect(new_full_path)
    