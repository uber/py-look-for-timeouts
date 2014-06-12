import clay
from clay import http

c = request('method', 'foo', 'data', 'headers', 0)
c = request('method', 'foo')
c = request('method', 'foo', timeout=0)

c = http.request('method', 'foo', 'data', 'headers', 0)
c = http.request('method', 'foo')
c = http.request('method', 'foo', timeout=0)
