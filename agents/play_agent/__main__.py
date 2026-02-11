import sys
import os
from pathlib import Path

# Add parent directory to path to allow imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from agents.play_agent.agent import PlayAgent

def main():
    if len(sys.argv) < 2:
        print("Usage: python -m agents.play_agent <path_to_game_file> [--sim]")
        sys.exit(1)

    game_path = sys.argv[1]
    use_sim = "--sim" in sys.argv

    if not os.path.exists(game_path):
        print(f"Error: File not found - {game_path}")
        sys.exit(1)

    mode = "Simulation" if use_sim else "Playwright"
    print(f"Starting Play Agent (Mode: {mode})")

    try:
        agent = PlayAgent()
        report_path = agent.run(game_path, use_simulation=use_sim)
        print(f"\nQA Testing Complete!")
        print(f"Report: {report_path}")
    except Exception as e:
        print(f"\nError: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
