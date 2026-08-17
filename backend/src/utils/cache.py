import hashlib
from typing import Optional, Dict

class ReviewCache:
    def __init__(self):
        self._cache: Dict[str, dict] = {}

    def get_key(self, code: str, filename: str) -> str:
        return hashlib.md5(f"{filename}:{code}".encode()).hexdigest()

    def get(self, code: str, filename: str) -> Optional[dict]:
        return self._cache.get(self.get_key(code, filename))

    def set(self, code: str, filename: str, result: dict):
        self._cache[self.get_key(code, filename)] = result

    def clear(self):
        self._cache.clear()

    def size(self) -> int:
        return len(self._cache)

cache = ReviewCache()
