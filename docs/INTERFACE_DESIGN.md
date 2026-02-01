# Interface Design Document
## Feeding Caiso - UI/UX Specification

### 1. Design Philosophy

- **Kid-Friendly:** Bright colors, large readable text, cute designs
- **Clear Feedback:** Immediate visual response to all actions
- **Accessible:** Large touch targets, high contrast, simple icons
- **Fun:** Bouncy animations, particle effects, celebratory moments

### 2. Color Palette

```
Primary Colors:
┌─────────────────────────────────────────────────┐
│ Background    │ #1a1a2e │ Dark purple-blue      │
│ Caiso Body    │ #6c5ce7 │ Soft purple           │
│ Caiso Accent  │ #a29bfe │ Light purple          │
│ Hunger Bar    │ #ff6b6b │ Coral red             │
│ Health/Safe   │ #2ed573 │ Bright green          │
│ Warning       │ #ffa502 │ Orange                │
│ Danger        │ #ff4757 │ Red                   │
│ UI Panel      │ #2d3436 │ Dark gray (80% alpha) │
│ Text Primary  │ #ffffff │ White                 │
│ Text Secondary│ #b2bec3 │ Light gray            │
│ Accent        │ #00d2d3 │ Cyan                  │
└─────────────────────────────────────────────────┘
```

### 3. Typography

| Element | Font | Size | Weight |
|---------|------|------|--------|
| Title | 'Fredoka One' | 48px | Bold |
| Headers | 'Fredoka One' | 32px | Bold |
| UI Text | 'Nunito' | 24px | Semi-bold |
| Body | 'Nunito' | 18px | Regular |
| Small | 'Nunito' | 14px | Regular |

### 4. Screen Layouts

#### 4.1 Title Screen
```
┌─────────────────────────────────────────────┐
│                                             │
│           🎮 FEEDING CAISO 🎮               │
│                                             │
│              ╭─────────╮                    │
│              │  (◕‿◕)  │  ← Caiso waving    │
│              │   ~~~   │                    │
│              ╰─────────╯                    │
│                                             │
│         ▶ PRESS SPACE TO START ◀           │
│                                             │
│            [🔊 Sound: ON]                   │
│                                             │
│     Controls: SPACE=Feed  C=Menu  P=Pause   │
│                                             │
└─────────────────────────────────────────────┘
```

#### 4.2 Main Game Screen
```
┌─────────────────────────────────────────────┐
│ ┌─────────────────────────────────────────┐ │
│ │ 🍖 HUNGER ████████████░░░░ 67%          │ │ ← Hunger Bar
│ └─────────────────────────────────────────┘ │
│                                             │
│ ┌──────────┐                 ┌───────────┐  │
│ │ LVL: 25  │                 │ COMBO x3  │  │ ← Level & Combo
│ └──────────┘                 │ 🔥🔥🔥    │  │
│                              └───────────┘  │
│                                             │
│              ╭───────────╮                  │
│              │   (◕口◕)  │  ← Caiso         │
│              │   ╰▽▽▽╯   │    (mouth open)  │
│              │    ~~~~   │                  │
│              ╰───────────╯                  │
│                    🍔                       │ ← Food flying
│                   ↗                         │
│ ┌──────────┐              ┌───────────────┐ │
│ │ 👥 85    │              │ 🍎 🍔 🍕      │ │ ← People & Food
│ │ PEOPLE   │              │ [1] [2] [3]   │ │   Selection
│ └──────────┘              └───────────────┘ │
└─────────────────────────────────────────────┘
```

#### 4.3 Food Selection Menu (Pause)
```
┌─────────────────────────────────────────────┐
│                                             │
│            ═══ CHOOSE FOOD ═══              │
│                                             │
│   ┌─────────────────────────────────────┐   │
│   │  🍎 Apple      -0.1%    [1] ✓       │   │
│   │  🌶️ Dorito     -0.1%    [2] ✓       │   │
│   │  🍔 Burger     -0.2%    [3] ✓       │   │
│   │  🧨 Dynamite   -5.0%    [4] 🔒 Lv30 │   │
│   │  🍕 Pizza      -0.5%    [5] 🔒 Lv50 │   │
│   │  🍉 Watermelon -7.0%    [6] 🔒 Lv100│   │
│   └─────────────────────────────────────┘   │
│                                             │
│   Current Level: 25                         │
│   Press [C] to close                        │
│                                             │
└─────────────────────────────────────────────┘
```

#### 4.4 Game Over Screen
```
┌─────────────────────────────────────────────┐
│                                             │
│              💀 GAME OVER 💀                │
│                                             │
│              ╭─────────╮                    │
│              │  (╥﹏╥)  │  ← Caiso sad      │
│              │   ~~~   │                    │
│              ╰─────────╯                    │
│                                             │
│     Caiso ate all the villagers...          │
│                                             │
│     ┌──────────────────────────┐            │
│     │ Final Level: 45          │            │
│     │ Highest Combo: 8x        │            │
│     │ Villagers Saved: 0       │            │
│     └──────────────────────────┘            │
│                                             │
│         ▶ PRESS R TO RETRY ◀                │
│                                             │
└─────────────────────────────────────────────┘
```

#### 4.5 Victory Screen
```
┌─────────────────────────────────────────────┐
│                                             │
│     🎉🎊 YOU WIN! 🎊🎉                      │
│                                             │
│              ╭─────────╮                    │
│              │  (^▽^)  │  ← Caiso happy     │
│              │   ~~~   │    + sparkles      │
│              ╰─────────╯                    │
│                ✨  ✨  ✨                    │
│                                             │
│     Caiso is full! Villagers are safe!      │
│                                             │
│     ┌──────────────────────────────────┐    │
│     │ Final Level: 100+                │    │
│     │ Max Combo: 15x FEEDING FRENZY!   │    │
│     │ Villagers Saved: 42              │    │
│     │ Time: 2:34                       │    │
│     └──────────────────────────────────┘    │
│                                             │
│         ▶ PRESS R TO PLAY AGAIN ◀           │
│                                             │
└─────────────────────────────────────────────┘
```

### 5. UI Components

#### 5.1 Hunger Bar
```
Normal (>50%):
┌─────────────────────────────────────┐
│ 🍖 HUNGER ████████████░░░░░░ 67%    │  (Red gradient)
└─────────────────────────────────────┘

Warning (25-50%):
┌─────────────────────────────────────┐
│ 🍖 HUNGER █████░░░░░░░░░░░░░ 32%    │  (Orange, pulsing)
└─────────────────────────────────────┘

Low (<25%):
┌─────────────────────────────────────┐
│ 🍖 HUNGER ██░░░░░░░░░░░░░░░░ 12%    │  (Green, celebratory)
└─────────────────────────────────────┘
```

#### 5.2 Villager Counter
```
Safe (>50):
┌──────────┐
│ 👥 85    │  (Green text)
│ PEOPLE   │
└──────────┘

Warning (25-50):
┌──────────┐
│ 👥 42    │  (Orange text, slight shake)
│ PEOPLE   │
└──────────┘

Danger (<25):
┌──────────┐
│ 👥 12    │  (Red text, intense shake)
│ DANGER!  │
└──────────┘
```

#### 5.3 Combo Display
```
No Combo (1-2):
┌───────────┐
│ COMBO x1  │
└───────────┘

Combo Active (3-4):
┌───────────┐
│ COMBO x3  │  (Yellow glow)
│ 🔥        │
└───────────┘

High Combo (5-9):
┌───────────┐
│ COMBO x7  │  (Orange glow + flames)
│ 🔥🔥      │
└───────────┘

FRENZY (10+):
┌─────────────────┐
│ FEEDING FRENZY! │  (Rainbow animation)
│ 🔥🔥🔥 x12      │
└─────────────────┘
```

### 6. Caiso Character Design

#### 6.1 Base Design
```
       ╭───────────────╮
      ╱                 ╲
     │    ◕       ◕     │   ← Big cute eyes
     │       👃         │   ← Small nose
     │    ╰─────╯       │   ← Wide mouth
     │     ▽▽▽▽▽        │   ← Silly teeth (when open)
      ╲       ~~~      ╱    ← Drool animation
       ╰───────────────╯
            │   │
           ╱     ╲          ← Stubby arms
```

#### 6.2 Expressions
| State | Eyes | Mouth | Extra |
|-------|------|-------|-------|
| Idle | ◕ ◕ | ╰─╯ | Gentle bounce |
| Hungry | ◕益◕ | ╰───╯ | Drooling, stomach rumble |
| Eating | >◡< | ▽▽▽▽ | Chomp animation |
| Happy | ^◡^ | ╰▽╯ | Sparkles, blush |
| Full | ─◡─ | ╰◡╯ | Hearts, satisfied |
| Angry | ◕益◕ | ╰△╯ | Red tint (villager eaten) |

### 7. Animations

#### 7.1 Food Throw Animation
- Duration: 500ms
- Path: Parabolic arc from food panel to Caiso's mouth
- Effect: Food spins while flying
- Impact: Small burst particles

#### 7.2 Eating Animation
1. Mouth opens wide (100ms)
2. Food enters mouth
3. Chomp motion (200ms)
4. Mouth closes with satisfied expression (200ms)
5. "+X%" floating text appears

#### 7.3 Villager Eaten Animation
1. Screen flash red (100ms)
2. Caiso shows guilty expression
3. "-1" appears near villager counter
4. Small scream icon 💀

#### 7.4 Level Up Animation
1. Screen flash white
2. "LEVEL UP!" text scales up
3. Confetti particles
4. New food unlock notification (if applicable)

#### 7.5 Combo Animation
- Numbers scale up with each combo
- Fire particles increase with combo level
- Screen shake on FEEDING FRENZY

### 8. Particle Effects

| Effect | Trigger | Description |
|--------|---------|-------------|
| Sparkles | Feeding | Small white stars |
| Confetti | Level Up | Multi-colored squares |
| Fire | High Combo | Orange/red particles |
| Hearts | Victory | Pink floating hearts |
| Crumbs | Eating | Food-colored bits |

### 9. Sound Design

| Action | Sound | Duration |
|--------|-------|----------|
| Feed | "Chomp!" | 300ms |
| Villager Lost | "Aaah!" (cute) | 500ms |
| Level Up | Fanfare jingle | 1s |
| Combo (3+) | "Combo!" | 300ms |
| Frenzy | "FRENZY!" | 500ms |
| Victory | Happy music | 3s |
| Game Over | Sad trombone | 2s |
| BGM | Upbeat loop | Continuous |

### 10. Responsive Breakpoints

| Device | Width | Layout Changes |
|--------|-------|----------------|
| Desktop | >1024px | Full layout |
| Tablet | 768-1024px | Scaled UI, larger buttons |
| Mobile | <768px | Stacked UI, touch controls |

### 11. Touch Controls (Mobile)
```
┌─────────────────────────────────────────────┐
│                                             │
│     [Stats/UI at top - same as desktop]     │
│                                             │
│              ╭───────────╮                  │
│              │   CAISO   │                  │
│              ╰───────────╯                  │
│                                             │
│  ┌────────────────────────────────────────┐ │
│  │         TAP ANYWHERE TO FEED           │ │
│  │              🍎 🍔 🍕                   │ │
│  └────────────────────────────────────────┘ │
│                                             │
│  ┌─────────┐                  ┌─────────┐   │
│  │  MENU   │                  │  PAUSE  │   │
│  └─────────┘                  └─────────┘   │
└─────────────────────────────────────────────┘
```

### 12. Accessibility

- High contrast mode available
- Large touch targets (minimum 44x44px)
- Screen reader labels for all UI elements
- Reduced motion option
- Colorblind-friendly indicators (icons + colors)

---
*Document Version: 1.0*
*Last Updated: 2026-02-01*
