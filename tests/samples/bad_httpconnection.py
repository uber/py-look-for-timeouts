import httplib
from httplib import HTTPConnection, HTTPSConnection

c = httplib.HTTPConnection('foo')
c = httplib.HTTPSConnection('foo')
c = httplib.HTTPConnection('foo', timeout=0)
c = HTTPConnection('foo', timeout=0)
c = HTTPSConnection('foo', timeout=0)
c = httplib.HTTPConnection('foo', 80, 'bar', 'baz', False, 0)
