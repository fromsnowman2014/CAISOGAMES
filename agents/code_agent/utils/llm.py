import json
import os
import urllib.request
import urllib.error
import time
from typing import Optional, Dict, Any

class LLMService:
    """
    Zero-dependency LLM client using Gemini API via urllib.
    Identical to DesignAgent's LLMService but with CodeAgent specific mocks.
    """
    
    BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models"
    DEFAULT_MODEL = "gemini-1.5-flash"
    
    def __init__(self, api_key: Optional[str] = None, model: str = DEFAULT_MODEL):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        self.model = model
        if not self.api_key:
            print("⚠️ Warning: GEMINI_API_KEY not found. Using Mock LLM mode.")
            self.mock_mode = True
        else:
            self.mock_mode = False
            
    def generate(self, prompt: str, system_instruction: Optional[str] = None) -> str:
        """
        Generate text response from Gemini (or Mock).
        """
        if self.mock_mode:
            return self._generate_mock(prompt)

        url = f"{self.BASE_URL}/{self.model}:generateContent?key={self.api_key}"
        
        # Construct payload
        contents = [{"parts": [{"text": prompt}]}]
        
        # Add system instruction if supported (Gemini 1.5 supports it)
        payload: Dict[str, Any] = {
            "contents": contents,
            "generationConfig": {
                "temperature": 0.2, # Lower temperature for code analysis
                "maxOutputTokens": 4000,
            }
        }
        
        if system_instruction:
             payload["systemInstruction"] = {
                "parts": [{"text": system_instruction}]
             }
            
        data = json.dumps(payload).encode('utf-8')
        
        req = urllib.request.Request(
            url, 
            data=data, 
            headers={'Content-Type': 'application/json'}
        )
        
        try:
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
                
                # Parse response
                try:
                    candidates = result.get('candidates', [])
                    if not candidates:
                        return "Error: No candidates returned from API."
                        
                    content = candidates[0].get('content', {})
                    parts = content.get('parts', [])
                    if not parts:
                        return "Error: Empty response parts."
                        
                    return parts[0].get('text', '')
                    
                except (KeyError, IndexError) as e:
                    return f"Error parsing API response: {str(e)}"
                    
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            return f"API Error {e.code}: {e.reason}\nDetails: {error_body}"
        except Exception as e:
            return f"Network Error: {str(e)}"

    def _generate_mock(self, prompt: str) -> str:
        """Return a plausible mock response based on the prompt type for Code Agent."""
        
        # Match keywords from prompts/analyze_structure.txt
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
        # Match keywords from prompts/optimize_performance.txt
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
        # Match keywords from prompts/mobile_support.txt
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

# Convenience instance
def get_llm():
    return LLMService()
