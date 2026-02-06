# 📦 Feeding Caiso Phase 4: Asset Production List

> **Focus**: Graphics & Audio Requirements
> **Agents**: Image Agent, Sound Agent
> **Status**: READY FOR PRODUCTION

---

## 1. 🎨 Image Assets (Image Agent Targets)

**Art Style**: "Neon Kawaii Vector"
- **Keywords**: Flat design, thick outlines, vibrant neon colors (Pink/Cyan/Yellow), slight gradient, no pixel art (Vector style).

### Character: Caiso (The Monster)
| Asset Name | Description | Prompt (Concept) |
|------------|-------------|------------------|
| `caiso_baby.png` | Tier 1 (Small) | `Cute purple slime monster baby, kawaii face, neon glowing outline, vector style, transparent background` |
| `caiso_teen.png` | Tier 2 (Medium) | `Teenage purple monster, slightly messy hair, eating a burger, neon style, kawaii vector` |
| `caiso_adult.png` | Tier 3 (Large) | `Round purple monster, big belly, happy expression, neon highlights, vector illustration` |
| `caiso_king.png` | Tier 4 (Huge) | `Giant purple monster wearing a neon crown, regal but cute, glowing eyes, synthwave colors` |

### Food Items (Projectiles)
| Asset Name | Description | Prompt (Concept) |
|------------|-------------|------------------|
| `food_neon_burger.png` | Basic Food | `Stylized hamburger with neon glowing lettuce and bun, vector icon, dark background contrast` |
| `food_neon_pizza.png` | Fast Food | `Slice of pepperoni pizza with dripping neon cheese, holographic effect, vector` |
| `food_star_candy.png` | Special Food | `Konpeito star candy, glowing rainbow colors, shiny vector art` |
| `food_golden_sushi.png` | Premium Food | `Golden sushi roll, sparkling effect, luxury neon aesthetic, kawaii vector` |

### Backgrounds (Parallax Layers)
| Asset Name | Description | Prompt (Concept) |
|------------|-------------|------------------|
| `bg_cyber_sky.png` | Far Background | `Synthewave sunset sky, purple to orange gradient, retro grid at bottom, seamless horizontal` |
| `bg_neon_city.png` | Mid Background | `Silhouette of futuristic cute city, neon windows, rounded buildings, kawaii cyberpunk, seamless` |
| `bg_ground_grid.png` | Foreground | `Retro 80s perspective grid, glowing pink lines on dark blue floor, seamless horizontal` |

### UI Elements
| Asset Name | Description | Prompt (Concept) |
|------------|-------------|------------------|
| `ui_button_feed.png` | Main Button | `Round glossy button, text "FEED ME", neon pink border, hover glow effect` |
| `ui_panel_glass.png` | Panels | `Glassmorphism panel, semi-transparent dark blue, neon cyan border, rounded corners` |

---

## 2. 🔊 Audio Assets (Sound Agent Targets)

**Audio Style**: "8-bit meets Synthwave"
- **Keywords**: Retro, Crunchy, Upbeat, Synthesizer.

### Sound Effects (SFX)
| Asset Name | Description | Duration | Type |
|------------|-------------|----------|------|
| `sfx_throw.mp3` | Player throws food | 0.2s | `Retro jump/throw sound, light synth pluck` |
| `sfx_eat_crunch.mp3` | Caiso eats food | 0.3s | `Crunchy bite sound mixed with a happy chirp` |
| `sfx_combo_rise.mp3` | Combo increases | 0.5s | `Rising pitch synth scale, energetic` |
| `sfx_fever_start.mp3` | Fever Mode ON | 1.5s | `Explosive neon transition, power-up sound, rapid arpeggio` |
| `sfx_gameover.mp3` | Defeat | 2.0s | `Slow down tape stop effect, sad trombone synth` |

### Background Music (BGM)
| Asset Name | Description | Duration | Vibe |
|------------|-------------|----------|------|
| `bgm_main_loop.mp3` | Main Gameplay | 60s (Loop) | `Kawaii Future Bass, 128 BPM, upbeat, happy chiptune melody` |
| `bgm_fever_loop.mp3` | Fever Mode | 30s (Loop) | `High energy drum and bass, faster tempo (150 BPM), intense synth lead` |
| `bgm_menu.mp3` | Title Screen | 30s (Loop) | `Chill Lo-fi beats, relaxing, waiting elevator music style but neon` |

---

## 3. 🛠️ Implementation Note

1.  **Spritesheets**: 성능을 위해 `Image Agent`로 생성된 개별 이미지를 `Texture Packer` 등을 이용해 하나의 Sprite Atlas로 병합 권장. (Phase 4 후반 작업)
2.  **Audio Formats**: 모바일 호환성을 위해 `MP3`와 `WebM` 두 가지 포맷 준비 권장 (Sound Agent 파이프라인에는 MP3 기본).
