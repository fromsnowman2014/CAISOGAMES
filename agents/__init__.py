"""
CAISOGAMES Agents Package

This package contains modular AI agents for game development automation.

Available Agents:
- design_agent: Analyzes game code for mechanics, balance, and narrative.
- code_agent: Analyzes code structure, performance, and mobile support.
- sound_agent: Audits and generates game audio (SFX/BGM).
- play_agent: Automated gameplay testing and QA.
- image_agent: Generates game assets using AI image APIs.
"""

from agents.design_agent.agent import DesignAgent
from agents.code_agent.agent import CodeAgent
from agents.sound_agent.agent import SoundAgent
from agents.play_agent.agent import PlayAgent

__all__ = [
    "DesignAgent",
    "CodeAgent",
    "SoundAgent",
    "PlayAgent",
]
