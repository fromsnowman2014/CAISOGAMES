"""
Image Agent - AI-powered game asset generation with quality review

This module provides an intelligent agent system that:
1. Parses game asset requests
2. Generates detailed prompts for image generation
3. Creates images using the image_generator API
4. Reviews quality from a professional game designer perspective
5. Iteratively improves until 90% quality or 5 iterations

Usage:
    from image_agent import ImageAgent, AssetRequest

    agent = ImageAgent()
    request = AssetRequest(
        asset_type='sprite',
        description='cute red apple',
        style='kawaii',
        size=(64, 64),
        transparency=True
    )
    result = await agent.generate(request)
"""

from image_agent.core.data_classes import (
    AssetRequest,
    AssetType,
    StyleType,
    DetailedPrompt,
    QualityReport,
    TransparencyReport,
    IterationRecord,
    AgentResult,
)

__version__ = "0.1.0"
__all__ = [
    "ImageAgent",
    "AssetRequest",
    "AssetType",
    "StyleType",
    "DetailedPrompt",
    "QualityReport",
    "TransparencyReport",
    "IterationRecord",
    "AgentResult",
]

# Lazy import to avoid circular dependencies
def __getattr__(name):
    if name == "ImageAgent":
        from image_agent.core.image_agent import ImageAgent
        return ImageAgent
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
