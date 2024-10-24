#!/usr/bin/env python3
import unittest
import time
from web import get_page, r

class TestWebCache(unittest.TestCase):

    def test_get_page_cache(self):
        url = 'http://google.com'
        result_1 = get_page(url)
        result_2 = get_page(url)
        self.assertEqual(result_1, result_2)

        time.sleep(11)
        result_3 = get_page(url)
        self.assertNotEqual(result_1, result_3)

    def test_increment_count(self):
        url = 'http://google.com'
        r.delete(f'count:{url}')  # Reset count for testing

        get_page(url)
        count_1 = r.get(f'count:{url}')

        get_page(url)
        count_2 = r.get(f'count:{url}')

        self.assertEqual(int(count_1) + 1, int(count_2))

if __name__ == '__main__':
    unittest.main()
