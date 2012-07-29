from django.utils.http import urlencode
from django.http import HttpResponseRedirect

class CsrfMiddleware(object):
    '''
    Detect "csrfmiddlewaretoken" in the request string, and if it is there then
    remove it and redirect to the new version without that parameter.
    For example:

    /foo?a=1&b=2&csrfmiddlewaretoken=foo&d=4

    should redirect to

    /foo?a=1&b=2&d=4
    '''
    def process_request(self, request):
        if request.method=='GET' and request.GET.has_key('csrfmiddlewaretoken'):
            query_dict = request.GET.copy()
            query_dict.pop('csrfmiddlewaretoken')
            
            # query_dict is a MultiValueDict, e.g. {u'a': [u'1'], u'b': [u'2'], u'd': [u'4']}
            # convert query_dict to a list of tuple of string
            query_tuple_list = [(k, v[0]) for k,v in query_dict.items()]
            query_string = urlencode(query_tuple_list)
            redirect_url = request.path + '?' + query_string
            return HttpResponseRedirect(redirect_url)
    