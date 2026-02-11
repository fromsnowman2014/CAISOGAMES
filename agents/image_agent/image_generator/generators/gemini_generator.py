"""
Google Gemini/Imagen image generator implementation.
"""

import asyncio
import base64
import io
from typing import List, Optional, Dict, Any
from datetime import datetime

try:
    import google.generativeai as genai
    from google.generativeai.types import HarmCategory, HarmBlockThreshold
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False

from .base import (
    BaseGenerator,
    GeneratedImage,
    GeneratorError,
    RateLimitError,
    ContentFilterError,
    APIError,
)


class GeminiGenerator(BaseGenerator):
    """
    Image generator using Google Gemini API.

    Supports both Imagen models and Gemini native image generation.
    """

    SUPPORTED_SIZES = [
        (256, 256),
        (512, 512),
        (1024, 1024),
        (1024, 768),
        (768, 1024),
        (1536, 1024),
        (1024, 1536),
    ]

    def __init__(self, api_key: str, model_name: str = "gemini-3-pro-preview"):
        """
        Initialize Gemini generator.

        Args:
            api_key: Google AI API key
            model_name: Model to use (default: gemini-2.0-flash-exp for image gen)
        """
        if not GENAI_AVAILABLE:
            raise ImportError(
                "google-generativeai package is required. "
                "Install with: pip install google-generativeai"
            )

        super().__init__(api_key)
        self.model_name = model_name

        # Configure the API
        genai.configure(api_key=api_key)

        # Initialize model
        self._model = genai.GenerativeModel(
            model_name=model_name,
            safety_settings={
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            }
        )

    @property
    def name(self) -> str:
        return f"Gemini ({self.model_name})"

    @property
    def supported_sizes(self) -> List[tuple]:
        return self.SUPPORTED_SIZES

    async def generate(
        self,
        prompt: str,
        width: int = 1024,
        height: int = 1024,
        num_images: int = 1,
        style: Optional[str] = None,
        negative_prompt: Optional[str] = None,
        **kwargs
    ) -> List[GeneratedImage]:
        """
        Generate images using Gemini API.

        Args:
            prompt: Text description of the image
            width: Output width (will be adjusted to supported size)
            height: Output height (will be adjusted to supported size)
            num_images: Number of images to generate (1-4)
            style: Optional style modifier
            negative_prompt: What to avoid in the image

        Returns:
            List of GeneratedImage objects
        """
        # Validate and adjust size
        width, height = self.validate_size(width, height)

        # Build enhanced prompt
        enhanced_prompt = self._build_prompt(prompt, style, negative_prompt)

        # Generate images
        results = []

        for i in range(min(num_images, 4)):
            try:
                image = await self._generate_single(enhanced_prompt, width, height)
                if image:
                    results.append(image)
            except Exception as e:
                # Log but continue with other images
                print(f"Failed to generate image {i+1}: {e}")

        if not results:
            raise GeneratorError(f"Failed to generate any images for prompt: {prompt}")

        return results

    async def _generate_single(
        self,
        prompt: str,
        width: int,
        height: int
    ) -> Optional[GeneratedImage]:
        """Generate a single image."""

        # Gemini 2.0 Flash supports image generation with response_modalities
        generation_prompt = f"""Generate an image based on this description:

{prompt}

Requirements:
- Create a high-quality game asset image
- The image should be suitable for use in a children's casual game
- Use vibrant, appealing colors
- Make the style consistent and professional"""

        try:
            # Use asyncio to run the synchronous API call
            response = await asyncio.to_thread(
                self._model.generate_content,
                generation_prompt,
                generation_config=genai.GenerationConfig(
                    response_mime_type="image/png",
                )
            )

            # Check if we got an image response
            if response.parts:
                for part in response.parts:
                    if hasattr(part, 'inline_data') and part.inline_data:
                        image_data = part.inline_data.data
                        if isinstance(image_data, str):
                            image_data = base64.b64decode(image_data)

                        return GeneratedImage(
                            image_data=image_data,
                            format='png',
                            width=width,
                            height=height,
                            prompt=prompt,
                            metadata={
                                'model': self.model_name,
                                'generator': 'gemini',
                            },
                            timestamp=datetime.now()
                        )

            # Fallback: Try using Imagen API if available
            return await self._generate_with_imagen(prompt, width, height)

        except Exception as e:
            error_msg = str(e).lower()

            if 'rate' in error_msg or 'quota' in error_msg:
                raise RateLimitError(f"Rate limit exceeded: {e}")
            elif 'safety' in error_msg or 'blocked' in error_msg:
                raise ContentFilterError(f"Content filtered: {e}")
            else:
                raise APIError(f"API error: {e}")

    async def _generate_with_imagen(
        self,
        prompt: str,
        width: int,
        height: int
    ) -> Optional[GeneratedImage]:
        """Fallback to Imagen API if available."""
        try:
            # Try using the imagen model directly
            imagen = genai.ImageGenerationModel("imagen-4.0-generate-001")

            response = await asyncio.to_thread(
                imagen.generate_images,
                prompt=prompt,
                number_of_images=1,
                aspect_ratio=self._get_aspect_ratio(width, height),
            )

            if response.images:
                image = response.images[0]
                image_data = image._pil_image

                # Convert PIL image to bytes
                buffer = io.BytesIO()
                image_data.save(buffer, format='PNG')
                image_bytes = buffer.getvalue()

                return GeneratedImage(
                    image_data=image_bytes,
                    format='png',
                    width=width,
                    height=height,
                    prompt=prompt,
                    metadata={
                        'model': 'imagen-4.0-generate-001',
                        'generator': 'imagen',
                    },
                    timestamp=datetime.now()
                )

        except Exception as e:
            print(f"Imagen fallback failed: {e}")

        return None

    def _get_aspect_ratio(self, width: int, height: int) -> str:
        """Convert dimensions to aspect ratio string."""
        ratio = width / height

        if abs(ratio - 1.0) < 0.1:
            return "1:1"
        elif abs(ratio - 16/9) < 0.1:
            return "16:9"
        elif abs(ratio - 9/16) < 0.1:
            return "9:16"
        elif abs(ratio - 4/3) < 0.1:
            return "4:3"
        elif abs(ratio - 3/4) < 0.1:
            return "3:4"
        else:
            return "1:1"

    def _build_prompt(
        self,
        prompt: str,
        style: Optional[str] = None,
        negative_prompt: Optional[str] = None
    ) -> str:
        """Build enhanced prompt with style and negative prompts."""
        parts = [prompt]

        if style:
            parts.append(f"Art style: {style}")

        if negative_prompt:
            parts.append(f"Avoid: {negative_prompt}")

        return ". ".join(parts)

    async def check_health(self) -> bool:
        """Check if the API is accessible."""
        try:
            # Simple test to verify API key works
            models = await asyncio.to_thread(genai.list_models)
            return len(list(models)) > 0
        except Exception:
            return False


class GeminiTextToImage:
    """
    Simplified interface for text-to-image generation with Gemini.
    """

    def __init__(self, api_key: str):
        self.generator = GeminiGenerator(api_key)

    async def generate(
        self,
        prompt: str,
        output_path: str,
        size: tuple = (1024, 1024),
        style: Optional[str] = None
    ) -> str:
        """
        Generate an image and save it to a file.

        Args:
            prompt: Description of the image
            output_path: Where to save the image
            size: (width, height) tuple
            style: Optional style modifier

        Returns:
            Path to the saved image
        """
        images = await self.generator.generate(
            prompt=prompt,
            width=size[0],
            height=size[1],
            num_images=1,
            style=style
        )

        if images:
            return str(images[0].save(output_path))

        raise GeneratorError("Failed to generate image")
