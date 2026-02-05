#!/usr/bin/env python3
"""
Test script for Image Generator API
Tests the Vercel-deployed API endpoint and saves sample output
"""

import httpx
import base64
import sys
import os
from pathlib import Path

# Try to get URL from environment or use default
VERCEL_URL = os.getenv("VERCEL_APP_URL", "https://caisogames.vercel.app")
ENDPOINT = f"{VERCEL_URL}/api/generate-image"


def test_health():
    """Test API health check"""
    print(f"Testing health: {ENDPOINT}")
    try:
        response = httpx.get(ENDPOINT, timeout=10)
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Response: {data}")
        return data.get('api_configured', False)
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_generate(prompt: str, output_path: str = None):
    """Test image generation"""
    print(f"\nGenerating: {prompt}")
    
    payload = {
        "prompt": prompt,
        "width": 512,
        "height": 512,
        "style": "pixel_art"
    }
    
    try:
        response = httpx.post(ENDPOINT, json=payload, timeout=120)
        data = response.json()
        
        if data.get('success'):
            print("✓ Generation successful!")
            if output_path:
                image_data = base64.b64decode(data['image'])
                Path(output_path).write_bytes(image_data)
                print(f"✓ Saved to: {output_path}")
            return True
        else:
            print(f"✗ Failed: {data.get('error')}")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


if __name__ == "__main__":
    prompt = sys.argv[1] if len(sys.argv) > 1 else "pixel art cute monster character"
    output = sys.argv[2] if len(sys.argv) > 2 else "test_output.png"
    
    print(f"=== Image Generator API Test ===")
    print(f"Endpoint: {ENDPOINT}\n")
    
    if test_health():
        print("\n--- API is configured, testing generation ---")
        test_generate(prompt, output)
    else:
        print("\n✗ API not configured or not accessible.")
        print("  Check: 1) Vercel deployment exists")
        print("         2) GEMINI_API_KEY is set in Vercel env vars")
