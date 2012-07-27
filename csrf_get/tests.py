from django.test import TestCase, client
import urlparse

class CsrfGetTest(TestCase):
    
    def test_csrf_get(self):
        c = client.Client()
        response = c.get('/some/path/?csrfmiddlewaretoken=a&*2;b&aa=22&bb=33')
        self.assertEqual(urlparse.urlparse(response.get('location')).query, urlparse.urlparse('/some/path/?aa=22&bb=33').query)
