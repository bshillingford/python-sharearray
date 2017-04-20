import unittest
import os.path

import numpy as np

import sharearray


class TestCache(unittest.TestCase):
    def test_simple(self):
        identifier = 'testcache_simple'
        arr = np.random.normal(size=(5, 6))

        # create from scratch:
        arr1 = sharearray.cache(identifier,
                                array_or_callback=arr,
                                timeout=-1,
                                verbose=True)
        self.assertTrue((arr1 == arr).all())
        # opens view
        arr2 = sharearray.cache(identifier,
                                array_or_callback=arr,
                                timeout=-1,
                                verbose=True)
        self.assertTrue((arr2 == arr).all())

        # close views:
        del arr1
        del arr2

        # free memory:
        sharearray.free(identifier)

    def test_callback(self):
        identifier = 'testcache_callback'

        # ensure already freed:
        sharearray.free(identifier)
        fn, fn_lock = sharearray._build_path(identifier,
                                             shm_path='/dev/shm',
                                             prefix='sharearray_')
        self.assertTrue(not os.path.exists(fn) and not os.path.exists(fn_lock))
        print("*****", fn, fn_lock)

        # create from scratch or open view
        arr = sharearray.cache(identifier,
                               array_or_callback=lambda: np.ones((5, 6)),
                               timeout=-1,
                               verbose=True)
        self.assertTrue(os.path.exists(fn) and not os.path.exists(fn_lock))
        del arr
        # should still exist after removing memmapped view
        self.assertTrue(os.path.exists(fn) and not os.path.exists(fn_lock))

        # free memory:
        sharearray.free(identifier)
        self.assertTrue(not os.path.exists(fn) and not os.path.exists(fn_lock))

    def test_decorator(self):
        identifier = 'testcache_decorator'

        @sharearray.decorator(identifier, verbose=False)
        def data():
            return np.ones((5, 6))

        # ensure memory is freed; neither lock nor file should exist
        sharearray.free(identifier)
        fn, fn_lock = sharearray._build_path(identifier,
                                             shm_path='/dev/shm',
                                             prefix='sharearray_')
        self.assertTrue(not os.path.exists(fn) and not os.path.exists(fn_lock))
        # 1st call should create item, and lock should be gone
        data1 = data()
        self.assertTrue((data1 == 1).all())
        self.assertTrue(os.path.exists(fn) and not os.path.exists(fn_lock))

        # 2nd call should just view
        data2 = data()
        self.assertTrue((data2 == 1).all())
        self.assertTrue(os.path.exists(fn) and not os.path.exists(fn_lock))

        # free memory:
        sharearray.free(identifier)
        self.assertTrue(not os.path.exists(fn) and not os.path.exists(fn_lock))

if __name__ == '__main__':
    unittest.main()

# TODO: test exceptions?
