import pytest
from src.utils.cache import ReviewCache

def test_cache_set_and_get():
    cache = ReviewCache()
    cache.set("code", "file.py", {"findings": []})
    result = cache.get("code", "file.py")
    assert result is not None

def test_cache_miss():
    cache = ReviewCache()
    assert cache.get("nonexistent", "file.py") is None

def test_cache_size():
    cache = ReviewCache()
    cache.set("code1", "a.py", {})
    cache.set("code2", "b.py", {})
    assert cache.size() == 2

def test_cache_clear():
    cache = ReviewCache()
    cache.set("code", "file.py", {})
    cache.clear()
    assert cache.size() == 0
