import urllib2
import httplib
import requests
import foobar

TIMEOUT = 0

urllib2.urlopen('foo', timeout=2)
urllib2.urlopen('foo', timeout=TIMEOUT)
foobar.urlopen('baz')

urllib2.urlopen('foo', None, 2)
urllib2.urlopen('foo', None, TIMEOUT)

c = httplib.HTTPConnection('foo', timeout=2)
c = httplib.HTTPConnection('foo', 80, 'bar', 'baz', False, 2)

requests.get('foo', timeout=2)
requests.put('foo', timeout=TIMEOUT)

# junk to make sure we parse stuff correctly
print [1, 2, 3][1]
print {"foo", urllib2.urlopen}["foo"]()
