# Design Agent

The **Design Agent** is an AI-powered tool that acts as a virtual Game Designer. It analyzes your game's source code to provide professional insights on mechanics, balance, and narrative.

## Features

- **Mechanics Analysis**: Identifies genre, core loops, and rules.
- **Balance Audit**: Evaluates difficulty curves and progression.
- **Narrative Proposal**: Suggests lore, character backstories, and world-building.
- **Mock Mode**: Runs without an API key for testing purposes.

## Usage

### 1. Setup
Make sure you have your API Key ready (Gemini is supported).

```bash
export GEMINI_API_KEY="your_api_key_here"
```

### 2. Run Analysis
Run the agent against your game file (e.g., `index.html`):

```bash
python -m design_agent games/feeding-caiso/index.html
```

### 3. View Report
The agent will generate a Markdown report in the `docs/` folder:

- `docs/{game_name}_design_review.md`

## Configuration
You can customize the agent by editing `design_agent/config.yaml` or setting environment variables:

- `AGENT_MODEL_NAME`: model to use (default: gemini-1.5-flash)
- `AGENT_MAX_TOKENS`: max output tokens
