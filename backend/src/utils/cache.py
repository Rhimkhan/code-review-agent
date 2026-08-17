import hashlib
import json
from typing import Optional, Dict

class ReviewCache:
    def __init__(self):
        self._cache: Dict[str, dict] = {}

    def get_key(self, code: str, filename: str) -> str:
        content = f"{filename}:{code}"
        return hashlib.md5(content.encode()).hexdigest()

    def get(self, code: str, filename: str) -> Optional[dict]:
        key = self.get_key(code, filename)
        return self._cache.get(key)

    def set(self, code: str, filename: str, result: dict):
        key = self.get_key(code, filename)
        self._cache[key] = result

    def clear(self):
        self._cache.clear()

    def size(self) -> int:
        return len(self._cache)

cache = ReviewCache()
