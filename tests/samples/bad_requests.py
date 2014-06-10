import requests

requests.get('foo')
requests.put('bar', timeout=0)
requests.post('baz')
requests.head('bing')
requests.request('bing', method='GET', timeout=0)
