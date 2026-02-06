"""
Sound Agent CLI Entry Point
Run with: python -m agents.sound_agent <game_path>
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agents.sound_agent.agent import SoundAgent


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m agents.sound_agent <path_to_game_file>")
        print()
        print("Example:")
        print("  python -m agents.sound_agent games/feeding-caiso/index.html")
        sys.exit(1)
    
    game_path = sys.argv[1]
    
    if not os.path.exists(game_path):
        print(f"Error: File not found - {game_path}")
        sys.exit(1)
    
    print("🎧 Starting Sound Agent")
    
    # Check for API key
    if not os.environ.get("GEMINI_API_KEY"):
        print("⚠️ Warning: GEMINI_API_KEY not found. Using Mock LLM mode.")
    
    print()
    
    try:
        agent = SoundAgent()
        report_path = agent.analyze(game_path)
        print()
        print("✨ Analysis Complete!")
        print(f"📄 Report: {report_path}")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
