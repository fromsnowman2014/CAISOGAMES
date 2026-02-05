# Feeding Caiso - Asset Generation Checklist

> Track asset generation progress for Phase 2 development.

## Status Legend
- [ ] Not started
- [~] In progress / Needs revision
- [x] Complete and integrated

---

## 1. Caiso Character Sprites

### Evolution Tiers

| Asset | Size | Status | Command |
|-------|------|--------|---------|
| `caiso_baby.png` | 128x128 | [ ] | `python scripts/generate_asset.py sprite "cute chibi purple monster, small round body, big sparkly eyes, tiny horns, happy expression, neon glow outline, cyberpunk style, transparent background" caiso_baby --size 128x128 --output games/feeding-caiso/assets/sprites/` |
| `caiso_young.png` | 192x192 | [ ] | `python scripts/generate_asset.py sprite "cute cartoon purple monster, medium round body, friendly eyes, small horns, slightly open mouth, soft neon glow, cyberpunk cute style, transparent background" caiso_young --size 192x192 --output games/feeding-caiso/assets/sprites/` |
| `caiso_adult_hungry.png` | 256x256 | [ ] | `python scripts/generate_asset.py sprite "cartoon purple monster, round body, big eyes, horns on head, mouth wide open hungry, drooling, neon purple glow, cyberpunk style, transparent background" caiso_adult_hungry --size 256x256 --output games/feeding-caiso/assets/sprites/` |
| `caiso_adult_happy.png` | 256x256 | [ ] | `python scripts/generate_asset.py sprite "cartoon purple monster, round body, closed happy eyes, big smile, sparkles, neon purple glow, cyberpunk style, transparent background" caiso_adult_happy --size 256x256 --output games/feeding-caiso/assets/sprites/` |
| `caiso_adult_sad.png` | 256x256 | [ ] | `python scripts/generate_asset.py sprite "cartoon purple monster, round body, sad teary eyes, frown, neon purple dim glow, cyberpunk style, transparent background" caiso_adult_sad --size 256x256 --output games/feeding-caiso/assets/sprites/` |
| `caiso_elder.png` | 320x320 | [ ] | `python scripts/generate_asset.py sprite "majestic cartoon purple monster, large round body, wise eyes, crown-like horns, regal pose, bright neon purple aura, cyberpunk style, transparent background" caiso_elder --size 320x320 --output games/feeding-caiso/assets/sprites/` |
| `caiso_legendary.png` | 384x384 | [ ] | `python scripts/generate_asset.py sprite "legendary cartoon purple monster, massive round body, golden crown, glowing eyes, rainbow neon aura, legendary effects, cyberpunk style, transparent background" caiso_legendary --size 384x384 --output games/feeding-caiso/assets/sprites/` |

**Priority**: HIGH - Required for core gameplay

---

## 2. Food Item Sprites

| Asset | Size | Status | Command |
|-------|------|--------|---------|
| `food_apple.png` | 64x64 | [ ] | `python scripts/generate_asset.py sprite "cartoon apple, shiny red, neon glow outline, cyberpunk game item style, simple design, transparent background" food_apple --size 64x64 --output games/feeding-caiso/assets/sprites/` |
| `food_burger.png` | 64x64 | [ ] | `python scripts/generate_asset.py sprite "cartoon burger, colorful layers, neon glow outline, cyberpunk game item style, delicious looking, transparent background" food_burger --size 64x64 --output games/feeding-caiso/assets/sprites/` |
| `food_pizza.png` | 64x64 | [ ] | `python scripts/generate_asset.py sprite "cartoon pizza slice, pepperoni cheese, neon glow outline, cyberpunk game item style, transparent background" food_pizza --size 64x64 --output games/feeding-caiso/assets/sprites/` |
| `food_dorito.png` | 64x64 | [ ] | `python scripts/generate_asset.py sprite "cartoon triangle chip, orange nacho, neon glow outline, cyberpunk game item style, transparent background" food_dorito --size 64x64 --output games/feeding-caiso/assets/sprites/` |
| `food_golden_apple.png` | 64x64 | [ ] | `python scripts/generate_asset.py sprite "magical golden apple, glowing aura, sparkles, legendary game item, neon gold glow, cyberpunk style, transparent background" food_golden_apple --size 64x64 --output games/feeding-caiso/assets/sprites/` |
| `food_fever.png` | 64x64 | [ ] | `python scripts/generate_asset.py sprite "magical rainbow food item, spinning, sparkles all around, legendary game item, rainbow neon glow, transparent background" food_fever --size 64x64 --output games/feeding-caiso/assets/sprites/` |

**Priority**: HIGH - Required for core gameplay

---

## 3. Villager Sprites

| Asset | Size | Status | Command |
|-------|------|--------|---------|
| `villager_normal.png` | 64x64 | [ ] | `python scripts/generate_asset.py sprite "tiny cute chibi villager character, simple design, blue clothes, worried expression, running pose, neon outline, cyberpunk style, transparent background" villager_normal --size 64x64 --output games/feeding-caiso/assets/sprites/` |
| `villager_scared.png` | 64x64 | [ ] | `python scripts/generate_asset.py sprite "tiny cute chibi villager character, red clothes, terrified screaming expression, arms up in panic, neon outline, cyberpunk style, transparent background" villager_scared --size 64x64 --output games/feeding-caiso/assets/sprites/` |
| `villager_golden.png` | 64x64 | [ ] | `python scripts/generate_asset.py sprite "tiny cute chibi villager character, golden glowing outfit, special sparkle effects, royal appearance, neon gold outline, cyberpunk style, transparent background" villager_golden --size 64x64 --output games/feeding-caiso/assets/sprites/` |

**Priority**: MEDIUM - Can use fallback SVG initially

---

## 4. Player Sprite

| Asset | Size | Status | Command |
|-------|------|--------|---------|
| `player_idle.png` | 128x128 | [ ] | `python scripts/generate_asset.py sprite "cartoon character, colorful outfit, holding basket of food, back view, neon outline, cyberpunk style, transparent background" player_idle --size 128x128 --output games/feeding-caiso/assets/sprites/` |
| `player_throwing.png` | 128x128 | [ ] | `python scripts/generate_asset.py sprite "cartoon character, colorful outfit, throwing motion, arm raised, neon outline, cyberpunk style, transparent background" player_throwing --size 128x128 --output games/feeding-caiso/assets/sprites/` |

**Priority**: MEDIUM - Can use fallback SVG initially

---

## 5. Background Layers (Parallax)

| Asset | Size | Status | Command |
|-------|------|--------|---------|
| `bg_sky.png` | 480x300 | [ ] | `python scripts/generate_asset.py background "cyberpunk night sky, deep blue purple gradient, stars, no moon, simple, game background, seamless horizontal" bg_sky --size 480x300 --output games/feeding-caiso/assets/backgrounds/` |
| `bg_clouds.png` | 960x150 | [ ] | `python scripts/generate_asset.py background "neon glowing clouds, pink and cyan, cyberpunk style, game background layer, semi-transparent, seamless horizontal" bg_clouds --size 960x150 --output games/feeding-caiso/assets/backgrounds/` |
| `bg_city.png` | 960x250 | [ ] | `python scripts/generate_asset.py background "cyberpunk city silhouette, neon window lights, dark buildings, game background layer, seamless horizontal" bg_city --size 960x250 --output games/feeding-caiso/assets/backgrounds/` |
| `bg_ground.png` | 960x300 | [ ] | `python scripts/generate_asset.py background "cyberpunk street ground, neon grid lines, dark surface, game platform, seamless horizontal" bg_ground --size 960x300 --output games/feeding-caiso/assets/backgrounds/` |

**Priority**: LOW - Can use CSS gradient initially

---

## 6. UI Elements

| Asset | Size | Status | Command |
|-------|------|--------|---------|
| `ui_feed_button.png` | 128x128 | [ ] | `python scripts/generate_asset.py sprite "circular game button, neon purple glow, bite mark icon, cyberpunk style, transparent background" ui_feed_button --size 128x128 --output games/feeding-caiso/assets/ui/` |
| `ui_hunger_frame.png` | 100x100 | [ ] | `python scripts/generate_asset.py sprite "circular progress bar frame, neon style, cyberpunk, futuristic, transparent center, game UI" ui_hunger_frame --size 100x100 --output games/feeding-caiso/assets/ui/` |
| `ui_fever_bar.png` | 30x200 | [ ] | `python scripts/generate_asset.py sprite "vertical progress bar frame, neon style, cyberpunk, transparent center, game UI element" ui_fever_bar --size 30x200 --output games/feeding-caiso/assets/ui/` |

**Priority**: LOW - Can use canvas drawing initially

---

## Quick Reference Commands

### Generate All Priority HIGH Assets
```bash
# Create directories
mkdir -p games/feeding-caiso/assets/{sprites,backgrounds,ui}

# Caiso sprites
python scripts/generate_asset.py sprite "cute chibi purple monster, small round body, big sparkly eyes, tiny horns, happy expression, neon glow outline, cyberpunk style, transparent background" caiso_baby --size 128x128 --output games/feeding-caiso/assets/sprites/

python scripts/generate_asset.py sprite "cartoon purple monster, round body, big eyes, horns on head, mouth wide open hungry, drooling, neon purple glow, cyberpunk style, transparent background" caiso_adult_hungry --size 256x256 --output games/feeding-caiso/assets/sprites/

python scripts/generate_asset.py sprite "cartoon purple monster, round body, closed happy eyes, big smile, sparkles, neon purple glow, cyberpunk style, transparent background" caiso_adult_happy --size 256x256 --output games/feeding-caiso/assets/sprites/

# Food sprites
python scripts/generate_asset.py sprite "cartoon apple, shiny red, neon glow outline, cyberpunk game item style, simple design, transparent background" food_apple --size 64x64 --output games/feeding-caiso/assets/sprites/

python scripts/generate_asset.py sprite "cartoon burger, colorful layers, neon glow outline, cyberpunk game item style, delicious looking, transparent background" food_burger --size 64x64 --output games/feeding-caiso/assets/sprites/

python scripts/generate_asset.py sprite "cartoon pizza slice, pepperoni cheese, neon glow outline, cyberpunk game item style, transparent background" food_pizza --size 64x64 --output games/feeding-caiso/assets/sprites/
```

### Verify Assets
```bash
# List all generated assets
ls -la games/feeding-caiso/assets/sprites/
ls -la games/feeding-caiso/assets/backgrounds/
ls -la games/feeding-caiso/assets/ui/
```

---

## Notes

### Asset Generation Tips
1. Run one command at a time to check quality
2. If results are poor, try adjusting the prompt
3. Add "game character", "flat design", "simple" for better game assets
4. Check file sizes - should be < 100KB for sprites

### Fallback Strategy
If image generation fails or produces poor results:
1. Keep using embedded SVG assets as fallback
2. Try different prompt variations
3. Consider using free game asset packs as temporary placeholders

### Quality Checklist for Each Asset
- [ ] Transparent background (PNG)
- [ ] Correct dimensions
- [ ] Neon/cyberpunk style consistent
- [ ] Works on dark background
- [ ] File size < 100KB

---

*Last Updated: 2026-02-04*
