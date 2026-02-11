"""
Run CAISOGAMES agents pipeline on a game file.

Usage:
    python -m agents <game_path> [--agents design,code,sound,play]

Examples:
    python -m agents games/feeding-caiso/index.html
    python -m agents games/caiso-mario/index.html --agents design,code
"""

import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.shared.pipeline import AgentPipeline
from agents.design_agent.agent import DesignAgent
from agents.code_agent.agent import CodeAgent
from agents.sound_agent.agent import SoundAgent
from agents.play_agent.agent import PlayAgent

AGENT_MAP = {
    "design": DesignAgent,
    "code": CodeAgent,
    "sound": SoundAgent,
    "play": PlayAgent,
}


def main():
    parser = argparse.ArgumentParser(description="Run CAISOGAMES agents pipeline")
    parser.add_argument("game_path", help="Path to game index.html")
    parser.add_argument(
        "--agents",
        default="design,code,sound",
        help="Comma-separated agent names: design,code,sound,play (default: design,code,sound)",
    )
    args = parser.parse_args()

    if not Path(args.game_path).exists():
        print(f"Error: File not found - {args.game_path}")
        sys.exit(1)

    pipeline = AgentPipeline()
    agent_names = [n.strip() for n in args.agents.split(",")]

    for name in agent_names:
        if name in AGENT_MAP:
            pipeline.add(name, AGENT_MAP[name])
        else:
            print(f"Warning: Unknown agent '{name}'. Available: {', '.join(AGENT_MAP)}")

    if not pipeline.steps:
        print("Error: No valid agents specified.")
        sys.exit(1)

    print(f"CAISOGAMES Agent Pipeline")
    print(f"Game: {args.game_path}")
    print(f"Agents: {', '.join(agent_names)}")

    results = pipeline.run(args.game_path)

    print(f"\n{'='*50}")
    print(f"  PIPELINE COMPLETE ({results.total_time:.1f}s)")
    print(f"{'='*50}")
    for step in results.steps:
        status = "OK" if step["status"] == "success" else "FAIL"
        print(f"  [{status}] {step['agent']:>8s} ({step['time']:.1f}s)", end="")
        if step["status"] == "success":
            print(f" -> {step['report']}")
        else:
            print(f" : {step.get('error', 'Unknown error')}")


if __name__ == "__main__":
    main()
