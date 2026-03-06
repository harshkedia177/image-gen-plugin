---
name: generate
description: Generate an AI image from a text description. Optionally pass a description inline, or start an interactive session.
argument-hint: "[optional: image description]"
allowed-tools: ["Read", "Write", "Bash", "Glob", "Grep", "Agent", "AskUserQuestion"]
---

# Image Generation Command

Generate a high-quality AI image using Nano Banana (Gemini) models.

## Workflow

### 1. Load Settings

Read `.claude/image-gen.local.md` in the current project directory (if it exists) to get user preferences. Apply these defaults:

```yaml
output_dir: ./generated-images
default_model: nano-banana-2
default_resolution: 1K
default_aspect_ratio: 1:1
review_rounds: 0
save_prompt: true
thinking_level: auto
search_grounding: false
```

### 2. Gather Requirements

If the user provided a description as arguments, use it as the starting point. Otherwise, ask what they want to generate.

Ask clarifying questions to understand the full picture. Focus on:
- **Subject**: What exactly should be in the image?
- **Style**: Photorealistic, illustration, watercolor, 3D render, etc.?
- **Mood/Atmosphere**: What feeling should it convey?
- **Composition**: Close-up, wide shot, specific angle?
- **Special requirements**: Text in the image? Transparent background? Specific aspect ratio?

Keep questions focused — don't overwhelm. Ask 2-3 questions max, then generate. If the description is already detailed, skip straight to generation.

### 3. Determine Model

Unless the user specified a preference, use the model from settings (default: `nano-banana-2`). If the request is extremely quality-sensitive (professional photography, complex multi-subject scene), suggest Nano Banana Pro.

### 4. Craft the Prompt

Load the `nano-banana-prompting` skill knowledge. Based on request complexity:

- **Simple requests**: Use natural language prompting
- **Complex requests** (3+ subjects, precise camera/lighting, text rendering, batch): Use JSON structured prompting

Craft the best possible prompt applying all best practices from the skill.

### 5. Generate the Image

Verify `GEMINI_API_KEY` environment variable is set. If not, inform the user to set it.

**IMPORTANT**: Use `curl` via Bash to call the Gemini API. WebFetch does NOT support POST requests.

Resolve the model ID using this priority chain:

**Nano Banana 2:**
1. `gemini-3.1-flash-image-preview` (primary)
2. `gemini-2.5-flash-image` (fallback)
3. Auto-discover (last resort)

**Nano Banana Pro:**
1. `gemini-3-pro-image-preview` (primary)
2. `gemini-2.5-flash-image` (fallback)
3. Auto-discover (last resort)

If primary returns 404, try fallback. If fallback also fails, **auto-discover** the latest available image model:

```bash
curl -s "https://generativelanguage.googleapis.com/v1beta/models?key=$GEMINI_API_KEY" | \
  python3 -c "
import sys, json
models = json.load(sys.stdin).get('models', [])
image_models = [m['name'].replace('models/', '') for m in models if 'image' in m.get('name', '').lower()]
flash_image = [m for m in image_models if 'flash' in m]
pro_image = [m for m in image_models if 'pro' in m]
print('FLASH:', flash_image[0] if flash_image else 'none')
print('PRO:', pro_image[0] if pro_image else 'none')
print('ALL_IMAGE:', image_models)
"
```

Use the discovered model ID and inform the user which model was selected.

**Generate the image with curl**:

```bash
curl -s "https://generativelanguage.googleapis.com/v1beta/models/${MODEL_ID}:generateContent?key=$GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{"parts": [{"text": "Generate an image: [CRAFTED PROMPT]"}]}],
    "generationConfig": {
      "responseModalities": ["TEXT", "IMAGE"],
      "temperature": 1.0,
      "imageConfig": {
        "aspectRatio": "[from settings or user request]",
        "imageSize": "[from settings or user request]"
      }
    }
  }'
```

**Thinking Mode**: If `thinking_level` is `auto`, determine based on complexity:
- Simple → omit `thinkingConfig` (fastest)
- Moderate → add `"thinkingConfig": {"thinkingBudget": 2048}`
- Complex → add `"thinkingConfig": {"thinkingBudget": 8192}`

If user explicitly set a thinking level, use: `off` = omit, `moderate` = 2048, `advanced` = 8192.

**Search Grounding**: If `search_grounding` is `true`, or the request involves real-world landmarks/logos/products/current events, add to the request body:
```json
"tools": [{"googleSearch": {"searchTypes": ["imageSearch", "webSearch"]}}]
```
This is only available with Nano Banana 2. Warn the user if they request grounding with Pro.

**Extract and save the image** from the curl response:
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

Pipe the curl output into the python extraction script. Create the output directory first if it doesn't exist.

### 6. Assess Complexity & Self-Review

If `review_rounds` is 0 (auto mode):
- **Simple request**: Skip review, deliver the image
- **Moderate/complex request**: Run 1 review round

If `review_rounds` > 0, run that many rounds.

For each review round, use the `image-reviewer` agent to evaluate the generated image. If the reviewer suggests prompt modifications, apply them and regenerate.

### 7. Post-Processing

If the user requested a transparent background:
1. Check if `rembg` is available
2. Run `${CLAUDE_PLUGIN_ROOT}/scripts/remove-bg.py` on the generated image
3. Save the result as a PNG with alpha channel

### 8. Save Output

Create the output directory if it doesn't exist. Save the image with a descriptive filename based on the prompt (kebab-case, max 50 chars).

If `save_prompt` is true, create a markdown sidecar file alongside the image:

```markdown
# [Descriptive Title]

## Generated Image
- **File**: filename.png
- **Model**: nano-banana-2
- **Resolution**: 1K
- **Aspect Ratio**: 1:1
- **Date**: YYYY-MM-DD

## Prompt Used
[The exact prompt sent to the API — natural language or JSON]

## Settings
[Any non-default settings applied]

## Review Notes
[If review was performed, include the reviewer's assessment and any modifications made]
```

### 9. Present to User

Show the user:
- The file path of the generated image
- A brief summary of what was generated
- The prompt used (so they can iterate)
- Any review notes if applicable
- Offer to refine: "Want me to adjust anything? I can edit this image conversationally."

### 10. Conversational Refinement (If Requested)

If the user wants changes to the generated image, follow the **edit, don't re-roll** pattern:
1. Upload the generated image as a reference in the next API call
2. Use direct, conversational edit instructions: "Change the background to sunset", "Add a hat", "Make the lighting warmer"
3. For large edits, chain small steps rather than one massive instruction
4. Preserve the aspect ratio — if the model changes it, add "Do not change the input aspect ratio"

### Text-Heavy Images

For images with significant text (posters, infographics, signage), use the **text-first hack**:
1. First, generate the text content in conversation with the user
2. Confirm the exact wording
3. Then craft the image prompt with the confirmed text in quotes
4. Enable Advanced thinking mode for multi-text-element layouts

This produces significantly better text rendering than putting everything in one prompt.
