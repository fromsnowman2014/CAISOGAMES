"""Logging utilities for image generator."""

import logging
import sys
from pathlib import Path
from typing import Optional
from datetime import datetime


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the given name.

    Args:
        name: Logger name (usually __name__)

    Returns:
        Configured logger
    """
    return logging.getLogger(f"image_generator.{name}")


def setup_logging(
    level: int = logging.INFO,
    log_file: Optional[Path] = None,
    format_string: Optional[str] = None
) -> None:
    """
    Set up logging for the image generator.

    Args:
        level: Logging level
        log_file: Optional file to write logs to
        format_string: Custom format string
    """
    if format_string is None:
        format_string = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"

    # Create formatter
    formatter = logging.Formatter(format_string, datefmt="%Y-%m-%d %H:%M:%S")

    # Get root logger for image_generator
    root_logger = logging.getLogger("image_generator")
    root_logger.setLevel(level)

    # Remove existing handlers
    root_logger.handlers.clear()

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # File handler (if specified)
    if log_file:
        log_file = Path(log_file)
        log_file.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)


class GenerationLogger:
    """Specialized logger for tracking image generation."""

    def __init__(self, logger: Optional[logging.Logger] = None):
        self.logger = logger or get_logger("generation")
        self._generation_id = 0

    def start_generation(
        self,
        prompt: str,
        generator: str,
        width: int,
        height: int
    ) -> int:
        """Log the start of a generation request."""
        self._generation_id += 1
        self.logger.info(
            f"[Gen #{self._generation_id}] Starting generation | "
            f"generator={generator} | size={width}x{height} | "
            f"prompt=\"{prompt[:50]}{'...' if len(prompt) > 50 else ''}\""
        )
        return self._generation_id

    def generation_success(
        self,
        gen_id: int,
        duration: float,
        cached: bool = False
    ) -> None:
        """Log successful generation."""
        source = "cache" if cached else "API"
        self.logger.info(
            f"[Gen #{gen_id}] Success | source={source} | duration={duration:.2f}s"
        )

    def generation_error(
        self,
        gen_id: int,
        error: Exception,
        attempt: int
    ) -> None:
        """Log generation error."""
        self.logger.warning(
            f"[Gen #{gen_id}] Error on attempt {attempt} | "
            f"error={type(error).__name__}: {str(error)}"
        )

    def generation_failed(
        self,
        gen_id: int,
        error: Exception
    ) -> None:
        """Log final generation failure."""
        self.logger.error(
            f"[Gen #{gen_id}] Failed | "
            f"error={type(error).__name__}: {str(error)}"
        )

    def cache_hit(self, key: str) -> None:
        """Log cache hit."""
        self.logger.debug(f"Cache hit | key={key}")

    def cache_miss(self, key: str) -> None:
        """Log cache miss."""
        self.logger.debug(f"Cache miss | key={key}")

    def rate_limited(self, wait_time: float) -> None:
        """Log rate limiting."""
        self.logger.warning(f"Rate limited | waiting {wait_time:.1f}s")
