import redis
import requests
from functools import wraps

# Initialize the Redis client
redis_client = redis.Redis()

def cache_page(url: str):
    """Decorator to cache the page content and track access counts."""
    @wraps(get_page)
    def wrapper(url: str):
        # Increment the access count for the URL
        redis_client.incr(f"count:{url}")
        
        # Check if the URL content is already cached
        cached_content = redis_client.get(url)
        if cached_content:
            return cached_content.decode('utf-8')

        # If not cached, fetch the content from the URL
        response = requests.get(url)
        if response.status_code == 200:
            # Cache the result with an expiration time of 10 seconds
            redis_client.setex(url, 10, response.text)
            return response.text
        else:
            return f"Error: Unable to fetch {url}"

    return wrapper

@cache_page
def get_page(url: str) -> str:
    """Get the HTML content of a particular URL."""
    pass  
