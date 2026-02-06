# Sound Agent

AI-powered game sound analysis and generation.

## Features

- **Sound Audit**: Analyze existing audio implementation
- **Requirements**: Define needed sounds based on game events
- **SFX Generation**: Create Web Audio API code for effects
- **BGM Generation**: Create Tone.js code for music
- **Integration**: Ready-to-use JavaScript snippets

## Usage

### CLI

```bash
python -m agents.sound_agent games/feeding-caiso/index.html
```

### Python API

```python
from agents.sound_agent import SoundAgent

agent = SoundAgent()

# Full analysis
report_path = agent.analyze("games/my-game/index.html")

# Individual steps
audit = agent.audit_sounds("games/my-game/index.html")
requirements = agent.define_requirements("games/my-game/index.html", audit)
sfx_code = agent.generate_sfx_code(requirements[0])
bgm_code = agent.generate_bgm_code("gameplay", "ingame", "energetic", 120)
```

## Sound Categories

| Category | Examples |
|----------|----------|
| 🔊 UI | button_click, menu_open, select |
| 💥 Gameplay | collision, jump, item_pickup, attack |
| 🎵 BGM | menu_theme, gameplay_loop, game_over |
| 📣 Feedback | success, failure, combo, level_up |

## Output

The agent generates:
1. `{game}_sound_audit.md` - Analysis report
2. Web Audio API JavaScript snippets
3. Tone.js BGM code templates

## Configuration

Edit `config.yaml` for custom settings:
- Sound categories
- Default durations
- Tempo settings
- Output directory
