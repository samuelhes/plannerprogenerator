"""
Caching layer for application data
"""
from functools import lru_cache
import time


class SimpleCache:
    """Simple in-memory cache with TTL"""
    
    def __init__(self, ttl=3600):
        self.ttl = ttl
        self.cache = {}
        self.timestamps = {}
    
    def get(self, key):
        """Get item from cache"""
        if key not in self.cache:
            return None
        
        # Check TTL
        if time.time() - self.timestamps[key] > self.ttl:
            self.delete(key)
            return None
        
        return self.cache[key]
    
    def set(self, key, value):
        """Set item in cache"""
        self.cache[key] = value
        self.timestamps[key] = time.time()
    
    def delete(self, key):
        """Delete item from cache"""
        if key in self.cache:
            del self.cache[key]
            del self.timestamps[key]
    
    def clear(self):
        """Clear all cache"""
        self.cache.clear()
        self.timestamps.clear()


# Global cache instance
app_cache = SimpleCache(ttl=3600)  # 1 hour TTL
