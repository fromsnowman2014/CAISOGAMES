# Feeding Caiso Phase 5: Natural & Sophisticated (Ethereal Evolution)

## 1. Competitive Analysis & Inspiration

### **Comparison Target: Donut County & Alto's Odyssey**

To achieve a "Modern, Natural, and Sophisticated" feel, we will pivot from the current "Neon Kawaii" (High Contrast/Arcade) style to a **"Zen/Ethereal"** aesthetic.

| Feature | **Feeding Caiso (Current)** | **Donut County** (Inspiration 1) | **Alto's Odyssey** (Inspiration 2) | **Phase 5 Target** |
| :--- | :--- | :--- | :--- | :--- |
| **Visual Style** | Neon, Pixel/Vector, Dark Background | Low-poly, Pastel, Clean, Physics-based | Minimalist, Gradient heavy, Weather effects | **Soft Vector Art, Dynamic Gradients, Organic lighting** |
| **Gameplay** | Fast-paced, Arcade, Survival | Relaxing but destructive, Physics puzzle | Flow-state, Endless runner, Trick-based | **Rhythmic Feeding, Stage Progression, interactive environments** |
| **Structure** | Endless Leveling | Story-driven Levels | Endless Biomes | **10 Distinct Stages with Narrative Progression** |
| **Difficulty** | Linear ramping speed | Puzzle complexity | Speed & Obstacle density | **Environmental challenges + Resource Scarcity** |
| **Addictiveness**| High Score / fever loops | Curiosity / "Completion" satisfaction | "Just one more run" / Audio-visual flow | **Unlockable Aesthetics, Calm "Flow" State** |

### **Why this direction?**
- **Modern Trend**: Mobile games are moving towards "Cozy" and "Healing" experiences (e.g., *Cats & Soup*).
- **Differentiation**: Moving away from the generic "Arcade" look makes it feel more premium.
- **Sophistication**: Using natural palettes and fluid animations creates a sense of quality.

---

## 2. Phase 5 Concept: "Nature's Cycle"

**Theme**: Caiso is a spirit of nature. Instead of "eating to survive", Caiso "absorbs elements to restore balance".
**Villagers**: Replaced by **"Lost Spirits"** or **"Wandering Wisps"** that need guidance (protection).
**Food**: Replaced by **"Essence"** (Dew drops, Sun rays, Moon beams, Star fragments).

### **10-Stage Progression Plan**

Each stage represents a time of day or environment, influencing the color palette and "Food" types.

| Stage | Name | Time/Theme | Palette | Food / Essence | Hazard / Challenge |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | **Morning Dew** | Dawn (6 AM) | Soft Teal, Pale Gold, White | Dew Drops | Birds (stealing dew) |
| **2** | **Sunlit Bloom** | Morning (9 AM) | Vibrant Green, Yellow, Pink | Flower Nectar | Bees/Insects |
| **3** | **Whispering Breeze**| Noon (12 PM) | Sky Blue, Cloud White | Wind Gusts (Invisible/Semi-transparent) | Strong Winds (pushes food away) |
| **4** | **Golden Harvest** | Afternoon (3 PM) | Amber, Orange, Wheat Gold | Grains/Seeds | Falling Leaves (visual clutter) |
| **5** | **Crimson Sunset** | Sunset (6 PM) | Deep Orange, Purple, Red | Sun Embers | Cooling Air (slower movement) |
| **6** | **Twilight Grove** | Dusk (8 PM) | Indigo, Violet, Bioluminescent Blue | Glowing Mushrooms | Shadows (obscure view) |
| **7** | **Moonlit Lake** | Night (10 PM) | Silver, Navy Blue, Black | Moon Reflections | Ripples (distort position) |
| **8** | **Starry Expanse** | Midnight (12 AM) | Deep Space Blue, Starlight White | Star Fragments | Shooting Stars (fast moving food) |
| **9** | **Aurora Borealis** | Deep Night | Neon Green (Soft), Magenta | Aurora Waves | Magnetic Fields (curved throw paths) |
| **10** | **Cosmic Dawn** | The Void/Rebirth | Iridescent, Holo, Prism | Pure Light / Prisms | Gravity Shifts |

---

## 3. Implementation Plan & Agent Integration

We will use the **CAISOGAMES Agents** to execute this plan efficiently.

### **Step 1: Structural Refactoring (Code Agent)**
- **Objective**: Refactor `Game.js` to support a `StageManager` that handles the 10 distinct stages, asset loading per stage, and unique mechanics (Gravity, Wind).
- **Agent Usage**:
    - **`code_agent`**: Run analysis on `src/core/Game.js` to identify coupling that prevents easy stage switching.
    - **Task**: "Analyze `Game.js` for hardcoded dependencies and propose a `Stage` interface pattern."
    - **Reference**: `agents/code_agent/README.md` (Use `python -m agents.code_agent.agent ...`).

### **Step 2: Asset Generation (Image Agent / Generator)**
- **Objective**: Create "Sophisticated" assets for all 10 stages.
- **Style Prompt**: *"Vector art, minimalist, gradient shading, soft lighting, mobile game asset, [Stage Theme Specifics]"*
- **Agent Usage**:
    - **`image_generator`**:
        - Generate 10 Backgrounds (Parallax ready).
        - Generate Caiso "Skins" (Evolution tiers matching the theme).
        - Generate "Food" icons (Dew, Star, etc.).
    - **Process**:
        1. Define Prompts in `phase5/assets_req.yaml`.
        2. Run generator.
        3. Review and refine and enhance to get the 90% quality (repeat 5 times as maximum).

### **Step 3: Gameplay Mechanics (Code Agent / Play Agent)**
- **Objective**: Implement the mechanics (Wind, Gravity, Lighting).
- **Agent Usage**:
    - **`code_agent`**: Review the implementation of physics (wind/gravity) for performance bottlenecks.
    - **`play_agent`**:
        - **Making**: Enhance a detailed plan about 10 stages with different difficulty levels/items/obstacles/graphics. difficulty goes up as the stage goes up.
        - **Training**: use the agent review and enhance the difficulty of the stages 
        - **Balancing**: Use the agent to find the optimal difficulty (spawn rates, wind speed) for each stage to ensure it is "Challenging but Relaxing" (Flow state).
        - **Feedback**: Adjust parameters based on agent's failure rate.

### **Step 4: UI/UX Polish (Design Agent - Concept)**
- **Objective**: Minimalist UI. Glassmorphism HUD.
- **Plan**:
    - Remove "Arcade" score counters. Replace with subtle progress bars.
    - Use sophisticated fonts (e.g., *Montserrat* or *Quicksand*).
    - **Agent Usage**: Use LLM to generate CSS for "Glassmorphism" consistent with the new palette.

---

## 4. Technical Architecture Updates

### New Classes
- `StageManager.js`: Handles transitions, asset pre-loading for next stage.
- `Environment.js`: Handles stage-specific effects (Wind, Lighting, Gravity).
- `LightingSystem.js`: Renders overlay gradients for time-of-day feel.

### Data Structure (`stages.json`)
```json
{
  "stage_1": {
    "name": "Morning Dew",
    "background": "bg_dawn.png",
    "palette": ["#E0F7FA", "#FFF8E1"],
    "mechanic": "none",
    "duration": 60
  },
  "stage_9": {
    "name": "Aurora",
    "background": "bg_aurora.png",
    "mechanic": "curved_path",
    "physics": { "gravity_y": 0.5 }
  }
}
```

## 5. Next Steps

1.  **Approve Plan**: User to review this document.
2.  **Generate Assets**: Start with Stage 1 & 2 (Dawn/Morning).
3.  **Refactor Code**: Extract `Stage` logic.
4.  **Prototype**: Build Stage 1.
