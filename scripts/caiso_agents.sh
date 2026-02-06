#!/bin/bash

# Caiso Games Agent Runner
# Usage: ./scripts/caiso_agents.sh <agent_name> [args...]

AGENT=$1
shift # Remove agent name from args

case "$AGENT" in
  "code")
    echo "🕵️‍♀️ Running Code Agent..."
    python3 agents/code_agent/agent.py "$@"
    ;;
  "design")
    echo "🎨 Running Design Agent..."
    python3 agents/design_agent/agent.py "$@"
    ;;
  "image")
    echo "🖼️ Running Image Agent..."
    python3 agents/image_agent/cli.py "$@"
    ;;
  "sound")
    echo "🔊 Running Sound Agent..."
    python3 agents/sound_agent/agent.py "$@"
    ;;
  "play")
    echo "🎮 Running Play Agent..."
    python3 agents/play_agent/agent.py "$@"
    ;;
  *)
    echo "Usage: $0 {code|design|image|sound|play} [arguments]"
    echo "Example: $0 image generate --desc 'pixel art cat'"
    exit 1
    ;;
esac
