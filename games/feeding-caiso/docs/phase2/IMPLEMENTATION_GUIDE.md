# Feeding Caiso - Implementation Guide

> **Reference**: Always read `PHASE2_DEVELOPMENT.md` before making changes.

This guide provides step-by-step implementation instructions for the Phase 2 overhaul. Follow the phases in order, and check off tasks as you complete them.

---

## Before You Begin

### Required Context Files
Before implementing any feature, read these documents:
1. `docs/PHASE2_DEVELOPMENT.md` - Overall design and specifications
2. `docs/ASSET_CHECKLIST.md` - Track which assets are ready
3. `index.html` - Current game implementation

### Environment Setup
```bash
# Set up image generator (Vercel proxy)
export VERCEL_APP_URL=https://caisogames.vercel.app

# Test image generator
python scripts/generate_asset.py sprite "test purple circle" test_sprite --size 64x64

# Create asset directories
mkdir -p games/feeding-caiso/assets/{sprites,backgrounds,ui}
```

---

## Phase 2.1: Layout Refactoring

### Task 1.1: Update HTML Structure
Replace the game container HTML:

```html
<!-- OLD -->
<div id="gameContainer">
    <canvas id="gameCanvas"></canvas>
    <button id="touchFeedBtn">FEED!</button>
</div>

<!-- NEW -->
<div id="game-container">
    <canvas id="gameCanvas"></canvas>
    <div id="control-zone">
        <button id="feed-btn">FEED</button>
    </div>
    <a href="../../" id="backBtn">...</a>
</div>
```

### Task 1.2: Update CSS for Portrait Mode
Replace the CSS with mobile-first styles:

```css
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    touch-action: manipulation;
}

body {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    font-family: 'Nunito', sans-serif;
    overflow: hidden;
}

#game-container {
    position: relative;
    width: 100%;
    height: 100vh;
    max-width: 480px;
    aspect-ratio: 9 / 16;
    overflow: hidden;
    touch-action: none;
}

#gameCanvas {
    width: 100%;
    height: 100%;
    display: block;
    border-radius: 0;
}

#control-zone {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 120px;
    display: flex;
    justify-content: center;
    align-items: center;
    pointer-events: none;
}

#feed-btn {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    background: linear-gradient(135deg, #9b59b6, #6c3483);
    border: 4px solid rgba(255, 255, 255, 0.3);
    color: white;
    font-family: 'Fredoka One', cursive;
    font-size: 18px;
    cursor: pointer;
    pointer-events: auto;
    box-shadow: 0 0 30px rgba(155, 89, 182, 0.5);
    transition: transform 0.1s;
}

#feed-btn:active {
    transform: scale(0.9);
}

/* Desktop: center with pillarbox */
@media (min-aspect-ratio: 9/16) {
    #game-container {
        height: 100vh;
        width: auto;
        box-shadow: 0 0 60px rgba(108, 92, 231, 0.4);
    }
}
```

### Task 1.3: Update Canvas Dimensions
In the JavaScript, change the game constants:

```javascript
// OLD
const GAME_WIDTH = 900;
const GAME_HEIGHT = 562;

// NEW
const GAME_WIDTH = 480;
const GAME_HEIGHT = 854;

// New zone definitions
const HUD_ZONE = { y: 0, height: 60 };
const ACTION_ZONE = { y: 60, height: 674 };
const CONTROL_ZONE = { y: 734, height: 120 };
```

### Task 1.4: Reposition Game Elements
Update entity positions for vertical layout:

```javascript
// Caiso - now at top of action area
this.caiso = new Caiso(GAME_WIDTH / 2, 180);

// Player - near bottom, above controls
this.player = new Player(GAME_WIDTH / 2, 650);

// Villagers spawn from sides and walk horizontally toward Caiso
// (instead of left to right, they come from all directions)
```

### Verification Checklist for Phase 2.1:
- [ ] Canvas displays in 9:16 portrait mode
- [ ] Game is centered on desktop browsers
- [ ] No horizontal scrolling on mobile
- [ ] Touch events don't trigger browser gestures
- [ ] Back button is visible and functional

---

## Phase 2.2: Input System

### Task 2.1: Implement VirtualJoystick Class
Add this class before the Game class:

```javascript
class VirtualJoystick {
    constructor(canvas) {
        this.canvas = canvas;
        this.size = 100;
        this.threshold = 0.1;

        this.active = false;
        this.origin = { x: 0, y: 0 };
        this.position = { x: 0, y: 0 };
        this.direction = { x: 0, y: 0 };

        this.setupListeners();
    }

    setupListeners() {
        const canvas = this.canvas;

        canvas.addEventListener('touchstart', (e) => this.onStart(e), { passive: false });
        canvas.addEventListener('touchmove', (e) => this.onMove(e), { passive: false });
        canvas.addEventListener('touchend', (e) => this.onEnd(e));

        // Mouse fallback
        canvas.addEventListener('mousedown', (e) => this.onStart(e));
        canvas.addEventListener('mousemove', (e) => this.onMove(e));
        canvas.addEventListener('mouseup', (e) => this.onEnd(e));
    }

    getCanvasPoint(e) {
        const rect = this.canvas.getBoundingClientRect();
        const point = e.touches ? e.touches[0] : e;
        return {
            x: (point.clientX - rect.left) * (GAME_WIDTH / rect.width),
            y: (point.clientY - rect.top) * (GAME_HEIGHT / rect.height)
        };
    }

    onStart(e) {
        const point = this.getCanvasPoint(e);

        // Only activate in bottom portion (control zone + action area bottom)
        if (point.y > GAME_HEIGHT * 0.5) {
            e.preventDefault();
            this.active = true;
            this.origin.x = point.x;
            this.origin.y = point.y;
            this.position = { ...this.origin };
        }
    }

    onMove(e) {
        if (!this.active) return;
        e.preventDefault();

        const point = this.getCanvasPoint(e);
        this.position.x = point.x;
        this.position.y = point.y;

        const dx = this.position.x - this.origin.x;
        const dy = this.position.y - this.origin.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        const maxDistance = this.size / 2;

        if (distance > this.threshold * maxDistance) {
            const clampedDist = Math.min(distance, maxDistance);
            this.direction.x = (dx / distance) * (clampedDist / maxDistance);
            this.direction.y = (dy / distance) * (clampedDist / maxDistance);
        } else {
            this.direction = { x: 0, y: 0 };
        }
    }

    onEnd(e) {
        this.active = false;
        this.direction = { x: 0, y: 0 };
    }

    draw(ctx) {
        if (!this.active) return;

        // Outer ring
        ctx.beginPath();
        ctx.arc(this.origin.x, this.origin.y, this.size / 2, 0, Math.PI * 2);
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.3)';
        ctx.lineWidth = 3;
        ctx.stroke();

        // Inner stick
        const stickX = this.origin.x + this.direction.x * (this.size / 2);
        const stickY = this.origin.y + this.direction.y * (this.size / 2);

        ctx.beginPath();
        ctx.arc(stickX, stickY, this.size / 4, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(255, 255, 255, 0.6)';
        ctx.fill();
    }
}
```

### Task 2.2: Update Player Class for Movement
Modify the Player class to support movement:

```javascript
class Player {
    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.vx = 0;
        this.vy = 0;
        this.throwing = false;
        this.throwTimer = 0;

        // Boundaries
        this.minX = 50;
        this.maxX = GAME_WIDTH - 50;
        this.minY = ACTION_ZONE.y + 400;  // Can only move in lower action area
        this.maxY = CONTROL_ZONE.y - 30;
    }

    move(dirX, dirY, deltaTime) {
        const speed = 5;
        const friction = 0.85;

        this.vx += dirX * speed * 0.1;
        this.vy += dirY * speed * 0.1;

        this.vx *= friction;
        this.vy *= friction;

        this.x += this.vx * deltaTime / 16;
        this.y += this.vy * deltaTime / 16;

        // Clamp to boundaries
        this.x = Math.max(this.minX, Math.min(this.maxX, this.x));
        this.y = Math.max(this.minY, Math.min(this.maxY, this.y));
    }

    // ... rest of Player class
}
```

### Task 2.3: Connect Joystick to Game
In the Game class:

```javascript
class Game {
    constructor(canvas) {
        // ... existing code ...
        this.joystick = new VirtualJoystick(canvas);
    }

    update(deltaTime) {
        // ... existing update code ...

        // Player movement via joystick
        this.player.move(
            this.joystick.direction.x,
            this.joystick.direction.y,
            deltaTime
        );
    }

    render() {
        // ... existing render code ...

        // Draw joystick overlay
        this.joystick.draw(this.ctx);
    }
}
```

### Task 2.4: Update Feed Button Handler
```javascript
setupEventListeners() {
    // Feed button (both HTML button and spacebar)
    document.getElementById('feed-btn').addEventListener('click', () => {
        if (this.state === 'playing') this.feedCaiso();
    });

    document.getElementById('feed-btn').addEventListener('touchstart', (e) => {
        e.preventDefault();
        if (this.state === 'playing') this.feedCaiso();
    });

    // Keep spacebar for desktop testing
    document.addEventListener('keydown', (e) => {
        if (e.code === 'Space' && this.state === 'playing') {
            e.preventDefault();
            this.feedCaiso();
        }
    });
}
```

### Verification Checklist for Phase 2.2:
- [ ] Virtual joystick appears when touching bottom half
- [ ] Player moves smoothly in response to joystick
- [ ] Feed button works on both tap and click
- [ ] Player cannot move outside boundaries
- [ ] Joystick disappears when touch ends

---

## Phase 2.3: Visual Assets

### Task 3.1: Generate Caiso Sprites
Run these commands to generate Caiso evolution sprites:

```bash
# Ensure output directory exists
mkdir -p games/feeding-caiso/assets/sprites

# Generate Baby Caiso
python scripts/generate_asset.py sprite \
  "cute chibi purple monster, small round body, big sparkly eyes, tiny horns, happy expression, neon glow outline, cyberpunk style, transparent background, game character" \
  caiso_baby --size 128x128 --output games/feeding-caiso/assets/sprites/

# Generate Adult Caiso (hungry)
python scripts/generate_asset.py sprite \
  "cartoon purple monster, round body, big eyes, horns on head, mouth wide open hungry, drooling, neon purple glow, cyberpunk style, transparent background, game character" \
  caiso_adult_hungry --size 256x256 --output games/feeding-caiso/assets/sprites/

# Check ASSET_CHECKLIST.md for full list
```

### Task 3.2: Generate Food Sprites
```bash
python scripts/generate_asset.py sprite \
  "cartoon apple, shiny red, neon glow outline, cyberpunk game item style, simple design, transparent background" \
  food_apple --size 64x64 --output games/feeding-caiso/assets/sprites/

# Continue with burger, pizza, etc.
```

### Task 3.3: Generate Backgrounds
```bash
python scripts/generate_asset.py background \
  "cyberpunk night sky, deep blue purple gradient, stars, simple, game background, tileable horizontal" \
  bg_sky --size 480x300 --output games/feeding-caiso/assets/backgrounds/
```

### Task 3.4: Integrate Assets into Game
Update the ImageLoader to load external PNG files:

```javascript
class ImageLoader {
    constructor() {
        this.images = {};
        this.loaded = 0;
        this.total = 0;
    }

    async loadAll(assetManifest) {
        const entries = Object.entries(assetManifest);
        this.total = entries.length;

        const loadPromises = entries.map(([key, src]) => {
            return new Promise((resolve) => {
                const img = new Image();
                img.onload = () => {
                    this.images[key] = img;
                    this.loaded++;
                    resolve();
                };
                img.onerror = () => {
                    console.warn(`Failed to load: ${src}`);
                    this.loaded++;
                    resolve();
                };
                img.src = src;
            });
        });

        await Promise.all(loadPromises);
    }

    get(key) {
        return this.images[key];
    }

    getProgress() {
        return this.total > 0 ? this.loaded / this.total : 1;
    }
}

// Asset manifest (update paths as assets are generated)
const ASSET_MANIFEST = {
    // Caiso
    caisoBaby: 'assets/sprites/caiso_baby.png',
    caisoAdultHungry: 'assets/sprites/caiso_adult_hungry.png',
    caisoAdultHappy: 'assets/sprites/caiso_adult_happy.png',

    // Food
    foodApple: 'assets/sprites/food_apple.png',
    foodBurger: 'assets/sprites/food_burger.png',
    foodPizza: 'assets/sprites/food_pizza.png',

    // Backgrounds
    bgSky: 'assets/backgrounds/bg_sky.png',
    bgCity: 'assets/backgrounds/bg_city.png',
    bgGround: 'assets/backgrounds/bg_ground.png',

    // Fallback to embedded SVG if PNG not found
    // ... keep SVG assets as backup
};
```

### Verification Checklist for Phase 2.3:
- [ ] All generated PNGs exist in assets folder
- [ ] Images load without CORS errors
- [ ] Loading screen shows progress
- [ ] Fallback works if image fails to load
- [ ] All sprites display correctly in game

---

## Phase 2.4: Animation Systems

### Task 4.1: Implement Squash & Stretch
See PHASE2_DEVELOPMENT.md Section 2.5 for full implementation.

Key integration points:
```javascript
// In Caiso class
class Caiso {
    constructor(x, y) {
        // ... existing code ...
        this.squash = new SquashStretch(this);
    }

    eat() {
        this.squash.triggerEat();
        // ... existing code ...
    }

    draw(ctx, images) {
        const transform = this.squash.getTransform();
        ctx.save();
        ctx.translate(this.x, this.y);
        ctx.scale(transform.scaleX, transform.scaleY);
        // Draw centered at origin
        ctx.drawImage(img, -width/2, -height/2, width, height);
        ctx.restore();
    }
}
```

### Task 4.2: Implement Enhanced Particle System
```javascript
class ParticleSystem {
    constructor() {
        this.particles = [];
    }

    emit(type, x, y) {
        const config = PARTICLE_TYPES[type];
        for (let i = 0; i < config.count; i++) {
            this.particles.push({
                x, y,
                vx: (Math.random() - 0.5) * config.speed.max * 2,
                vy: (Math.random() - 0.5) * config.speed.max * 2 - 2,
                color: config.colors[Math.floor(Math.random() * config.colors.length)],
                size: config.size.min + Math.random() * (config.size.max - config.size.min),
                life: config.lifetime,
                maxLife: config.lifetime
            });
        }
    }

    update(deltaTime) {
        this.particles = this.particles.filter(p => {
            p.x += p.vx * deltaTime / 16;
            p.y += p.vy * deltaTime / 16;
            p.vy += 0.2;  // Gravity
            p.life -= deltaTime;
            p.size *= 0.98;
            return p.life > 0;
        });
    }

    draw(ctx) {
        this.particles.forEach(p => {
            ctx.globalAlpha = p.life / p.maxLife;
            ctx.fillStyle = p.color;
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
            ctx.fill();
        });
        ctx.globalAlpha = 1;
    }
}
```

### Verification Checklist for Phase 2.4:
- [ ] Caiso squashes when eating
- [ ] Player stretches when moving fast
- [ ] Particles emit on food consumption
- [ ] Trail particles follow fast-moving entities
- [ ] Animations run at 60fps

---

## Phase 2.5: Fever Mode

### Task 5.1: Add Fever System to Game
See PHASE2_DEVELOPMENT.md Section 2.6 for full implementation.

Integration:
```javascript
class Game {
    constructor(canvas) {
        // ... existing code ...
        this.fever = new FeverMode(this);
    }

    consumeFood(food) {
        // ... existing code ...

        // Charge fever gauge
        const chargeAmount = 5 + this.combo * 2;
        this.fever.charge(chargeAmount);

        // Apply fever multiplier
        const multiplier = this.getComboMultiplier() * this.fever.getMultiplier();
        const reduction = food.hungerReduction * multiplier;

        // ... rest of consumeFood
    }

    update(deltaTime) {
        // ... existing code ...
        this.fever.update(deltaTime);
    }

    render() {
        // ... existing code ...
        this.fever.draw(this.ctx);
    }
}
```

### Verification Checklist for Phase 2.5:
- [ ] Fever gauge fills when eating
- [ ] Fever activates at 100%
- [ ] Screen flashes on activation
- [ ] Score multiplier applies during fever
- [ ] Fever particles display correctly
- [ ] Gauge resets after fever ends

---

## Phase 2.6: Evolution System

### Task 6.1: Implement Evolution Tiers
```javascript
const EVOLUTION_TIERS = [
    { level: 1, name: 'Baby Caiso', scale: 0.6, sprite: 'caisoBaby' },
    { level: 10, name: 'Young Caiso', scale: 0.8, sprite: 'caisoYoung' },
    { level: 25, name: 'Adult Caiso', scale: 1.0, sprite: 'caisoAdultHungry' },
    { level: 50, name: 'Elder Caiso', scale: 1.2, sprite: 'caisoElder' },
    { level: 100, name: 'Legendary Caiso', scale: 1.4, sprite: 'caisoLegendary' }
];

class Caiso {
    constructor(x, y) {
        // ... existing code ...
        this.evolutionTier = 0;
        this.scale = 0.6;
    }

    checkEvolution(level) {
        for (let i = EVOLUTION_TIERS.length - 1; i >= 0; i--) {
            if (level >= EVOLUTION_TIERS[i].level && i > this.evolutionTier) {
                this.evolve(i);
                return true;
            }
        }
        return false;
    }

    evolve(tierIndex) {
        const tier = EVOLUTION_TIERS[tierIndex];
        this.evolutionTier = tierIndex;
        this.targetScale = tier.scale;
        this.currentSprite = tier.sprite;

        // Trigger celebration
        this.evolutionCelebration = true;
        this.celebrationTimer = 2000;
    }
}
```

### Verification Checklist for Phase 2.6:
- [ ] Caiso starts as Baby
- [ ] Evolution triggers at correct levels
- [ ] Sprite changes on evolution
- [ ] Scale changes smoothly
- [ ] Celebration effects display

---

## Final Integration Checklist

Before marking Phase 2 complete:

- [ ] All assets generated and loading correctly
- [ ] Mobile layout works on real devices (test on phone)
- [ ] Touch controls responsive (<16ms latency)
- [ ] 60fps maintained on mid-range devices
- [ ] No console errors
- [ ] Back to Hub link works
- [ ] Game restarts correctly
- [ ] All game states (menu, playing, gameover, victory) work
- [ ] Fever mode fully functional
- [ ] Evolution system fully functional

---

## Troubleshooting

### Image Generator Issues
```bash
# If "Connection refused" error:
export VERCEL_APP_URL=https://caisogames.vercel.app

# If API key missing:
# Check that GEMINI_API_KEY is set in Vercel environment variables

# Use mock generator for testing without API:
export USE_MOCK_GENERATOR=true
```

### Canvas Scaling Issues
```javascript
// Ensure proper DPI handling
const dpr = window.devicePixelRatio || 1;
canvas.width = GAME_WIDTH * dpr;
canvas.height = GAME_HEIGHT * dpr;
canvas.style.width = `${GAME_WIDTH}px`;
canvas.style.height = `${GAME_HEIGHT}px`;
ctx.scale(dpr, dpr);
```

### Touch Event Issues
```javascript
// Prevent default on touch events
canvas.addEventListener('touchstart', (e) => {
    e.preventDefault();
    // ... handler
}, { passive: false });
```

---

*Last Updated: 2026-02-04*
