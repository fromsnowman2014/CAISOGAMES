"""
Sound Maker Service - Client for Vercel Sound Generation API

This module provides a client to call the /api/generate-sound endpoint
for generating Web Audio API SFX and Tone.js BGM code.
"""

import os
import json
import urllib.request
import urllib.error
from typing import Optional, Dict, Any


class SoundMakerService:
    """
    Client for the Sound Generation API hosted on Vercel.
    
    Usage:
        service = SoundMakerService()
        sfx_code = service.generate_sfx("button_click", "Short click sound", 100)
        bgm_code = service.generate_bgm("gameplay", "ingame", "energetic", 120)
    """
    
    DEFAULT_URL = "https://caisogames.vercel.app"
    
    def __init__(self, base_url: Optional[str] = None):
        """
        Initialize the Sound Maker Service.
        
        Args:
            base_url: Vercel app URL (uses VERCEL_APP_URL env var if not provided)
        """
        self.base_url = base_url or os.getenv("VERCEL_APP_URL", self.DEFAULT_URL)
        self.endpoint = f"{self.base_url}/api/generate-sound"
    
    def _call_api(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Make API request to the sound generation endpoint."""
        try:
            req = urllib.request.Request(
                self.endpoint,
                data=json.dumps(data).encode('utf-8'),
                headers={'Content-Type': 'application/json'},
                method='POST'
            )
            
            with urllib.request.urlopen(req, timeout=60) as response:
                result = json.loads(response.read().decode('utf-8'))
                return result
                
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            try:
                error_data = json.loads(error_body)
                raise Exception(f"API Error: {error_data.get('error', str(e))}")
            except json.JSONDecodeError:
                raise Exception(f"API Error {e.code}: {e.reason}")
                
        except urllib.error.URLError as e:
            raise Exception(f"Connection Error: {str(e)}")
    
    def check_health(self) -> Dict[str, Any]:
        """Check if the API is available and configured."""
        try:
            req = urllib.request.Request(self.endpoint, method='GET')
            with urllib.request.urlopen(req, timeout=10) as response:
                return json.loads(response.read().decode('utf-8'))
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def generate_sfx(
        self,
        name: str,
        description: str,
        duration: int = 200,
        category: str = "ui"
    ) -> str:
        """
        Generate Web Audio API code for a sound effect.
        
        Args:
            name: Sound name (e.g., "button_click")
            description: Description of the sound
            duration: Duration in milliseconds
            category: Category (ui, gameplay, feedback)
            
        Returns:
            JavaScript code string
        """
        result = self._call_api({
            "type": "sfx",
            "params": {
                "name": name,
                "description": description,
                "duration": duration,
                "category": category
            }
        })
        
        if not result.get('success'):
            raise Exception(result.get('error', 'Unknown error'))
        
        return result.get('code', '')
    
    def generate_bgm(
        self,
        track_name: str,
        scene: str,
        mood: str,
        tempo: int = 120
    ) -> str:
        """
        Generate Tone.js code for background music.
        
        Args:
            track_name: Name for the BGM track
            scene: Scene type (menu, gameplay, gameover)
            mood: Mood description
            tempo: BPM
            
        Returns:
            JavaScript code string
        """
        result = self._call_api({
            "type": "bgm",
            "params": {
                "track_name": track_name,
                "scene": scene,
                "mood": mood,
                "tempo": tempo
            }
        })
        
        if not result.get('success'):
            raise Exception(result.get('error', 'Unknown error'))
        
        return result.get('code', '')
    
    def audit_sounds(self, source_code: str) -> str:
        """
        Analyze a game's sound implementation.
        
        Args:
            source_code: Game HTML/JS source code
            
        Returns:
            Markdown analysis text
        """
        result = self._call_api({
            "type": "audit",
            "source_code": source_code
        })
        
        if not result.get('success'):
            raise Exception(result.get('error', 'Unknown error'))
        
        return result.get('code', '')


# Convenience function
def get_sound_maker() -> SoundMakerService:
    """Get a configured SoundMakerService instance."""
    return SoundMakerService()
