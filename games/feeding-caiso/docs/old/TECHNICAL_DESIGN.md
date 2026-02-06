# Feeding Caiso - Technical Design Document

## Architecture Overview

Feeding Caiso is a single-file HTML5 Canvas game with all assets, styles, and logic embedded in one `index.html` file (~60KB, 1533 lines).

```
games/feeding-caiso/
├── index.html          # Complete game (HTML + CSS + JS + SVG assets)
├── docs/
│   ├── PRD.md          # Product requirements
│   └── TECHNICAL_DESIGN.md  # This file
└── assets/             # Reserved for future external assets
    ├── sprites/
    ├── backgrounds/
    └── ui/
```

## Core Classes

### Game Class (Main Controller)
```javascript
class Game {
    // State management
    state: 'loading' | 'menu' | 'playing' | 'paused' | 'gameover' | 'victory'

    // Game data
    hunger: number          // 0-100
    villagerCount: number   // Remaining villagers
    level: number           // Current level
    combo: number           // Current combo count
    selectedFoodKey: string // Active food type

    // Game objects
    caiso: Caiso
    player: Player
    villagers: Villager[]
    flyingFoods: FlyingFood[]
    particles: Particle[]
}
```

### Caiso Class (Monster)
```javascript
class Caiso {
    x, y: number           // Position
    expression: 'idle' | 'eating' | 'happy' | 'sad'
    bounceOffset: number   // Animation offset

    eat()                  // Trigger eating animation
    showGuilty()           // Show sad expression
    getMouthPosition()     // Get food target position
}
```

### Villager Class
```javascript
class Villager {
    x, y: number           // Position
    speed: number          // Movement speed
    scared: boolean        // Scared state (near Caiso)
    beingEaten: boolean    // Currently being eaten
    scale: number          // Size variation
}
```

### Player Class
```javascript
class Player {
    x, y: number           // Position
    throwing: boolean      // Animation state
    throwTimer: number     // Animation timer
}
```

### FlyingFood Class
```javascript
class FlyingFood {
    // Arc trajectory from player to Caiso's mouth
    startX, startY: number  // Start position
    endX, endY: number      // Target position
    progress: number        // 0-1 animation progress
    rotation: number        // Spin animation
}
```

### ImageLoader Class
```javascript
class ImageLoader {
    // Converts SVG strings to Image objects
    loadAll(assets)         // Async batch load
    get(key)               // Retrieve loaded image
}
```

## Asset System

### SVG Embedded Assets
All graphics are stored as SVG strings in the `ASSETS` object:

```javascript
const ASSETS = {
    caisoIdle: `<svg>...</svg>`,
    caisoEating: `<svg>...</svg>`,
    caisoHappy: `<svg>...</svg>`,
    caisoSad: `<svg>...</svg>`,
    villager: `<svg>...</svg>`,
    villagerScared: `<svg>...</svg>`,
    player: `<svg>...</svg>`,
    playerThrowing: `<svg>...</svg>`,
    foodApple: `<svg>...</svg>`,
    foodBurger: `<svg>...</svg>`,
    foodPizza: `<svg>...</svg>`,
    foodDorito: `<svg>...</svg>`,
    foodDynamite: `<svg>...</svg>`,
    foodWatermelon: `<svg>...</svg>`
};
```

### SVG to Image Conversion
```javascript
// Convert SVG string to Image object via Blob URL
const svgBlob = new Blob([svgString], { type: 'image/svg+xml' });
const url = URL.createObjectURL(svgBlob);
img.src = url;
```

## Game Loop

### Main Loop Structure
```javascript
gameLoop(timestamp) {
    const deltaTime = timestamp - lastTime;

    if (state === 'playing') {
        update(deltaTime);
    }

    render();
    requestAnimationFrame(gameLoop);
}
```

### Update Cycle
1. Update game time and timers
2. Increase hunger based on level
3. Spawn villagers periodically
4. Update all game objects (Caiso, villagers, food, particles)
5. Check villager consumption (if hunger >= 100%)
6. Update combo timer
7. Check win/lose conditions

### Render Pipeline
1. Draw gradient background
2. Draw floor and decorations
3. Draw villagers (sorted by Y for depth)
4. Draw Caiso
5. Draw player
6. Draw flying food
7. Draw particles and floating text
8. Draw UI (hunger bar, score, food selector)

## Difficulty Scaling

### Hunger Rate Formula
```javascript
hungerIncreaseRate = 0.012 * level;
// Level 1: 0.012/frame
// Level 50: 0.6/frame
// Level 100: 1.2/frame
```

### Villager Spawn Rate
```javascript
spawnInterval = Math.max(1000, 2000 - level * 15);
// Level 1: 2000ms
// Level 50: 1250ms
// Level 100: 1000ms (cap)
```

### Level Progression
```javascript
// Level up every 10 successful feeds
totalHungerReduced += foodValue;
level = Math.floor(totalHungerReduced / 10) + 1;
```

## Combo System

### Mechanics
- Combo increases with each feed within timeout (1500ms)
- Combo resets if timeout expires
- Higher combo = bonus points

```javascript
const COMBO_TIMEOUT = 1500; // ms

onFeed() {
    combo++;
    maxCombo = Math.max(maxCombo, combo);
    comboTimer = COMBO_TIMEOUT;
}
```

## Input Handling

### Keyboard
```javascript
keydown(e) {
    'Space' -> feedCaiso()
    '1'-'6' -> selectFood(key)
    'P'/'C' -> togglePause()
    'R'     -> restart() // game over only
}
```

### Touch
```javascript
// Touch feed button visible on mobile (max-width: 768px)
#touchFeedBtn.onclick -> feedCaiso()
```

## Performance Considerations

### Optimizations
- Single canvas (no layer splitting)
- Object pooling for particles
- Limited particle count
- RequestAnimationFrame for smooth updates
- Blob URL cleanup after image load

### Memory Management
```javascript
// Clean up Blob URLs after loading
img.onload = () => {
    URL.revokeObjectURL(url);
};

// Remove inactive objects
villagers = villagers.filter(v => v.active);
particles = particles.filter(p => p.active);
```

## Constants

```javascript
const GAME_WIDTH = 900;
const GAME_HEIGHT = 562;
const VILLAGER_CONSUME_INTERVAL = 2000;  // ms between eating
const COMBO_TIMEOUT = 1500;              // ms combo window
```

## Future Technical Considerations

### Audio System (Not Implemented)
- Web Audio API for sound effects
- Background music with mute toggle
- Sound pooling for rapid effects

### Save System (Not Implemented)
- LocalStorage for high scores
- Session persistence

### External Assets Migration
If migrating to external assets:
```
assets/
├── sprites/
│   ├── caiso_idle.svg
│   ├── caiso_eating.svg
│   ├── villager.svg
│   └── food_*.svg
├── backgrounds/
└── ui/
```

## File Structure Summary

| File | Size | Purpose |
|------|------|---------|
| index.html | ~60KB | Complete game |
| docs/PRD.md | ~2KB | Requirements |
| docs/TECHNICAL_DESIGN.md | ~5KB | This document |
