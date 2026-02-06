"""
Configuration for Image Agent

Manages settings, thresholds, and environment configuration
"""

import os
from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass
class AgentConfig:
    """
    Configuration for the Image Agent system

    Can be customized via environment variables or direct initialization
    """

    # Quality thresholds
    quality_threshold: float = 0.9  # 90% to pass
    max_iterations: int = 5

    # Weights for quality scoring
    quality_weights: Dict[str, float] = field(default_factory=lambda: {
        'transparency': 0.20,
        'size': 0.10,
        'style': 0.25,
        'color': 0.15,
        'quality': 0.20,
        'game_fit': 0.10,
    })

    # Image generation settings
    default_size: tuple = (64, 64)
    max_size: tuple = (1024, 1024)
    default_format: str = 'png'

    # Model settings
    use_premium_model: bool = True
    model_tier: str = 'premium'  # 'standard', 'premium', 'fast'

    # Caching
    enable_cache: bool = True
    cache_ttl_days: int = 7

    # Logging
    log_level: str = 'INFO'
    log_iterations: bool = True
    save_iteration_images: bool = True

    # Paths
    output_dir: str = './generated_assets'
    cache_dir: str = './cache'

    # API settings
    vercel_app_url: Optional[str] = None
    gemini_api_key: Optional[str] = None
    request_timeout: int = 120  # seconds
    retry_attempts: int = 3

    def __post_init__(self):
        """Load from environment variables"""
        # Quality settings
        self.quality_threshold = float(
            os.getenv('AGENT_QUALITY_THRESHOLD', self.quality_threshold)
        )
        self.max_iterations = int(
            os.getenv('AGENT_MAX_ITERATIONS', self.max_iterations)
        )

        # Model settings
        self.use_premium_model = os.getenv(
            'AGENT_USE_PREMIUM_MODEL', 'true'
        ).lower() == 'true'
        self.model_tier = os.getenv('AGENT_MODEL_TIER', self.model_tier)

        # API settings
        self.vercel_app_url = os.getenv('VERCEL_APP_URL', self.vercel_app_url)
        self.gemini_api_key = os.getenv('GEMINI_API_KEY', self.gemini_api_key)

        # Logging
        self.log_level = os.getenv('AGENT_LOG_LEVEL', self.log_level)

        # Paths
        self.output_dir = os.getenv('AGENT_OUTPUT_DIR', self.output_dir)
        self.cache_dir = os.getenv('AGENT_CACHE_DIR', self.cache_dir)

    @classmethod
    def from_env(cls) -> 'AgentConfig':
        """Create config from environment variables"""
        return cls()

    @classmethod
    def for_testing(cls) -> 'AgentConfig':
        """Create config suitable for testing"""
        return cls(
            max_iterations=2,
            quality_threshold=0.5,
            use_premium_model=False,
            enable_cache=False,
            save_iteration_images=False,
        )

    def get_generator_config(self) -> Dict:
        """Get configuration for the image generator"""
        return {
            'model_tier': self.model_tier if self.use_premium_model else 'standard',
            'timeout': self.request_timeout,
            'max_retries': self.retry_attempts,
            'use_cache': self.enable_cache,
        }

    def validate(self) -> bool:
        """Validate configuration"""
        errors = []

        if not 0 < self.quality_threshold <= 1:
            errors.append("quality_threshold must be between 0 and 1")

        if self.max_iterations < 1:
            errors.append("max_iterations must be at least 1")

        if self.max_iterations > 10:
            errors.append("max_iterations should not exceed 10 (cost control)")

        weight_sum = sum(self.quality_weights.values())
        if abs(weight_sum - 1.0) > 0.01:
            errors.append(f"quality_weights must sum to 1.0 (current: {weight_sum})")

        if errors:
            raise ValueError("Configuration errors:\n" + "\n".join(errors))

        return True


# Default configuration instance
default_config = AgentConfig()
