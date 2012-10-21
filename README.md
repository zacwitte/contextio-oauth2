contextio-oauth2
================

A helper function for making oauth requests to Context.IO's version 2.0 API

Examples
========

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
