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
import json
import urllib.request
import urllib.error
import asyncio
import ssl
from typing import List, Optional, Dict, Any

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
        timeout: int = 300
    ):
        """
        Initialize the Vercel proxy generator.
        
        Args:
            vercel_url: Base URL of the Vercel deployment
            api_key: Not used for proxy, but required by base class
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
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

        # Create unverified SSL context for local dev
        self.ssl_ctx = ssl.create_default_context()
        self.ssl_ctx.check_hostname = False
        self.ssl_ctx.verify_mode = ssl.CERT_NONE

    @property
    def name(self) -> str:
        return "vercel-proxy"

    @property
    def supported_sizes(self) -> List[tuple]:
        return self.SUPPORTED_SIZES

    async def check_health(self) -> bool:
        """Check if the Vercel endpoint is accessible."""
        return await asyncio.to_thread(self._check_health_sync)

    def _check_health_sync(self) -> bool:
        try:
            with urllib.request.urlopen(self.endpoint, timeout=10, context=self.ssl_ctx) as response:
                data = json.loads(response.read().decode('utf-8'))
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
        """Generate images via Vercel proxy."""
        
        payload = {
            "prompt": prompt,
            "width": width,
            "height": height,
            "style": style,
            **kwargs
        }

        return await asyncio.to_thread(self._generate_sync, payload)

    def _generate_sync(self, payload: Dict[str, Any]) -> List[GeneratedImage]:
        try:
            req = urllib.request.Request(
                self.endpoint,
                data=json.dumps(payload).encode('utf-8'),
                headers={'Content-Type': 'application/json'}
            )

            with urllib.request.urlopen(req, timeout=self.timeout, context=self.ssl_ctx) as response:
                data = json.loads(response.read().decode('utf-8'))

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
                    prompt=payload['prompt'],
                    width=data.get('width', payload['width']),
                    height=data.get('height', payload['height']),
                    format=data.get('format', 'png')
                )]

        except urllib.error.HTTPError as e:
            if e.code == 429:
                raise RateLimitError("Rate limit exceeded")
            elif e.code == 400:
                try:
                    error_body = e.read().decode('utf-8')
                    data = json.loads(error_body)
                    error_msg = data.get('error', 'Bad request')
                    if 'safety' in error_msg.lower() or 'filter' in error_msg.lower():
                        raise ContentFilterError(f"Content filtered: {error_msg}")
                    raise GeneratorError(f"Bad request: {error_msg}")
                except json.JSONDecodeError:
                    raise GeneratorError(f"Bad request: {e.reason}")
            elif e.code == 504:
                raise APIError(f"Gateway Timeout (Vercel function timed out)")
            else:
                raise APIError(f"Proxy error: {e.code} {e.reason}")
                
        except urllib.error.URLError as e:
            if isinstance(e.reason, TimeoutError):
                raise APIError(f"Request timed out after {self.timeout}s")
            raise APIError(f"Connection failed: {str(e)}")
            
        except Exception as e:
            raise GeneratorError(f"Unexpected error: {str(e)}")
