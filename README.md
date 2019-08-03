# Cachew
 File-based cache that supports multiprocessing


# Documentation:
```python
>>> help(http_bin_service)
```


# Usage:
```python
>>> import requests
>>> from cachew import Cachew
>>> http_bin_service = Cachew(
...     path='/tmp/http_bin',
...     getter=lambda key: requests.get('https://httpbin.org/anything/%s' % key).json(),
...     transformer=lambda response: response['url'].split('/')[-1]
... )

>>> http_bin_service['test1']
u'test1'
>>> http_bin_service['test2']
u'test2'
```
