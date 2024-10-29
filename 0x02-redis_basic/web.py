import requests
import redis
import time

# Initialize Redis connection
r = redis.Redis()

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

    return

if __name__ == "__main__":
    url = 'http://slowwly.robertomurray.co.uk'
    print(get_page(url))  # First access, should fetch and cache
    time.sleep(5)
    print(get_page(url))  # Cache hit, should be faster
    time.sleep(6)
    print(get_page(url))  # Cache expired, should fetch again

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
    url = 'http://slowwly.robertomurray.co.uk/delay/5000/url/http://www.example.com'
    print(get_page(url))  # First access, should fetch and cache
    time.sleep(5)
    print(get_page(url))  # Cache hit, should be faster
    time.sleep(6)
    print(get_page(url))  # Cache expired, should fetch again
