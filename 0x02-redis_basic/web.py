#!/usr/bin/env python3
""" web """

import redis
import requests
from functools import wraps
from datetime import timedelta

# Redis connection details (adjust as needed)
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
CACHE_EXPIRY = 10  # Cache entries expire after 10 seconds

# Redis client instance
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)


def cache_and_track(func):
    """
    Decorator to cache web page content and track access count.

    Args:
        func: The function to decorate (expected to be `get_page`).

    Returns:
        function: The decorated function with caching and tracking behavior.
    """

    @wraps(func)
    def wrapper(url):
        cache_key = f"content:{url}"  # Cache key format for content
        count_key = f"count:{url}"  # Cache key format for access count

        cached_content = r.get(cache_key)

        if cached_content:
            # Cache hit: Increment access count and return cached content
            r.incr(count_key)
            return cached_content.decode()

        else:
            # Cache miss: Fetch content from URL, cache it, and return
            content = func(url)
            r.set(cache_key, content, ex=CACHE_EXPIRY)  # Set cache expiry
            r.incr(count_key)
            return content

    return wrapper


@cache_and_track
def get_page(url: str) -> str:
    """
    Fetches a web page's content, using Redis cache for efficiency.

    Args:
        url (str): The URL of the web page to fetch.

    Returns:
        str: The HTML content of the web page.
    """

    content = requests.get(url).text
    return content


if __name__ == "__main__":
    # Example usage (assuming slowwly.robertomurray.co.uk is the target)
    url = "http://slowwly.robertomurray.co.uk"
    for _ in range(3):  # Simulate 3 requests
        content = get_page(url)
        print(f"Fetched content for '{url}':")
        print(content[:100])  # Print a snippet
        print("-" * 20)
