# Feeding Caiso - Phase 2: Visual Overhaul & Vertical Evolution

## Project Vision (Re-defined)

> **"From a simple web game to an addictive Mobile-First Action Experience."**

기존의 정적인 데스크탑 웹 게임 경험을 탈피하여, 모바일 환경(9:16 비율)에 최적화된 **세로형 하이퍼 캐주얼 액션 게임**으로 재설계합니다. 핵심 목표는 "한 손 조작의 편리함"과 "시각적 타격감(Juiciness)"의 극대화입니다.

---

## Part 1: Refactoring Plan - Remove, Add, Refine

### 1.1 Remove (과감히 삭제할 요소)

| Element | Reason | Replacement |
|---------|--------|-------------|
| **Landscape Layout (16:10)** | 데스크탑 중심 설계, 모바일에서 불편 | Portrait (9:16) |
| **Keyboard Controls (WASD)** | 모바일에서 사용 불가 | Virtual Joystick |
| **Static Background** | 깊이감 없음, 지루함 | Parallax Scrolling |
| **Hard Borders** | 딱딱한 느낌 | Wall Bounce / Looping |
| **Fixed Camera** | 성장 시 변화 없음 | Dynamic Zoom Camera |

### 1.2 Add (새롭게 추가할 요소)

#### A. Vertical UX & Controls
```javascript
// Virtual Joystick Configuration
const JOYSTICK_CONFIG = {
    zone: 'bottom-half',          // 화면 하단 영역 어디든 터치
    type: 'floating',             // 터치 위치에 조이스틱 출현
    size: 100,                    // 조이스틱 크기 (px)
    threshold: 0.1,               // Dead zone
    fadeTime: 200                 // 손 뗄 때 페이드아웃
};

// Safe Zone Design
const SAFE_ZONES = {
    top: { height: 60, content: 'HUD (score, level, hunger)' },
    center: { content: 'Action Area (80% of screen)' },
    bottom: { height: 120, content: 'Controls + Feed Button' }
};
```

#### B. Visual "Juice" (타격감 및 연출)
```javascript
// Squash & Stretch Animation
const SQUASH_STRETCH = {
    move: { scaleX: 1.2, scaleY: 0.8 },    // 이동 시
    stop: { scaleX: 0.9, scaleY: 1.1 },    // 멈출 때 출렁임
    eat: { scaleX: 1.3, scaleY: 0.7 },     // 먹을 때
    duration: 100,
    easing: 'elastic'
};

// Particle Effects
const PARTICLE_TYPES = {
    eat: {
        count: 15,
        colors: ['#ff6b6b', '#ffd93d', '#6bcb77'],
        size: { min: 4, max: 12 },
        speed: { min: 3, max: 8 },
        lifetime: 500
    },
    trail: {
        count: 1,
        color: 'rgba(255, 255, 255, 0.3)',
        size: 8,
        lifetime: 200
    },
    fever: {
        count: 30,
        colors: ['#ff006e', '#fb5607', '#ffbe0b'],
        size: { min: 6, max: 16 },
        speed: { min: 5, max: 15 },
        lifetime: 800
    }
};

// Glow Effects (Cyberpunk/Deep Sea Theme)
const GLOW_CONFIG = {
    player: { color: '#00d4ff', intensity: 0.6, blur: 15 },
    food: { color: '#ffd93d', intensity: 0.8, blur: 10 },
    caiso: { color: '#9b59b6', intensity: 0.5, blur: 20 },
    fever: { color: '#ff006e', intensity: 1.0, blur: 30 }
};
```

#### C. Game Mechanics (재미 요소)
```javascript
// Fever Mode System
const FEVER_MODE = {
    gaugeMax: 100,
    chargeRate: 5,              // Per food eaten
    comboBonus: 2,              // Extra charge per combo
    duration: 5000,             // 5 seconds
    effects: {
        invincible: true,
        speedMultiplier: 2,
        magnetRange: 200,       // Auto-attract food
        screenEffect: 'invert', // Visual feedback
        scoreMultiplier: 3
    }
};

// Evolution System
const EVOLUTION_TIERS = [
    { level: 1, name: 'Baby Caiso', scale: 0.5, sprite: 'caiso_baby' },
    { level: 10, name: 'Young Caiso', scale: 0.7, sprite: 'caiso_young' },
    { level: 25, name: 'Adult Caiso', scale: 1.0, sprite: 'caiso_adult' },
    { level: 50, name: 'Elder Caiso', scale: 1.3, sprite: 'caiso_elder' },
    { level: 100, name: 'Legendary Caiso', scale: 1.5, sprite: 'caiso_legendary' }
];

// Combo System Enhanced
const COMBO_SYSTEM = {
    window: 1500,               // ms to maintain combo
    thresholds: [
        { combo: 3, text: 'Good!', color: '#ffd93d' },
        { combo: 5, text: 'Great!', color: '#6bcb77' },
        { combo: 10, text: 'Excellent!', color: '#4ecdc4' },
        { combo: 20, text: 'UNSTOPPABLE!', color: '#ff006e' }
    ],
    multiplier: combo => 1 + Math.floor(combo / 3) * 0.5
};
```

### 1.3 Refine (보완 및 개선할 요소)

```javascript
// Movement Physics - Smooth Lerp
const PHYSICS = {
    acceleration: 0.15,         // Lerp factor
    maxSpeed: 8,
    friction: 0.92,             // Deceleration when not moving
    bounceRestitution: 0.6      // Wall bounce elasticity
};

// Collision Detection - Coyote Time
const COLLISION = {
    hitboxScale: 0.7,           // 실제 이미지보다 작은 판정
    coyoteTime: 100,            // ms of forgiveness
    iframes: 500                // Invincibility after hit
};

// UI/HUD - Icon-based
const HUD_DESIGN = {
    hungerBar: {
        type: 'circular',       // 원형 게이지
        position: 'top-center',
        size: 80
    },
    score: {
        type: 'icon',           // 아이콘 + 숫자
        position: 'top-right'
    },
    feverGauge: {
        type: 'vertical-bar',
        position: 'right-edge',
        width: 20
    },
    combo: {
        type: 'popup',          // 화면 중앙 팝업
        animation: 'bounce'
    }
};
```

---

## Part 2: Technical Implementation

### 2.1 Responsive Design (Mobile First)

```css
/* Portrait Container (9:16) */
#game-container {
    width: 100%;
    height: 100vh;
    max-width: 480px;
    margin: 0 auto;
    aspect-ratio: 9 / 16;
    overflow: hidden;
    touch-action: none;
    position: relative;
}

/* Canvas fills container */
#gameCanvas {
    width: 100%;
    height: 100%;
    display: block;
}

/* Desktop fallback - centered with pillarbox */
@media (min-aspect-ratio: 9/16) {
    #game-container {
        height: 100vh;
        width: auto;
    }
}

/* Prevent zoom on double-tap */
* {
    touch-action: manipulation;
}
```

### 2.2 Game Constants (Vertical Layout)

```javascript
// New dimensions for 9:16
const GAME_CONFIG = {
    // Canvas dimensions (internal)
    WIDTH: 480,
    HEIGHT: 854,

    // Zones
    HUD_HEIGHT: 60,
    CONTROL_HEIGHT: 120,
    ACTION_HEIGHT: 674,  // 854 - 60 - 120

    // Positions
    CAISO_Y: 200,        // Upper portion
    VILLAGER_SPAWN_Y: 700,
    PLAYER_Y: 750,

    // Gameplay
    VILLAGER_CONSUME_INTERVAL: 2000,
    COMBO_TIMEOUT: 1500,
    FEVER_CHARGE_MAX: 100
};
```

### 2.3 Virtual Joystick Implementation

```javascript
class VirtualJoystick {
    constructor(options) {
        this.zone = options.zone || document.body;
        this.size = options.size || 100;
        this.threshold = options.threshold || 0.1;

        this.active = false;
        this.origin = { x: 0, y: 0 };
        this.position = { x: 0, y: 0 };
        this.direction = { x: 0, y: 0 };

        this.setupListeners();
    }

    setupListeners() {
        this.zone.addEventListener('touchstart', (e) => this.onStart(e));
        this.zone.addEventListener('touchmove', (e) => this.onMove(e));
        this.zone.addEventListener('touchend', (e) => this.onEnd(e));

        // Mouse fallback for desktop testing
        this.zone.addEventListener('mousedown', (e) => this.onStart(e));
        this.zone.addEventListener('mousemove', (e) => this.onMove(e));
        this.zone.addEventListener('mouseup', (e) => this.onEnd(e));
    }

    onStart(e) {
        const point = e.touches ? e.touches[0] : e;
        const rect = this.zone.getBoundingClientRect();
        const y = point.clientY - rect.top;

        // Only activate in bottom half
        if (y > rect.height * 0.5) {
            this.active = true;
            this.origin.x = point.clientX - rect.left;
            this.origin.y = y;
            this.position.x = this.origin.x;
            this.position.y = this.origin.y;
        }
    }

    onMove(e) {
        if (!this.active) return;
        e.preventDefault();

        const point = e.touches ? e.touches[0] : e;
        const rect = this.zone.getBoundingClientRect();

        this.position.x = point.clientX - rect.left;
        this.position.y = point.clientY - rect.top;

        // Calculate direction
        const dx = this.position.x - this.origin.x;
        const dy = this.position.y - this.origin.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        const maxDistance = this.size / 2;

        if (distance > this.threshold * maxDistance) {
            this.direction.x = Math.min(1, dx / maxDistance);
            this.direction.y = Math.min(1, dy / maxDistance);
        } else {
            this.direction.x = 0;
            this.direction.y = 0;
        }
    }

    onEnd(e) {
        this.active = false;
        this.direction.x = 0;
        this.direction.y = 0;
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
        const stickX = this.origin.x + this.direction.x * (this.size / 3);
        const stickY = this.origin.y + this.direction.y * (this.size / 3);

        ctx.beginPath();
        ctx.arc(stickX, stickY, this.size / 4, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(255, 255, 255, 0.6)';
        ctx.fill();
    }
}
```

### 2.4 Parallax Background System

```javascript
class ParallaxBackground {
    constructor(layers) {
        this.layers = layers.map(layer => ({
            ...layer,
            offset: 0
        }));
    }

    update(playerVelocity, deltaTime) {
        this.layers.forEach(layer => {
            // Move opposite to player direction
            layer.offset -= playerVelocity.x * layer.speed * deltaTime * 0.01;

            // Wrap around
            if (layer.offset > layer.width) layer.offset = 0;
            if (layer.offset < 0) layer.offset = layer.width;
        });
    }

    draw(ctx, canvasWidth, canvasHeight) {
        this.layers.forEach(layer => {
            const img = layer.image;
            if (!img) return;

            // Draw twice for seamless scrolling
            ctx.drawImage(img, layer.offset, layer.y, layer.width, layer.height);
            ctx.drawImage(img, layer.offset - layer.width, layer.y, layer.width, layer.height);
        });
    }
}

// Layer configuration
const PARALLAX_LAYERS = [
    { name: 'sky', speed: 0, y: 0, height: 300 },
    { name: 'clouds', speed: 0.1, y: 50, height: 150 },
    { name: 'mountains', speed: 0.3, y: 200, height: 200 },
    { name: 'village', speed: 0.5, y: 350, height: 250 },
    { name: 'ground', speed: 1.0, y: 550, height: 304 }
];
```

### 2.5 Squash & Stretch Animation System

```javascript
class SquashStretch {
    constructor(entity) {
        this.entity = entity;
        this.scaleX = 1;
        this.scaleY = 1;
        this.targetScaleX = 1;
        this.targetScaleY = 1;
        this.animating = false;
    }

    // Apply effect based on velocity
    applyMovement(velocityX, velocityY) {
        const speed = Math.sqrt(velocityX * velocityX + velocityY * velocityY);
        const stretchFactor = Math.min(speed / 10, 0.3);

        if (speed > 0.5) {
            // Stretch in movement direction
            const angle = Math.atan2(velocityY, velocityX);
            this.targetScaleX = 1 + stretchFactor * Math.abs(Math.cos(angle));
            this.targetScaleY = 1 - stretchFactor * 0.5;
        } else {
            // Return to normal with overshoot (jelly effect)
            this.targetScaleX = 1;
            this.targetScaleY = 1;
        }
    }

    // Trigger eating animation
    triggerEat() {
        this.scaleX = 1.3;
        this.scaleY = 0.7;
        this.targetScaleX = 1;
        this.targetScaleY = 1;
    }

    // Trigger bounce on wall
    triggerBounce() {
        this.scaleX = 0.7;
        this.scaleY = 1.4;
        this.targetScaleX = 1;
        this.targetScaleY = 1;
    }

    update(deltaTime) {
        const lerp = 0.15;
        this.scaleX += (this.targetScaleX - this.scaleX) * lerp;
        this.scaleY += (this.targetScaleY - this.scaleY) * lerp;
    }

    getTransform() {
        return { scaleX: this.scaleX, scaleY: this.scaleY };
    }
}
```

### 2.6 Fever Mode Implementation

```javascript
class FeverMode {
    constructor(game) {
        this.game = game;
        this.gauge = 0;
        this.maxGauge = 100;
        this.active = false;
        this.duration = 5000;
        this.timer = 0;

        // Visual effects
        this.screenFlash = 0;
        this.particles = [];
    }

    charge(amount) {
        if (this.active) return;
        this.gauge = Math.min(this.maxGauge, this.gauge + amount);

        if (this.gauge >= this.maxGauge) {
            this.activate();
        }
    }

    activate() {
        this.active = true;
        this.timer = this.duration;
        this.screenFlash = 1;

        // Spawn burst particles
        for (let i = 0; i < 50; i++) {
            this.particles.push(this.createFeverParticle());
        }

        // Play fever sound
        // this.game.audio.play('fever_start');
    }

    update(deltaTime) {
        if (this.active) {
            this.timer -= deltaTime;

            if (this.timer <= 0) {
                this.deactivate();
            }

            // Continuous particle emission
            if (Math.random() < 0.3) {
                this.particles.push(this.createFeverParticle());
            }
        }

        // Update particles
        this.particles = this.particles.filter(p => {
            p.x += p.vx;
            p.y += p.vy;
            p.life -= deltaTime;
            p.size *= 0.98;
            return p.life > 0;
        });

        // Fade screen flash
        if (this.screenFlash > 0) {
            this.screenFlash -= deltaTime * 0.003;
        }
    }

    deactivate() {
        this.active = false;
        this.gauge = 0;
    }

    createFeverParticle() {
        const colors = ['#ff006e', '#fb5607', '#ffbe0b', '#8338ec'];
        return {
            x: Math.random() * this.game.width,
            y: Math.random() * this.game.height,
            vx: (Math.random() - 0.5) * 10,
            vy: (Math.random() - 0.5) * 10,
            size: Math.random() * 15 + 5,
            color: colors[Math.floor(Math.random() * colors.length)],
            life: 800
        };
    }

    draw(ctx) {
        // Screen flash effect
        if (this.screenFlash > 0) {
            ctx.fillStyle = `rgba(255, 0, 110, ${this.screenFlash * 0.3})`;
            ctx.fillRect(0, 0, ctx.canvas.width, ctx.canvas.height);
        }

        // Draw particles
        this.particles.forEach(p => {
            ctx.globalAlpha = p.life / 800;
            ctx.fillStyle = p.color;
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
            ctx.fill();
        });
        ctx.globalAlpha = 1;

        // Fever gauge UI
        this.drawGauge(ctx);
    }

    drawGauge(ctx) {
        const x = ctx.canvas.width - 30;
        const y = 80;
        const height = 200;
        const width = 20;

        // Background
        ctx.fillStyle = 'rgba(0, 0, 0, 0.5)';
        ctx.fillRect(x, y, width, height);

        // Fill
        const fillHeight = (this.gauge / this.maxGauge) * height;
        const gradient = ctx.createLinearGradient(x, y + height, x, y);
        gradient.addColorStop(0, '#ff006e');
        gradient.addColorStop(0.5, '#fb5607');
        gradient.addColorStop(1, '#ffbe0b');

        ctx.fillStyle = gradient;
        ctx.fillRect(x, y + height - fillHeight, width, fillHeight);

        // Border
        ctx.strokeStyle = this.active ? '#fff' : 'rgba(255, 255, 255, 0.5)';
        ctx.lineWidth = 2;
        ctx.strokeRect(x, y, width, height);

        // "FEVER" text when active
        if (this.active) {
            ctx.save();
            ctx.translate(x + width / 2, y + height / 2);
            ctx.rotate(-Math.PI / 2);
            ctx.fillStyle = '#fff';
            ctx.font = 'bold 16px Fredoka One';
            ctx.textAlign = 'center';
            ctx.fillText('FEVER!', 0, 5);
            ctx.restore();
        }
    }

    getMultiplier() {
        return this.active ? 3 : 1;
    }

    isMagnetActive() {
        return this.active;
    }
}
```

---

## Part 3: Visual Assets Generation

### 3.1 Art Style Direction

**Target Style**: Neon Cyberpunk meets Cute Cartoon
- Glowing outlines on dark backgrounds
- Vibrant neon colors
- Soft, rounded character designs
- Particle-heavy effects

**Color Palette**:
```
Primary (Caiso): #9b59b6, #8e44ad, #6c3483
Neon Accent: #00d4ff, #ff006e, #ffbe0b
Dark Background: #1a1a2e, #16213e, #0f3460
Glow Effects: #00fff0, #ff00ff, #ffd700
```

### 3.2 Sprite Generation Prompts (Image Generator API)

#### Caiso Character Sprites
```bash
# Baby Caiso (Level 1-9)
python scripts/generate_asset.py sprite \
  "cute chibi purple monster, small round body, big sparkly eyes, tiny horns, happy expression, neon glow outline, cyberpunk style, transparent background" \
  caiso_baby --size 128x128 --output games/feeding-caiso/assets/sprites/

# Young Caiso (Level 10-24)
python scripts/generate_asset.py sprite \
  "cute cartoon purple monster, medium round body, friendly eyes, small horns, slightly open mouth, soft neon glow, cyberpunk cute style, transparent background" \
  caiso_young --size 192x192 --output games/feeding-caiso/assets/sprites/

# Adult Caiso (Level 25-49) - Multiple expressions
python scripts/generate_asset.py sprite \
  "cartoon purple monster, round body, big eyes, horns on head, mouth wide open hungry, drooling, neon purple glow, cyberpunk style, transparent background" \
  caiso_adult_hungry --size 256x256 --output games/feeding-caiso/assets/sprites/

python scripts/generate_asset.py sprite \
  "cartoon purple monster, round body, closed happy eyes, big smile, sparkles, neon purple glow, cyberpunk style, transparent background" \
  caiso_adult_happy --size 256x256 --output games/feeding-caiso/assets/sprites/

python scripts/generate_asset.py sprite \
  "cartoon purple monster, round body, sad teary eyes, frown, neon purple dim glow, cyberpunk style, transparent background" \
  caiso_adult_sad --size 256x256 --output games/feeding-caiso/assets/sprites/

# Elder Caiso (Level 50-99)
python scripts/generate_asset.py sprite \
  "majestic cartoon purple monster, large round body, wise eyes, crown-like horns, regal pose, bright neon purple aura, cyberpunk style, transparent background" \
  caiso_elder --size 320x320 --output games/feeding-caiso/assets/sprites/

# Legendary Caiso (Level 100+)
python scripts/generate_asset.py sprite \
  "legendary cartoon purple monster, massive round body, golden crown, glowing eyes, rainbow neon aura, legendary effects, cyberpunk style, transparent background" \
  caiso_legendary --size 384x384 --output games/feeding-caiso/assets/sprites/
```

#### Food Items
```bash
# Apple (neon style)
python scripts/generate_asset.py sprite \
  "cartoon apple, shiny red, neon glow outline, cyberpunk game item style, simple design, transparent background" \
  food_apple --size 64x64 --output games/feeding-caiso/assets/sprites/

# Burger (neon style)
python scripts/generate_asset.py sprite \
  "cartoon burger, colorful layers, neon glow outline, cyberpunk game item style, delicious looking, transparent background" \
  food_burger --size 64x64 --output games/feeding-caiso/assets/sprites/

# Pizza (neon style)
python scripts/generate_asset.py sprite \
  "cartoon pizza slice, pepperoni cheese, neon glow outline, cyberpunk game item style, transparent background" \
  food_pizza --size 64x64 --output games/feeding-caiso/assets/sprites/

# Golden Apple (special)
python scripts/generate_asset.py sprite \
  "magical golden apple, glowing aura, sparkles, legendary game item, neon gold glow, cyberpunk style, transparent background" \
  food_golden_apple --size 64x64 --output games/feeding-caiso/assets/sprites/

# Fever Food (rainbow)
python scripts/generate_asset.py sprite \
  "magical rainbow food item, spinning, sparkles all around, legendary game item, rainbow neon glow, transparent background" \
  food_fever --size 64x64 --output games/feeding-caiso/assets/sprites/
```

#### Backgrounds (Parallax Layers)
```bash
# Sky layer (deep blue/purple gradient)
python scripts/generate_asset.py background \
  "cyberpunk night sky, deep blue purple gradient, stars, no moon, simple, game background, tileable" \
  bg_sky --size 480x300 --output games/feeding-caiso/assets/backgrounds/

# Clouds layer
python scripts/generate_asset.py background \
  "neon glowing clouds, pink and cyan, cyberpunk style, game background layer, transparent areas, tileable" \
  bg_clouds --size 960x150 --output games/feeding-caiso/assets/backgrounds/

# City/Village layer (silhouette)
python scripts/generate_asset.py background \
  "cyberpunk city silhouette, neon window lights, dark buildings, game background layer, tileable" \
  bg_city --size 960x250 --output games/feeding-caiso/assets/backgrounds/

# Ground layer
python scripts/generate_asset.py background \
  "cyberpunk street ground, neon grid lines, dark surface, game platform, tileable" \
  bg_ground --size 960x300 --output games/feeding-caiso/assets/backgrounds/
```

#### UI Elements
```bash
# Feed button
python scripts/generate_asset.py sprite \
  "circular game button, neon purple glow, bite mark icon, cyberpunk style, transparent background" \
  ui_feed_button --size 128x128 --output games/feeding-caiso/assets/ui/

# Hunger gauge frame
python scripts/generate_asset.py sprite \
  "circular progress bar frame, neon style, cyberpunk, futuristic, transparent center, game UI" \
  ui_hunger_frame --size 100x100 --output games/feeding-caiso/assets/ui/
```

---

## Part 4: Gameplay Loop (Revised)

### 4.1 Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        TITLE SCREEN                         │
│              "Tap to Play" (pulsing animation)              │
└─────────────────────────┬───────────────────────────────────┘
                          │ Tap
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                      GAMEPLAY LOOP                          │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 1. Player moves with joystick                       │   │
│  │ 2. Tap FEED button to throw food                    │   │
│  │ 3. Food reaches Caiso → Hunger decreases            │   │
│  │ 4. Combo builds → Fever gauge charges               │   │
│  │ 5. Villager timer ticks → Caiso eats villager       │   │
│  │ 6. Level up → Caiso evolves                         │   │
│  │ 7. Fever activated → FEVER TIME!                    │   │
│  └─────────────────────────────────────────────────────┘   │
│                          │                                  │
│         ┌────────────────┼────────────────┐                │
│         ▼                ▼                ▼                │
│   [Hunger = 0%]   [Villagers = 0]   [Fever Mode]          │
│         │                │                │                │
│         ▼                ▼                ▼                │
│      VICTORY          GAME OVER      5s MAYHEM             │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 Input Mapping

| Input | Action | Visual Feedback |
|-------|--------|-----------------|
| Touch bottom half + drag | Move player | Joystick appears, player moves |
| Tap FEED button | Throw selected food | Button pulse, throw animation |
| Swipe up (future) | Quick throw | Arc trajectory |
| Double tap | Activate fever (if ready) | Screen flash, particles |

---

## Part 5: Development Phases

### Phase 2.1: Layout Refactoring (Day 1-2)
- [ ] Change canvas aspect ratio to 9:16 (480x854)
- [ ] Update CSS for mobile-first responsive design
- [ ] Reposition all game elements for vertical layout
- [ ] Add touch-action: none to prevent scrolling
- [ ] Test on actual mobile devices

### Phase 2.2: Input System (Day 2-3)
- [ ] Implement VirtualJoystick class
- [ ] Create large FEED button at bottom
- [ ] Remove/deprecate keyboard controls (keep for debug)
- [ ] Add haptic feedback for mobile
- [ ] Test touch responsiveness

### Phase 2.3: Visual Assets (Day 3-5)
- [ ] Generate all Caiso evolution sprites
- [ ] Generate food item sprites
- [ ] Generate parallax background layers
- [ ] Generate UI elements
- [ ] Integrate assets into game

### Phase 2.4: Animation Systems (Day 5-7)
- [ ] Implement SquashStretch system
- [ ] Add particle effects (eat, trail, fever)
- [ ] Add screen shake on events
- [ ] Add glow effects (CSS filter or canvas)
- [ ] Implement parallax background scrolling

### Phase 2.5: Fever Mode (Day 7-8)
- [ ] Implement FeverMode class
- [ ] Add fever gauge UI
- [ ] Implement fever effects (speed, magnet, invincible)
- [ ] Add fever particles and screen effects
- [ ] Balance fever charge rate

### Phase 2.6: Evolution System (Day 8-9)
- [ ] Implement evolution tier checking
- [ ] Add sprite swapping on evolution
- [ ] Add scale changes
- [ ] Add evolution celebration effects
- [ ] Camera zoom adjustments

### Phase 2.7: Polish & Balance (Day 9-10)
- [ ] Fine-tune all animations
- [ ] Balance difficulty curve
- [ ] Add combo text popups
- [ ] Performance optimization
- [ ] Bug fixes and testing

---

## Part 6: Success Metrics

| Metric | Current | Target |
|--------|---------|--------|
| Session Time | ~2 min | 5-8 min |
| Fever Activations per Game | N/A | 3-5 |
| Evolution Reached | N/A | Level 25+ average |
| Mobile Touch Responsiveness | Basic | <16ms input lag |
| Frame Rate | ~60fps | Stable 60fps |
| Return Rate (D1) | N/A | >40% |

---

## Appendix A: File Structure

```
games/feeding-caiso/
├── index.html              # Main game (single-file, updated)
├── docs/
│   ├── PRD.md
│   ├── TECHNICAL_DESIGN.md
│   ├── PHASE2_DEVELOPMENT.md    # This document
│   ├── IMPLEMENTATION_GUIDE.md  # Step-by-step guide
│   └── ASSET_CHECKLIST.md       # Asset generation tracker
└── assets/
    ├── sprites/
    │   ├── caiso_baby.png
    │   ├── caiso_young.png
    │   ├── caiso_adult_hungry.png
    │   ├── caiso_adult_happy.png
    │   ├── caiso_adult_sad.png
    │   ├── caiso_elder.png
    │   ├── caiso_legendary.png
    │   ├── food_apple.png
    │   ├── food_burger.png
    │   ├── food_pizza.png
    │   ├── food_golden_apple.png
    │   └── food_fever.png
    ├── backgrounds/
    │   ├── bg_sky.png
    │   ├── bg_clouds.png
    │   ├── bg_city.png
    │   └── bg_ground.png
    └── ui/
        ├── ui_feed_button.png
        └── ui_hunger_frame.png
```

---

*Document Version: 2.0*
*Last Updated: 2026-02-04*
*Vision: Mobile-First Hyper Casual Action*
