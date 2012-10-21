import oauth2
import httplib2
import time
import urllib
import json


"""
A helper function for making oauth requests to Context.IO's version 2.0 API


Example Usage:

    contextio_api_key = 'foo'
    contextio_api_secret = 'bar'

    conn = contextio.ContextIO(contextio_api_key, contextio_api_secret)

    result, data = conn.request('POST', 'connect_tokens', {'callback_url':'http://example.com/contextio_callback'})
    print data['uuid']

    
    result, user = conn.request('GET', 'connect_tokens/'+contextio_token)
    print data['account']['email']


    result, data = conn.request('GET', url, {'file_name':'test.pdf'})

    # If the result from the API is not content-type: application/json, the raw body is returned instead of a
    # the parsed json object
    result, link = conn.request('GET', url, {'as_link':1})
    print link

"""


class ContextIO(httplib2.Http):

    def __init__(self, api_key, api_secret):
        self.consumer = oauth2.Consumer(key=api_key, secret=api_secret)
        super(ContextIO, self).__init__()

    def request(self, action, url, context={}):
        url = "https://api.context.io/2.0/" + url

        params = {
            'oauth_version': "1.0",
        }
        params['oauth_consumer_key'] = self.consumer.key
        params['oauth_nonce'] = oauth2.generate_nonce()
        params['oauth_timestamp'] = '%s' % int(time.time())

        queryString = ''

        if action.lower() == 'get':
            queryString = urllib.urlencode(context)
            url += '?'+queryString
        else:
            for key in context:
                params[key] = context[key]
                    
        req = oauth2.Request(method=action, url=url, parameters=params)
        # Sign the request.
        signature_method = oauth2.SignatureMethod_HMAC_SHA1()
        req.sign_request(signature_method, self.consumer, None)
        
        body = '' if action.lower() == 'get' else req.to_postdata()
        headers = {} if action.lower() == 'get' else {'Content-Type': 'application/x-www-form-urlencoded'}
        url = req.to_url() if action.lower() == 'get' else url
        
        response, content = super(ContextIO, self).request(url,
                                        method=action,
                                        body=body,
                                        headers=headers,
                                        redirections=httplib2.DEFAULT_MAX_REDIRECTS,
                                        connection_type=None)
        
        if response['content-type'] == 'application/json':
            return response, json.loads(content)
        else:
            return response, content
