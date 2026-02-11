"""
Vercel Serverless Function: Code Analysis Proxy

This endpoint allows code_agent to analyze game code via Gemini API.

Usage:
  POST /api/analyze-code
  {
    "type": "structure",  // structure | performance | mobile
    "code": "// Game source code...",
    "context": "Additional context (optional)"
  }

Returns:
  {
    "success": true,
    "analysis": "# Code Analysis Report..."
  }
"""

import os
import json
from http.server import BaseHTTPRequestHandler
import httpx

# Gemini API configuration
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')
BASE_URL = "https://generativelanguage.googleapis.com/v1beta"
MODEL = "gemini-3-pro-preview"

def get_structure_prompt(code: str) -> str:
    return f"""You are a Senior Game Developer and Software Architect.
Analyze the following game code structure and quality.

**Code:**
```javascript
{code[:20000]}
```

**Task:**
1. **Architecture Overview**: Explain the high-level structure.
2. **Code Quality**: Identify patterns (Modular vs Monolithic? Clean code?).
3. **Maintainability**: Flag global variables, callback hell, or coupled logic.
4. **Key Recommendations**: 3 concrete refactoring steps.

Output a structured markdown report."""

def get_performance_prompt(code: str) -> str:
    return f"""You are a Game Performance Optimization Specialist.
Audit the following game code for performance bottlenecks.

**Code:**
```javascript
{code[:20000]}
```

**Task:**
1. **Rendering Loop**: Analyze `requestAnimationFrame` and canvas drawing usage.
2. **Memory**: Check for object creation in loops (GC pressure).
3. **Assets**: Review image/sound loading strategies.
4. **Optimization Plan**: List prioritized optimizations.

Output a structured markdown report."""

def get_mobile_prompt(code: str) -> str:
    return f"""You are a Mobile Web Game Specialist.
Analyze the following game code for mobile compatibility.

**Code:**
```javascript
{code[:20000]}
```

**Task:**
1. **Touch Controls**: Does it handle `touchstart`/`touchend`?
2. **Responsive Design**: Is canvas resizing handled for mobile screens?
3. **Constraints**: Check for heavy operations unsuitable for mobile.
4. **Action Plan**: Steps to make it "Mobile-First".

Output a structured markdown report."""

async def generate_with_gemini(prompt: str) -> str:
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY not configured")
    
    url = f"{BASE_URL}/models/{MODEL}:generateContent"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.4, "maxOutputTokens": 4000}
    }
    params = {"key": GEMINI_API_KEY}
    
    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(url, json=payload, params=params)
        if response.status_code != 200:
            raise Exception(f"API Error: {response.text}")
            
        data = response.json()
        return data['candidates'][0]['content']['parts'][0]['text']

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            data = json.loads(body) if body else {}
            
            analysis_type = data.get('type', 'structure')
            code = data.get('code', '')
            
            if not code:
                raise ValueError("Source code is required")
                
            if analysis_type == 'structure':
                prompt = get_structure_prompt(code)
            elif analysis_type == 'performance':
                prompt = get_performance_prompt(code)
            elif analysis_type == 'mobile':
                prompt = get_mobile_prompt(code)
            else:
                raise ValueError(f"Unknown type: {analysis_type}")
            
            import asyncio
            result = asyncio.run(generate_with_gemini(prompt))
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'success': True, 'analysis': result}).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'success': False, 'error': str(e)}).encode())

    def do_GET(self):
        """Health check endpoint."""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({
            'status': 'ok',
            'endpoint': '/api/analyze-code',
            'method': 'POST',
            'types': ['structure', 'performance', 'mobile'],
            'model': MODEL,
            'api_configured': bool(GEMINI_API_KEY)
        }).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
