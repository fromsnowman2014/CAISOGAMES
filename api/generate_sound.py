"""
Vercel Serverless Function: Sound Generation Proxy

This endpoint allows sound_agent to generate sound code via Gemini API
by proxying requests through Vercel where the API key is stored.

Usage:
  POST /api/generate-sound
  {
    "type": "sfx",           // sfx | bgm | audit
    "prompt": "button click sound",
    "params": {
      "name": "button_click",
      "duration": 100,
      "category": "ui"
    }
  }

Returns:
  {
    "success": true,
    "code": "// JavaScript code...",
    "type": "sfx"
  }
"""

import os
import json
import urllib.request
import urllib.error
from http.server import BaseHTTPRequestHandler

# Gemini API configuration
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')
BASE_URL = "https://generativelanguage.googleapis.com/v1beta"

# Models
# Use Pro for high-quality code generation (SFX/BGM)
MODEL_CODE = "gemini-3-pro-preview"
# Use same model for analysis/audit
MODEL_AUDIT = "gemini-3-pro-preview"


def get_sfx_prompt(params: dict) -> str:
    """Generate prompt for SFX code generation."""
    name = params.get('name', 'sound')
    description = params.get('description', 'a sound effect')
    duration = params.get('duration', 200)
    category = params.get('category', 'ui')
    
    return f"""You are an Expert Audio Programmer generating Web Audio API code.

Generate JavaScript code to create the following sound effect:

**Sound Name**: {name}
**Description**: {description}
**Duration**: {duration}ms
**Category**: {category}

Requirements:
1. Use only Web Audio API (no external libraries)
2. Create a self-contained function
3. Include AudioContext management (handle user gesture requirement)
4. Keep code minimal but functional
5. Add brief comments explaining the synthesis

Output ONLY valid JavaScript code that can be directly used. No markdown, no explanation, just the code."""


def get_bgm_prompt(params: dict) -> str:
    """Generate prompt for BGM code generation."""
    track_name = params.get('track_name', 'gameplay')
    scene = params.get('scene', 'ingame')
    mood = params.get('mood', 'energetic')
    tempo = params.get('tempo', 120)
    
    return f"""You are an Expert Music Programmer generating Tone.js background music code.

Generate JavaScript code to create the following background music:

**Track Name**: {track_name}
**Scene**: {scene}
**Mood**: {mood}
**Tempo**: {tempo} BPM
**Looping**: Yes

Requirements:
1. Use Tone.js library
2. Create a loopable pattern
3. Include start/stop functions
4. Keep it simple but musically interesting
5. Use 2-3 instrument layers maximum
6. Include volume control

Output ONLY valid JavaScript code that works with Tone.js. No markdown, no explanation, just the code."""


def get_audit_prompt(source_code: str) -> str:
    """Generate prompt for sound audit analysis."""
    # Truncate source code if too long
    truncated = source_code[:20000] if len(source_code) > 20000 else source_code
    
    return f"""You are an Expert Game Sound Designer analyzing a game's audio implementation.

Analyze the following game source code and identify:

## 1. Existing Audio Implementation
- Any <audio> tags or Audio() objects
- Web Audio API usage
- Sound file references (.mp3, .wav, .ogg)
- Volume controls or audio settings

## 2. Game Events Needing Sounds
Identify all events in the code that would benefit from sound effects:
- User interactions (clicks, touches, keypresses)
- Game state changes (start, pause, game over)
- Object interactions (collisions, pickups, spawns)
- Feedback moments (success, failure, achievements)

## 3. Sound Gap Analysis
List specific sounds that are MISSING but would significantly improve the game experience.

## 4. Sound Priority List
Rank the top 5 most important missing sounds by impact on player experience.

---

**Game Source Code:**
```html
{truncated}
```

---

Provide your analysis in markdown format with clear sections."""


def call_gemini_api(prompt: str, model: str) -> str:
    """Call Gemini API via urllib (Zero Dependency)."""
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY not configured")
    
    url = f"{BASE_URL}/models/{model}:generateContent?key={GEMINI_API_KEY}"
    
    payload = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 4000,
        }
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        url,
        data=data,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode('utf-8'))
            
            candidates = result.get('candidates', [])
            if not candidates:
                raise Exception("No candidates returned")
                
            content = candidates[0].get('content', {})
            parts = content.get('parts', [])
            if not parts:
                blocked = candidates[0].get('finishReason')
                if blocked:
                    raise Exception(f"Blocked by safety settings: {blocked}")
                raise Exception("Empty response content")
                
            return parts[0].get('text', '')
            
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        try:
            error_json = json.loads(error_body)
            msg = error_json.get('error', {}).get('message', str(e))
            if e.code == 429:
                 raise Exception("Rate limit exceeded")
            raise Exception(f"API Error {e.code}: {msg}")
        except:
            raise Exception(f"API Error {e.code}: {e.reason} - {error_body}")
    except Exception as e:
        raise Exception(f"Request failed: {str(e)}")


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Read request body
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            data = json.loads(body) if body else {}
            
            # Extract parameters
            gen_type = data.get('type', 'sfx')
            params = data.get('params', {})
            
            # Build prompt and select model based on type
            if gen_type == 'sfx':
                prompt = get_sfx_prompt(params)
                model = MODEL_CODE
            elif gen_type == 'bgm':
                prompt = get_bgm_prompt(params)
                model = MODEL_CODE
            elif gen_type == 'audit':
                source_code = data.get('source_code', '')
                if not source_code:
                    raise ValueError("source_code is required for audit type")
                prompt = get_audit_prompt(source_code)
                model = MODEL_AUDIT
            else:
                raise ValueError(f"Unknown type: {gen_type}")
            
            # Generate with Gemini
            result = call_gemini_api(prompt, model)
            
            # Clean up code (remove markdown code blocks if present)
            code = result.strip()
            if code.startswith('```') and gen_type != 'audit':
                lines = code.split('\n')
                # Remove first line (```javascript) and last line (```)
                if len(lines) >= 2:
                    code = '\n'.join(lines[1:-1] if lines[-1].strip() == '```' else lines[1:])
            
            # Send success response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                'success': True,
                'type': gen_type,
                'code': code,
                'model': model
            }).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                'success': False,
                'error': str(e)
            }).encode())
    
    def do_OPTIONS(self):
        """Handle CORS preflight."""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_GET(self):
        """Health check endpoint."""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({
            'status': 'ok',
            'endpoint': '/api/generate-sound',
            'method': 'POST',
            'types': ['sfx', 'bgm', 'audit'],
            'models': {'code': MODEL_CODE, 'audit': MODEL_AUDIT},
            'api_configured': bool(GEMINI_API_KEY)
        }).encode())
