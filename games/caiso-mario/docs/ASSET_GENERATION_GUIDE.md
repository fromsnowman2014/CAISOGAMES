# Asset Generation Guide

This document defines the **exact prompts and settings** to generate all required assets for Caiso Mario Phase 2. Use the Image Generator API with these parameters.

## Global Style Guide
*   **Style**: 16-bit SNES Pixel Art
*   **Palette**: Vibrant but slightly desaturated retro colors (Nintendo style)
*   **Background**: Must be **Transparent**
*   **Format**: PNG

---

## 1. Player Character: Jay Oh
*Base Size: 32x48 px*

| Asset Name | Prompt | Width | Height |
|------------|--------|-------|--------|
| `jay_idle_01` | "pixel art game sprite of a boy standing still, wearing round glasses, green vest, white shirt, brown shorts, brown backpack. 16-bit snes style, transparent background, full body front view" | 32 | 48 |
| `jay_run_right` | "pixel art game sprite of a boy running to the right, dynamic pose, green vest, brown backpack, motion blur on legs. 16-bit snes style, transparent background" | 32 | 48 |
| `jay_jump` | "pixel art game sprite of a boy jumping up, knees tucked, arms up, green vest. 16-bit snes style, transparent background" | 32 | 48 |
| `jay_fall` | "pixel art game sprite of a boy falling down, flailing arms, green vest. 16-bit snes style, transparent background" | 32 | 48 |
| `jay_attack` | "pixel art game sprite of a boy swinging a large golden chess pawn like a sword. dynamic attack pose. 16-bit snes style, transparent background" | 48 | 48 |

## 2. Enemies (The Chess Pieces)

### Pawn (The Grunt)
*Size: 32x32 px*

| Asset Name | Prompt | Width | Height |
|------------|--------|-------|--------|
| `pawn_idle` | "pixel art game enemy sprite, a living stone chess pawn with angry red eyes and cracks. dark grey stone texture. 16-bit snes style, transparent background" | 32 | 32 |
| `pawn_walk` | "pixel art game enemy sprite, stone chess pawn waddling to the left. angry expression. 16-bit snes style, transparent background" | 32 | 32 |

### Knight (The Jumper)
*Size: 48x48 px*

| Asset Name | Prompt | Width | Height |
|------------|--------|-------|--------|
| `knight_idle` | "pixel art game enemy sprite, a dark metallic chess knight horse head on legs. glowing orange eyes. menacing. 16-bit snes style, transparent background" | 48 | 48 |
| `knight_jump` | "pixel art game enemy sprite, chess knight jumping high, mid-air pose. metallic shine. 16-bit snes style, transparent background" | 48 | 48 |

## 3. Environment (Tilesets)
*Size: 32x32 px (Tileable)*

| Asset Name | Prompt | Width | Height |
|------------|--------|-------|--------|
| `tile_ground_wood` | "pixel art seamless texture of dark mahogany wood bookshelf surface. nice wood grain. game tile. 16-bit snes style" | 32 | 32 |
| `tile_chess_white` | "pixel art seamless texture of white marble chess square. clean and polished. game tile. 16-bit snes style" | 32 | 32 |
| `tile_chess_black` | "pixel art seamless texture of black obsidian chess square. reflective. game tile. 16-bit snes style" | 32 | 32 |
| `tile_book_spine` | "pixel art game tile, side view of old red leather book spine with gold letters. seamless horizontal. 16-bit snes style" | 32 | 32 |

## 4. Backgrounds (Parallax)
*Size: 512x288 px (Upscale game resolution)*

| Asset Name | Prompt | Width | Height |
|------------|--------|-------|--------|
| `bg_layer_far` | "pixel art background, infinite magical library, silhouettes of giant bookshelves fading into golden mist. atmospheric, dim lighting. 16-bit snes style" | 512 | 288 |
| `bg_layer_mid` | "pixel art background layer, rows of floating books and wooden platforms, magical library interior. 16-bit snes style, transparent parts" | 512 | 288 |

## 5. UI Elements

| Asset Name | Prompt | Width | Height |
|------------|--------|-------|--------|
| `ui_heart_full` | "pixel art ui icon, a shiny red heart detailed with white highlight. 16-bit snes style, transparent background" | 16 | 16 |
| `ui_coin` | "pixel art ui icon, gold coin with a star symbol. shiny yellow metal. 16-bit snes style, transparent background" | 16 | 16 |
