import json
import os
import urllib.request
import urllib.error
import time
from typing import Optional, Dict, Any

class LLMService:
    """
    Zero-dependency LLM client using Gemini API via urllib.
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
                "temperature": 0.7,
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
        """Return a plausible mock response based on the prompt type."""
        if "Identify the following elements" in prompt:
            return """
**Genre**: Casual / Arcade Feeding Game
**Core Loop**:
- **Action**: Player throws food at Caiso (the monster).
- **Feedback**: Caiso reacts (Happy/Sad), Audio plays, Particles appear.
- **Reward**: Score increases, Level up unlocks new food.
**Controls**: Mouse Click or Touch (Mobile), Spacebar (PC).
**Win/Loss**:
- **Win**: Feed Caiso until fullness reaches 100%.
- **Loss**: Villagers (lives) reach 0.
**Key Entities**: Caiso (Monster), Player (Avatar), Food Items, Villagers.
"""
        elif "Evaluate the difficulty" in prompt:
            return """
**Difficulty Curve**: Static/Flat.
- The game relies on speed increasing, but the code shows fixed speeds for some elements.
- **Analysis**: The hunger decay rate seems linear (`this.hunger -= 0.1`).
**Progression**:
- New foods unlock at levels 2, 3, 4, 5.
- Visually rewarding but mechanically identical (just different textures).
**Risk vs Reward**:
- Low risk. Missed shots have no penalty specific enough other than time loss.
**Issues**:
- No 'Game Over' state handled robustly in some edge cases.
"""
        elif "Propose a compelling narrative" in prompt:
            return """
**Title Proposal**: "Caiso's Midnight Snack"
**The World**: A neon-lit cyber-city where 'Caiso' is a guardian kaiju.
**The Protagonist**: 'Chef K', a legendary food truck owner capable of feeding titans.
**Conflict**: Caiso gets 'Hangry' and threatens to eat the city's power grid (represented by villagers).
**Flavor Text**:
- Start: "Order Up! Feed the Beast!"
- Game Over: "The City went Dark..."
- Level Up: "Expansion Pack Unlocked!"
"""
        return "Mock Analysis Response"

# Convenience instance
def get_llm():
    return LLMService()
