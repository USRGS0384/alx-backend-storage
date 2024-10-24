import requests
import redis
import time

# Initialize Redis connection
r = redis.Redis()

# Cache decorator to handle caching and expiration
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

# Apply the decorator with a 10-second expiration
@cache_decorator(10)
def get_page(url: str) -> str:
    response = requests.get(url)
    return response.text

# Simulate a slow response and test caching
url = 'http://slowwly.robertomurray.co.uk/delay/5000/url/http://www.example.com'
print(get_page(url))
time.sleep(5)
