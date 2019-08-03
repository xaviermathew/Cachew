import glob
import logging
import os
import pickle
import shelve

_LOG = logging.getLogger(__name__)

class Cachew(object):
    '''
   :param str path: file path where data will be cached
   :param callable getter: callable used for cache misses; accepts a key as param
   :param str transformer: optional callable used for any transformations that need to happen
   :param list<str> shelfs: optional file paths where `Shelve`s have been stored.
                            For cache misses, will lookup key in these paths using Shelve
                            before using `getter`
   '''

    def __init__(self, path, getter, transformer=lambda x: x, shelfs=[]):
        self.path = path
        try:
            os.mkdir(path)
        except OSError:
            pass
        self.getter = getter
        self.transformer = transformer
        self.shelfs = shelfs

    @staticmethod
    def _get_cache_key(key):
        if isinstance(key, tuple):
            cache_key = ':'.join(map(str, key))
        else:
            cache_key = str(key)
        return cache_key

    def _get_cache_path(self, key):
        cache_key = self._get_cache_key(key)
        path = os.path.join(self.path, cache_key + '.pkl')
        return path

    def __contains__(self, key):
        path = self._get_cache_path(key)
        return os.path.exists(path)

    def has_key(self, key):
        # to make this behave like Shelve
        return key in self

    def __getitem__(self, key):
        path = self._get_cache_path(key)
        if key in self:
            _LOG.debug('cache hit - key:[%s]', key)
        else:
            _LOG.debug('cache miss - key:[%s]', key)
            data = None
            cache_key = self._get_cache_key(key)
            for shelf_path in self.shelfs:
                shelf = shelve.open(shelf_path)
                if shelf.has_key(cache_key):
                    data = shelf[cache_key]
                    break
            if data is None:
                data = self.getter(key)
            self[key] = data
        return self.transformer(pickle.load(open(path)))

    def __setitem__(self, key, data):
        cache_key = self._get_cache_key(key)
        path = os.path.join(self.path, cache_key + '.pkl')
        with open(path, 'w') as f:
            pickle.dump(data, f)

    def load_from_shelf(self, shelf):
        for k, v in shelf.iteritems():
            self[k] = v

    def iterkeys(self):
        files = glob.iglob(self.path + '/*.pkl')
        for f in files:
            yield f.split('.pkl')[0]

    def keys(self):
        return list(self.keys())

    def iteritems(self):
        for k in self.keys():
            yield os.path.basename(k), self[k]

    def items(self):
        return list(self.iteritems())

    def itervalues(self):
        for k, v in self.items():
            yield v

    def values(self):
        return list(self.itervalues())

