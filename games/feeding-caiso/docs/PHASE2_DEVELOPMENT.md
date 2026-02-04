# Feeding Caiso - Phase 2 Development Plan

## Executive Summary

This document outlines a comprehensive Phase 2 development plan to transform Feeding Caiso from a functional prototype into an engaging, polished casual game. The improvements focus on five pillars: **Gameplay Depth**, **Visual Polish**, **Audio Experience**, **Progression Systems**, and **Replayability**.

---

## Part 1: Current Game Analysis

### 1.1 Core Mechanics Assessment

| Mechanic | Implementation | Rating | Notes |
|----------|---------------|--------|-------|
| Hunger System | Starts at 100%, reduce to 0% to win | 3/5 | Lacks tension buildup |
| Villager Consumption | Every 2 seconds | 2/5 | Too predictable, no variation |
| Food Throwing | Click/Space to feed | 4/5 | Simple, accessible |
| Combo System | 1.5s window, multipliers | 4/5 | Good risk/reward |
| Level Progression | Every 5 hunger reduced | 3/5 | Unlocks feel arbitrary |
| Food Selection | 6 types, unlock by level | 3/5 | No strategic depth |

### 1.2 Strengths

1. **Accessibility**: One-button core mechanic perfect for target audience (ages 5-12)
2. **Visual Feedback**: Particles, floating text, and combo indicators provide satisfaction
3. **Clear Goals**: Simple win/lose conditions easy to understand
4. **Mobile Ready**: Touch controls and responsive design
5. **Expressive Character**: Caiso has 4 emotional states creating empathy

### 1.3 Critical Weaknesses

#### Gameplay Issues
1. **No Tension Curve**: Hunger starts at 100% and only decreases - there's no building threat
2. **Passive Experience**: Player just spam-clicks without meaningful decisions
3. **Zero Strategy**: No reason to choose different foods beyond "pick highest unlocked"
4. **Repetitive Loop**: Same 2-second cycle from start to finish
5. **Missing Risk/Reward**: No high-risk, high-reward moments

#### Engagement Issues
1. **No Progression Save**: High scores and achievements not persisted
2. **No Audio**: Silent gameplay dramatically reduces engagement
3. **No Variety**: Every game feels identical
4. **Weak Victory Satisfaction**: Reducing hunger to 0% feels arbitrary

#### Visual Issues
1. **Static SVG Graphics**: Look like programmer art placeholders
2. **No Animation Frames**: Characters lack movement animations
3. **Plain Background**: Static scene with no depth or parallax
4. **No Visual Progression**: Level 1 looks identical to Level 100

### 1.4 Player Psychology Analysis

**Current Loop (Weak)**:
```
Press Button → Food Flies → Number Changes → Repeat
```

**Target Loop (Engaging)**:
```
Assess Threat → Make Decision → Execute → Receive Feedback → Feel Accomplishment → New Threat
```

---

## Part 2: Gameplay Improvements

### 2.1 Core Mechanic Overhaul: Dynamic Hunger System

**Current**: Hunger starts at 100%, decrease only
**Proposed**: Hunger starts at 50%, increases over time, player must maintain balance

```javascript
// New hunger mechanics
const HUNGER_SYSTEM = {
    startingHunger: 50,
    baseIncreaseRate: 0.5,      // Per second
    levelMultiplier: 1.1,       // Rate increases per level
    dangerThreshold: 80,        // Visual warning begins
    criticalThreshold: 95,      // Urgent warning + speed up
    overflowConsumeRate: 0.5    // Seconds per villager when at 100%
};
```

### 2.2 New Mechanic: Food Cooldowns & Energy System

Add strategic depth with cooldown management:

```javascript
const FOODS_V2 = {
    apple: {
        name: 'Apple',
        hungerReduction: 5,
        cooldown: 0,           // Instant, can spam
        energyCost: 0,
        unlockLevel: 1
    },
    sandwich: {
        name: 'Sandwich',
        hungerReduction: 12,
        cooldown: 1000,        // 1 second cooldown
        energyCost: 1,
        unlockLevel: 5
    },
    burger: {
        name: 'Burger',
        hungerReduction: 20,
        cooldown: 2000,
        energyCost: 2,
        unlockLevel: 15
    },
    feast: {
        name: 'Royal Feast',
        hungerReduction: 40,
        cooldown: 5000,
        energyCost: 5,
        special: 'combo_boost', // Doubles next 3 combos
        unlockLevel: 30
    },
    goldenApple: {
        name: 'Golden Apple',
        hungerReduction: 60,
        cooldown: 8000,
        energyCost: 8,
        special: 'time_slow',   // Slows hunger gain for 5s
        unlockLevel: 50
    },
    caisoFavorite: {
        name: "Caiso's Favorite",
        hungerReduction: 100,
        cooldown: 15000,
        energyCost: 15,
        special: 'full_heal',   // Also heals 10 villagers
        unlockLevel: 100
    }
};

// Energy regenerates over time, faster with combos
const ENERGY_SYSTEM = {
    maxEnergy: 20,
    baseRegenRate: 1,          // Per second
    comboRegenBonus: 0.5       // Per combo level
};
```

### 2.3 New Mechanic: Special Events

Random events add variety and excitement:

```javascript
const SPECIAL_EVENTS = {
    villagerRush: {
        name: 'Villager Rush!',
        description: '5 villagers enter at once',
        frequency: 60000,       // Every ~60 seconds
        duration: 5000
    },
    hungerSpike: {
        name: 'Hunger Spike!',
        description: 'Caiso gets extra hungry',
        effect: 'hunger rate x2 for 10 seconds'
    },
    goldenVillager: {
        name: 'Golden Villager',
        description: 'Save this one for bonus points!',
        reward: 'level_up'
    },
    foodRain: {
        name: 'Food Rain!',
        description: 'Free food falls from sky',
        effect: 'auto-feeds every 0.5s for 5s'
    },
    caisoNap: {
        name: "Caiso's Nap",
        description: 'Caiso falls asleep briefly',
        effect: 'hunger paused for 8 seconds'
    }
};
```

### 2.4 New Mechanic: Power-Ups

Collectible power-ups spawn on screen:

| Power-Up | Effect | Duration | Spawn Rate |
|----------|--------|----------|------------|
| Speed Boost | Throw food 2x faster | 10s | Common |
| Double Reduction | Food effects doubled | 8s | Uncommon |
| Shield | Protects 1 villager from being eaten | One-time | Rare |
| Combo Freeze | Combo timer doesn't decay | 15s | Uncommon |
| Energy Surge | Instant full energy | Instant | Rare |
| Time Warp | Slow hunger increase by 50% | 12s | Rare |

### 2.5 Boss Levels (Every 25 Levels)

Special challenge levels with modified rules:

**Level 25 - "Hungry Night"**
- Dark background, limited visibility
- Hunger increases 50% faster
- Reward: Unlock "Night Vision" food (illuminates + feeds)

**Level 50 - "The Feast"**
- 200% starting hunger
- All food cooldowns halved
- Reward: Unlock "Mega Burger"

**Level 75 - "Caiso's Tantrum"**
- Caiso moves around screen
- Must aim throws
- Reward: Unlock "Homing Pizza"

**Level 100 - "Ultimate Challenge"**
- All previous mechanics combined
- Hunger increases exponentially
- Victory: Permanent golden crown for Caiso

---

## Part 3: Visual Overhaul

### 3.1 Art Style Direction

**Target Style**: Soft, rounded, colorful cartoon - similar to modern mobile games like Candy Crush meets Monsters Inc.

**Color Palette**:
```
Primary Purple (Caiso): #9B59B6, #8E44AD, #6C3483
Grass Green: #27AE60, #2ECC71, #58D68D
Sky Blue: #3498DB, #5DADE2, #85C1E9
Warning Red: #E74C3C, #C0392B
Gold/Reward: #F1C40F, #F39C12
UI Dark: #2C3E50, #34495E
```

### 3.2 Asset Generation Plan

Using the Image Generator API, create the following assets:

#### Caiso Character Sprites (Priority: HIGH)
```
Prompt Template: "Cute cartoon purple monster character, large friendly eyes,
small horns, round body, [EXPRESSION], mobile game style, flat shading,
transparent background, 256x256 pixels"

Assets Needed:
1. caiso_idle.png - Neutral, mouth slightly open
2. caiso_happy.png - Big smile, closed eyes, sparkles
3. caiso_eating.png - Wide open mouth, chomping animation frame
4. caiso_sad.png - Tears, droopy expression
5. caiso_hungry.png - Drooling, desperate look
6. caiso_sleeping.png - For "Caiso's Nap" event
7. caiso_angry.png - For boss levels / tantrum
8. caiso_victory.png - With crown, celebrating

Size: 256x256, PNG with transparency
```

#### Villager Sprites (Priority: HIGH)
```
Prompt Template: "Tiny cute cartoon villager character, simple design,
[COLOR] shirt, worried expression, chibi style, mobile game,
transparent background, 64x64 pixels"

Assets Needed:
1. villager_blue.png - Blue shirt, normal
2. villager_red.png - Red shirt variant
3. villager_green.png - Green shirt variant
4. villager_yellow.png - Yellow shirt variant
5. villager_scared.png - Terrified expression
6. villager_golden.png - Special golden villager (glowing)

Size: 64x64, PNG with transparency
```

#### Player Character (Priority: MEDIUM)
```
Prompt Template: "Cartoon character back view, holding woven basket,
chef hat, colorful outfit, ready to throw food, mobile game style,
transparent background"

Assets Needed:
1. player_idle.png - Standing with basket
2. player_throwing.png - Arm raised, throwing motion
3. player_celebrating.png - Victory pose

Size: 128x128, PNG with transparency
```

#### Food Items (Priority: HIGH)
```
Prompt Template: "Cartoon [FOOD] icon, shiny, delicious looking,
mobile game style, simple design, transparent background, 64x64"

Assets Needed:
1. food_apple.png - Shiny red apple
2. food_sandwich.png - Layered sandwich
3. food_burger.png - Juicy burger with toppings
4. food_pizza.png - Pizza slice with toppings
5. food_feast.png - Royal banquet platter
6. food_golden_apple.png - Glowing golden apple
7. food_caiso_favorite.png - Special purple-themed food

Size: 64x64, PNG with transparency
```

#### Backgrounds (Priority: MEDIUM)
```
Prompt Template: "Cartoon game background, [SCENE], colorful,
bright, child-friendly, 16:10 aspect ratio, no characters"

Assets Needed:
1. bg_village_day.png - Sunny village scene
2. bg_village_sunset.png - Orange/pink sky variant
3. bg_village_night.png - Dark blue with stars
4. bg_castle.png - Boss level background
5. bg_feast_hall.png - Level 50 boss background

Size: 1920x1200 (scales to game)
```

#### UI Elements (Priority: LOW)
```
Assets Needed:
1. ui_hunger_bar_frame.png - Decorative bar frame
2. ui_button_feed.png - Feed button design
3. ui_panel_bg.png - Translucent panel background
4. ui_combo_badge.png - Combo multiplier badge
5. ui_level_star.png - Level indicator
6. icon_energy.png - Energy indicator
7. icon_cooldown.png - Cooldown overlay

Size: Various
```

#### Power-Up Icons (Priority: MEDIUM)
```
Assets Needed (64x64 each):
1. powerup_speed.png - Lightning bolt
2. powerup_double.png - x2 symbol
3. powerup_shield.png - Protective bubble
4. powerup_combo.png - Snowflake (freeze)
5. powerup_energy.png - Battery/bolt
6. powerup_time.png - Clock/hourglass
```

#### Particle Effects (Priority: LOW)
```
Assets Needed (32x32 each):
1. particle_sparkle.png - Star sparkle
2. particle_heart.png - Heart shape
3. particle_star.png - 5-point star
4. particle_food_crumb.png - Generic food particle
```

### 3.3 Animation Specifications

#### Caiso Animations
```javascript
const CAISO_ANIMATIONS = {
    idle: {
        frames: ['caiso_idle_1', 'caiso_idle_2'],
        frameTime: 500,
        loop: true
    },
    eating: {
        frames: ['caiso_eating_1', 'caiso_eating_2', 'caiso_eating_3'],
        frameTime: 100,
        loop: false,
        onComplete: 'idle'
    },
    bounce: {
        amplitude: 8,
        frequency: 0.003
    },
    drool: {
        enabled: true,
        threshold: 80,  // hunger level
        particleRate: 200
    }
};
```

#### Villager Animations
```javascript
const VILLAGER_ANIMATIONS = {
    walk: {
        frames: ['villager_walk_1', 'villager_walk_2', 'villager_walk_3', 'villager_walk_4'],
        frameTime: 150,
        loop: true
    },
    scared: {
        frames: ['villager_scared'],
        shake: { amplitude: 2, frequency: 0.02 }
    },
    eaten: {
        scale: { from: 1, to: 0, duration: 300 },
        opacity: { from: 1, to: 0, duration: 300 },
        position: { y: -30, duration: 300 }
    }
};
```

### 3.4 Parallax Background System

```javascript
const PARALLAX_LAYERS = [
    { asset: 'bg_sky', speed: 0, y: 0 },
    { asset: 'bg_clouds', speed: 0.1, y: 20 },
    { asset: 'bg_mountains', speed: 0.3, y: 150 },
    { asset: 'bg_village', speed: 0.5, y: 250 },
    { asset: 'bg_ground', speed: 1, y: 400 }
];
```

---

## Part 4: Audio Design

### 4.1 Sound Effects List

| Sound | Trigger | Priority | Notes |
|-------|---------|----------|-------|
| throw_whoosh | Food thrown | High | Short swoosh |
| eat_chomp | Food eaten | High | Satisfying crunch |
| combo_ding | Combo increase | High | Musical, ascending |
| combo_break | Combo lost | Medium | Disappointed sound |
| villager_scream | Villager eaten | High | Cute "eek!" |
| level_up | Level increase | High | Triumphant fanfare |
| unlock_food | New food unlocked | High | Magical chime |
| powerup_collect | Power-up grabbed | Medium | Positive sparkle |
| warning_alarm | Hunger > 90% | High | Urgent but not scary |
| caiso_happy | Low hunger | Low | Content purr |
| caiso_hungry | High hunger | Low | Stomach growl |
| victory_fanfare | Win game | High | Full celebration |
| game_over | Lose game | High | Sad trombone |

### 4.2 Background Music

```javascript
const MUSIC_TRACKS = {
    menu: {
        file: 'music_menu.mp3',
        tempo: 'medium',
        mood: 'playful'
    },
    gameplay_calm: {
        file: 'music_calm.mp3',
        tempo: 'medium',
        mood: 'cheerful',
        hungerThreshold: [0, 50]
    },
    gameplay_tense: {
        file: 'music_tense.mp3',
        tempo: 'fast',
        mood: 'urgent',
        hungerThreshold: [50, 80]
    },
    gameplay_critical: {
        file: 'music_critical.mp3',
        tempo: 'very_fast',
        mood: 'panic',
        hungerThreshold: [80, 100]
    },
    boss: {
        file: 'music_boss.mp3',
        tempo: 'epic',
        mood: 'challenging'
    },
    victory: {
        file: 'music_victory.mp3',
        tempo: 'triumphant',
        mood: 'celebration'
    }
};
```

### 4.3 Audio Implementation

```javascript
class AudioManager {
    constructor() {
        this.sounds = {};
        this.music = null;
        this.musicVolume = 0.5;
        this.sfxVolume = 0.7;
        this.muted = false;
    }

    crossfadeMusic(newTrack, duration = 1000) {
        // Smooth transition between music tracks
    }

    playSound(key, options = {}) {
        // With pooling for rapid repeated sounds
    }
}
```

---

## Part 5: Progression & Retention Systems

### 5.1 Achievement System

```javascript
const ACHIEVEMENTS = {
    // Beginner
    first_feed: { name: 'First Meal', desc: 'Feed Caiso for the first time', reward: 50 },
    first_combo: { name: 'Combo Starter', desc: 'Get a 3x combo', reward: 100 },
    first_win: { name: 'Village Hero', desc: 'Complete your first game', reward: 200 },

    // Intermediate
    combo_master: { name: 'Combo Master', desc: 'Reach 10x combo', reward: 500 },
    speed_demon: { name: 'Speed Demon', desc: 'Win in under 60 seconds', reward: 750 },
    no_loss: { name: 'Perfect Protector', desc: 'Win without losing any villagers', reward: 1000 },

    // Advanced
    level_50: { name: 'Halfway Hero', desc: 'Reach level 50', reward: 1500 },
    level_100: { name: 'Master Feeder', desc: 'Reach level 100', reward: 5000 },
    all_foods: { name: 'Full Menu', desc: 'Unlock all food types', reward: 2000 },

    // Secret
    golden_save: { name: 'Golden Guardian', desc: 'Save 10 golden villagers', reward: 3000 },
    boss_slayer: { name: 'Boss Slayer', desc: 'Complete all boss levels', reward: 10000 }
};
```

### 5.2 Currency & Shop System

```javascript
const SHOP_ITEMS = {
    // Cosmetics
    caiso_hat_chef: { name: 'Chef Hat', cost: 500, type: 'cosmetic' },
    caiso_hat_crown: { name: 'Royal Crown', cost: 2000, type: 'cosmetic' },
    caiso_skin_blue: { name: 'Blue Caiso', cost: 1000, type: 'skin' },
    caiso_skin_golden: { name: 'Golden Caiso', cost: 5000, type: 'skin' },

    // Upgrades (permanent)
    energy_max_up: { name: 'Energy Tank', cost: 1500, effect: '+5 max energy' },
    combo_time_up: { name: 'Combo Extender', cost: 2000, effect: '+0.5s combo window' },
    starting_food: { name: 'Better Start', cost: 3000, effect: 'Start with sandwich unlocked' }
};
```

### 5.3 Daily Challenges

```javascript
const DAILY_CHALLENGES = [
    { type: 'reach_combo', target: 15, reward: 200, desc: 'Reach 15x combo' },
    { type: 'save_villagers', target: 95, reward: 300, desc: 'Save 95+ villagers' },
    { type: 'use_food', food: 'apple', count: 50, reward: 150, desc: 'Feed 50 apples' },
    { type: 'win_fast', time: 45, reward: 500, desc: 'Win in under 45 seconds' },
    { type: 'no_powerups', reward: 400, desc: 'Win without using power-ups' }
];
```

### 5.4 Local Storage Save System

```javascript
const SAVE_DATA_STRUCTURE = {
    version: 2,
    player: {
        currency: 0,
        highScore: 0,
        maxLevel: 1,
        totalGamesPlayed: 0,
        totalVillagersSaved: 0,
        totalFoodFed: 0
    },
    achievements: [],
    unlockedCosmetics: [],
    equippedCosmetic: null,
    upgrades: [],
    settings: {
        musicVolume: 0.5,
        sfxVolume: 0.7,
        muted: false
    },
    dailyChallenge: {
        date: null,
        progress: {},
        completed: false
    }
};
```

---

## Part 6: UI/UX Improvements

### 6.1 Main Menu Redesign

```
┌─────────────────────────────────────────────┐
│                                             │
│        [Animated Caiso Character]           │
│                                             │
│         ★ FEEDING CAISO ★                   │
│         Save the Villagers!                 │
│                                             │
│     ┌─────────────────────────┐             │
│     │       ▶ PLAY            │             │
│     └─────────────────────────┘             │
│                                             │
│     [Shop]    [Achievements]    [Settings]  │
│                                             │
│     High Score: 12,450    Level: 47         │
│                                             │
│                        🔊 Music  🔈 SFX     │
└─────────────────────────────────────────────┘
```

### 6.2 In-Game HUD Redesign

```
┌─────────────────────────────────────────────┐
│ [🍎 x5] [🍔 --] [🍕 3s]     LVL 12    ⚡ 15/20│
│ ┌─────────────────────────────────────────┐ │
│ │█████████████████████░░░░░ HUNGER: 72%  │ │
│ └─────────────────────────────────────────┘ │
│                                             │
│                [GAME AREA]                  │
│                                             │
│    [COMBO: 5x]                              │
│                                             │
│ ┌─────────┐                                 │
│ │ 👥 87   │    ════════════▓▓▓  [2.0s]    │
│ │VILLAGERS│                                 │
│ └─────────┘                                 │
└─────────────────────────────────────────────┘
```

### 6.3 Touch Control Improvements

```javascript
const TOUCH_ZONES = {
    feedButton: {
        position: 'bottom-center',
        size: 'large',
        feedback: 'haptic'
    },
    foodSelector: {
        position: 'bottom-left',
        layout: 'horizontal-scroll',
        quickSelect: true
    },
    pauseButton: {
        position: 'top-right',
        size: 'small'
    }
};
```

### 6.4 Accessibility Features

```javascript
const ACCESSIBILITY = {
    colorBlindMode: {
        patterns: true,          // Add patterns to colored elements
        labels: true             // Text labels on all icons
    },
    screenReader: {
        announceCombo: true,
        announceHunger: true,
        announceVillagers: true
    },
    reducedMotion: {
        disableParticles: true,
        simplifyAnimations: true
    },
    fontSize: {
        options: ['normal', 'large', 'extra-large']
    }
};
```

---

## Part 7: Technical Implementation

### 7.1 Performance Optimizations

```javascript
// Object pooling for particles
class ParticlePool {
    constructor(size = 100) {
        this.pool = [];
        for (let i = 0; i < size; i++) {
            this.pool.push(new Particle());
        }
    }

    acquire() {
        return this.pool.pop() || new Particle();
    }

    release(particle) {
        particle.reset();
        this.pool.push(particle);
    }
}

// Canvas layer separation
const CANVAS_LAYERS = {
    background: { zIndex: 0, static: true },
    gameObjects: { zIndex: 1, dynamic: true },
    particles: { zIndex: 2, dynamic: true },
    ui: { zIndex: 3, semi-static: true }
};
```

### 7.2 Asset Loading System

```javascript
class AssetManager {
    constructor() {
        this.images = {};
        this.sounds = {};
        this.loadProgress = 0;
    }

    async loadAll() {
        const manifest = await fetch('assets/manifest.json');
        const assets = await manifest.json();

        const total = assets.images.length + assets.sounds.length;
        let loaded = 0;

        const updateProgress = () => {
            loaded++;
            this.loadProgress = loaded / total;
            this.onProgress?.(this.loadProgress);
        };

        await Promise.all([
            ...assets.images.map(img => this.loadImage(img).then(updateProgress)),
            ...assets.sounds.map(snd => this.loadSound(snd).then(updateProgress))
        ]);
    }
}
```

### 7.3 State Machine

```javascript
const GAME_STATES = {
    LOADING: 'loading',
    MENU: 'menu',
    PLAYING: 'playing',
    PAUSED: 'paused',
    BOSS: 'boss',
    EVENT: 'event',
    VICTORY: 'victory',
    GAME_OVER: 'gameover',
    SHOP: 'shop',
    ACHIEVEMENTS: 'achievements'
};

class GameStateMachine {
    constructor() {
        this.currentState = GAME_STATES.LOADING;
        this.previousState = null;
        this.stateData = {};
    }

    transition(newState, data = {}) {
        this.previousState = this.currentState;
        this.currentState = newState;
        this.stateData = data;
        this.onStateChange?.(this.previousState, newState);
    }
}
```

---

## Part 8: Development Phases

### Phase 2.1: Core Gameplay (Week 1-2)
- [ ] Implement dynamic hunger system (increases over time)
- [ ] Add energy system for food
- [ ] Implement food cooldowns
- [ ] Balance testing

### Phase 2.2: Visual Overhaul (Week 2-3)
- [ ] Generate new Caiso sprites with Image Generator API
- [ ] Generate villager sprites
- [ ] Generate food icons
- [ ] Create new backgrounds
- [ ] Implement sprite animation system
- [ ] Add parallax background

### Phase 2.3: Audio Integration (Week 3-4)
- [ ] Find/create sound effects (royalty-free)
- [ ] Find/create background music
- [ ] Implement AudioManager
- [ ] Add dynamic music transitions

### Phase 2.4: Special Features (Week 4-5)
- [ ] Implement power-up system
- [ ] Create special events
- [ ] Design and implement boss levels
- [ ] Add event triggers

### Phase 2.5: Progression Systems (Week 5-6)
- [ ] Implement LocalStorage save system
- [ ] Create achievement system
- [ ] Add currency/shop (cosmetics only)
- [ ] Implement daily challenges

### Phase 2.6: Polish & Testing (Week 6-7)
- [ ] UI/UX refinements
- [ ] Mobile optimization
- [ ] Accessibility features
- [ ] Performance optimization
- [ ] Bug fixing
- [ ] Balance adjustments

---

## Part 9: Asset Generation Prompts

### 9.1 Caiso Character Prompts

```bash
# Idle State
python scripts/generate_asset.py sprite \
  "cute cartoon purple monster, round body, big friendly eyes, small horns on head, slightly open mouth, happy expression, simple flat shading, mobile game style, facing forward" \
  caiso_idle --size 256x256 --output games/feeding-caiso/assets/sprites/

# Eating State
python scripts/generate_asset.py sprite \
  "cute cartoon purple monster, round body, eyes closed with happiness, mouth wide open eating, crumbs flying, excited expression, flat shading, mobile game style" \
  caiso_eating --size 256x256 --output games/feeding-caiso/assets/sprites/

# Hungry State
python scripts/generate_asset.py sprite \
  "cute cartoon purple monster, round body, big pleading eyes, drooling, hungry desperate expression, flat shading, mobile game style" \
  caiso_hungry --size 256x256 --output games/feeding-caiso/assets/sprites/

# Sad State
python scripts/generate_asset.py sprite \
  "cute cartoon purple monster, round body, teary eyes, sad frown, droopy posture, apologetic expression, flat shading, mobile game style" \
  caiso_sad --size 256x256 --output games/feeding-caiso/assets/sprites/

# Happy State
python scripts/generate_asset.py sprite \
  "cute cartoon purple monster, round body, closed happy eyes, big smile, sparkles around, celebrating, flat shading, mobile game style" \
  caiso_happy --size 256x256 --output games/feeding-caiso/assets/sprites/
```

### 9.2 Villager Prompts

```bash
# Normal Villager
python scripts/generate_asset.py sprite \
  "tiny cute chibi villager character, simple design, blue medieval clothes, worried expression, looking back, running pose, flat shading, mobile game style" \
  villager_blue --size 64x64 --output games/feeding-caiso/assets/sprites/

# Scared Villager
python scripts/generate_asset.py sprite \
  "tiny cute chibi villager character, red clothes, terrified screaming expression, arms up in panic, sweat drops, running away, flat shading, mobile game style" \
  villager_scared --size 64x64 --output games/feeding-caiso/assets/sprites/

# Golden Villager
python scripts/generate_asset.py sprite \
  "tiny cute chibi villager character, golden glowing outfit, special sparkle effects, royal appearance, worried but brave expression, flat shading, mobile game style" \
  villager_golden --size 64x64 --output games/feeding-caiso/assets/sprites/
```

### 9.3 Food Item Prompts

```bash
# Apple
python scripts/generate_asset.py sprite \
  "cartoon shiny red apple, game icon style, simple, cute, delicious looking, small leaf on top, glossy highlight, flat shading" \
  food_apple --size 64x64 --output games/feeding-caiso/assets/sprites/

# Burger
python scripts/generate_asset.py sprite \
  "cartoon delicious burger, sesame seed bun, lettuce tomato cheese patty, game icon style, simple, appetizing, flat shading" \
  food_burger --size 64x64 --output games/feeding-caiso/assets/sprites/

# Pizza
python scripts/generate_asset.py sprite \
  "cartoon pizza slice, pepperoni and cheese, game icon style, simple, delicious looking, melted cheese, flat shading" \
  food_pizza --size 64x64 --output games/feeding-caiso/assets/sprites/

# Golden Apple
python scripts/generate_asset.py sprite \
  "magical golden apple, glowing aura, sparkles, game icon style, legendary item appearance, flat shading, precious looking" \
  food_golden_apple --size 64x64 --output games/feeding-caiso/assets/sprites/

# Royal Feast
python scripts/generate_asset.py sprite \
  "cartoon royal feast platter, turkey leg, fruits, goblet, golden plate, game icon style, luxurious food, flat shading" \
  food_feast --size 64x64 --output games/feeding-caiso/assets/sprites/
```

### 9.4 Background Prompts

```bash
# Village Day
python scripts/generate_asset.py background \
  "cartoon medieval village background, sunny day, cute cottages, green hills, blue sky with fluffy clouds, cobblestone path, game background style, bright cheerful colors, no characters" \
  bg_village_day --size 1920x1200 --output games/feeding-caiso/assets/backgrounds/

# Village Night
python scripts/generate_asset.py background \
  "cartoon medieval village background, night time, stars and moon, cottage windows glowing, dark blue sky, peaceful atmosphere, game background style, no characters" \
  bg_village_night --size 1920x1200 --output games/feeding-caiso/assets/backgrounds/

# Castle (Boss Level)
python scripts/generate_asset.py background \
  "cartoon castle interior, grand hall, stone walls, torches, banners, medieval fantasy style, epic atmosphere, game background, no characters" \
  bg_castle --size 1920x1200 --output games/feeding-caiso/assets/backgrounds/
```

---

## Part 10: Success Metrics

### 10.1 Target KPIs

| Metric | Current | Phase 2 Target |
|--------|---------|----------------|
| Average Session Time | ~2 min | 8-10 min |
| Return Rate (D1) | N/A | >40% |
| Return Rate (D7) | N/A | >15% |
| Games per Session | 1-2 | 3-5 |
| Level Completion Rate | ~30% | >50% |
| Achievement Unlock Rate | N/A | >20 avg |

### 10.2 Quality Gates

Before Phase 2 release, all must pass:
- [ ] 60 FPS on mid-range mobile devices
- [ ] < 3 second load time
- [ ] < 2MB total asset size
- [ ] All achievements attainable
- [ ] No game-breaking bugs
- [ ] Touch controls responsive
- [ ] Audio properly balanced

---

## Appendix A: File Structure (Phase 2)

```
games/feeding-caiso/
├── index.html              # Main game file
├── docs/
│   ├── PRD.md
│   ├── TECHNICAL_DESIGN.md
│   └── PHASE2_DEVELOPMENT.md  # This document
└── assets/
    ├── sprites/
    │   ├── caiso_idle.png
    │   ├── caiso_eating.png
    │   ├── caiso_hungry.png
    │   ├── caiso_sad.png
    │   ├── caiso_happy.png
    │   ├── villager_blue.png
    │   ├── villager_scared.png
    │   ├── villager_golden.png
    │   ├── player_idle.png
    │   ├── player_throwing.png
    │   ├── food_apple.png
    │   ├── food_burger.png
    │   ├── food_pizza.png
    │   ├── food_feast.png
    │   ├── food_golden_apple.png
    │   ├── powerup_speed.png
    │   ├── powerup_double.png
    │   ├── powerup_shield.png
    │   └── ...
    ├── backgrounds/
    │   ├── bg_village_day.png
    │   ├── bg_village_night.png
    │   ├── bg_castle.png
    │   └── ...
    ├── ui/
    │   ├── ui_hunger_bar.png
    │   ├── ui_button_feed.png
    │   ├── ui_panel.png
    │   └── ...
    └── audio/
        ├── sfx/
        │   ├── throw_whoosh.mp3
        │   ├── eat_chomp.mp3
        │   ├── combo_ding.mp3
        │   └── ...
        └── music/
            ├── music_menu.mp3
            ├── music_calm.mp3
            ├── music_tense.mp3
            └── ...
```

---

## Appendix B: Recommended Libraries

For future consideration (if moving beyond single-file):

| Library | Purpose | Size |
|---------|---------|------|
| Howler.js | Audio management | 10KB |
| anime.js | UI animations | 17KB |
| localForage | Better localStorage | 10KB |

---

*Document Version: 1.0*
*Last Updated: 2026-02-04*
*Author: Game Design Team*
