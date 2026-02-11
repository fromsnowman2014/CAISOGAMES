"""Code Agent LLM Service - extends shared LLM with code analysis mocks."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from agents.shared.llm import LLMService as BaseLLMService


class LLMService(BaseLLMService):
    """LLM Service with Code Agent specific mock responses."""

    def __init__(self, **kwargs):
        kwargs.setdefault("temperature", 0.2)
        super().__init__(**kwargs)

    def _generate_mock(self, prompt: str) -> str:
        """Return a plausible mock response based on the prompt type for Code Agent."""

        if "Architecture Overview" in prompt or "Code Quality Audit" in prompt:
            return """
### 1. Code Logic & Structure
- **Game Engine**: Custom vanilla JS engine using `requestAnimationFrame`.
- **State Management**: Distributed global variables (`score`, `lives`, `gameState`).
- **Modularity**: Low. Single monolithic file structure detected.
- **Event Handling**: Direct `addEventListener` usage mixed with game logic.

### 2. Design Patterns
- **Game Loop**: Standard update/draw loop pattern.
- **Object Pooling**: Not detected. Frequent object creation/deletion observed (Garbage Collection risk).
- **Component System**: None. Inheritance based entities.

### 3. Maintainability
- **Magic Numbers**: High usage of hardcoded values for physics/positioning.
- **Comments**: Sparse. Key logic lacks documentation.
- **Naming**: Generally clear variables, but inconsistent casing in some functions.
"""
        elif "Performance Optimization Expert" in prompt or "Rendering Loop" in prompt:
            return """
### Performance Audit
- **Rendering**: Uses `CanvasRenderingContext2D`. No offscreen canvas usage.
- **Garbage Collection**: Objects are created in the loop (e.g., `new Projectile()`). Recommend Object Pooling.
- **Event Listeners**: Attached globally, no cleanup on game restart. Potential memory leak.
- **Asset Loading**: Synchronous image loading detected. Should use `Promise.all` or an Asset Manager.

### Optimization Plan
1. **Implement Object Pool** for Projectiles and Particles.
2. **Cache DOM queries** outside the game loop.
3. **Use OffscreenCanvas** for static background layers.
4. **Debounce** resize events.
"""
        elif "Mobile Web Game Specialist" in prompt or "Touch Controls" in prompt:
            return """
### Mobile Adaptation Strategy
1. **Touch Controls**:
   - Add virtual joystick for movement (if applicable).
   - Implement `touchstart` handling for "Throw" action.
2. **Responsive Canvas**:
   - Canvas currently fixed size. Needs `window.innerWidth/Height` scaling.
   - CSS `touch-action: none` required to prevent scrolling.
3. **UI Scaling**:
   - Buttons and text need to be larger on small screens (min 44px target).
"""

        return "Mock Code Analysis Response"


def get_llm():
    return LLMService()
