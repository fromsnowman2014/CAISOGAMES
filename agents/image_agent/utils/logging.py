"""
Logging utilities for Image Agent

Provides structured logging with iteration tracking
"""

import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional


class AgentLogger:
    """
    Custom logger for Image Agent with iteration tracking
    """

    def __init__(
        self,
        name: str = "image_agent",
        level: str = "INFO",
        log_file: Optional[Path] = None
    ):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, level.upper()))

        # Clear existing handlers
        self.logger.handlers = []

        # Console handler with colored output
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(self._get_formatter())
        self.logger.addHandler(console_handler)

        # File handler if specified
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(self._get_formatter(include_time=True))
            self.logger.addHandler(file_handler)

        self.current_iteration = 0
        self.request_id = ""

    def _get_formatter(self, include_time: bool = False) -> logging.Formatter:
        """Get log formatter"""
        if include_time:
            fmt = "%(asctime)s | %(levelname)s | %(message)s"
        else:
            fmt = "%(levelname)s | %(message)s"
        return logging.Formatter(fmt, datefmt="%Y-%m-%d %H:%M:%S")

    def set_iteration(self, iteration: int):
        """Set current iteration for context"""
        self.current_iteration = iteration

    def set_request(self, request_id: str):
        """Set current request ID for context"""
        self.request_id = request_id

    def _format_message(self, message: str) -> str:
        """Add iteration context to message"""
        prefix = ""
        if self.request_id:
            prefix += f"[{self.request_id[:8]}] "
        if self.current_iteration > 0:
            prefix += f"[Iter {self.current_iteration}] "
        return prefix + message

    def info(self, message: str):
        """Log info message"""
        self.logger.info(self._format_message(message))

    def debug(self, message: str):
        """Log debug message"""
        self.logger.debug(self._format_message(message))

    def warning(self, message: str):
        """Log warning message"""
        self.logger.warning(self._format_message(message))

    def error(self, message: str):
        """Log error message"""
        self.logger.error(self._format_message(message))

    def iteration_start(self, iteration: int, prompt_version: int):
        """Log start of an iteration"""
        self.set_iteration(iteration)
        self.info(f"Starting iteration (prompt v{prompt_version})")

    def iteration_end(self, score: float, passed: bool):
        """Log end of an iteration"""
        status = "PASSED" if passed else "FAILED"
        self.info(f"Iteration complete: {score*100:.1f}% [{status}]")

    def generation_start(self):
        """Log start of image generation"""
        self.debug("Generating image...")

    def generation_complete(self, time_taken: float):
        """Log completion of image generation"""
        self.debug(f"Image generated in {time_taken:.2f}s")

    def review_start(self):
        """Log start of quality review"""
        self.debug("Starting quality review...")

    def review_complete(self, scores: dict):
        """Log completion of quality review"""
        scores_str = ", ".join([f"{k}: {v*100:.0f}%" for k, v in scores.items()])
        self.debug(f"Review complete: {scores_str}")

    def improvement_applied(self, areas: list):
        """Log prompt improvement"""
        self.info(f"Improving prompt for: {', '.join(areas)}")

    def final_result(self, success: bool, score: float, iterations: int, time: float):
        """Log final result"""
        status = "SUCCESS" if success else "BEST EFFORT"
        self.info(f"Final result [{status}]: {score*100:.1f}% after {iterations} iterations ({time:.2f}s)")


# Global logger instance
_logger: Optional[AgentLogger] = None


def setup_logging(
    level: str = "INFO",
    log_file: Optional[Path] = None
) -> AgentLogger:
    """
    Setup and return the global logger

    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR)
        log_file: Optional file path for log output

    Returns:
        Configured AgentLogger instance
    """
    global _logger
    _logger = AgentLogger(level=level, log_file=log_file)
    return _logger


def get_logger() -> AgentLogger:
    """
    Get the global logger instance

    Creates a default logger if not yet initialized
    """
    global _logger
    if _logger is None:
        _logger = AgentLogger()
    return _logger
