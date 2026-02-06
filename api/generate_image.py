"""
Vercel Serverless Function: Image Generation Proxy

This endpoint allows Claude Code to generate images via Gemini API
by proxying requests through Vercel where the API key is stored.

Supports:
  - Imagen 4 (primary, highest quality)
  - Gemini 2.0 Flash (fallback)

Usage:
  POST /api/generate-image
  {
    "prompt": "pixel art monster character",
    "width": 512,
    "height": 512,
    "style": "pixel_art",
    "aspect_ratio": "1:1"
  }

Returns:
  {
    "success": true,
    "image": "base64_encoded_image_data",
    "format": "png",
    "model": "imagen-4.0-generate-001"
  }
"""

import os
import json
import base64
from http.server import BaseHTTPRequestHandler
import httpx

# API configuration
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')
BASE_URL = "https://generativelanguage.googleapis.com/v1beta"

# Models: Primary (Imagen 4) and Fallback (Gemini Flash)
IMAGEN4_MODEL = "imagen-4.0-generate-001"
GEMINI_FLASH_MODEL = "gemini-2.0-flash-exp-image-generation"


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


async def generate_image_imagen4(prompt: str, aspect_ratio: str = "1:1"):
    """Generate image using Imagen 4 API (highest quality)."""
    url = f"{BASE_URL}/models/{IMAGEN4_MODEL}:predict"
    
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": GEMINI_API_KEY
    }
    
    payload = {
        "instances": [{"prompt": prompt}],
        "parameters": {
            "sampleCount": 1,
            "aspectRatio": aspect_ratio,
            "personGeneration": "allow_adult"
        }
    }
    
    async with httpx.AsyncClient(timeout=120) as client:
        response = await client.post(url, json=payload, headers=headers)
        
        if response.status_code != 200:
            error_msg = f"Imagen 4 error: Status {response.status_code}"
            try:
                error_data = response.json()
                error_msg = error_data.get('error', {}).get('message', error_msg)
            except:
                pass
            raise Exception(error_msg)
        
        data = response.json()
        predictions = data.get('predictions', [])
        
        if predictions and 'bytesBase64Encoded' in predictions[0]:
            return {
                'image': predictions[0]['bytesBase64Encoded'],
                'format': 'png',
                'model': IMAGEN4_MODEL
            }
        
        raise Exception("No image in Imagen 4 response")


async def generate_image_gemini_flash(prompt: str):
    """Generate image using Gemini Flash (fallback)."""
    url = f"{BASE_URL}/models/{GEMINI_FLASH_MODEL}:generateContent"
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseModalities": ["image", "text"]}
    }
    params = {"key": GEMINI_API_KEY}
    
    async with httpx.AsyncClient(timeout=120) as client:
        response = await client.post(url, json=payload, params=params)
        
        if response.status_code != 200:
            error_msg = f"Gemini Flash error: Status {response.status_code}"
            try:
                error_data = response.json()
                error_msg = error_data.get('error', {}).get('message', error_msg)
            except:
                pass
            raise Exception(error_msg)
        
        data = response.json()
        candidates = data.get('candidates', [])
        
        for candidate in candidates:
            parts = candidate.get('content', {}).get('parts', [])
            for part in parts:
                if 'inlineData' in part:
                    inline_data = part['inlineData']
                    return {
                        'image': inline_data.get('data', ''),
                        'format': inline_data.get('mimeType', 'image/png').split('/')[-1],
                        'model': GEMINI_FLASH_MODEL
                    }
        
        raise Exception("No image in Gemini Flash response")


async def generate_image(prompt: str, width: int = 512, height: int = 512, 
                         style: str = 'pixel_art', aspect_ratio: str = "1:1"):
    """Generate image with Imagen 4, fallback to Gemini Flash on failure."""
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY not configured")

    style_prompt = get_style_prompt(style)
    full_prompt = f"{prompt}. {style_prompt}"
    
    # Try Imagen 4 first (highest quality)
    try:
        result = await generate_image_imagen4(full_prompt, aspect_ratio)
        result['width'] = width
        result['height'] = height
        return result
    except Exception as imagen_error:
        # Fallback to Gemini Flash
        try:
            result = await generate_image_gemini_flash(full_prompt)
            result['width'] = width
            result['height'] = height
            result['fallback_reason'] = str(imagen_error)
            return result
        except Exception as flash_error:
            raise Exception(f"Both models failed. Imagen 4: {imagen_error}, Gemini Flash: {flash_error}")


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
            aspect_ratio = data.get('aspect_ratio', '1:1')

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
            result = asyncio.run(generate_image(prompt, width, height, style, aspect_ratio))

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
            'primary_model': IMAGEN4_MODEL,
            'fallback_model': GEMINI_FLASH_MODEL,
            'api_configured': bool(GEMINI_API_KEY)
        }).encode())
