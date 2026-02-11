import sys
import os
from pathlib import Path

# Add parent directory to path to allow imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from agents.code_agent.agent import CodeAgent

def main():
    if len(sys.argv) < 2:
        print("Usage: python -m agents.code_agent <path_to_game_file>")
        sys.exit(1)

    game_path = sys.argv[1]
    if not os.path.exists(game_path):
        print(f"Error: File not found - {game_path}")
        sys.exit(1)

    print(f"Starting Code Agent (API: {os.environ.get('VERCEL_APP_URL', 'https://caisogames.vercel.app')})")

    try:
        agent = CodeAgent()
        report_path = agent.analyze(game_path)
        print(f"\nAnalysis Complete!")
        print(f"Report: {report_path}")
    except Exception as e:
        print(f"\nError: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
