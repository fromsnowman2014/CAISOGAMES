"""Play Agent LLM Service - extends shared LLM with QA analysis mocks."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from agents.shared.llm import LLMService as BaseLLMService


class LLMService(BaseLLMService):
    """LLM Service with Play Agent specific mock responses."""

    def __init__(self, **kwargs):
        kwargs.setdefault("temperature", 0.4)
        super().__init__(**kwargs)

    def _generate_mock(self, prompt: str) -> str:
        """Mock responses for Play Agent QA Analysis."""

        if "QA Engineer" in prompt or "Gameplay Logs" in prompt:
            return """
### 1. Stability Assessment
- **Crash Rate**: 0% (in observed session).
- **Errors**: No critical JS errors found.
- **Performance**: Average FPS 58. Stable rendering loop.

### 2. Gameplay Issues
- **Hit Detection**: Occasional miss when projectile hits the very edge of Caiso's sprite.
- **Input Lag**: Touch events simulated with 50ms delay showed no significant lag.
- **State Validity**: Score updated correctly (incrementing by 10).

### 3. Recommendations
- **Optimize Hitbox**: Increase Caiso's hitbox by 5px to improve "Game Feel".
- **Monitor FPS**: Slight drop detected during particle explosion (58 -> 45 FPS). Optimize particle pool.
"""
        return "Mock QA Report"


def get_llm():
    return LLMService()
