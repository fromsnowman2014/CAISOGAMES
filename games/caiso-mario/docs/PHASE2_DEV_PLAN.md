# Phase 2 Development Plan: "The Visual Upgrade"

## Goal
Transform **Caiso Mario** from a procedural canvas prototype into a polished, asset-rich platformer using the Image Generator API. Refactor the codebase to support scalable asset loading and game logic.

## 1. Architecture Refactor
**Objective**: Break the `index.html` monolith.

- [ ] **Folder Structure Setup**
    ```
    games/caiso-mario/
    ├── index.html          (Entry point)
    ├── assets/             (Generated images)
    │   ├── sprites/
    │   ├── tiles/
    │   └── backgrounds/
    └── src/
        ├── main.js         (Game Loop)
        ├── config.js       (Constants)
        ├── systems/
        │   ├── AssetManager.js
        │   ├── Input.js
        │   └── Physics.js
        └── entities/
            ├── Player.js
            └── Enemy.js
    ```

- [ ] **Module Implementation**
    - Convert global objects (`PHYSICS`, `Input`) to ES6 modules.
    - Create `AssetManager` to handle asynchronous image loading.

## 2. Asset Integration Pipeline
**Objective**: Replace `Sprites.create*()` methods with real image rendering.

- [ ] **Asset Generation (using API)**
    - Generate all required assets defined in `ASSET_GENERATION_GUIDE.md`.
    - Verify transparency and aspect ratios.
    - Save to `assets/` folder.

- [ ] **Sprite Rendering System**
    - Update `draw()` methods in entities to use `ctx.drawImage` instead of `ctx.fillRect`.
    - Implement a simple **Animator** class to handle frame switching (Idle -> Run).

## 3. Gameplay Enhancements
**Objective**: Deepen the "Chess" mechanics.

- [ ] **Enemy AI Upgrade**
    - **Knight**: Implement parabolic jump arc physics.
    - **Bishop**: Implement line-of-sight diagonal raycasting.
    - **Rook**: Implement "see player -> charge" logic.

- [ ] **Juice Effects**
    - **Particles**: Create a particle system for dust, sparks, and debris.
    - **Screen Shake**: Add `Camera.shake()` on impacts.

## 4. Execution Steps

1.  **Setup**: Create folders and move existing logic into modules.
2.  **Generate**: Run batch generation scripts for all core assets.
3.  **Integrate**: Swap the Player drawing code first.
4.  **Expand**: Swap Enemy and Tile codes.
5.  **Polish**: Add backgrounds and UI.

## 5. Review Criteria
- [ ] No `ctx.fillRect` used for characters (only debug boxes).
- [ ] Game runs at 60 FPS with full image assets.
- [ ] Folder structure is modular.
