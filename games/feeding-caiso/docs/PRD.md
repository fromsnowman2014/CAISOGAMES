# Feeding Caiso - Product Requirements Document

## Overview
Feeding Caiso is a casual arcade game where players must feed a hungry monster named Caiso to prevent it from eating villagers. The game features simple one-button mechanics suitable for children, with increasing difficulty through unlockable food items.

## Game Concept

### Core Loop
1. Caiso's hunger meter constantly increases
2. Villagers walk toward Caiso from the left side
3. Player throws food to reduce Caiso's hunger
4. If hunger reaches 100%, Caiso eats a villager
5. Game ends when all villagers are eaten or player wins by reaching high level

### Target Audience
- Children ages 5-12
- Casual gamers
- Mobile-first users

## Features

### MVP Features (Implemented)
- [x] Hunger meter system (0-100%)
- [x] Villager spawning and movement
- [x] Food throwing mechanics
- [x] Combo system for consecutive feeds
- [x] Level progression (1-100+)
- [x] 6 food types with unlock progression
- [x] Touch-friendly controls
- [x] Particle effects and animations
- [x] Game states: Menu, Playing, Paused, Game Over, Victory

### Food Items
| Food | Unlock Level | Hunger Reduction | Key |
|------|-------------|------------------|-----|
| Apple | 1 | 0.5 | 1 |
| Dorito | 10 | 0.8 | 2 |
| Burger | 20 | 1.5 | 3 |
| Dynamite | 30 | 5.0 | 4 |
| Pizza | 50 | 2.5 | 5 |
| Watermelon | 100 | 7.0 | 6 |

### Controls
- **Space/Click**: Feed Caiso
- **1-6 Keys**: Select food type
- **P/C**: Pause game
- **R**: Restart (game over)
- **Touch Button**: Mobile feed button

## Visual Design

### Characters
- **Caiso**: Purple monster with horns, large mouth, expressive eyes
- **Villagers**: Small human figures that walk backwards toward Caiso
- **Player**: Back-view character with food basket

### Art Style
- Colorful, cartoon-style SVG graphics
- Embedded assets (no external files)
- Smooth animations with particle effects

### Expressions (Caiso)
- Idle: Mouth open, looking hungry
- Eating: Eyes closed, bigger mouth
- Happy: Smiling, sparkles
- Sad: Tears, drooping posture

## Metrics

### Success Criteria
- Level completion rate
- Average playtime
- Combo frequency
- Food type usage distribution

### Performance Targets
- 60 FPS on mid-range devices
- < 2 second load time
- < 100KB total size (single HTML file)

## Future Enhancements
- [ ] Sound effects and music
- [ ] Additional food types
- [ ] Boss levels
- [ ] Achievements system
- [ ] Leaderboards
- [ ] Multiple Caiso skins
- [ ] Seasonal events
