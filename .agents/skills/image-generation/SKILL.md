---
name: image-generation
description: This skill should be used when the user asks to "generate an image", "create a picture", "make an illustration", "design a graphic", "create a logo", "make a poster", "generate a photo", "create visual content", "batch generate images", "create variations", or any request involving AI image generation. Provides a complete end-to-end workflow for generating images via Google's Nano Banana (Gemini) models, including prompt crafting, API calling, quality review, and post-processing.
version: 0.1.0
---

# AI Image Generation

## Purpose

End-to-end image generation assistant using Google's Nano Banana (Gemini) models. Gathers requirements, crafts optimal prompts, generates images, reviews quality, and handles post-processing.

## Prerequisites

- `GEMINI_API_KEY` environment variable must be set
- Python 3.9+ with `rembg` installed (only for background removal): `pip install rembg`

## Models

| Model | API ID | Fallback | Best For |
|---|---|---|---|
| Nano Banana 2 | `gemini-3.1-flash-image-preview` | `gemini-2.5-flash-image` | Fast iteration, web-grounded, batch |
| Nano Banana Pro | `gemini-3-pro-image-preview` | `gemini-2.5-flash-image` | Maximum quality, complex scenes |

Default to NB2 unless the user explicitly requests Pro or the request demands maximum quality.

If both primary and fallback return 404, auto-discover available image models:
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

## Workflow

### Step 1: Gather Requirements

If the user provided a description, use it. Otherwise, ask clarifying questions (2-3 max):
- **Subject**: What exactly should be in the image?
- **Style**: Photorealistic, illustration, watercolor, 3D render?
- **Mood**: What feeling should it convey?
- **Special needs**: Text in image? Transparent background? Specific aspect ratio?

If the description is already detailed, skip straight to prompt crafting.

### Step 2: Craft the Prompt

**Strategy selection based on complexity:**
- **Simple** (single subject, basic scene) → Natural language prompt
- **Complex** (3+ subjects, precise camera/lighting, text rendering) → JSON structured prompt

**Natural language prompt structure** (priority order — earlier elements carry more weight):
1. Subject — who/what, count, age, materials, physical traits
2. Action & Relationships — what they're doing, how elements interact
3. Setting — place, time of day, weather, environment
4. Style & Medium — photo/illustration/3D/watercolor, realism level
5. Composition & Camera — shot type, angle, lens, depth of field
6. Constraints — exclusions ("no text", "no watermark")

**Key rules:**
- Write descriptive narrative prompts, not keyword soup
- Wrap in-image text in quotes: `a sign that says "Welcome"`
- Avoid contradictions in a single prompt

**For text-heavy images** (posters, infographics): Use the **text-first hack** — generate the text content first in conversation, confirm wording, then craft the image prompt with confirmed text in quotes.

**For character consistency** across multiple images: Build a 360-degree character sheet first, then use identity locking prompts. See `references/character-consistency.md`.

**JSON template for complex requests:**
```json
{
  "Subject": ["description line 1", "description line 2"],
  "MadeOutOf": ["material/texture descriptions"],
  "Arrangement": "pose and spatial placement",
  "Lighting": { "source": "type and direction", "quality": "hard/soft, color temp" },
  "Camera": { "lens": "focal length", "aperture": "f-stop" },
  "Background": "environment description",
  "ColorRestriction": "palette constraints",
  "Constraints": ["no text", "no watermark"]
}
```

See `references/json-schema.md` for the complete schema.

### Step 3: Configure API Parameters

Build the request with structured `imageConfig` — do NOT rely on prompt text for resolution/aspect ratio.

**Supported resolutions**: `512px`, `0.5K`, `1K`, `2K`, `4K`

**Supported aspect ratios** (14 options): `1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9`, `1:4`, `4:1`, `1:8`, `8:1`

**Thinking mode** (NB2 only — improves complex scene quality):
- Simple → omit `thinkingConfig`
- Moderate → `"thinkingConfig": {"thinkingBudget": 2048}`
- Complex → `"thinkingConfig": {"thinkingBudget": 8192}` (costs 20-40% more)

**Search grounding** (NB2 only — for real-world accuracy):
Add `"tools": [{"googleSearch": {"searchTypes": ["imageSearch", "webSearch"]}}]` when generating real landmarks, logos, products, or current events.

### Step 4: Generate the Image

Use `curl` to call the Gemini API (most coding agents don't have a native POST-capable fetch):

```bash
curl -s "https://generativelanguage.googleapis.com/v1beta/models/${MODEL_ID}:generateContent?key=$GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{"parts": [{"text": "Generate an image: [CRAFTED PROMPT]"}]}],
    "generationConfig": {
      "responseModalities": ["TEXT", "IMAGE"],
      "temperature": 1.0,
      "imageConfig": {
        "aspectRatio": "1:1",
        "imageSize": "1K"
      }
    }
  }'
```

Extract and save the base64 image from the response:
```bash
python3 -c "
import json, base64, sys
data = json.load(sys.stdin)
for part in data['candidates'][0]['content']['parts']:
    if 'inlineData' in part:
        img = base64.b64decode(part['inlineData']['data'])
        with open('OUTPUT_PATH', 'wb') as f:
            f.write(img)
        print(f'IMAGE_SAVED: OUTPUT_PATH')
        print(f'SIZE: {len(img)} bytes')
        break
"
```

If the model returns 404, retry with the fallback ID, then auto-discover.

### Step 5: Review (If Warranted)

Assess complexity to decide if review is needed:
- **Simple**: Single subject, basic scene → skip review
- **Moderate**: Multiple subjects, specific lighting, text → review once
- **Complex**: Professional photography, intricate composition → review once or more

For each review round, evaluate:
1. **Prompt adherence** — does the image match the request?
2. **Technical quality** — artifacts, distortions, text rendering errors?
3. **Composition** — framing, balance, visual appeal?
4. **Fitness for purpose** — right for the intended use case?

If issues found, craft specific prompt modifications (surgical — change only what needs fixing), regenerate, and re-evaluate.

### Step 6: Post-Processing

**Transparent background** (if requested):
```bash
python3 remove-bg.py input.png output.png
```
Requires `rembg`: `pip install rembg`. Generate with a clean/white background for best removal results.

**Format conversion**:
```bash
python3 remove-bg.py input.png output.webp --convert webp
```
Supported: `jpeg`, `jpg`, `webp`, `png` (default).

### Step 7: Save and Present

Save the image with a descriptive kebab-case filename. Create a markdown sidecar file alongside:

```markdown
# [Title]
- **File**: filename.png
- **Model**: [model used]
- **Resolution**: [resolution]
- **Aspect Ratio**: [ratio]
- **Date**: [date]

## Prompt
[Exact prompt sent to API]

## Review Notes
[Assessment and any modifications made]
```

Present the file path, summary, and prompt to the user. Offer conversational refinement: "Want me to adjust anything?"

### Step 8: Conversational Refinement (If Requested)

Follow the **edit, don't re-roll** pattern:
- Upload the generated image as reference in the next API call
- Use direct edit instructions: "Change the background to sunset", "Make the lighting warmer"
- For large edits, chain small steps: background → lighting → color grading
- If the model changes aspect ratio, add: "Do not change the input aspect ratio"

## Batch Generation

For batch requests (multiple variations from one concept):
1. Ask what should vary: style, aspect ratio, color palette, lighting, mood
2. Present a plan showing all variations before generating
3. Prefer JSON prompting for batch — swap specific fields while keeping base constant
4. Generate sequentially (respect rate limits), report progress
5. Save to a subdirectory with a `batch-summary.md`

## Hybrid Workflow

The recommended professional approach:
1. **Explore** with natural language — try creative directions quickly
2. **Lock down** with JSON — for production consistency and batch variations

## Known Limitations

- Small faces may lack detail — use 2K+ resolution or close-up composition
- Text spelling can be wrong — use text-first hack, verify output
- Infographic data may be inaccurate — model generates design, not accurate data
- Hands/fingers can be distorted — add constraint "anatomically correct hands"
- Character consistency isn't pixel-perfect — 90%+ perceptual consistency is achievable

## Additional Resources

- **`references/json-schema.md`** — Complete JSON prompt schema
- **`references/prompt-examples.md`** — Curated examples by category
- **`references/advanced-techniques.md`** — Thinking mode, search grounding, conversational editing, text-first hack, prompt chaining
- **`references/character-consistency.md`** — 360-degree sheets, identity locking, multi-image references
- **`references/gemini-api.md`** — Full API reference with all parameters
