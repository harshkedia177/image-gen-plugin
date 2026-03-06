---
name: nano-banana-prompting
description: This skill should be used when the user asks to "generate an image", "create a picture", "make an illustration", "design a graphic", "craft an image prompt", "use Nano Banana", "use Gemini image generation", or when crafting prompts for AI image generation. Provides comprehensive Nano Banana prompting knowledge including natural language best practices, JSON structured prompting, model selection (NB2 vs Pro), and prompt optimization strategies.
version: 0.1.0
---

# Nano Banana Prompting Guide

## Purpose

Provide expert-level prompt crafting for Google's Nano Banana image generation models. Select the optimal prompting strategy (natural language vs JSON) based on request complexity, and apply best practices for maximum output quality.

## Model Selection

### Nano Banana 2 (Gemini 3.1 Flash Image)
- **API model ID**: `gemini-3.1-flash-image-preview`
- **Fallback**: `gemini-2.5-flash-image` (if primary returns 404)
- **Speed**: ~3s at 1K resolution
- **Best for**: Fast iteration, web-grounded generation, batch work
- **Unique features**: Search-grounded generation, Thinking Mode (3 levels)
- **Cost**: ~$0.067 per 2K image

### Nano Banana Pro (Gemini 3 Pro Image)
- **API model ID**: `gemini-3-pro-image-preview`
- **Fallback**: `gemini-2.5-flash-image` (if primary returns 404)
- **Speed**: ~10-20s at 1K resolution
- **Best for**: Maximum quality, complex scenes, professional output
- **Unique features**: Superior textures, lighting, spatial composition
- **Cost**: ~$0.134 per 2K image

**Selection rule**: Default to NB2 unless user explicitly requests Pro or the request demands maximum quality (professional photography, complex multi-subject scenes, intricate lighting setups).

## Prompting Strategy Selection

### Use Natural Language When:
- Simple, straightforward requests (single subject, basic scene)
- Quick iterations and exploration
- User provides a clear description that maps well to prose

### Use JSON Structured Prompting When:
- Complex multi-element scenes (3+ subjects, specific spatial relationships)
- Precise camera/lighting control needed (aperture, lens, film stock)
- Batch generation requiring systematic variations
- Text rendering with specific typography requirements
- Professional photography simulation

## Natural Language Prompting Best Practices

### Prompt Structure (Priority Order)
Elements listed first carry more weight in generation:

1. **Subject** — who/what, count, age, materials, physical traits
2. **Action & Relationships** — what they're doing, how elements interact
3. **Setting** — place, time of day, weather, environment
4. **Style & Medium** — photo/illustration/3D/watercolor, realism level
5. **Composition & Camera** — shot type, angle, lens, depth of field
6. **Constraints** — exclusions ("no text", "no watermark")

### Key Rules
- Write descriptive, narrative-style prompts — not keyword soup
- Wrap in-image text in quotes: `a sign that says "Welcome"`
- Specify typography when needed: `bold sans-serif in white`
- Use constraints to narrow output: "no extra people", "no heavy blur"
- Avoid contradictions in a single prompt

### Example
> A 30-year-old woman with auburn hair standing in a sunlit meadow during golden hour, wearing a navy wool peacoat, captured with an 85mm lens at f/2.0 with shallow depth of field, cinematic color grading with warm earth tones

## JSON Structured Prompting

For complex requests, structure the prompt as JSON to prevent concept bleeding and achieve photographer-level control.

Consult **`references/json-schema.md`** for the complete JSON schema with all fields and examples.

### Quick JSON Template

```json
{
  "Subject": ["description line 1", "description line 2"],
  "MadeOutOf": ["material descriptions for textures"],
  "Arrangement": "pose and spatial placement",
  "Lighting": {
    "source": "light type and direction",
    "quality": "hard/soft, color temperature"
  },
  "Camera": {
    "lens": "focal length",
    "aperture": "f-stop",
    "film_stock": "optional film simulation"
  },
  "Background": "environment description",
  "ColorRestriction": "palette constraints",
  "Constraints": ["no text", "no watermark"]
}
```

### JSON Advantages
- Significantly improved precision for color, lighting, and composition vs natural language
- Generally faster processing since the model skips natural language parsing
- No concept bleeding between elements
- Reproducible — easy systematic variations for batch work

## Thinking Mode (NB2)

Nano Banana 2 supports configurable thinking levels. When enabled, the model reasons through the prompt before rendering — dramatically improving spatial reasoning, multi-object placement, and complex compositions.

| Level | `thinkingBudget` | Cost | Use When |
|---|---|---|---|
| Minimal (default) | 0 or omit | Baseline | Simple prompts, fast iteration |
| Moderate | 1024-4096 | +10-20% | Multiple subjects, specific layouts |
| Advanced | 8192+ | +20-40% | Complex scenes, interlocking objects, infographics |

Apply advanced thinking for: spatial reasoning tasks, multi-character scenes, infographics with logical flow, architectural scenes, text-heavy layouts.

## Search Grounding (NB2 Only)

Enable Google Search to let the model retrieve real-world references before generating. Add `tools` with `googleSearch` to the API request. Use for: real landmarks, brand logos, current events, specific real-world objects. Cost: 1,500 free queries/day, then $35/1,000. See **`references/gemini-api.md`** for the exact API parameter.

## Resolution and Aspect Ratio

Control resolution and aspect ratio via `generationConfig.imageConfig` parameters — not prompt text. This is more reliable.

| Resolution | Size | Use Case |
|---|---|---|
| `512px` | 512×512 | Ultra-fast previews |
| `0.5K` | ~500px | Low-res preview (NB2 only) |
| `1K` | 1024×1024 | Standard generation |
| `2K` | 2048×2048 | High quality |
| `4K` | 4096×4096 | Professional, print-ready |

Supported aspect ratios (14 options): `1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9`, `1:4`, `4:1`, `1:8`, `8:1`

## Text Rendering

Nano Banana excels at in-image text. Best practices:
- **Text-first hack**: First generate the text content in conversation, then request the image with that text. The model renders text more accurately when concepts are established in context first.
- Wrap desired text in quotes in the prompt: `a sign that says "Welcome"`
- Specify font style, weight, and color
- Supports 10+ languages including in-image translation
- For complex text layouts, use JSON prompting with a dedicated `Text` section
- Use Advanced thinking mode for multi-text-element layouts

## Conversational Editing

The official recommended workflow: **edit, don't re-roll**.

If an image is 80%+ correct, refine with conversational follow-ups instead of regenerating:
- "Keep everything the same but change the lighting to golden hour"
- "Remove the person in the background"
- "Change her expression to a smile"

For large edits, chain small focused steps: background swap → lighting update → color grading → final retouch. This reduces unexpected cross-effects.

The model automatically adjusts lighting and reflections to match edits. If it changes the aspect ratio, explicitly state: "Do not change the input aspect ratio."

## Hybrid Workflow: NL → JSON

The recommended professional approach:
1. **Explore** with natural language prompts — try creative directions quickly
2. **Lock down** with JSON once the direction is established — for production consistency, batch variations, and reproducibility

Natural language is faster for ideation. JSON is more precise for production.

## Character Consistency

For maintaining character identity across multiple generations, consult **`references/character-consistency.md`** which covers:
- 360-degree character sheet technique
- Identity locking prompts
- Character naming/tokens for multi-character scenes
- Multi-image reference role assignment (up to 14 references)

## Complexity Assessment

To determine prompt complexity for review round decisions:

- **Simple** (0 review rounds): Single subject, basic scene, standard style
- **Moderate** (1 review round): Multiple subjects, specific lighting/camera, text rendering, detailed composition requirements
- **Complex** (1+ review rounds): Multi-character scenes, infographics, specific brand requirements, professional photography simulation

## Known Limitations

Set expectations for these issues:
- Small faces may lack detail — generate at 2K+ or use close-up composition
- Text spelling can be wrong — use text-first hack, verify output
- Infographic data may be inaccurate — the model generates design, not accurate data
- Hands/fingers can be distorted — add constraint "anatomically correct hands"
- Character consistency isn't pixel-perfect — 90%+ perceptual consistency is achievable

## Additional Resources

### Reference Files
- **`references/json-schema.md`** — Complete JSON prompt schema with all fields, advanced features, and worked examples
- **`references/prompt-examples.md`** — Curated prompt examples for common use cases (portraits, products, landscapes, logos, UI mockups)
- **`references/advanced-techniques.md`** — Thinking mode, search grounding, conversational editing, text-first hack, hybrid workflow, prompt chaining, multi-image composition
- **`references/character-consistency.md`** — 360-degree character sheets, identity locking, character naming, multi-image reference roles, storyboarding

### API Reference
- **`references/gemini-api.md`** — Gemini API request/response format, `imageConfig` parameters, thinking mode, search grounding, all 14 aspect ratios, error handling
