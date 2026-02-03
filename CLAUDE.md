# CAISOGAMES Development Guidelines

## Project Overview
CAISOGAMES is a multi-game platform featuring casual games for children. The platform uses a modular architecture where each game is isolated in its own folder under `games/`.

---

# Game Development Rules (Super Mario Style)

## Graphics Pipeline
- Use the `generate_image_script.py` to create assets.
- All assets must be saved in `./assets/sprites/` or `./assets/backgrounds/`.
- File format: PNG (prefer pixel art style).
- Naming convention: {entity}_{state}_{frame}.png (e.g., mario_walk_01.png).

## Iterative Refinement Process
1. **Drafting:** Generate a base sprite using a prompt (e.g., "16-bit pixel art of a plumber jumping, side view").
2. **Review:** Main agent calls a 'visual-critic' subagent to check if the style matches existing assets.
3. **Editing:** If the style doesn't match, re-run generation with specific feedback (e.g., "increase contrast", "reduce palette to 8 colors").
4. **Integration:** Automatically update the `assets.json` or CSS/JS code to reference the new file path.

## Tools
- `python scripts/process_image.py`: Used for background removal or resizing.
- `python scripts/gen_gif.py`: Used to combine frames into an animated GIF.

---

## Project Structure
```
CAISOGAMES/
├── index.html                    # Main landing page (Xbox-style hub)
├── CLAUDE.md                     # This file - development guidelines
├── assets/
│   ├── sprites/                  # Character and object sprites
│   └── backgrounds/              # Background images
├── scripts/
│   ├── generate_image_script.py  # Image generation script
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
