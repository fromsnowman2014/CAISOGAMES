"""
Base classes for image generators.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path
import hashlib
import json


@dataclass
class GeneratedImage:
    """Represents a generated image with metadata."""

    image_data: bytes
    format: str  # 'png', 'jpg', 'webp'
    width: int
    height: int
    prompt: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)

    @property
    def size(self) -> tuple:
        """Return (width, height) tuple."""
        return (self.width, self.height)

    @property
    def cache_key(self) -> str:
        """Generate a cache key for this image."""
        data = f"{self.prompt}:{self.width}x{self.height}:{json.dumps(self.metadata, sort_keys=True)}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]

    def save(self, path: Path) -> Path:
        """Save image to file."""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, 'wb') as f:
            f.write(self.image_data)

        return path


class BaseGenerator(ABC):
    """Abstract base class for image generators."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self._validate_api_key()

    def _validate_api_key(self):
        """Validate API key format."""
        if not self.api_key:
            raise ValueError("API key is required")

    @abstractmethod
    async def generate(
        self,
        prompt: str,
        width: int = 1024,
        height: int = 1024,
        num_images: int = 1,
        **kwargs
    ) -> List[GeneratedImage]:
        """
        Generate images from a text prompt.

        Args:
            prompt: Text description of the image to generate
            width: Output image width
            height: Output image height
            num_images: Number of images to generate
            **kwargs: Additional generator-specific parameters

        Returns:
            List of GeneratedImage objects
        """
        pass

    @abstractmethod
    async def check_health(self) -> bool:
        """Check if the generator is working properly."""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Generator name for logging."""
        pass

    @property
    @abstractmethod
    def supported_sizes(self) -> List[tuple]:
        """List of supported (width, height) tuples."""
        pass

    def validate_size(self, width: int, height: int) -> tuple:
        """Validate and adjust size to nearest supported size."""
        if (width, height) in self.supported_sizes:
            return (width, height)

        # Find closest supported size
        min_diff = float('inf')
        closest = self.supported_sizes[0]

        for size in self.supported_sizes:
            diff = abs(size[0] - width) + abs(size[1] - height)
            if diff < min_diff:
                min_diff = diff
                closest = size

        return closest


class GeneratorError(Exception):
    """Base exception for generator errors."""
    pass


class RateLimitError(GeneratorError):
    """Raised when API rate limit is exceeded."""
    pass


class ContentFilterError(GeneratorError):
    """Raised when content is filtered by the API."""
    pass


class APIError(GeneratorError):
    """Raised for general API errors."""
    pass
