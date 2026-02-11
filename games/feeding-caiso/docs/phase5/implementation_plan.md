# Phase 5 Implementation Plan: Ethereal Evolution

## Goal Description
Transform "Feeding Caiso" from a "Neon Kawaii" arcade game into a "Zen/Ethereal" experience. This involves a complete visual overhaul, a structural refactor to support a 10-stage progression system, and the introduction of new gameplay mechanics (wind, gravity, lighting) based on the "Nature's Cycle" theme.

## Architecture & Code Changes

### 1. Core Engine Refactoring
We need to decouple the game logic to support distinct stages with unique properties.

#### [NEW] `src/core/StageManager.js`
- Responsibilities:
    - Manage the current stage index (0-9).
    - Load stage configuration from `stages.json` (or internal config object).
    - Handle transitions between stages (fade out/in, asset swapping).
    - Trigger "Level Up" events that change the environment.

#### [NEW] `src/core/Environment.js`
- Responsibilities:
    - Handle stage-specific physics and effects.
    - **Wind**: Apply forces to falling objects (x-axis push).
    - **Gravity**: Modify global gravity (y-axis acceleration).
    - **Visuals**: Manage background layers (parallax).

#### [NEW] `src/systems/LightingSystem.js`
- Responsibilities:
    - Render full-screen overlay gradients to simulate time of day (Dawn, Noon, Dusk, Night).
    - Apply "Global Illumination" feel (tinting game objects).

#### [MODIFY] `src/core/Game.js`
- **Changes**:
    - Remove hardcoded level progression.
    - Integrate `StageManager`, `Environment`, and `LightingSystem`.
    - Update the main game loop to delegate updates to these new systems.

### 2. Gameplay Mechanics
- **Progression**: Implement the 10-stage flow.
- **Entities**: Refactor `Food` and `Obstacle` classes to support new types (Essence, Nature Hazards).
- **Physics**: Update physics engine to respect `Environment` modifiers (Wind, Gravity).

### 3. UI/UX Overhaul
- **Style**: Glassmorphism (translucent backgrounds, blur, thin borders).
- **HUD**: Replace arcade score with a "Harmony" or "Balance" progress bar.
- **Font**: Switch to a clean, sans-serif font (Montserrat/Quicksand).

## Implementation Steps

### Step 1: Foundation & Refactoring
1.  Create `StageManager.js`, `Environment.js`, `LightingSystem.js` scaffolds.
2.  Define the `stages` configuration object (Stage 1-10 specs).
3.  Refactor `Game.js` to initialize these systems.
4.  Standardize the asset loading pipeline to support per-stage assets.

### Step 2: Visual & Atmospheric Systems
1.  Implement `LightingSystem` to draw gradient overlays.
2.  Implement `Environment` background rendering (placeholders initially).
3.  Apply the "Glassmorphism" CSS to the HUD.

### Step 3: Mechanics - Physics & Interaction
1.  Update `Physics.js` (or inline physics logic) to accept external forces from `Environment` (Wind).
2.  Implement variable gravity logic.
3.  Create the mechanics for Stage 1 (morning dew behaviors).

### Step 4: Content - Stages 1-3 (Morning to Noon)
1.  Configure Stage 1 (Dawn): Calm, standard gravity.
2.  Configure Stage 2 (Morning): Active, insect hazards.
3.  Configure Stage 3 (Noon): Wind mechanic introduction.

### Step 5: Content - Stages 4-6 (Afternoon to Dusk)
1.  Stage 4 (Harvest): Visual clutter (leaves).
2.  Stage 5 (Sunset): Cooling air (physics tweak).
3.  Stage 6 (Twilight): Low visibility/darkness.

### Step 6: Content - Stages 7-10 (Night to Cosmic)
1.  Stage 7 (Moonlit): Ripples/Distortion (shader or canvas effect).
2.  Stage 8 (Starry): Fast falling stars.
3.  Stage 9 (Aurora): Magnetic/Curved paths.
4.  Stage 10 (Cosmic): Gravity shifts.

## Verification Plan

### Automated Tests
- **Unit Tests**:
    - Test `StageManager` transitions (index increment, config loading).
    - Test `Environment` physics modifiers (wind force calculation).
- **Browser Tests**:
    - Verify game loads without errors.
    - Verify clicking "Start" enters Stage 1.

### Manual Verification
- **Visual Check**:
    - Verify gradient overlays match the time of day.
    - Verify UI looks "Glassmorphic".
- **Gameplay Check**:
    - Play through Stage 1 to Stage 2 transition.
    - Observe Wind effect in Stage 3 (objects drift).
    - Observe Gravity smoothing in later stages.

