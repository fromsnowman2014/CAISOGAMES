"""
CAISOGAMES Agents Package

This package contains modular AI agents for game development automation.

Available Agents:
- design_agent: Analyzes game code for mechanics, balance, and narrative.
- image_agent: Generates game assets using AI image APIs.
"""

from agents.design_agent import DesignAgent
# from agents.image_agent import ImageAgent  # Uncomment when needed

__all__ = [
    "DesignAgent",
    # "ImageAgent",
]
