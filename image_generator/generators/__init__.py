"""Image generation backends."""

from .base import BaseGenerator, GeneratedImage, GeneratorError, RateLimitError, ContentFilterError, APIError
from .gemini_rest_generator import GeminiRestGenerator
from .mock_generator import MockGenerator
from .vercel_proxy_generator import VercelProxyGenerator

# Legacy import (uses gRPC, may have SSL issues in some environments)
# from .gemini_generator import GeminiGenerator

__all__ = [
    "BaseGenerator",
    "GeneratedImage",
    "GeneratorError",
    "RateLimitError",
    "ContentFilterError",
    "APIError",
    "GeminiRestGenerator",
    "MockGenerator",
    "VercelProxyGenerator",
]
