# CAISOGAMES Platform Architecture Plan

## 1. Executive Summary

Transform CAISOGAMES from a single-game application into a modular multi-game platform with a modern Xbox-style landing page.

## 2. Architecture Analysis

### 2.1 Current State
```
CAISOGAMES/
├── src/
│   └── index.html      # Feeding Caiso game (monolithic)
├── docs/
└── vercel.json
```

**Problems:**
- Single game occupies root level
- No scalability for multiple games
- No central navigation
- Games cannot be developed independently

### 2.2 Target State
```
CAISOGAMES/
├── index.html                    # Main landing page (dashboard)
├── css/
│   └── main.css                  # Landing page styles
├── js/
│   └── main.js                   # Landing page interactions
├── assets/
│   ├── logo.svg                  # Platform logo
│   └── thumbnails/
│       ├── feeding-caiso.png     # Game preview images
│       └── coming-soon.png
├── games/
│   ├── feeding-caiso/
│   │   └── index.html            # Feeding Caiso (standalone)
│   ├── game-2/                   # Future game slot
│   └── game-3/                   # Future game slot
├── docs/
│   ├── PRD.md
│   ├── TECHNICAL_DESIGN.md
│   ├── INTERFACE_DESIGN.md
│   └── PLATFORM_ARCHITECTURE.md  # This document
└── vercel.json
```

## 3. Priority Analysis

| Priority | Task | Reason |
|----------|------|--------|
| P0 | Folder restructure | Foundation - must be done first |
| P0 | Move game to subfolder | Enables modular architecture |
| P1 | Create landing page | User-facing entry point |
| P1 | Game card design | Core UI component |
| P2 | Animations | Visual polish |
| P2 | Coming soon placeholders | Future extensibility |
| P3 | Vercel config update | Deployment requirement |

## 4. Technical Decisions

### 4.1 Landing Page Technology
- **Pure HTML/CSS/JS** - No framework needed for simplicity
- **CSS Grid** - For responsive game card layout
- **CSS Animations** - For modern feel (no JS animation libraries)
- **Intersection Observer** - For scroll-based animations

### 4.2 Game Loading Strategy
- **Separate HTML files** - Each game is completely standalone
- **iframe-free** - Direct navigation (better performance)
- **Back button** - Each game has navigation back to hub

### 4.3 Thumbnail Strategy
- **SVG-based** - Generate thumbnails from game assets
- **Base64 inline** - No external image dependencies
- **Aspect ratio** - 16:9 for consistency

## 5. Landing Page Design Spec

### 5.1 Xbox-Inspired Layout
```
┌─────────────────────────────────────────────────────────────┐
│  🎮 CAISOGAMES                              [Settings] [?]  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                                                     │    │
│  │            FEATURED GAME (Large Card)               │    │
│  │               Feeding Caiso                         │    │
│  │         "Save the villagers from Caiso!"            │    │
│  │                  [PLAY NOW]                         │    │
│  │                                                     │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
│  ALL GAMES                                                  │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐               │
│  │  Game 1   │  │  Game 2   │  │  Game 3   │               │
│  │  (Active) │  │  (Soon)   │  │  (Soon)   │               │
│  └───────────┘  └───────────┘  └───────────┘               │
│                                                             │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐               │
│  │  Game 4   │  │  Game 5   │  │  Game 6   │               │
│  │  (Empty)  │  │  (Empty)  │  │  (Empty)  │               │
│  └───────────┘  └───────────┘  └───────────┘               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 5.2 Color Scheme
```
Background:      #0e0e10 (Xbox dark)
Card Background: #1f1f23
Card Hover:      #2d2d35
Accent:          #107c10 (Xbox green)
Accent Alt:      #9147ff (Purple highlight)
Text Primary:    #ffffff
Text Secondary:  #adadb8
```

### 5.3 Animations
| Element | Animation | Trigger |
|---------|-----------|---------|
| Page load | Fade in + slide up | On load |
| Game cards | Scale up (1.05) | Hover |
| Featured card | Subtle pulse glow | Continuous |
| Coming soon | Shimmer effect | Hover |
| Play button | Glow pulse | Hover |

## 6. Game Card Component

### 6.1 Structure
```html
<article class="game-card" data-status="active|coming-soon|empty">
  <div class="card-thumbnail">
    <img src="thumbnail.png" alt="Game preview">
    <div class="card-overlay">
      <span class="status-badge">PLAY</span>
    </div>
  </div>
  <div class="card-info">
    <h3 class="card-title">Game Name</h3>
    <p class="card-description">Brief description...</p>
  </div>
</article>
```

### 6.2 States
- **Active**: Clickable, full color, "PLAY" badge
- **Coming Soon**: Dimmed, "COMING SOON" badge, shimmer
- **Empty**: Placeholder, "+" icon, dashed border

## 7. Implementation Steps

### Phase 1: Foundation (This PR)
1. Create new folder structure
2. Move Feeding Caiso to `games/feeding-caiso/`
3. Add "Back to Hub" button to game
4. Create landing page HTML/CSS/JS
5. Implement game cards
6. Add animations
7. Update Vercel config

### Phase 2: Future Enhancements
- User preferences (localStorage)
- Game progress tracking
- Sound effects for UI
- Keyboard navigation
- Search functionality

## 8. File Dependencies

```
index.html
├── css/main.css
├── js/main.js
└── games/
    └── feeding-caiso/
        └── index.html (standalone, no dependencies)
```

## 9. Vercel Routing

```json
{
  "routes": [
    { "src": "/games/(.*)", "dest": "/games/$1" },
    { "src": "/(.*)", "dest": "/$1" }
  ]
}
```

## 10. Success Criteria

- [ ] Landing page loads in < 1s
- [ ] Games load independently
- [ ] Smooth 60fps animations
- [ ] Mobile responsive
- [ ] Back navigation works
- [ ] Future games can be added without touching landing page

---
*Document Version: 1.0*
*Created: 2026-02-02*
