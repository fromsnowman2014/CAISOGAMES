"""Caching utilities for generated images."""

import hashlib
import json
import time
from pathlib import Path
from typing import Optional, Dict, Any
from dataclasses import dataclass, asdict
import shutil


@dataclass
class CacheEntry:
    """Represents a cached image entry."""
    key: str
    file_path: str
    prompt: str
    generator: str
    width: int
    height: int
    created_at: float
    size_bytes: int
    metadata: Dict[str, Any]

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'CacheEntry':
        return cls(**data)


class ImageCache:
    """Manages caching of generated images to reduce API calls."""

    def __init__(
        self,
        cache_dir: Path,
        max_size_mb: int = 500,
        ttl_hours: int = 168  # 7 days
    ):
        """
        Initialize the image cache.

        Args:
            cache_dir: Directory for cached images
            max_size_mb: Maximum cache size in MB
            ttl_hours: Time-to-live for cache entries in hours
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        self.images_dir = self.cache_dir / 'images'
        self.images_dir.mkdir(exist_ok=True)

        self.index_path = self.cache_dir / 'cache_index.json'
        self.max_size_bytes = max_size_mb * 1024 * 1024
        self.ttl_seconds = ttl_hours * 3600

        self._index: Dict[str, CacheEntry] = {}
        self._load_index()

    def _load_index(self) -> None:
        """Load the cache index from disk."""
        if self.index_path.exists():
            try:
                data = json.loads(self.index_path.read_text())
                self._index = {
                    k: CacheEntry.from_dict(v)
                    for k, v in data.items()
                }
            except (json.JSONDecodeError, KeyError):
                self._index = {}

    def _save_index(self) -> None:
        """Save the cache index to disk."""
        data = {k: v.to_dict() for k, v in self._index.items()}
        self.index_path.write_text(json.dumps(data, indent=2))

    @staticmethod
    def generate_key(
        prompt: str,
        generator: str,
        width: int,
        height: int,
        **kwargs
    ) -> str:
        """
        Generate a unique cache key for the given parameters.

        Args:
            prompt: Generation prompt
            generator: Generator name
            width: Image width
            height: Image height
            **kwargs: Additional parameters

        Returns:
            SHA256 hash as cache key
        """
        key_data = {
            'prompt': prompt,
            'generator': generator,
            'width': width,
            'height': height,
            **kwargs
        }
        key_string = json.dumps(key_data, sort_keys=True)
        return hashlib.sha256(key_string.encode()).hexdigest()[:16]

    def get(self, key: str) -> Optional[bytes]:
        """
        Retrieve a cached image.

        Args:
            key: Cache key

        Returns:
            Image bytes if found and valid, None otherwise
        """
        entry = self._index.get(key)

        if entry is None:
            return None

        # Check TTL
        if time.time() - entry.created_at > self.ttl_seconds:
            self.delete(key)
            return None

        # Check file exists
        file_path = Path(entry.file_path)
        if not file_path.exists():
            del self._index[key]
            self._save_index()
            return None

        return file_path.read_bytes()

    def get_entry(self, key: str) -> Optional[CacheEntry]:
        """
        Get cache entry metadata.

        Args:
            key: Cache key

        Returns:
            CacheEntry if found, None otherwise
        """
        return self._index.get(key)

    def put(
        self,
        key: str,
        data: bytes,
        prompt: str,
        generator: str,
        width: int,
        height: int,
        metadata: Optional[Dict[str, Any]] = None
    ) -> CacheEntry:
        """
        Store an image in the cache.

        Args:
            key: Cache key
            data: Image bytes
            prompt: Generation prompt
            generator: Generator name
            width: Image width
            height: Image height
            metadata: Additional metadata

        Returns:
            Created cache entry
        """
        # Ensure space available
        self._ensure_space(len(data))

        # Save image file
        file_path = self.images_dir / f"{key}.png"
        file_path.write_bytes(data)

        # Create entry
        entry = CacheEntry(
            key=key,
            file_path=str(file_path),
            prompt=prompt,
            generator=generator,
            width=width,
            height=height,
            created_at=time.time(),
            size_bytes=len(data),
            metadata=metadata or {}
        )

        self._index[key] = entry
        self._save_index()

        return entry

    def delete(self, key: str) -> bool:
        """
        Delete a cached image.

        Args:
            key: Cache key

        Returns:
            True if deleted, False if not found
        """
        entry = self._index.get(key)
        if entry is None:
            return False

        # Delete file
        file_path = Path(entry.file_path)
        if file_path.exists():
            file_path.unlink()

        del self._index[key]
        self._save_index()

        return True

    def _ensure_space(self, needed_bytes: int) -> None:
        """Ensure there's enough space for new data."""
        current_size = self.get_total_size()

        if current_size + needed_bytes <= self.max_size_bytes:
            return

        # Sort entries by age (oldest first)
        entries = sorted(
            self._index.values(),
            key=lambda e: e.created_at
        )

        # Delete oldest entries until we have space
        for entry in entries:
            if current_size + needed_bytes <= self.max_size_bytes:
                break
            self.delete(entry.key)
            current_size -= entry.size_bytes

    def get_total_size(self) -> int:
        """Get total size of cached images in bytes."""
        return sum(e.size_bytes for e in self._index.values())

    def get_stats(self) -> dict:
        """Get cache statistics."""
        return {
            'entries': len(self._index),
            'total_size_mb': self.get_total_size() / (1024 * 1024),
            'max_size_mb': self.max_size_bytes / (1024 * 1024),
            'usage_percent': (self.get_total_size() / self.max_size_bytes) * 100 if self.max_size_bytes > 0 else 0
        }

    def clear(self) -> int:
        """
        Clear all cached images.

        Returns:
            Number of entries cleared
        """
        count = len(self._index)

        # Delete all files
        for entry in self._index.values():
            file_path = Path(entry.file_path)
            if file_path.exists():
                file_path.unlink()

        self._index.clear()
        self._save_index()

        return count

    def cleanup_expired(self) -> int:
        """
        Remove expired cache entries.

        Returns:
            Number of entries removed
        """
        now = time.time()
        expired_keys = [
            key for key, entry in self._index.items()
            if now - entry.created_at > self.ttl_seconds
        ]

        for key in expired_keys:
            self.delete(key)

        return len(expired_keys)
