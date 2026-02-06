import sys
import os
from pathlib import Path

# Add parent directory to path to allow imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from agents.design_agent.agent import DesignAgent

def main():
    if len(sys.argv) < 2:
        print("Usage: python -m design_agent <path_to_game_file>")
        sys.exit(1)
        
    game_path = sys.argv[1]
    if not os.path.exists(game_path):
        print(f"Error: File not found - {game_path}")
        sys.exit(1)

    print(f"🚀 Starting Design Agent using {os.environ.get('AGENT_MODEL_NAME', 'Gemini')}")
    
    try:
        agent = DesignAgent()
        report_path = agent.analyze(game_path)
        print(f"\n✨ Analysis Complete!")
        print(f"📄 Report: {report_path}")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
