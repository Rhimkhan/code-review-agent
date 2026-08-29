import hashlib
from typing import Optional, Dict
from datetime import datetime

class ReviewCache:
    def __init__(self, max_size: int = 100):
        self._cache: Dict[str, dict] = {}
        self.max_size = max_size
        self.hits = 0
        self.misses = 0

    def get_key(self, code: str, filename: str) -> str:
        return hashlib.md5(f"{filename}:{code}".encode()).hexdigest()

    def get(self, code: str, filename: str) -> Optional[dict]:
        key = self.get_key(code, filename)
        if key in self._cache:
            self.hits += 1
            return self._cache[key]
        self.misses += 1
        return None

    def set(self, code: str, filename: str, result: dict):
        if len(self._cache) >= self.max_size:
            oldest = next(iter(self._cache))
            del self._cache[oldest]
        key = self.get_key(code, filename)
        self._cache[key] = {**result, "cached_at": datetime.now().isoformat()}

    def clear(self):
        self._cache.clear()
        self.hits = 0
        self.misses = 0

    def size(self) -> int:
        return len(self._cache)

    def stats(self) -> Dict:
        return {
            "size": self.size(),
            "hits": self.hits,
            "misses": self.misses,
            "max_size": self.max_size
        }

cache = ReviewCache()
