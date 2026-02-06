import json
import os
import urllib.request
import urllib.error
from typing import Optional, Dict, Any

class LLMService:
    """
    Zero-dependency LLM client for Play Agent.
    Includes specialized mocks for QA log analysis.
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
        if self.mock_mode:
            return self._generate_mock(prompt)

        url = f"{self.BASE_URL}/{self.model}:generateContent?key={self.api_key}"
        
        contents = [{"parts": [{"text": prompt}]}]
        
        payload: Dict[str, Any] = {
            "contents": contents,
            "generationConfig": {
                "temperature": 0.4, # Balanced for QA analysis
                "maxOutputTokens": 4000,
            }
        }
        
        if system_instruction:
             payload["systemInstruction"] = {
                "parts": [{"text": system_instruction}]
             }
            
        try:
            req = urllib.request.Request(
                url, 
                data=json.dumps(payload).encode('utf-8'), 
                headers={'Content-Type': 'application/json'}
            )
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
                return result['candidates'][0]['content']['parts'][0]['text']
        except Exception as e:
            return f"Error: {str(e)}"

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
