"""
Prompt Generator - Creates detailed image generation prompts

This module transforms AssetRequest objects into optimized prompts
for image generation APIs like Gemini/Imagen.
"""

from typing import Dict, List, Optional

from agents.image_agent.core.data_classes import (
    AssetRequest,
    AssetType,
    DetailedPrompt,
    StyleType,
)


class PromptGenerator:
    """
    Generates detailed prompts for image generation from game asset requests

    Acts as a professional game artist, creating prompts that capture:
    - Visual style and aesthetics
    - Technical requirements
    - Game-specific context
    """

    # Style-specific keywords and modifiers
    STYLE_TEMPLATES: Dict[StyleType, Dict[str, any]] = {
        StyleType.PIXEL_ART: {
            'keywords': ['pixel art', 'pixelated', 'retro game style', '2D sprite'],
            'modifiers': ['clean pixels', 'no anti-aliasing', 'limited color palette'],
            'negative': 'blurry, smooth gradients, 3D, realistic, photographic',
        },
        StyleType.KAWAII: {
            'keywords': ['kawaii', 'cute', 'chibi proportions', 'adorable', 'japanese cute style'],
            'modifiers': ['big eyes', 'soft colors', 'rounded shapes', 'friendly expression'],
            'negative': 'scary, realistic proportions, dark, gritty, violent',
        },
        StyleType.CHIBI: {
            'keywords': ['chibi', 'super deformed', 'big head small body', 'cute anime style'],
            'modifiers': ['2-3 head ratio', 'simplified features', 'expressive eyes'],
            'negative': 'realistic proportions, detailed anatomy, photorealistic',
        },
        StyleType.CARTOON: {
            'keywords': ['cartoon', 'animated style', 'stylized', 'colorful'],
            'modifiers': ['bold outlines', 'vibrant colors', 'exaggerated features'],
            'negative': 'realistic, photographic, dull colors, no outlines',
        },
        StyleType.FLAT: {
            'keywords': ['flat design', 'minimalist', 'vector style', 'simple shapes'],
            'modifiers': ['no gradients', 'solid colors', 'geometric', 'clean edges'],
            'negative': 'detailed textures, gradients, shadows, 3D effects',
        },
        StyleType.REALISTIC: {
            'keywords': ['realistic', 'detailed', 'lifelike', 'high quality'],
            'modifiers': ['proper lighting', 'detailed textures', 'accurate proportions'],
            'negative': 'cartoon, stylized, pixelated, low quality',
        },
        StyleType.RETRO_8BIT: {
            'keywords': ['8-bit', 'NES style', 'retro game', 'classic pixel art'],
            'modifiers': ['very limited colors (4-8)', 'chunky pixels', 'simple shapes'],
            'negative': 'high resolution, smooth, modern graphics, many colors',
        },
        StyleType.RETRO_16BIT: {
            'keywords': ['16-bit', 'SNES style', 'Sega Genesis style', 'retro pixel art'],
            'modifiers': ['medium color palette (16-32)', 'detailed sprites', 'classic gaming'],
            'negative': 'modern HD, smooth gradients, photorealistic',
        },
        StyleType.WATERCOLOR: {
            'keywords': ['watercolor', 'painted', 'artistic', 'soft edges'],
            'modifiers': ['flowing colors', 'paper texture', 'artistic brushstrokes'],
            'negative': 'sharp edges, digital look, pixel art, vector',
        },
        StyleType.MINIMALIST: {
            'keywords': ['minimalist', 'simple', 'clean', 'essential shapes only'],
            'modifiers': ['few colors', 'lots of white space', 'basic geometry'],
            'negative': 'detailed, complex, busy, cluttered',
        },
    }

    # Asset type specific prompts
    ASSET_TEMPLATES: Dict[AssetType, Dict[str, any]] = {
        AssetType.SPRITE: {
            'prefix': 'game sprite of',
            'suffix': 'isolated character, game asset, single object',
            'technical': 'centered composition, clear silhouette',
        },
        AssetType.BACKGROUND: {
            'prefix': 'game background scene of',
            'suffix': 'environment art, parallax-ready',
            'technical': 'wide composition, layered depth',
        },
        AssetType.UI: {
            'prefix': 'game UI element',
            'suffix': 'interface design, clean edges',
            'technical': 'crisp borders, readable at small size',
        },
        AssetType.ANIMATION: {
            'prefix': 'animation frame of',
            'suffix': 'sprite sheet ready, consistent style',
            'technical': 'clear pose, exaggerated motion',
        },
        AssetType.ICON: {
            'prefix': 'game icon of',
            'suffix': 'recognizable silhouette, simple design',
            'technical': 'readable at 32x32, high contrast',
        },
        AssetType.TILE: {
            'prefix': 'seamless game tile of',
            'suffix': 'tileable texture, repeating pattern',
            'technical': 'edges match seamlessly',
        },
    }

    def __init__(self):
        """Initialize the prompt generator"""
        pass

    def generate(self, request: AssetRequest) -> DetailedPrompt:
        """
        Generate a detailed prompt from an asset request

        Args:
            request: The asset request containing specifications

        Returns:
            DetailedPrompt with all components for image generation
        """
        # Get templates
        style_template = self.STYLE_TEMPLATES.get(request.style, {})
        asset_template = self.ASSET_TEMPLATES.get(request.asset_type, {})

        # Build main prompt
        main_prompt = self._build_main_prompt(request, asset_template, style_template)

        # Build style modifiers
        style_modifiers = self._build_style_modifiers(request, style_template)

        # Build technical specs
        technical_specs = self._build_technical_specs(request, asset_template)

        # Build negative prompt
        negative_prompt = self._build_negative_prompt(request, style_template)

        return DetailedPrompt(
            main_prompt=main_prompt,
            style_modifiers=style_modifiers,
            technical_specs=technical_specs,
            negative_prompt=negative_prompt,
            version=1,
            source_request_id=request.request_id,
        )

    def _build_main_prompt(
        self,
        request: AssetRequest,
        asset_template: Dict,
        style_template: Dict
    ) -> str:
        """Build the main descriptive prompt"""
        parts = []

        # Asset type prefix
        prefix = asset_template.get('prefix', '')
        if prefix:
            parts.append(prefix)

        # Main description
        parts.append(request.description)

        # Style keywords
        keywords = style_template.get('keywords', [])
        if keywords:
            parts.append(', '.join(keywords[:3]))  # Top 3 keywords

        # Asset suffix
        suffix = asset_template.get('suffix', '')
        if suffix:
            parts.append(suffix)

        # Must-have elements
        if request.must_have:
            must_have_str = ', '.join(request.must_have)
            parts.append(f"must include: {must_have_str}")

        # Game context
        if request.game_context:
            parts.append(f"for {request.game_context} game")

        return ', '.join(parts)

    def _build_style_modifiers(
        self,
        request: AssetRequest,
        style_template: Dict
    ) -> List[str]:
        """Build style modifier list"""
        modifiers = []

        # Style-specific modifiers
        modifiers.extend(style_template.get('modifiers', []))

        # Transparency modifier
        if request.transparency:
            modifiers.append('transparent background')
            modifiers.append('isolated on transparent')
            modifiers.append('PNG with alpha')

        # Color palette
        if request.color_palette:
            colors = ', '.join(request.color_palette[:5])
            modifiers.append(f'color palette: {colors}')

        # Size-based modifiers
        width, height = request.size
        if max(width, height) <= 64:
            modifiers.append('simple details')
            modifiers.append('readable at small size')
        elif max(width, height) >= 256:
            modifiers.append('detailed')
            modifiers.append('high quality')

        return modifiers

    def _build_technical_specs(
        self,
        request: AssetRequest,
        asset_template: Dict
    ) -> str:
        """Build technical specification string"""
        specs = []

        # Size specification
        width, height = request.size
        specs.append(f'{width}x{height} pixels')

        # Asset-specific technical requirements
        technical = asset_template.get('technical', '')
        if technical:
            specs.append(technical)

        # Format
        specs.append(f'{request.output_format.upper()} format')

        # Transparency
        if request.transparency:
            specs.append('with alpha channel')

        return ', '.join(specs)

    def _build_negative_prompt(
        self,
        request: AssetRequest,
        style_template: Dict
    ) -> str:
        """Build negative prompt (things to avoid)"""
        negatives = []

        # Style-specific negatives
        style_negative = style_template.get('negative', '')
        if style_negative:
            negatives.append(style_negative)

        # Must-not-have from request
        if request.must_not_have:
            negatives.extend(request.must_not_have)

        # Common negatives for game assets
        common_negatives = [
            'watermark',
            'signature',
            'text',
            'logo',
            'border',
            'frame',
            'multiple objects',
            'collage',
        ]

        # Add transparency-related negatives
        if request.transparency:
            common_negatives.extend([
                'background',
                'solid background',
                'colored background',
            ])

        negatives.extend(common_negatives)

        return ', '.join(negatives)

    def generate_variation(
        self,
        original: DetailedPrompt,
        variation_type: str = 'style'
    ) -> DetailedPrompt:
        """
        Generate a variation of an existing prompt

        Args:
            original: The original prompt to vary
            variation_type: Type of variation ('style', 'composition', 'color')

        Returns:
            New DetailedPrompt with variations applied
        """
        new_prompt = DetailedPrompt(
            main_prompt=original.main_prompt,
            style_modifiers=original.style_modifiers.copy(),
            technical_specs=original.technical_specs,
            negative_prompt=original.negative_prompt,
            version=original.version + 1,
            source_request_id=original.source_request_id,
        )

        if variation_type == 'style':
            # Add emphasis to style modifiers
            new_prompt.style_modifiers.insert(0, 'highly stylized')
        elif variation_type == 'composition':
            new_prompt.style_modifiers.append('dynamic pose')
            new_prompt.style_modifiers.append('interesting angle')
        elif variation_type == 'color':
            new_prompt.style_modifiers.append('vibrant colors')
            new_prompt.style_modifiers.append('high saturation')

        return new_prompt
