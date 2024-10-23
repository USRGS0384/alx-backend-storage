#!/usr/bin/env python3
""" web """

from functools import wraps
from typing import Callable
import requests
import redis

# Initialize Redis client
r = redis.Redis()


def count_requests(method: Callable) -> Callable:
    """Tracks how many times a particular URL was accessed
    in the key 'count:{url}' and caches the result with an expiration
    time of 10 seconds.
    """
    @wraps(method)
    def wrapper(url):
        # Increment the access count
        r.incr(f"count:{url}")

        # Check if the result is already cached
        cached_html = r.get(f"cached:{url}")
        if cached_html:
            return cached_html.decode('utf-8')

        # Fetch the content and cache it
        html = method(url)
        r.setex(f"cached:{url}", 10, html)
        return html
    return wrapper


@count_requests
def get_page(url: str) -> str:
    """Obtains the HTML content of a particular URL and returns it."""
    req = requests.get(url)
    return req.text


if __name__ == "__main__":
    get_page('http://google.com')
