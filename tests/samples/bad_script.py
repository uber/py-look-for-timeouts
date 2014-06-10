import urllib2

urllib2.urlopen('foo')
urllib2.urlopen('foo', timeout=0)

with urllib2.urlopen('baz', None, 0) as f:
    pass
