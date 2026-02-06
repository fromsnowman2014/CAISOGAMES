"""
Entry point for running image_agent as a module

Usage:
    python -m image_agent generate --desc "cute apple" --style kawaii
    python -m image_agent review --image sprite.png
    python -m image_agent info
"""

from agents.image_agent.cli import main

if __name__ == '__main__':
    main()
