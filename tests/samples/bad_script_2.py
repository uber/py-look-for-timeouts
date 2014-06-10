from urllib2 import urlopen

urlopen('foo')
urlopen('foo', timeout=0)

with urlopen('baz', None, 0) as f:
    pass
