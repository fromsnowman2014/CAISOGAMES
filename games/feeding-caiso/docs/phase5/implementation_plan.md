# Phase 5 Implementation Plan

## Current State

The v5.0 refactor is complete. The codebase is modular and all Phase 5 systems are scaffolded and integrated:

| System | File | Status | Notes |
|--------|------|--------|-------|
| Stage Config | `src/config/Stages.js` | Done | 10 stages with atmosphere, hazards, colors |
| Stage Manager | `src/core/StageManager.js` | Done | Auto-advances by level, spawns hazards |
| Environment | `src/core/Environment.js` | Done | Wind, gravity, background color per stage |
| Lighting | `src/systems/LightingSystem.js` | Done | Overlay color tinting per stage |
| Hazards | `src/entities/Hazard.js` | Done | Physics-aware, wind/gravity affected |
| Food Physics | `src/entities/Food.js` | Done | Arc trajectory with wind drift + gravity |
| UI Overlay | `src/managers/UIManager.js` | Done | Glassmorphism HUD, all 6 foods shown |
| Constants | `src/utils/Constants.js` | Done | Centralized config, no magic numbers |
| Assets | `src/managers/AssetManager.js` | Done | Clean manifest, all keys aligned |

**All old assets have been removed.** Directory structure is preserved and ready for new art.

---

## Step 1: Asset Generation (Priority: HIGH)

The game runs with canvas fallbacks (colored circles/rectangles) when assets are missing, so it's playable but needs art.

### 1.1 Sprites (7 files)

Generate using `python scripts/generate_asset.py sprite "<prompt>" <name>`:

```bash
# Caiso expressions (256x256, transparent background)
python scripts/generate_asset.py sprite "cute round spirit creature, soft purple lavender, large gentle eyes, peaceful, floating, soft glow, zen aesthetic" caiso_idle --size 256x256
python scripts/generate_asset.py sprite "cute round spirit creature, soft purple, wide open mouth, eager expression, glowing" caiso_hungry --size 256x256
python scripts/generate_asset.py sprite "cute round spirit creature, soft purple, closed happy eyes, satisfied smile, sparkle" caiso_happy --size 256x256
python scripts/generate_asset.py sprite "cute round spirit creature, soft purple, droopy eyes, guilty expression, blue tint" caiso_sad --size 256x256

# Player (128x160)
python scripts/generate_asset.py sprite "small nature keeper character, earth tones, holding glowing orb, side view" player_throwing --size 128x160

# Villagers (64x64)
python scripts/generate_asset.py sprite "tiny wandering wisp, soft blue-white glow, orb with trailing light, calm" villager_normal --size 64x64
python scripts/generate_asset.py sprite "tiny wandering wisp, orange-red glow, fast trailing particles, alarmed" villager_scared --size 64x64
```

**Output paths** (move after generation):
```
assets/sprites/caiso/caiso_idle.png
assets/sprites/caiso/caiso_hungry.png
assets/sprites/caiso/caiso_happy.png
assets/sprites/caiso/caiso_sad.png
assets/sprites/player/player_throwing.png
assets/sprites/villagers/villager_normal.png
assets/sprites/villagers/villager_scared.png
```

### 1.2 Food Items (6 files)

```bash
# All 64x64, transparent background
python scripts/generate_asset.py sprite "glowing red nature essence orb, apple shape, soft light" food_apple --size 64x64
python scripts/generate_asset.py sprite "warm amber essence, layered circular, golden glow" food_burger --size 64x64
python scripts/generate_asset.py sprite "golden triangle essence, warm tones, soft sparkle" food_pizza --size 64x64
python scripts/generate_asset.py sprite "light purple crystal shard, floating, ethereal glow" food_dorito --size 64x64
python scripts/generate_asset.py sprite "green and pink nature orb, crescent shape, fresh glow" food_watermelon --size 64x64
python scripts/generate_asset.py sprite "intense red-orange energy core, pulsing, powerful glow" food_dynamite --size 64x64
```

**Output**: `assets/items/food_*.png`

### 1.3 Backgrounds (4 files)

```bash
# Seamless tileable, horizontal strips
python scripts/generate_asset.py background "ethereal gradient sky, soft teal to pale gold, minimalist, seamless" bg_sky --size 960x300
python scripts/generate_asset.py background "soft wispy clouds, translucent, watercolor, horizontal strip, seamless" bg_clouds --size 960x150
python scripts/generate_asset.py background "distant ethereal landscape silhouette, soft mountains, muted tones, seamless" bg_city --size 960x250
python scripts/generate_asset.py background "natural ground layer, soft grass, zen garden feel, seamless" bg_ground --size 960x304
```

**Output**: `assets/backgrounds/bg_*.png`

### 1.4 UI (4 files)

```bash
python scripts/generate_asset.py background "ethereal nature scene, soft purple and teal gradients, zen, feeding game title screen" title_background --size 480x854
python scripts/generate_asset.py sprite "glowing feed button, circular, soft purple, nature energy" ui_button_feed --size 128x128
python scripts/generate_asset.py background "ethereal spirit creature feeding game, card thumbnail" card_thumbnail --size 300x200
python scripts/generate_asset.py background "ethereal spirit creature feeding game, featured banner, wide" featured_banner --size 800x400
```

**Output**: `assets/ui/*.png`

**Total**: 21 assets to generate.

---

## Step 2: Evolution Sprite Variants (Priority: MEDIUM)

Currently all 4 evolution tiers reference `caiso_idle`. Each tier should have a unique appearance.

### Changes Required

1. Generate 4 evolution sprites:
   - `caiso_baby.png` (smaller, simpler, fewer details)
   - `caiso_teen.png` (standard size, more defined)
   - `caiso_adult.png` (larger, more ornate, glowing aura)
   - `caiso_king.png` (largest, crown/halo, strong glow, particle trails)

2. Update `Constants.js` EVOLUTION_TIERS:
   ```js
   { level: 1,  name: 'Baby Caiso',  scale: 0.8, sprite: 'caiso_baby' },
   { level: 3,  name: 'Teen Caiso',  scale: 1.0, sprite: 'caiso_teen' },
   { level: 6,  name: 'Adult Caiso', scale: 1.2, sprite: 'caiso_adult' },
   { level: 10, name: 'King Caiso',  scale: 1.5, sprite: 'caiso_king' }
   ```

3. Add 4 entries to `AssetManager.js` asset list.

4. Update `Caiso.js` draw method to use `tier.sprite` instead of hardcoded expression sprites.

---

## Step 3: Sound Redesign (Priority: MEDIUM)

Current `SoundLibrary.js` has arcade-style procedural sounds. Phase 5 needs zen/ethereal tones.

### Sound Mapping

| Key | Current Style | Target Style |
|-----|--------------|-------------|
| `throw` | Retro triangle pitch slide | Soft whoosh, wind chime |
| `eat` | Happy chop sine burst | Gentle absorption, crystalline |
| `combo` | Arpeggio square wave | Harmonic bells, ascending |
| `fever` | Power-up glissando | Ethereal choir swell |
| `gameover` | Pitch-down sawtooth | Gentle fade, minor key |
| `levelup` | C-E-G-C fanfare | Wind chime cascade |

### Implementation
- Use `sound_agent` to generate new Web Audio API code:
  ```bash
  python -m agents.sound_agent games/feeding-caiso/index.html
  ```
- Replace `src/generated/SoundLibrary.js` with output.

---

## Step 4: Stage-Specific Backgrounds (Priority: LOW)

Currently all stages use the same parallax layers. For full Phase 5 vision, each stage could have unique backgrounds.

### Approach
- Add `backgroundKey` field to each stage in `Stages.js`
- Load per-stage background sets in AssetManager
- Update ParallaxBackground to swap layers on stage change

### Required Assets (if implemented)
- 10 sets x 3 layers = 30 additional background images
- Consider: Start with 3 sets (Dawn, Day, Night) and interpolate

---

## Step 5: Balance Tuning (Priority: LOW)

Use `play_agent` for automated gameplay testing:

```bash
python -m agents.play_agent games/feeding-caiso/index.html --sim
```

### Parameters to Tune

| Parameter | Location | Current | Notes |
|-----------|----------|---------|-------|
| `VILLAGER_CONSUME_INTERVAL` | Constants.js | 4000ms | Base eat speed |
| `HUNGER_PER_LEVEL` | Constants.js | 4 | Hunger reduced per level |
| `COMBO_TIMEOUT` | Constants.js | 2000ms | Combo window |
| `FEVER_CONFIG.duration` | Constants.js | 8000ms | Fever mode length |
| `FEVER_CONFIG.gaugeMax` | Constants.js | 100 | Charge needed for fever |
| `FEVER_CONFIG.scoreMultiplier` | Constants.js | 2.0 | Fever damage boost |
| Food `hungerReduction` | Constants.js | 8-40 | Per-food effectiveness |
| Food `unlockLevel` | Constants.js | 1-7 | When foods appear |
| Stage `windX` | Stages.js | 0-5.0 | Wind force per stage |
| Stage `gravityY` | Stages.js | 0.5-1.0 | Gravity modifier |
| Hazard spawn interval | StageManager.js | 500-2000ms | Hazard frequency |

### Target Metrics
- Average game duration: 3-5 minutes
- Win rate: ~40-50% (challenging but achievable)
- Stage 1-3: Easy introduction, learn mechanics
- Stage 4-6: Medium difficulty, wind/gravity challenges
- Stage 7-10: Hard, environmental mastery required

---

## Agent Usage Summary

| Agent | Task | Command |
|-------|------|---------|
| `image_agent` | Generate all 21+ assets | `python scripts/generate_asset.py ...` |
| `sound_agent` | Redesign SFX for zen aesthetic | `python -m agents.sound_agent games/feeding-caiso/index.html` |
| `code_agent` | Review physics/performance | `python -m agents.code_agent games/feeding-caiso/index.html` |
| `design_agent` | UI/palette consistency review | `python -m agents.design_agent games/feeding-caiso/index.html` |
| `play_agent` | Balance tuning (simulated) | `python -m agents.play_agent games/feeding-caiso/index.html --sim` |
| Pipeline | Run all agents | `python -m agents games/feeding-caiso/index.html` |

---

## Verification

### Quick Smoke Test
1. Open `games/feeding-caiso/index.html` in browser
2. Game should load with canvas fallbacks (no assets = colored shapes)
3. Click to start -> gameplay works with fallback graphics
4. Verify stage transitions happen as level increases
5. Verify wind affects food trajectory in Stage 3+
6. Verify gravity changes in Stage 5+

### After Asset Generation
1. All sprites render correctly (no console warnings for missing assets)
2. Food items match their Constants.js definitions
3. Parallax background scrolls smoothly
4. Title screen uses new background
5. UI food selector shows all 6 items with correct icons

### Full Playthrough
1. Play from Stage 1 to victory (hunger -> 0%)
2. Verify all 10 stage transitions with correct atmosphere
3. Verify evolution tier changes at levels 1, 3, 6, 10
4. Verify fever mode activates and multiplier works
5. Verify game over triggers when villagers reach 0
