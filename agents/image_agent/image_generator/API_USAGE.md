# Using the Image Generator API

This guide describes how to use the CAISOGAMES Image Generator API from any application or game engine. The API is deployed on Vercel and acts as a proxy to Google's Gemini API, allowing you to generate game assets dynamically.

## Base URL

> **Production Endpoint**: `https://caisogames.vercel.app/api/generate-image`

## Authentication

The API is public for development use but rate-limited by the underlying Gemini API tier. No additional headers are required for basic usage.

## Generating Images

To generate an image, send a `POST` request to the endpoint with a JSON body containing your prompt and configuration.

### Request Body

```json
{
  "prompt": "pixel art golden sword, game icon",
  "width": 512,
  "height": 512,
  "style": "pixel_art"
}
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `prompt` | string | (required) | Text description of the image to generate |
| `width` | number | 512 | Width of the image (aspect ratio will be calculated) |
| `height` | number | 512 | Height of the image |
| `style` | string | `pixel_art` | Style preset: `pixel_art`, `cartoon`, `realistic`, `sketch`, or `sprite` |

### Response Format

**Success (200 OK):**

```json
{
  "success": true,
  "image": "iVBORw0KGgoAAAANSUhEUgAA...", 
  "format": "png",
  "width": 512,
  "height": 512
}
```

- `image`: Base64 encoded PNG image data. You can decode this string to get the raw image bytes.

**Error:**

```json
{
  "success": false,
  "error": "Rate limit exceeded. Please try again later."
}
```

## Code Examples

### 1. cURL (Command Line)

```bash
curl -X POST "https://caisogames.vercel.app/api/generate-image" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "cute pixel art slime monster",
    "width": 512,
    "height": 512,
    "style": "pixel_art"
  }' > response.json
```

### 2. Python (Requests)

```python
import requests
import base64

url = "https://caisogames.vercel.app/api/generate-image"
payload = {
    "prompt": "isometric fantasy tavern",
    "style": "pixel_art",
    "width": 512,
    "height": 512
}

try:
    response = requests.post(url, json=payload, timeout=60)
    data = response.json()
    
    if data.get("success"):
        # Decode and save the image
        image_data = base64.b64decode(data["image"])
        with open("tavern.png", "wb") as f:
            f.write(image_data)
        print("Image saved successfully!")
    else:
        print(f"Error: {data.get('error')}")
        
except Exception as e:
    print(f"Request failed: {e}")
```

### 3. JavaScript / TypeScript (Web)

```javascript
async function generateGameAsset(prompt) {
  const url = 'https://caisogames.vercel.app/api/generate-image';
  
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        prompt: prompt,
        style: 'pixel_art',
        width: 512,
        height: 512
      })
    });

    const data = await response.json();
    
    if (data.success) {
      // Create an image element to display the result
      const img = document.createElement('img');
      img.src = `data:image/png;base64,${data.image}`;
      document.body.appendChild(img);
      return data.image; // Return base64 string
    } else {
      console.error('Generation failed:', data.error);
    }
  } catch (error) {
    console.error('Network error:', error);
  }
}

// Usage
generateGameAsset('pixel art potion bottle');
```

## Troubleshooting

### 429 Rate Limit Exceeded
The free tier of Gemini API (if used) has rate limits. If you receive this error:
1. Wait for 60 seconds.
2. Retry the request.
3. If persistent, consider implementing exponential backoff in your game's asset loading logic.

### 404 Not Found
- Ensure you are using the correct URL: `https://caisogames.vercel.app/api/generate-image`
- Check if the Vercel deployment is active.

### 504 Gateway Timeout
- Image generation can take 10-20 seconds. Ensure your HTTP client has a long enough timeout setting (at least 60 seconds recommended).
