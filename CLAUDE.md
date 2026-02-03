# CAISOGAMES Development Guidelines

## Project Overview
CAISOGAMES is a multi-game platform featuring casual games for children. The platform uses a modular architecture where each game is isolated in its own folder under `games/`.

---

# Game Development Rules (Super Mario Style)

## Graphics Pipeline

### AI Image Generation (via Vercel Proxy)

Since Claude Code environment cannot directly access Google APIs, we use a Vercel proxy:

```
[Claude Code] --> [Vercel API: /api/generate-image] --> [Gemini API]
                         (GEMINI_API_KEY stored here)
```

**Setup for Development:**
```bash
# Set the Vercel app URL for image generation
export VERCEL_APP_URL=https://caisogames.vercel.app

# Or use mock generator for testing without API
export USE_MOCK_GENERATOR=true
```

**Generate Assets:**
```bash
# Generate a sprite
python scripts/generate_asset.py sprite "cute pixel art monster" monster_idle

# Generate a background
python scripts/generate_asset.py background "fantasy forest" forest_day

# With custom size
python scripts/generate_asset.py sprite "dragon character" dragon --size 128x128
```

**Python API:**
```python
from image_generator import ImageGeneratorService
import asyncio

async def generate():
    service = ImageGeneratorService()  # Auto-detects VERCEL_APP_URL
    image = await service.generate("pixel art slime monster")
    image.save("assets/sprites/slime.png")

asyncio.run(generate())
```

### Asset Requirements
- All assets saved in `./assets/sprites/` or `./assets/backgrounds/`
- File format: PNG (transparent background for sprites)
- Naming convention: `{entity}_{state}_{frame}.png` (e.g., `mario_walk_01.png`)

## Iterative Refinement Process
1. **Drafting:** Generate a base sprite using a prompt (e.g., "16-bit pixel art of a plumber jumping, side view").
2. **Review:** Check if the style matches existing assets.
3. **Editing:** If the style doesn't match, re-run generation with specific feedback (e.g., "increase contrast", "reduce palette to 8 colors").
4. **Integration:** Save to assets folder and reference in game code.

## Tools
- `python scripts/generate_asset.py`: AI image generation (sprites, backgrounds)
- `python scripts/process_image.py`: Image processing (resize, bg removal)
- `python scripts/gen_gif.py`: Combine frames into animated GIF

---

## Project Structure
```
CAISOGAMES/
├── index.html                    # Main landing page (Xbox-style hub)
├── CLAUDE.md                     # This file - development guidelines
├── api/
│   └── generate-image.py         # Vercel serverless function (image proxy)
├── assets/
│   ├── sprites/                  # Character and object sprites
│   └── backgrounds/              # Background images
├── image_generator/              # Python package for AI image generation
│   ├── generators/               # Generator backends (Gemini, Mock, Vercel)
│   ├── processors/               # Image processing utilities
│   └── utils/                    # Caching, logging, retry logic
├── scripts/
│   ├── generate_asset.py         # CLI for generating game assets
│   ├── process_image.py          # Image processing (resize, bg removal)
│   └── gen_gif.py                # GIF animation generator
├── games/
│   ├── feeding-caiso/            # Feeding Caiso game (standalone)
│   │   └── index.html
│   └── [new-game]/               # Future games go here
├── docs/
│   ├── PRD.md
│   ├── TECHNICAL_DESIGN.md
│   ├── INTERFACE_DESIGN.md
│   └── PLATFORM_ARCHITECTURE.md
├── vercel.json
└── package.json
```

## Game Development Workflow

### Adding a New Game
1. Create folder: `games/[game-name]/`
2. Create standalone `index.html` with all game logic
3. Add "Back to Hub" button linking to `../../`
4. Update landing page `index.html`:
   - Add game card to grid
   - Create inline SVG thumbnail
5. Generate assets using graphics pipeline
6. Test navigation both ways

### Asset Naming Conventions
| Type | Pattern | Example |
|------|---------|---------|
| Sprite | `{character}_{action}_{frame}.png` | `caiso_eat_01.png` |
| Background | `{scene}_{variant}.png` | `village_day.png` |
| UI Element | `ui_{element}_{state}.png` | `ui_button_hover.png` |
| Animation | `{character}_{action}.gif` | `villager_walk.gif` |

## Code Style

### HTML/CSS/JS
- Single-file games preferred (all in one `index.html`)
- Use CSS custom properties for theming
- Inline SVG for small graphics
- External PNG/GIF for complex sprites

### Game Architecture
- Each game is completely standalone
- No shared dependencies between games
- Games should work offline after load
- Mobile touch support required

## Quality Checklist
- [ ] Game loads in < 2 seconds
- [ ] 60 FPS target on mid-range devices
- [ ] Touch controls work on mobile
- [ ] Back to Hub navigation works
- [ ] Assets follow naming convention
- [ ] No console errors
