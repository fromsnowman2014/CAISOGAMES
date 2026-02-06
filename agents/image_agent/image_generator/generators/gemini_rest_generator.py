"""
Gemini REST API Generator for Image Generation.
Uses httpx directly instead of the gRPC-based SDK for better compatibility.
"""

import base64
import asyncio
import ssl
from typing import List, Optional
try:
    import httpx
except ImportError:
    httpx = None


from .base import (
    BaseGenerator,
    GeneratedImage,
    GeneratorError,
    RateLimitError,
    ContentFilterError,
    APIError,
)


class GeminiRestGenerator(BaseGenerator):
    """
    Image generator using Gemini API via REST.
    More compatible with restricted environments.
    """

    # Gemini API endpoint for image generation
    BASE_URL = "https://generativelanguage.googleapis.com/v1beta"

    # Models for image generation
    # Imagen 3 for dedicated image generation
    IMAGEN_MODEL = "imagen-3.0-generate-001"
    # Gemini for multimodal (fallback)
    TEXT_MODEL = "gemini-1.5-flash"

    # Supported image sizes
    SUPPORTED_SIZES = [
        (256, 256), (512, 512), (1024, 1024),
        (1024, 768), (768, 1024),
        (1536, 1024), (1024, 1536),
    ]

    def __init__(self, api_key: str, timeout: int = 120):
        """
        Initialize the Gemini REST generator.

        Args:
            api_key: Google API key for Gemini
            timeout: Request timeout in seconds
        """
        if not api_key:
            raise GeneratorError("GEMINI_API_KEY is required")

        self.api_key = api_key
        self.timeout = timeout

        # Create SSL context that doesn't verify (for restricted environments)
        # In production on Vercel, this won't be needed
        self._ssl_context = ssl.create_default_context()
        self._ssl_context.check_hostname = False
        self._ssl_context.verify_mode = ssl.CERT_NONE

    @property
    def name(self) -> str:
        """Generator name for logging."""
        return "gemini-rest"

    @property
    def supported_sizes(self) -> List[tuple]:
        """List of supported (width, height) tuples."""
        return self.SUPPORTED_SIZES

    async def check_health(self) -> bool:
        """Check if the generator is working properly."""
        try:
            url = f"{self.BASE_URL}/models/{self.IMAGEN_MODEL}"
            params = {"key": self.api_key}
            async with httpx.AsyncClient(verify=False, timeout=10) as client:
                response = await client.get(url, params=params)
                return response.status_code == 200
        except Exception:
            return False

    def _get_style_prompt(self, style: str) -> str:
        """Get style-specific prompt additions."""
        styles = {
            'pixel_art': 'Style: 16-bit retro pixel art, limited color palette, crisp pixels, no anti-aliasing.',
            'cartoon': 'Style: cartoon illustration, bold outlines, vibrant colors, clean shapes.',
            'realistic': 'Style: photorealistic, detailed textures, natural lighting.',
            'sketch': 'Style: hand-drawn sketch, pencil lines, artistic shading.',
        }
        return styles.get(style, styles['pixel_art'])

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
        Generate images using Imagen 3 API.

        Args:
            prompt: Text description of the image
            width: Desired width (will be adjusted to supported size)
            height: Desired height (will be adjusted to supported size)
            num_images: Number of images to generate (max 4)
            style: Art style to apply
            **kwargs: Additional options

        Returns:
            List of GeneratedImage objects
        """
        # Build the full prompt with style
        style_prompt = self._get_style_prompt(style)
        full_prompt = f"{prompt}. {style_prompt}"

        # Use Imagen 3 API for image generation
        url = f"{self.BASE_URL}/models/{self.IMAGEN_MODEL}:predict"

        # Determine aspect ratio from dimensions
        aspect_ratio = self._get_aspect_ratio(width, height)

        payload = {
            "instances": [{
                "prompt": full_prompt
            }],
            "parameters": {
                "sampleCount": min(num_images, 4),
                "aspectRatio": aspect_ratio,
                "personGeneration": "allow_adult",
                "safetySetting": "block_only_high"
            }
        }

        params = {"key": self.api_key}

        try:
            async with httpx.AsyncClient(verify=False, timeout=self.timeout) as client:
                response = await client.post(url, json=payload, params=params)

                if response.status_code == 429:
                    raise RateLimitError("Rate limit exceeded")
                elif response.status_code == 400:
                    error_data = response.json()
                    error_msg = error_data.get('error', {}).get('message', 'Bad request')
                    if 'safety' in error_msg.lower() or 'block' in error_msg.lower():
                        raise ContentFilterError(f"Content filtered: {error_msg}")
                    raise GeneratorError(f"Bad request: {error_msg}")
                elif response.status_code == 403:
                    # Try fallback to generateContent API
                    return await self._generate_with_gemini(prompt, width, height, num_images, style, **kwargs)
                elif response.status_code != 200:
                    error_msg = response.text[:500] if response.text else "Unknown error"
                    raise APIError(f"API error: {response.status_code} - {error_msg}")

                data = response.json()

                # Parse Imagen response
                images = []
                predictions = data.get('predictions', [])

                for pred in predictions:
                    if 'bytesBase64Encoded' in pred:
                        image_data = base64.b64decode(pred['bytesBase64Encoded'])
                        mime_type = pred.get('mimeType', 'image/png')

                        format_map = {
                            'image/png': 'png',
                            'image/jpeg': 'jpeg',
                            'image/webp': 'webp',
                        }
                        img_format = format_map.get(mime_type, 'png')

                        images.append(GeneratedImage(
                            image_data=image_data,
                            prompt=prompt,
                            width=width,
                            height=height,
                            format=img_format
                        ))

                if not images:
                    # Fallback to Gemini multimodal
                    return await self._generate_with_gemini(prompt, width, height, num_images, style, **kwargs)

                return images[:num_images]

        except (RateLimitError, ContentFilterError, GeneratorError):
            raise
        except httpx.TimeoutException:
            raise APIError(f"Request timed out after {self.timeout}s")
        except httpx.RequestError as e:
            raise APIError(f"Request failed: {str(e)}")

    async def _generate_with_gemini(
        self,
        prompt: str,
        width: int = 512,
        height: int = 512,
        num_images: int = 1,
        style: str = 'pixel_art',
        **kwargs
    ) -> List[GeneratedImage]:
        """
        Fallback: Generate images using Gemini multimodal API.
        Uses text generation with image output capability.
        """
        style_prompt = self._get_style_prompt(style)
        full_prompt = f"Generate an image: {prompt}. {style_prompt}"

        url = f"{self.BASE_URL}/models/{self.TEXT_MODEL}:generateContent"

        payload = {
            "contents": [{
                "parts": [{
                    "text": full_prompt
                }]
            }],
            "generationConfig": {
                "responseMimeType": "text/plain"
            }
        }

        params = {"key": self.api_key}

        async with httpx.AsyncClient(verify=False, timeout=self.timeout) as client:
            response = await client.post(url, json=payload, params=params)

            if response.status_code != 200:
                raise APIError(f"Gemini fallback failed: {response.status_code}")

            data = response.json()
            candidates = data.get('candidates', [])

            images = []
            for candidate in candidates:
                parts = candidate.get('content', {}).get('parts', [])
                for part in parts:
                    if 'inlineData' in part:
                        inline_data = part['inlineData']
                        image_data = base64.b64decode(inline_data['data'])
                        images.append(GeneratedImage(
                            image_data=image_data,
                            prompt=prompt,
                            width=width,
                            height=height,
                            format='png'
                        ))

            if not images:
                # Return error with text response for debugging
                text_parts = []
                for candidate in candidates:
                    for part in candidate.get('content', {}).get('parts', []):
                        if 'text' in part:
                            text_parts.append(part['text'])

                raise GeneratorError(
                    f"No image generated. This model may not support image generation. "
                    f"Response: {' '.join(text_parts)[:200] if text_parts else 'Empty'}"
                )

            return images[:num_images]

    def _get_aspect_ratio(self, width: int, height: int) -> str:
        """Get aspect ratio string from dimensions."""
        ratio = width / height
        if ratio > 1.6:
            return "16:9"
        elif ratio > 1.2:
            return "4:3"
        elif ratio < 0.6:
            return "9:16"
        elif ratio < 0.8:
            return "3:4"
        else:
            return "1:1"
