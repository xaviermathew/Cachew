# Cachew
 File-based cache that supports multiprocessing


# Documentation:
```python
help(http_bin_service)
```


# Usage:
```python
import requests
from cachew import Cachew


http_bin_service = Cachew(
    '/tmp/http_bin',
    lambda key: requests.get('https://httpbin.org/anything/%s' % key).json(),
    lambda response: response['url'].split('/')[-1]
)
print http_bin_service['test1'] == 'test1'
print http_bin_service['test2'] != 'test1'
```