# CAISOGAMES Agents

This directory contains modular AI agents for game development automation.

## Available Agents

| Agent | Description | Status |
|-------|-------------|--------|
| **design_agent** | Analyzes game code for mechanics, balance, and narrative | ✅ Ready |
| **image_agent** | Generates game assets using AI image APIs | ✅ Ready |

## Usage

### Design Agent
```bash
python -m agents.design_agent games/your-game/index.html
```

### Image Agent
```bash
python -m agents.image_agent --prompt "cute monster" --style kawaii
```

## Architecture

```
agents/
├── __init__.py           # Package init
├── README.md             # This file
├── design_agent/         # Game design analysis agent
│   ├── agent.py          # Core logic
│   ├── prompts/          # LLM prompt templates
│   └── utils/            # Utilities (LLM client)
└── image_agent/          # Image generation agent
    ├── core/             # Core classes
    ├── prompts/          # Prompt generation
    ├── reviewers/        # Quality review
    └── utils/            # Utilities
```

## Future Agents (Planned)
- **play_agent**: Automated gameplay testing via Playwright
- **sound_agent**: Audio generation and integration
- **code_agent**: Code improvement suggestions
- **review_agent**: Quality and UX review
