from django.test import TestCase, client
import urlparse

class CsrfGetTest(TestCase):
    '''
    Detect "csrfmiddlewaretoken" in the request string, and if it is there 
    then remove it and redirect to the new version without that parameter.
    For example:

    /foo?a=1&b=2&csrfmiddlewaretoken=foo&d=4

    should redirect to

    /foo?a=1&b=2&d=4
    '''
    def test_query_string(self):
        c = client.Client()
        response = c.get('/foo?a=1&b=2&csrfmiddlewaretoken=foo&d=4')
        location_url = response.get('location')
        
        # get the query string from response
        query_string = urlparse.urlparse(location_url).query

        # get the query string that should be returned for test
        test_query_string = urlparse.urlparse('/foo?a=1&b=2&d=4').query
        
        self.assertEqual(query_string, test_query_string)
    
    def test_full_path(self):
        c = client.Client()
        response = c.get('/foo?a=1&b=2&csrfmiddlewaretoken=foo&d=4')
        location_url = response.get('location')
        parse_result = urlparse.urlparse(location_url)
        full_path = parse_result.path + '?' + parse_result.query
        
        self.assertEqual(full_path, '/foo?a=1&b=2&d=4')
    