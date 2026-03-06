# image-gen

AI image generation assistant plugin for Claude Code. Acts as a creative director — gathers requirements, crafts optimal prompts (natural language or JSON), generates images via Gemini API, self-reviews output, and handles post-processing.

## Features

- Interactive prompt crafting with clarifying questions
- Smart prompt strategy selection (natural language vs structured JSON)
- Nano Banana 2 and Nano Banana Pro model support
- Configurable thinking mode for complex scene reasoning (NB2)
- Google Search grounding for real-world accuracy (NB2)
- Conversational image editing — refine without regenerating
- Character consistency techniques (360-degree sheets, identity locking)
- Text-first workflow for superior text rendering
- Self-review loop with automatic complexity-based escalation
- Batch generation (variations, 14 aspect ratios, multiple resolutions)
- Background removal via `rembg`
- Markdown sidecar files with prompt, settings, and review notes

## Prerequisites

- `GEMINI_API_KEY` environment variable set with a valid Google AI Studio API key
- Python 3.9+ with `rembg` installed (only for background removal): `pip install rembg`

## Settings

Create `.claude/image-gen.local.md` in your project to customize defaults:

```yaml
---
output_dir: ./generated-images
default_model: nano-banana-2
default_resolution: 1K
default_aspect_ratio: 1:1
review_rounds: 0
save_prompt: true
thinking_level: auto
search_grounding: false
---
```

### Settings Reference

| Setting | Values | Default | Description |
|---|---|---|---|
| `output_dir` | Any path | `./generated-images` | Where to save generated images |
| `default_model` | `nano-banana-2`, `nano-banana-pro` | `nano-banana-2` | Default generation model |
| `default_resolution` | `512px`, `0.5K`, `1K`, `2K`, `4K` | `1K` | Default output resolution |
| `default_aspect_ratio` | 14 options (see below) | `1:1` | Default aspect ratio |
| `review_rounds` | `0`, `1`, `2`, `3` | `0` (auto) | Review iterations. 0 = auto-escalate for complex requests |
| `save_prompt` | `true`, `false` | `true` | Save markdown sidecar with prompt and metadata |
| `thinking_level` | `auto`, `off`, `moderate`, `advanced` | `auto` | Thinking mode for NB2. Auto = based on complexity. Advanced costs 20-40% more. |
| `search_grounding` | `true`, `false` | `false` | Enable Google Search grounding (NB2 only). Improves accuracy for real-world subjects. |

**Supported aspect ratios**: `1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9`, `1:4`, `4:1`, `1:8`, `8:1`

## Commands

- `/image-gen:generate [description]` — Generate an image. Pass a description or start interactive.
- `/image-gen:batch [description]` — Generate multiple variations or aspect ratios.

## Models

| Model | Best For | Speed | Quality | Unique Features |
|---|---|---|---|---|
| Nano Banana 2 | Fast iteration, web-grounded generation | ~3s at 1K | ~95% of Pro | Thinking mode, search grounding, 0.5K preview |
| Nano Banana Pro | Maximum quality, complex scenes | ~10-20s at 1K | Best-in-class | Superior textures, lighting, spatial composition |
