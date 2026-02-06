"""
Vercel Proxy Generator - Calls Vercel API endpoint for image generation.

This generator is designed for use in Claude Code development environment
where direct access to Gemini API is blocked. It proxies requests through
a Vercel serverless function that has access to the API key.

Usage:
    generator = VercelProxyGenerator("https://your-app.vercel.app")
    images = await generator.generate("pixel art monster")
"""

import base64
import os
from typing import List, Optional
import httpx

from .base import (
    BaseGenerator,
    GeneratedImage,
    GeneratorError,
    RateLimitError,
    ContentFilterError,
    APIError,
)


class VercelProxyGenerator(BaseGenerator):
    """
    Image generator that proxies requests through Vercel API.
    Use this when direct API access is blocked (e.g., in Claude Code environment).
    """

    SUPPORTED_SIZES = [
        (256, 256), (512, 512), (1024, 1024),
        (1024, 768), (768, 1024),
    ]

    def __init__(
        self,
        vercel_url: Optional[str] = None,
        api_key: str = "proxy",
        timeout: int = 180
    ):
        """
        Initialize the Vercel proxy generator.

        Args:
            vercel_url: Base URL of the Vercel deployment (e.g., "https://caisogames.vercel.app")
                        Can also be set via VERCEL_APP_URL environment variable.
            api_key: Not used for proxy, but required by base class
            timeout: Request timeout in seconds (longer for proxy)
        """
        self.api_key = api_key  # Not used but required by base class
        self.timeout = timeout

        # Get Vercel URL from parameter or environment
        self.vercel_url = vercel_url or os.getenv('VERCEL_APP_URL', '')

        if not self.vercel_url:
            raise GeneratorError(
                "Vercel URL not configured. Set VERCEL_APP_URL environment variable "
                "or pass vercel_url parameter."
            )

        # Normalize URL
        self.vercel_url = self.vercel_url.rstrip('/')
        self.endpoint = f"{self.vercel_url}/api/generate-image"

    @property
    def name(self) -> str:
        """Generator name for logging."""
        return "vercel-proxy"

    @property
    def supported_sizes(self) -> List[tuple]:
        """List of supported (width, height) tuples."""
        return self.SUPPORTED_SIZES

    async def check_health(self) -> bool:
        """Check if the Vercel endpoint is accessible."""
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(self.endpoint)
                data = response.json()
                return data.get('status') == 'ok' and data.get('api_configured', False)
        except Exception:
            return False

    async def generate(
        self,
        prompt: str,
        width: int = 512,
        height: int = 512,
        num_images: int = 1,
        style: str = 'pixel_art',
        **kwargs
    ) -> List[GeneratedImage]:
        """
        Generate images via Vercel proxy.

        Args:
            prompt: Text description of the image
            width: Desired width
            height: Desired height
            num_images: Number of images (currently only 1 supported via proxy)
            style: Art style to apply
            **kwargs: Additional options (passed to API)

        Returns:
            List of GeneratedImage objects
        """
        payload = {
            "prompt": prompt,
            "width": width,
            "height": height,
            "style": style,
            **kwargs
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(self.endpoint, json=payload)

                if response.status_code == 429:
                    raise RateLimitError("Rate limit exceeded")
                elif response.status_code == 400:
                    data = response.json()
                    error_msg = data.get('error', 'Bad request')
                    if 'safety' in error_msg.lower() or 'filter' in error_msg.lower():
                        raise ContentFilterError(f"Content filtered: {error_msg}")
                    raise GeneratorError(f"Bad request: {error_msg}")
                elif response.status_code != 200:
                    raise APIError(f"Proxy error: {response.status_code}")

                data = response.json()

                if not data.get('success'):
                    error = data.get('error', 'Unknown error')
                    raise GeneratorError(f"Generation failed: {error}")

                # Decode image
                image_b64 = data.get('image')
                if not image_b64:
                    raise GeneratorError("No image in response")

                image_data = base64.b64decode(image_b64)

                return [GeneratedImage(
                    image_data=image_data,
                    prompt=prompt,
                    width=data.get('width', width),
                    height=data.get('height', height),
                    format=data.get('format', 'png')
                )]

        except httpx.TimeoutException:
            raise APIError(f"Request timed out after {self.timeout}s")
        except httpx.RequestError as e:
            raise APIError(f"Request failed: {str(e)}")
