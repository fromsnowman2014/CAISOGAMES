# Technical Design Document
## Feeding Caiso - Game Architecture

### 1. Technology Stack

| Component | Technology |
|-----------|------------|
| Language | JavaScript (ES6+) |
| Rendering | HTML5 Canvas |
| Styling | CSS3 |
| Build | None (Vanilla) |
| Deployment | Vercel (Static) |

### 2. Project Structure

```
CAISOGAMES/
├── docs/
│   ├── PRD.md
│   ├── TECHNICAL_DESIGN.md
│   └── INTERFACE_DESIGN.md
├── src/
│   ├── index.html
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   ├── game.js          # Main game class
│   │   ├── caiso.js         # Caiso character
│   │   ├── food.js          # Food system
│   │   ├── ui.js            # UI rendering
│   │   ├── audio.js         # Sound manager
│   │   └── utils.js         # Utilities
│   └── assets/
│       ├── images/
│       └── sounds/
├── vercel.json
└── package.json
```

### 3. Core Classes & Modules

#### 3.1 Game Class (game.js)
```javascript
class Game {
    // Properties
    state: 'menu' | 'playing' | 'paused' | 'gameover' | 'victory'
    hunger: number          // 0-100
    villagers: number       // 0-100
    level: number           // 1+
    combo: number           // Current combo count
    comboMultiplier: number // 1.0 - 3.0
    selectedFood: Food
    unlockedFoods: Food[]

    // Core Methods
    init()                  // Initialize game
    start()                 // Start new game
    update(deltaTime)       // Main update loop
    render()                // Render frame
    feedCaiso()             // Feed action
    consumeVillager()       // Timer callback
    levelUp()               // Handle level up
    checkWinLose()          // Check game end
    pause() / resume()      // Pause control
}
```

#### 3.2 Caiso Class (caiso.js)
```javascript
class Caiso {
    // Properties
    x, y: number            // Position
    width, height: number   // Size
    mouthOpen: boolean      // Animation state
    expression: string      // 'hungry' | 'eating' | 'happy' | 'angry'

    // Methods
    draw(ctx)               // Render Caiso
    animate()               // Update animation
    openMouth()             // Eating animation
    closeMouth()            // After eating
    setExpression(expr)     // Change face
}
```

#### 3.3 Food System (food.js)
```javascript
const FOODS = {
    apple: {
        name: 'Apple',
        emoji: '🍎',
        hungerReduction: 0.1,
        unlockLevel: 1,
        color: '#ff6b6b'
    },
    dorito: {
        name: 'Dorito Chips',
        emoji: '🌶️',
        hungerReduction: 0.1,
        unlockLevel: 10,
        color: '#ff9f43'
    },
    burger: {
        name: 'Burger',
        emoji: '🍔',
        hungerReduction: 0.2,
        unlockLevel: 20,
        color: '#feca57'
    },
    dynamite: {
        name: 'Dynamite Candy',
        emoji: '🧨',
        hungerReduction: 5,
        unlockLevel: 30,
        color: '#ff4757'
    },
    pizza: {
        name: 'Pizza',
        emoji: '🍕',
        hungerReduction: 0.5,
        unlockLevel: 50,
        color: '#ffa502'
    },
    watermelon: {
        name: 'Watermelon',
        emoji: '🍉',
        hungerReduction: 7,
        unlockLevel: 100,
        color: '#2ed573'
    }
};

class FoodManager {
    getUnlockedFoods(level)
    throwFood(food, caiso)
    createFoodAnimation(food, targetX, targetY)
}
```

#### 3.4 UI Manager (ui.js)
```javascript
class UIManager {
    // Methods
    drawHungerBar(ctx, hunger)
    drawVillagerCounter(ctx, count)
    drawLevel(ctx, level)
    drawCombo(ctx, combo, multiplier)
    drawFoodSelection(ctx, foods, selected)
    drawScreen(ctx, screen)  // menu, gameover, victory
    showFloatingText(text, x, y)
}
```

### 4. Game Loop Architecture

```
┌─────────────────────────────────────────────────┐
│                  GAME LOOP                       │
├─────────────────────────────────────────────────┤
│  1. Process Input (keyboard events)              │
│  2. Update Game State                            │
│     - Update timers                              │
│     - Check villager consumption (every 2s)      │
│     - Update animations                          │
│     - Check level up conditions                  │
│     - Check win/lose conditions                  │
│  3. Render Frame                                 │
│     - Clear canvas                               │
│     - Draw background                            │
│     - Draw Caiso                                 │
│     - Draw UI elements                           │
│     - Draw food animations                       │
│     - Draw floating text                         │
│  4. Request next frame                           │
└─────────────────────────────────────────────────┘
```

### 5. State Machine

```
    ┌──────────┐
    │   MENU   │
    └────┬─────┘
         │ Press SPACE
         ▼
    ┌──────────┐
    │ PLAYING  │◄────────────┐
    └────┬─────┘             │
         │                   │
    ┌────┴────┐              │
    │         │              │
    ▼         ▼              │
┌───────┐ ┌───────┐     ┌────┴────┐
│GAMEOVER│ │VICTORY│     │ PAUSED  │
└───┬───┘ └───┬───┘     └─────────┘
    │         │              ▲
    └────┬────┘              │
         │ Press R           │ Press P/C
         ▼                   │
    ┌──────────┐             │
    │   MENU   │─────────────┘
    └──────────┘
```

### 6. Event System

| Event | Trigger | Action |
|-------|---------|--------|
| keydown:Space | Playing state | Feed Caiso |
| keydown:C | Playing state | Open food menu |
| keydown:P | Playing state | Pause game |
| keydown:1-6 | Playing state | Select food |
| keydown:Space | Menu/GameOver | Start game |
| timer:2000ms | Playing state | Consume villager |

### 7. Animation System

#### 7.1 Caiso Animations
- **Idle:** Slight bouncing, blinking
- **Hungry:** Drooling, angry eyes
- **Eating:** Mouth opens wide, chomping motion
- **Happy:** Smile, sparkles (when fed)
- **Full:** Satisfied expression (on victory)

#### 7.2 Food Throwing Animation
```javascript
// Parabolic arc from bottom to Caiso's mouth
function throwAnimation(food, startX, startY, endX, endY) {
    const duration = 500; // ms
    const height = 100;   // arc height

    // Bezier curve calculation
    t = elapsed / duration;
    x = lerp(startX, endX, t);
    y = quadraticBezier(startY, startY - height, endY, t);
}
```

### 8. Scoring & Progression

#### 8.1 Level Calculation
```javascript
// Level increases based on total hunger reduced
function calculateLevel(totalHungerReduced) {
    return Math.floor(totalHungerReduced / 20) + 1;
}
```

#### 8.2 Combo System
```javascript
function getComboMultiplier(combo) {
    if (combo >= 10) return 3.0;  // FEEDING FRENZY!
    if (combo >= 5) return 2.0;
    if (combo >= 3) return 1.5;
    return 1.0;
}

// Combo resets if no food thrown for 2 seconds
```

### 9. Performance Considerations

| Aspect | Strategy |
|--------|----------|
| Rendering | Use requestAnimationFrame |
| Object pooling | Reuse food projectile objects |
| Canvas | Single canvas, layered drawing |
| Assets | Preload all images/sounds |
| Memory | Clean up finished animations |

### 10. Browser Compatibility

```javascript
// Feature detection
const SUPPORTS = {
    canvas: !!document.createElement('canvas').getContext,
    audio: !!document.createElement('audio').canPlayType,
    localStorage: (() => {
        try { return !!localStorage; }
        catch { return false; }
    })()
};
```

### 11. Responsive Design

| Screen Size | Adaptation |
|-------------|------------|
| Desktop (>768px) | Full layout, keyboard controls |
| Tablet (768px) | Scaled canvas, touch buttons |
| Mobile (<480px) | Portrait mode, large touch targets |

### 12. Audio Implementation

```javascript
class AudioManager {
    sounds = {
        chomp: 'chomp.mp3',
        scream: 'scream.mp3',
        levelup: 'levelup.mp3',
        combo: 'combo.mp3',
        win: 'win.mp3',
        lose: 'lose.mp3',
        bgm: 'bgm.mp3'
    };

    // Web Audio API for low latency
    play(soundName)
    playBGM()
    stopBGM()
    setVolume(value)
}
```

---
*Document Version: 1.0*
*Last Updated: 2026-02-01*
