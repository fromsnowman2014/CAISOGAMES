# Caiso Games AI Agents

This repository contains several AI agents designed to assist with game development. Each agent specializes in a specific domain: Code analysis, Game Design, Image Generation, and Sound Design.

## 🤖 Available Agents

| Agent | Purpose | Usage |
|-------|---------|-------|
| **Code Agent** | Reviews code structure, performance, and mobile compatibility. | `python agents/code_agent/agent.py <game_file>` |
| **Design Agent** | Analyzes game mechanics, balance, and suggests narrative/lore. | `python agents/design_agent/agent.py <game_file>` |
| **Image Agent** | Generates game assets (sprites, backgrounds, UI) using AI. | `python agents/image_agent/cli.py generate --desc "<prompt>"` |
| **Sound Agent** | Audits sound implementation and generates SFX/BGM code. | `python agents/sound_agent/agent.py <game_file>` |
| **Play Agent** | Automated QA testing using Playwright or internal simulation. | `python agents/play_agent/agent.py <game_file>` |

## 🚀 Quick Start

### 1. Configure Environment
Ensure you have the necessary dependencies installed.
```bash
pip install -r requirements.txt
```
*Note: Ensure `playwright`, `Pillow`, and `google-generativeai` are installed.*

### 2. Run an Agent
Navigate to the root directory and run the agent scripts.

#### Code Analysis
```bash
python agents/code_agent/agent.py games/feeding-caiso/index.html
```

#### Design Review
```bash
python agents/design_agent/agent.py games/feeding-caiso/index.html
```

#### Image Generation
```bash
# Generate a sprite
python agents/image_agent/cli.py generate --desc "A cute pixel art cat" --size 64x64 --output assets/cat.png

# See help
python agents/image_agent/cli.py --help
```

#### Sound Audit
```bash
python agents/sound_agent/agent.py games/feeding-caiso/index.html
```

#### Play Testing
```bash
python agents/play_agent/agent.py games/feeding-caiso/index.html
```

## 🛠️ IDE Integration

### VS Code / Cursor
This repository includes a `.vscode/tasks.json` file. You can run agents directly from your editor:
1. Press `Cmd+Shift+P` (macOS) or `Ctrl+Shift+P` (Windows/Linux).
2. Type `Run Task`.
3. Select `Agent: Audit Code`, `Agent: Generate Asset`, etc.

### Cursor AI Rules
The `.cursorrules` file in the root directory helps Cursor AI understand these agents. You can ask Cursor:
- "Run a design review on this game."
- "Generate a sprite for the player."
- "Audit the sound implementation."

## 📂 Output
Agents typically generate reports in the `docs/` or specific game documentation directories.
- Code Agent: `docs/<game>_code_review.md`
- Design Agent: `docs/<game>_design_review.md`
- Play Agent: `docs/<game>_qa_report.md`
- Sound Agent: `docs/<game>_sound_audit.md`
