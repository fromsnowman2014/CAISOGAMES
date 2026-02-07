# Phase 2 Technical Specification

## 1. Asset Manager (`src/systems/AssetManager.js`)

The core of Phase 2 is the ability to load external images.

```javascript
export class AssetManager {
    constructor() {
        this.images = new Map();
        this.toLoad = 0;
        this.loaded = 0;
    }

    queueImage(key, src) {
        this.toLoad++;
        const img = new Image();
        img.src = src;
        img.onload = () => {
            this.loaded++;
            console.log(`Loaded: ${key}`);
        };
        this.images.set(key, img);
    }

    getImage(key) {
        return this.images.get(key);
    }

    get progress() {
        return this.toLoad === 0 ? 1 : this.loaded / this.toLoad;
    }

    get isDone() {
        return this.toLoad === this.loaded;
    }
}
```

## 2. Entity Class Hierarchy

Refactoring the monolith into classes.

- **Entity** (Base class)
    - `pos`: {x, y}
    - `vel`: {x, y}
    - `hitbox`: {w, h}
    - `update(dt)`
    - `draw(ctx)`

- **Actor** (extends Entity)
    - `animator`: Handles sprite animation
    - `stats`: { hp, speed }

- **Player** (extends Actor)
    - State Machine: `IDLE`, `RUN`, `JUMP`, `FALL`, `ATTACK`

- **Enemy** (extends Actor)
    - `type`: 'pawn', 'knight', 'bishop', 'rook'
    - `aiState`: `PATROL`, `CHASE`, `ATTACK`

## 3. Image Generation Integration

We will use the existing python script `api/generate_image.py` via the verified Vercel endpoint.

**API Call Structure:**
```json
{
    "prompt": "<Prompt from ASSET_GENERATION_GUIDE>",
    "width": <Width>,
    "height": <Height>,
    "style": "pixel_art"
}
```

## 4. Graphics Standards

- **Resolution**: Native game resolution is `320x180` (upscaled x3 to `960x540` via canvas scaling).
- **Sprite Sizes**:
    - Small: 16x16 / 16x24 (Items)
    - Medium: 32x32 / 32x48 (Player, Standard Enemies)
    - Large: 64x64+ (Bosses)
- **Transparency**: All sprites MUST have transparent backgrounds.

## 5. Performance Considerations

- **Sprite Sheets**: To reduce HTTP requests, we will eventually combine individual frames into sprite sheets using a canvasing script, but for initial generation, individual files are fine.
- **Canvas Optimization**:
    - Use `image-rendering: pixelated` CSS.
    - Disable image smoothing on the context: `ctx.imageSmoothingEnabled = false`.
