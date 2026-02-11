# Feeding Caiso Phase 5: Ethereal Evolution

## Overview

Phase 5 transforms Feeding Caiso from a "Neon Kawaii" arcade game into a "Zen/Ethereal" experience with a 10-stage day/night cycle, environmental physics, and regenerated art assets.

**Current State**: The v5.0 codebase has been fully refactored. All systems (StageManager, Environment, LightingSystem) are integrated and functional. All old assets have been removed. This phase focuses on generating new art and polishing the gameplay loop.

---

## Design Direction

### Inspiration
- **Donut County**: Clean vector art, pastel palettes, physics-driven
- **Alto's Odyssey**: Gradient-heavy, weather effects, flow-state gameplay
- **Cats & Soup**: Cozy/healing mobile trend

### Art Style Target
- Soft vector art with gradient shading
- Dynamic color palettes that shift with each stage
- Organic lighting overlays (dawn tint, golden hour, moonlight)
- Glassmorphism UI (already implemented in CSS)

---

## Current Architecture (v5.0)

```
src/
├── config/
│   └── Stages.js              # 10-stage configs (atmosphere, hazards, colors)
├── core/
│   ├── Game.js                 # Main game loop, state machine, entity orchestration
│   ├── Audio.js                # AudioManager (Web Audio API)
│   ├── Input.js                # VirtualJoystick (touch + mouse)
│   ├── StageManager.js         # Stage transitions, hazard spawning
│   └── Environment.js          # Wind, gravity, background color per stage
├── entities/
│   ├── Caiso.js                # Main character (4 expressions, evolution tiers)
│   ├── Player.js               # Player avatar (joystick-controlled)
│   ├── Villager.js             # NPCs that get consumed
│   ├── Food.js                 # Thrown food projectiles (arc trajectory + wind)
│   └── Hazard.js               # Stage hazards (leaf, star, shadow, etc.)
├── managers/
│   ├── AssetManager.js         # Image loading pipeline
│   └── UIManager.js            # DOM-based HUD (glassmorphism overlay)
├── systems/
│   └── LightingSystem.js       # Full-screen color overlay per stage
├── utils/
│   ├── Constants.js            # GAME_CONFIG, FOODS, EVOLUTION_TIERS, FEVER_CONFIG
│   ├── FeverMode.js            # Fever gauge, multiplier, particles
│   ├── Juice.js                # ScreenShake, ImpactFrame
│   ├── ParallaxBackground.js   # 3-layer scrolling (clouds, city, ground)
│   └── SquashStretch.js        # Spring-based animation
└── generated/
    └── SoundLibrary.js         # Web Audio procedural SFX
```

### Key Data Flows
- **Stage Progression**: `Game.level` increments -> `StageManager.update()` detects level > current stage -> calls `loadStage()` -> updates `Environment` (wind/gravity/color) + `LightingSystem` (overlay)
- **Food Physics**: `Food.update()` reads `environment.windX` and `environment.gravityY` to modify arc trajectory
- **Hazard Spawning**: `StageManager.update()` spawns `Hazard` entities based on `currentConfig.hazards[]`
- **UI Updates**: `UIManager.update()` reads game state and diffs against cached values to minimize DOM touches

---

## 10-Stage Progression

Stages are defined in `src/config/Stages.js`. Each stage = 1 game level.

| # | Name | Theme | Background | Wind | Gravity | Hazards |
|---|------|-------|------------|------|---------|---------|
| 1 | Morning Dew | Dawn | `#E0F7FA` | 0 | 1.0 | none |
| 2 | Sunlit Bloom | Morning | `#FFF8E1` | 0 | 1.0 | bee |
| 3 | Whispering Breeze | Noon | `#B3E5FC` | 2.5 | 1.0 | wind_gust |
| 4 | Golden Harvest | Afternoon | `#FFE0B2` | 0.5 | 1.0 | leaf |
| 5 | Crimson Sunset | Sunset | `#FFCCBC` | -0.5 | 0.9 | none |
| 6 | Twilight Grove | Dusk | `#9FA8DA` | 0 | 1.0 | shadow |
| 7 | Moonlit Lake | Night | `#283593` | 0 | 1.0 | ripple |
| 8 | Starry Expanse | Midnight | `#1A237E` | 0 | 0.8 | star |
| 9 | Aurora Borealis | Deep Night | `#311B92` | 5.0 | 0.7 | magnetic_field |
| 10 | Cosmic Dawn | Void | `#000000` | 0 | 0.5 | void |

---

## Asset Requirements

All assets were removed and need regeneration. The code expects these exact keys in `AssetManager.js`:

### Sprites (`assets/sprites/`)

| Key | Path | Description | Size |
|-----|------|-------------|------|
| `caiso_idle` | `caiso/caiso_idle.png` | Default resting state | 256x256 |
| `caiso_hungry` | `caiso/caiso_hungry.png` | Open mouth, wanting food | 256x256 |
| `caiso_happy` | `caiso/caiso_happy.png` | After eating, satisfied | 256x256 |
| `caiso_sad` | `caiso/caiso_sad.png` | After consuming villager | 256x256 |
| `player_idle` | `player/player_throwing.png` | Player character | 128x160 |
| `villager_normal` | `villagers/villager_normal.png` | Walking villager | 64x64 |
| `villager_scared` | `villagers/villager_scared.png` | Fleeing villager | 64x64 |

### Food Items (`assets/items/`)

| Key | Path | Description | Size |
|-----|------|-------------|------|
| `food_apple` | `food_apple.png` | Level 1 basic food | 64x64 |
| `food_burger` | `food_burger.png` | Level 2 unlock | 64x64 |
| `food_pizza` | `food_pizza.png` | Level 3 unlock | 64x64 |
| `food_dorito` | `food_dorito.png` | Level 4 unlock (light, fast) | 64x64 |
| `food_watermelon` | `food_watermelon.png` | Level 5 unlock (heavy) | 64x64 |
| `food_dynamite` | `food_dynamite.png` | Level 7 unlock (most powerful) | 64x64 |

### Backgrounds (`assets/backgrounds/`)

| Key | Path | Description | Size |
|-----|------|-------------|------|
| `bg_sky` | `bg_sky.png` | Sky layer (tinted by Environment) | 960x300 |
| `bg_clouds` | `bg_clouds.png` | Cloud parallax layer (0.15x speed) | 960x150 |
| `bg_city` | `bg_city.png` | Midground parallax (0.3x speed) | 960x250 |
| `bg_ground` | `bg_ground.png` | Ground parallax (0.6x speed) | 960x304 |

### UI (`assets/ui/`)

| Key | Path | Description | Size |
|-----|------|-------------|------|
| `title_background` | `title_background.png` | Menu screen background | 480x854 |
| `ui_button_feed` | `ui_button_feed.png` | Feed button sprite | 128x128 |
| `card_thumbnail` | `card_thumbnail.png` | Hub page game card | 300x200 |
| `featured_banner` | `featured_banner.png` | Hub page featured banner | 800x400 |

---

## Art Generation Prompts

Use the CAISOGAMES image generator (`python scripts/generate_asset.py`) or the Vercel API proxy.

### Style Directive
> "Soft vector art, minimalist, gradient shading, organic lighting, nature-inspired palette, mobile game asset, transparent background for sprites"

### Sprite Prompts

```
caiso_idle:    "cute round spirit creature, soft purple/lavender, large gentle eyes, peaceful expression, floating, soft glow, zen aesthetic, transparent background"
caiso_hungry:  "cute round spirit creature, soft purple, wide open mouth, eager expression, slight lean forward, glowing, transparent background"
caiso_happy:   "cute round spirit creature, soft purple, closed happy eyes, satisfied smile, slight sparkle, content expression, transparent background"
caiso_sad:     "cute round spirit creature, soft purple, droopy eyes, guilty expression, slight blue tint, transparent background"
player_idle:   "small human character, nature keeper outfit, earth tones, holding glowing orb, side view, transparent background"
villager_normal: "tiny wandering wisp, soft blue-white glow, orb shape with trailing light, calm, transparent background"
villager_scared: "tiny wandering wisp, orange-red glow, faster trailing particles, alarmed, transparent background"
```

### Food Prompts
```
food_apple:      "glowing red nature essence orb, apple shape, soft light, transparent background, 64x64"
food_burger:     "warm amber essence, layered circular shape, golden glow, transparent background, 64x64"
food_pizza:      "golden triangle essence, warm tones, soft sparkle, transparent background, 64x64"
food_dorito:     "light purple crystal shard, floating, ethereal glow, transparent background, 64x64"
food_watermelon: "green and pink nature orb, crescent shape, fresh glow, transparent background, 64x64"
food_dynamite:   "intense red-orange energy core, pulsing, powerful glow, transparent background, 64x64"
```

### Background Prompts
```
bg_sky:     "ethereal gradient sky, soft teal to pale gold, minimalist, no objects, seamless tileable, 960x300"
bg_clouds:  "soft wispy clouds, translucent, watercolor style, horizontal strip, seamless tileable, 960x150"
bg_city:    "distant ethereal landscape silhouette, soft mountains or forest, muted tones, seamless tileable, 960x250"
bg_ground:  "natural ground layer, soft grass or earth, zen garden feel, seamless tileable, 960x304"
```

---

## Remaining Work

### Completed (v5.0 Refactor)
- [x] StageManager integrated with Game.js
- [x] Environment system (wind, gravity, background color)
- [x] LightingSystem (per-stage overlay tinting)
- [x] 10-stage config in Stages.js
- [x] Hazard entity with physics
- [x] Food physics respects wind/gravity
- [x] Villager physics respects wind
- [x] UIManager DOM overlay (glassmorphism CSS)
- [x] Food selector shows all 6 items
- [x] FeverMode with gaugeMax and scoreMultiplier
- [x] Constants centralized (no magic numbers)
- [x] Old assets removed

### TODO
- [ ] **Generate all art assets** (sprites, items, backgrounds, UI)
- [ ] **Unique evolution sprites** per tier (currently all use `caiso_idle`)
- [ ] **Stage transition animations** (fade between stages)
- [ ] **Per-stage backgrounds** (currently using single set for all stages)
- [ ] **Sound redesign** (current SoundLibrary is arcade-style, needs zen/ethereal SFX)
- [ ] **Balance tuning** via play_agent (spawn rates, wind speeds, hunger reduction values)
- [ ] **Hub page integration** (update card thumbnail and banner for new art style)
