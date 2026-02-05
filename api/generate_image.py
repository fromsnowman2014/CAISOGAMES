"""
Vercel Serverless Function: Image Generation Proxy

This endpoint allows Claude Code to generate images via Gemini API
by proxying requests through Vercel where the API key is stored.

Usage:
  POST /api/generate-image
  {
    "prompt": "pixel art monster character",
    "width": 512,
    "height": 512,
    "style": "pixel_art"
  }

Returns:
  {
    "success": true,
    "image": "base64_encoded_image_data",
    "format": "png",
    "width": 512,
    "height": 512
  }
"""

import os
import json
import base64
from http.server import BaseHTTPRequestHandler
import httpx

# Gemini API configuration
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')
BASE_URL = "https://generativelanguage.googleapis.com/v1beta"
# Use Gemini native image generation model (works with v1beta API)
MODEL = "gemini-2.0-flash-exp-image-generation"


def get_style_prompt(style: str) -> str:
    """Get style-specific prompt additions."""
    styles = {
        'pixel_art': 'Style: 16-bit retro pixel art, limited color palette, crisp pixels, no anti-aliasing, transparent background.',
        'cartoon': 'Style: cartoon illustration, bold outlines, vibrant colors, clean shapes, transparent background.',
        'realistic': 'Style: photorealistic, detailed textures, natural lighting.',
        'sketch': 'Style: hand-drawn sketch, pencil lines, artistic shading.',
        'sprite': 'Style: game sprite, clean edges, transparent background, suitable for 2D game.',
    }
    return styles.get(style, styles['pixel_art'])


async def generate_image(prompt: str, width: int = 512, height: int = 512, style: str = 'pixel_art'):
    """Generate image using Gemini image generation API."""
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY not configured")

    style_prompt = get_style_prompt(style)
    full_prompt = f"{prompt}. {style_prompt}"

    # Use generateContent endpoint with image generation model
    url = f"{BASE_URL}/models/{MODEL}:generateContent"

    payload = {
        "contents": [{
            "parts": [{
                "text": full_prompt
            }]
        }],
        "generationConfig": {
            "responseModalities": ["image", "text"]
        }
    }

    params = {"key": GEMINI_API_KEY}

    async with httpx.AsyncClient(timeout=120) as client:
        response = await client.post(url, json=payload, params=params)

        if response.status_code == 429:
            raise Exception("Rate limit exceeded. Please try again later.")
        elif response.status_code == 400:
            error_data = response.json()
            error_msg = error_data.get('error', {}).get('message', 'Bad request')
            raise Exception(f"Bad request: {error_msg}")
        elif response.status_code != 200:
            try:
                error_data = response.json()
                error_msg = error_data.get('error', {}).get('message', f'Status {response.status_code}')
            except:
                error_msg = f"Status {response.status_code}"
            raise Exception(f"API error: {error_msg}")

        data = response.json()
        
        # Parse the generateContent response
        candidates = data.get('candidates', [])
        for candidate in candidates:
            content = candidate.get('content', {})
            parts = content.get('parts', [])
            for part in parts:
                # Check for inline image data (inlineData format)
                if 'inlineData' in part:
                    inline_data = part['inlineData']
                    image_data = inline_data.get('data', '')
                    mime_type = inline_data.get('mimeType', 'image/png')
                    return {
                        'image': image_data,
                        'format': mime_type.split('/')[-1] if '/' in mime_type else 'png',
                        'width': width,
                        'height': height
                    }

        raise Exception("No image generated in response")


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Read request body
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            data = json.loads(body) if body else {}

            # Extract parameters
            prompt = data.get('prompt', '')
            width = data.get('width', 512)
            height = data.get('height', 512)
            style = data.get('style', 'pixel_art')

            if not prompt:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'success': False,
                    'error': 'prompt is required'
                }).encode())
                return

            # Generate image
            import asyncio
            result = asyncio.run(generate_image(prompt, width, height, style))

            # Send success response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                'success': True,
                **result
            }).encode())

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                'success': False,
                'error': str(e)
            }).encode())

    def do_OPTIONS(self):
        """Handle CORS preflight."""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        """Health check endpoint."""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({
            'status': 'ok',
            'endpoint': '/api/generate-image',
            'method': 'POST',
            'model': MODEL,
            'api_configured': bool(GEMINI_API_KEY)
        }).encode())
