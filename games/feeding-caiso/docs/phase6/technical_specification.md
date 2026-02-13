# Feeding Caiso Phase 6: Technical Specification & Refactoring Plan

This document outlines the technical architecture and refactoring plan for "Feeding Caiso" Phase 6, focusing on implementing the "Hollow Knight" atmospheric style and the 10-stage progression system. It leverages the existing agent infrastructure as defined in `agents/docs/architecture_and_philosophy.md`.

## 1. Architecture Overview

The goal of Phase 6 is to transform the game from a casual arcade style to a high-fidelity, atmospheric experience ("The Hollow Deep"). This requires significant enhancements to the rendering, lighting, and audio systems while maintaining the core game loop.

### 1.1 Core Philosophy Alignment
-   **Modular Design:** We will continue to use the `core/`, `systems/`, `managers/` structure. New features (Parallax, Particles) will be implemented as independent systems.
-   **Data-Driven:** Stage configurations (enemy spawn rates, themes, lighting parameters) will be extracted into a configuration file (`src/config/stages.js`) derived from `game_scenario.md`, allowing the `DesignAgent` to tweak balance without touching code.
-   **Agent-Assisted:** The development process will heavily rely on `ImageAgent` for assets and `SoundAgent` for audio, following the established protocols.

## 2. Current Architecture & Refactoring Analysis

### 2.1 Existing Structure
-   `src/core/Game.js`: Main loop and initialization. **(KEEP & MODIFY)**
-   `src/core/StageManager.js`: Handles stage logic. **(REFACTOR)**
-   `src/managers/AssetManager.js`: Loads resources. **(KEEP)**
-   `src/systems/LightingSystem.js`: Existing lighting logic. **(REWRITE)**

### 2.2 Refactoring Plan

| Module | Status | Action Required |
| :--- | :--- | :--- |
| **Game Loop (`Game.js`)** | Good | Update to support new systems (`ParallaxSystem`, `ParticleSystem`) in the update/render cycle. |
| **Stage Manager** | Needs Update | Refactor to load stage data dynamically from a config object (e.g., `stages.js`). Implement distinct "Enter Stage" and "Exit Stage" transitions (fade in/out). |
| **Lighting System** | Too Simple | **Rewrite completely.** Implement 2D dynamic lighting with radial gradients, "vignette" effects for darkness, and potential simple occlusion/shadow casting if performance allows. |
| **Rendering** | Basic | Add **Parallax Scrolling** support. The simple canvas drawing needs to handle multiple background layers moving at different speeds. |
| **Entities** | Standard | Update `Player` and `Item` entities to support new visual states (e.g., "Silhouette" mode in unlit areas). |

## 3. New Systems Development

### 3.1 Parallax Background System (`src/systems/ParallaxSystem.js`)
-   **Goal:** Create depth using multiple background layers.
-   **Implementation:**
    -   Manage an array of `Layer` objects.
    -   Each layer has an image, scroll speed factor (0.1 to 1.0), and offset.
    -   `update(cameraX)` method calculates position based on player/camera movement.

### 3.2 Advanced Lighting System (`src/systems/LightingSystem.js`)
-   **Goal:** "Hollow Knight" style atmosphere.
-   **Features:**
    -   **Global Illumination:** Control base darkness level (Ambient Light).
    -   **Light Sources:** Entities (Player, Glowing Items) emit light.
    -   **Implementation:** Use HTML5 Canvas `globalCompositeOperation = 'multiply'` or `'overlay'` for blending darkness, and `'lighter'` or `'screen'` for light sources.
    -   **Dynamic Effects:** Flicker, pulse, and color tinting per stage.

### 3.3 Particle System (`src/systems/ParticleSystem.js`)
-   **Goal:** Environmental effects (Fog, Spores, Rain, Ash).
-   **Features:**
    -   Object pooling for performance (crucial for rain/ash).
    -   Emitter types: `RainEmitter`, `SporeEmitter`, `DustEmitter`.

### 3.4 Audio System Enhancement (`src/core/Audio.js`)
-   **Goal:** Atmospheric immersion.
-   **Features:**
    -   Implement **Cross-fading** between BGM tracks when changing stages.
    -   Add **Reverb** effect (via Web Audio API `ConvolverNode`) for "Cave" environments.

## 4. Asset Generation Pipeline (Agent Workflow)

Per `agents/docs/architecture_and_philosophy.md`, we will use agents for all asset creation.

### 4.1 Visual Assets (ImageAgent)
-   **Prompt Strategy:** "Hollow Knight style", "Hand-drawn", "Dark atmosphere".
-   **Workflow:**
    1.  **Refactor:** Create `src/config/assets.json` listing all needed assets per stage.
    2.  **Generate:** `ImageAgent` iterates through the list.
    3.  **Review:** Ensure style consistency (e.g., thick outlines, desaturated colors).

### 4.2 Audio Assets (SoundAgent)
-   **Prompt Strategy:** "Melancholic", "Orchestral", "Ambient", "Echoing".
-   **Workflow:**
    1.  Generate looped BGM for each major environment type (5-6 tracks).
    2.  Generate UI and interaction SFX (glass breaking, soul absorption).

## 5. Development Steps (Implementation Plan)

1.  **Stage Config Setup:** Create `src/config/stage_config.js` defining the 10 stages (colors, gravity, speed, spawn tables).
2.  **System Core Implementation:**
    -   Implement `ParallaxSystem`.
    -   Implement `LightingSystem` (v2).
    -   Implement `ParticleSystem`.
3.  **Asset Generation:** Batch generate placeholders or final assets for Stage 1-3 first.
4.  **Game Loop Integration:** Wire new systems into `Game.js`.
5.  **Gameplay Tuning:** Adjust difficulty curves in `stage_config.js` based on playtesting.

## 6. Directory Structure Changes

```text
games/feeding-caiso/src/
├── config/
│   ├── assets.js       # Asset manifest
│   ├── constants.js    # Global constants
│   └── stages.js       # 10-Stage definitions (NEW)
├── core/
│   ├── Game.js         # Modified
│   ├── Audio.js        # Modified (Web Audio API upgrades)
│   └── ...
├── systems/
│   ├── LightingSystem.js # Rewritten
│   ├── ParallaxSystem.js # NEW
│   └── ParticleSystem.js # NEW
└── ...
```

---
*This technical specification is the blueprint for the Phase 6 engineering effort.*
