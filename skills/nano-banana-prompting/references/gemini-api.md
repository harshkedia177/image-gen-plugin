# Gemini API Reference for Image Generation

## Endpoint

```
POST https://generativelanguage.googleapis.com/v1beta/models/{MODEL_ID}:generateContent?key={API_KEY}
```

### Model IDs

| Model | Primary ID | Fallback ID |
|---|---|---|
| Nano Banana 2 | `gemini-3.1-flash-image-preview` | `gemini-2.5-flash-image` |
| Nano Banana Pro | `gemini-3-pro-image-preview` | `gemini-2.5-flash-image` |

**Resolution order**: Try primary → if 404, try fallback → if 404, auto-discover by listing all models and filtering for `image` in the name.

**Auto-discover command** (last resort):
```bash
curl -s "https://generativelanguage.googleapis.com/v1beta/models?key=$GEMINI_API_KEY" | \
  python3 -c "
import sys, json
models = json.load(sys.stdin).get('models', [])
for m in models:
    if 'image' in m.get('name', '').lower():
        print(m['name'])
"
```

### API Call Method

**IMPORTANT**: Use `curl` via Bash. WebFetch in Claude Code does NOT support POST requests.

## Request Format

### Standard Text-to-Image Generation

```json
{
  "contents": [
    {
      "parts": [
        {
          "text": "Generate an image: [YOUR PROMPT HERE]"
        }
      ]
    }
  ],
  "generationConfig": {
    "responseModalities": ["TEXT", "IMAGE"],
    "temperature": 1.0,
    "imageConfig": {
      "aspectRatio": "16:9",
      "imageSize": "2K"
    }
  }
}
```

### With Thinking Mode (Complex Scenes)

```json
{
  "contents": [
    {
      "parts": [
        {
          "text": "Generate an image: [YOUR PROMPT HERE]"
        }
      ]
    }
  ],
  "generationConfig": {
    "responseModalities": ["TEXT", "IMAGE"],
    "temperature": 1.0,
    "imageConfig": {
      "aspectRatio": "1:1",
      "imageSize": "2K"
    },
    "thinkingConfig": {
      "thinkingBudget": 8192
    }
  }
}
```

Thinking budget values:
- `0` or omitted: Minimal thinking (default, fastest)
- `1024-4096`: Moderate thinking
- `8192+`: Advanced thinking (best for complex scenes, +20-40% cost)

### With Search Grounding (NB2 Only)

```json
{
  "contents": [
    {
      "parts": [
        {
          "text": "Generate an image: [YOUR PROMPT HERE]"
        }
      ]
    }
  ],
  "generationConfig": {
    "responseModalities": ["TEXT", "IMAGE"],
    "temperature": 1.0,
    "imageConfig": {
      "aspectRatio": "1:1",
      "imageSize": "2K"
    }
  },
  "tools": [{
    "googleSearch": {
      "searchTypes": ["imageSearch", "webSearch"]
    }
  }]
}
```

Search grounding enables the model to retrieve real-world references before generating. Use for landmarks, logos, real products, current events, or anything requiring factual visual accuracy.

**Cost**: First 1,500 queries/day free, then $35 per 1,000 queries. Each search the model executes counts separately.

### Image Editing (with Reference Image)

```json
{
  "contents": [
    {
      "parts": [
        {
          "text": "Edit this image: [EDIT INSTRUCTIONS]"
        },
        {
          "inlineData": {
            "mimeType": "image/png",
            "data": "[BASE64_ENCODED_IMAGE]"
          }
        }
      ]
    }
  ],
  "generationConfig": {
    "responseModalities": ["TEXT", "IMAGE"],
    "imageConfig": {
      "aspectRatio": "1:1",
      "imageSize": "2K"
    }
  }
}
```

Multiple reference images can be included (up to 14) by adding additional `inlineData` parts. Supported MIME types: `image/png`, `image/jpeg`, `image/webp`, `image/heic`, `image/heif`.

## imageConfig Parameters

### aspectRatio

Supported values (14 options):

| Aspect Ratio | Use Case |
|---|---|
| `1:1` | Square — Instagram posts, profile pictures |
| `2:3` | Portrait — phone wallpapers |
| `3:2` | Landscape — standard photography |
| `3:4` | Portrait — tablets, print |
| `4:3` | Landscape — presentations, monitors |
| `4:5` | Portrait — Instagram portrait posts |
| `5:4` | Landscape — print, desktop |
| `9:16` | Tall portrait — Stories, Reels, TikTok |
| `16:9` | Wide landscape — YouTube, desktop |
| `21:9` | Ultra-wide — cinematic, banners |
| `1:4` | Narrow vertical — bookmark, sidebar |
| `4:1` | Narrow horizontal — banner, header |
| `1:8` | Extra narrow vertical |
| `8:1` | Extra narrow horizontal |

### imageSize

| Value | Resolution | Use Case |
|---|---|---|
| `512px` | 512×512 | Ultra-fast previews, rapid iteration |
| `0.5K` | ~500px | Low-res preview (NB2 Flash only) |
| `1K` | 1024×1024 | Standard generation |
| `2K` | 2048×2048 | High quality output |
| `4K` | 4096×4096 | Professional, print-ready |

**Important**: Always set `imageConfig` parameters explicitly. Do NOT rely on prompt-based hints like "in 16:9 format" — use the structured `imageConfig` fields for reliable control.

## Response Format

```json
{
  "candidates": [
    {
      "content": {
        "parts": [
          {
            "text": "Here is the generated image..."
          },
          {
            "inlineData": {
              "mimeType": "image/png",
              "data": "[BASE64_ENCODED_IMAGE_DATA]"
            }
          }
        ]
      }
    }
  ],
  "groundingMetadata": {
    "searchEntryPoint": { "renderedContent": "..." },
    "groundingChunks": [...]
  }
}
```

The `groundingMetadata` field is only present when search grounding is enabled.

## Extracting the Image

1. Find the part with `inlineData` in `candidates[0].content.parts`
2. Extract the `data` field (base64-encoded)
3. Decode base64 to binary
4. Save as PNG/JPEG file

## Temperature

**Always keep temperature at 1.0** for Gemini 3 models. Google strongly recommends this — the model's reasoning capabilities are optimized for the default temperature and don't benefit from tuning.

## Rate Limits & Quotas

- Free tier: Limited requests per minute
- Paid tier: Higher quotas, check Google AI Studio dashboard
- Batch requests: Use separate API calls, respect rate limits
- Search grounding: 1,500 free queries/day, then $35/1,000

## Error Handling

| Code | Meaning | Action |
|---|---|---|
| `400` | Invalid request (bad prompt, missing fields) | Check request format |
| `403` | Invalid API key or quota exceeded | Verify `GEMINI_API_KEY` |
| `429` | Rate limit exceeded | Back off and retry with exponential backoff |
| `500` | Server error | Retry with exponential backoff |

## Safety Filters

The API may block generation for explicit content, violence, hate speech, or real people's faces. If blocked, the response contains a `safetyRatings` field with `BLOCK_*` reasons. Adjust the prompt to comply.
