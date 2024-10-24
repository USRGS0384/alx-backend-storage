#!/usr/bin/env python3
""" Implementing an expiring web cache and tracker
    obtain the HTML content of a particular URL and returns it """
import redis
import requests

r = redis.Redis()
count = 0

def get_page(url: str) -> str:
    cached_page = r.get(f'page:{url}')
    if cached_page:
        r.incr(f'count:{url}')
        return cached_page.decode('utf-8')

    response = requests.get(url)
    page_content = response.text

    # Store the page content in the cache with an expiration of 10 seconds
    r.set(f'page:{url}', page_content, ex=10)
    r.set(f'count:{url}', 1)

    return page_content

def cache_decorator(expiration_time: int):
    def decorator(func):
        def wrapper(url: str):
            cached_page = r.get(f'page:{url}')
            if cached_page:
                r.incr(f'count:{url}')
                return cached_page.decode('utf-8')

            result = func(url)
            r.set(f'page:{url}', result, ex=expiration_time)
            r.set(f'count:{url}', 1)
            return result
        return wrapper
    return decorator

@cache_decorator(10)
def get_page(url: str) -> str:
    response = requests.get(url)
    return response.text


if __name__ == "__main__":
    url = 'http://slowwly.robertomurray.co.uk/delay/5000/url/http://www.google.com'
print(get_page(url))
time.sleep(5)
print(get_page(url))
