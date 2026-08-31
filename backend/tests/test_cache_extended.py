import pytest
from src.utils.cache import ReviewCache

def test_cache_hit_tracking():
    cache = ReviewCache()
    cache.set("code", "file.py", {"findings": []})
    cache.get("code", "file.py")
    assert cache.hits == 1
    assert cache.misses == 0

def test_cache_miss_tracking():
    cache = ReviewCache()
    cache.get("nonexistent", "file.py")
    assert cache.misses == 1
    assert cache.hits == 0

def test_cache_max_size():
    cache = ReviewCache(max_size=2)
    cache.set("code1", "a.py", {})
    cache.set("code2", "b.py", {})
    cache.set("code3", "c.py", {})
    assert cache.size() == 2

def test_cache_stats():
    cache = ReviewCache()
    stats = cache.stats()
    assert "hits" in stats
    assert "misses" in stats
    assert "size" in stats

def test_cached_result_has_timestamp():
    cache = ReviewCache()
    cache.set("code", "file.py", {"findings": []})
    result = cache.get("code", "file.py")
    assert "cached_at" in result
