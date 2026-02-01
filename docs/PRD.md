# Product Requirements Document (PRD)
## Feeding Caiso - A Fun Monster Feeding Game

### 1. Product Overview

**Product Name:** Feeding Caiso
**Version:** 1.0
**Target Platform:** Web Browser (Desktop & Mobile)
**Target Audience:** Children ages 8-14
**Genre:** Casual / Time Management / Clicker Game

### 2. Executive Summary

Feeding Caiso is a fun, fast-paced casual game where players must feed a hungry monster named Caiso to prevent it from eating villagers. Players throw food into Caiso's mouth to reduce its hunger meter while racing against time as Caiso consumes one villager every 2 seconds.

### 3. Game Concept

#### 3.1 Core Loop
1. Player sees Caiso with 100% hunger and 100 villagers
2. Every 2 seconds, Caiso eats 1 villager
3. Player feeds food to Caiso by pressing SPACE
4. Each food reduces hunger by a certain percentage
5. Player levels up by reducing hunger, unlocking better foods
6. **WIN:** Reduce Caiso's hunger to 0%
7. **LOSE:** All 100 villagers get eaten

#### 3.2 Unique Selling Points
- Simple one-button gameplay (SPACE to feed)
- Cute monster character design
- Progression system with food unlocks
- Combo mechanics for strategic depth
- Time pressure creates excitement

### 4. Detailed Game Mechanics

#### 4.1 Hunger System
| Metric | Value |
|--------|-------|
| Starting Hunger | 100% |
| Win Condition | 0% |
| Hunger Display | Progress bar with percentage |

#### 4.2 Villager System
| Metric | Value |
|--------|-------|
| Starting Villagers | 100 |
| Consumption Rate | 1 villager every 2 seconds |
| Lose Condition | 0 villagers remaining |

#### 4.3 Food Items & Unlock Levels

| Food | Hunger Reduction | Unlock Level | Icon |
|------|-----------------|--------------|------|
| Apple | 0.1% | Level 1 (Start) | 🍎 |
| Dorito Chips | 0.1% | Level 10 | 🌶️ |
| Burger | 0.2% | Level 20 | 🍔 |
| Pizza | 0.5% | Level 50 | 🍕 |
| Dynamite Candy | 5% | Level 30 | 🧨 |
| Watermelon | 7% | Level 100 | 🍉 |

#### 4.4 Leveling System
- **Level Up Condition:** Every 20% hunger reduced
- **Combo Bonus:** +1 combo multiplier per level up
- **Max Level:** 100+

#### 4.5 Combo System
| Combo Count | Multiplier |
|-------------|------------|
| 1-2 | 1.0x |
| 3-4 | 1.5x |
| 5-9 | 2.0x |
| 10+ | 3.0x (FEEDING FRENZY!) |

### 5. Controls

| Key | Action |
|-----|--------|
| SPACE | Throw selected food to Caiso |
| C | Open food selection menu (pause) |
| 1-6 | Quick select food (if unlocked) |
| P | Pause game |

### 6. User Interface Requirements

#### 6.1 Main Game Screen
- **Top Bar:**
  - Hunger meter (large, prominent)
  - Level indicator
  - Combo counter
- **Center:**
  - Caiso character (animated)
  - Food throwing animation
- **Bottom Left:**
  - Villager counter with icons
- **Bottom Right:**
  - Food inventory/selection

#### 6.2 Screens Required
1. Title Screen
2. Main Game Screen
3. Pause/Food Selection Menu
4. Game Over Screen
5. Victory Screen

### 7. Visual Style

- **Art Style:** Cute, cartoonish, child-friendly
- **Color Palette:** Bright, vibrant colors
- **Caiso Design:** Round, purple/blue monster with big eyes and sharp but silly teeth
- **Animation:** Bouncy, playful movements

### 8. Audio Requirements

- Background music: Upbeat, playful
- Sound effects:
  - Chomp sound (eating food)
  - Villager scream (when eaten)
  - Level up fanfare
  - Combo sounds
  - Win/Lose jingles

### 9. Technical Requirements

- **Framework:** Vanilla JavaScript with HTML5 Canvas
- **Responsive:** Works on desktop and mobile
- **Performance:** 60 FPS target
- **Browser Support:** Chrome, Firefox, Safari, Edge
- **Deployment:** Vercel

### 10. Success Metrics

- Game completion rate > 30%
- Average session length > 3 minutes
- Return player rate > 20%

### 11. Future Enhancements (v2.0)

- Multiple levels/stages
- Caiso skins/customization
- Leaderboard system
- Daily challenges
- More food types
- Boss battles

---
*Document Version: 1.0*
*Last Updated: 2026-02-01*
