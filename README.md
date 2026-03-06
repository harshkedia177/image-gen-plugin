# image-gen

AI image generation for coding agents. Craft optimal prompts, generate images via Google's Nano Banana (Gemini) models, self-review output, and post-process — all from your AI coding assistant.

Works with **Claude Code, Codex CLI, Gemini CLI, GitHub Copilot, Cursor, OpenCode**, and any tool supporting the [SKILL.md open standard](https://skills.sh).

## Quick Start

### Install

Pick your platform:

**Claude Code (recommended):**
```bash
# 1. Add the marketplace
claude plugin marketplace add harshkedia177/image-gen-plugin

# 2. Install the plugin
claude plugin install image-gen
```

**Cross-platform (Codex, Gemini CLI, Copilot, Cursor, and more):**
```bash
npx skills add harshkedia177/image-gen-plugin
```

**Claude Code (local dev / one-off):**
```bash
git clone https://github.com/harshkedia177/image-gen-plugin.git
claude --plugin-dir ./image-gen-plugin
```

**Manual install (any agent):**
```bash
# Copy the cross-platform skills into your project
git clone https://github.com/harshkedia177/image-gen-plugin.git
cp -r image-gen-plugin/.agents/skills/* .agents/skills/
rm -rf image-gen-plugin
```

### Set Up Your API Key

Get a free API key from [Google AI Studio](https://aistudio.google.com/apikey) and set it:

```bash
export GEMINI_API_KEY="your-api-key-here"
```

Add it to your shell profile (`~/.zshrc`, `~/.bashrc`) to persist across sessions.

### Generate Your First Image

Just ask your coding agent:

```
Generate an image of a golden retriever puppy sitting in a sunlit meadow
```

Or use the slash command in Claude Code:

```
/image-gen:generate a cyberpunk city at night with neon reflections
```

That's it. The agent handles prompt crafting, model selection, API calls, and saving the output.

---

## What It Does

When you ask for an image, the skill:

1. **Gathers requirements** — asks 2-3 smart clarifying questions (style, mood, composition) or skips straight to generation if your description is detailed enough
2. **Selects the prompting strategy** — natural language for simple requests, JSON structured prompts for complex multi-element scenes
3. **Picks the right model** — Nano Banana 2 for speed, Pro for maximum quality
4. **Crafts an optimized prompt** — applies Gemini-specific best practices (priority ordering, constraint handling, text rendering tricks)
5. **Generates the image** — calls the Gemini API with proper `imageConfig` (resolution, aspect ratio, thinking mode)
6. **Self-reviews** — evaluates the output for prompt adherence, technical quality, and composition; regenerates with targeted fixes if needed
7. **Post-processes** — removes backgrounds, converts formats if requested
8. **Saves with metadata** — image file + markdown sidecar with the exact prompt, settings, and review notes

## Features

| Feature | Description |
|---|---|
| **Smart prompt crafting** | Natural language or JSON structured prompts based on complexity |
| **Two models** | Nano Banana 2 (fast, ~3s) and Pro (max quality, ~10-20s) |
| **Thinking mode** | Configurable reasoning for complex scenes (NB2 only, 3 levels) |
| **Search grounding** | Google Search for real-world accuracy — landmarks, logos, products (NB2 only) |
| **Self-review loop** | Automatically evaluates and improves output based on complexity |
| **Conversational editing** | Refine images with follow-ups instead of regenerating from scratch |
| **Batch generation** | Multiple variations from one concept — vary style, lighting, aspect ratio |
| **Text rendering** | Text-first workflow for accurate in-image text (signs, posters, logos) |
| **Character consistency** | 360-degree sheets, identity locking for multi-image character work |
| **Background removal** | Transparent PNGs via `rembg` — great for logos and stickers |
| **Format conversion** | Export as PNG, JPEG, or WebP |
| **14 aspect ratios** | From `1:1` to `21:9` ultrawide, `9:16` stories, and more |
| **5 resolutions** | `512px` preview to `4K` print-ready |
| **Markdown sidecars** | Every image saved with its prompt, model, settings, and review notes |

## Models

| Model | API ID | Speed | Cost | Best For |
|---|---|---|---|---|
| **Nano Banana 2** | `gemini-3.1-flash-image-preview` | ~3s at 1K | ~$0.067/2K | Fast iteration, batch, web-grounded generation |
| **Nano Banana Pro** | `gemini-3-pro-image-preview` | ~10-20s at 1K | ~$0.134/2K | Maximum quality, complex scenes, professional output |

Fallback: `gemini-2.5-flash-image` if primary models return 404. Auto-discovers latest models as a last resort.

## Usage Examples

**Simple generation:**
```
Generate a watercolor painting of a lighthouse at sunset
```

**With specific requirements:**
```
Create a 16:9 product photo of a matte black coffee mug on a marble countertop,
soft morning light from the left, shallow depth of field, no text
```

**Batch generation:**
```
/image-gen:batch Generate 4 variations of a minimalist logo for "Brew Lab" coffee shop
— vary the style: line art, geometric, hand-drawn, modern sans-serif
```

**With post-processing:**
```
Generate a cartoon mascot character on a white background, then remove the background
to make it a transparent PNG
```

**Conversational editing:**
```
> [generates initial image]
Make the lighting warmer and add a slight lens flare from the top right
```

**Prompt optimization (fix a bad prompt):**
```
Optimize this image prompt: "cat, cute, fluffy, orange, garden, sunny, sitting, flowers"
```

**Convert from another model:**
```
Optimize this Midjourney prompt for Nano Banana: "cyberpunk city --ar 16:9 --v 6 --style raw"
```

## Prerequisites

- **`GEMINI_API_KEY`** — required. Get one free at [Google AI Studio](https://aistudio.google.com/apikey)
- **Python 3.9+** with `rembg` — only needed for background removal:
  ```bash
  pip install rembg
  ```

## Settings (Claude Code)

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

| Setting | Options | Default | Description |
|---|---|---|---|
| `output_dir` | Any path | `./generated-images` | Where images are saved |
| `default_model` | `nano-banana-2`, `nano-banana-pro` | `nano-banana-2` | Generation model |
| `default_resolution` | `512px`, `0.5K`, `1K`, `2K`, `4K` | `1K` | Output resolution |
| `default_aspect_ratio` | 14 ratios (see below) | `1:1` | Output aspect ratio |
| `review_rounds` | `0`-`3` | `0` (auto) | Self-review iterations. 0 = auto based on complexity |
| `save_prompt` | `true`, `false` | `true` | Save markdown sidecar alongside image |
| `thinking_level` | `auto`, `off`, `moderate`, `advanced` | `auto` | NB2 thinking mode. Advanced costs 20-40% more |
| `search_grounding` | `true`, `false` | `false` | Enable Google Search for real-world subjects (NB2 only) |

**Aspect ratios:** `1:1` `2:3` `3:2` `3:4` `4:3` `4:5` `5:4` `9:16` `16:9` `21:9` `1:4` `4:1` `1:8` `8:1`

## Commands (Claude Code)

| Command | Description |
|---|---|
| `/image-gen:generate [description]` | Generate a single image. Interactive if no description provided. |
| `/image-gen:batch [concept]` | Generate multiple variations from one concept. |

## Skills Included

| Skill | What It Provides |
|---|---|
| **image-generation** | Complete end-to-end generation workflow (universal, works on all platforms) |
| **prompt-optimizer** | Takes rough/bad prompts and rewrites them — diagnoses issues, applies Gemini best practices, recommends settings |
| **nano-banana-prompting** | Prompt engineering expertise — NL vs JSON strategy, best practices, examples |
| **image-post-processing** | Background removal and format conversion |

Each skill includes detailed reference files for advanced techniques, character consistency, JSON schema, prompt examples, and full API documentation.

## Architecture

```
image-gen-plugin/
├── .agents/skills/           # Cross-platform skills (Codex, Gemini CLI, Copilot)
│   ├── image-generation/     # Universal end-to-end workflow
│   ├── prompt-optimizer/     # Prompt diagnosis and rewriting
│   ├── nano-banana-prompting/# Prompt crafting knowledge + references
│   └── image-post-processing/# Background removal & format conversion
├── .claude-plugin/           # Claude Code plugin manifest
├── commands/                 # Claude Code slash commands
│   ├── generate.md           # /image-gen:generate
│   └── batch.md              # /image-gen:batch
├── agents/                   # Claude Code subagents
│   ├── prompt-crafter.md     # Prompt engineering specialist
│   └── image-reviewer.md     # Quality review specialist
├── skills/                   # Claude Code plugin skills
│   ├── prompt-optimizer/
│   ├── nano-banana-prompting/
│   └── image-post-processing/
└── scripts/
    └── remove-bg.py          # Background removal script (rembg)
```

## How It Works Under the Hood

The plugin calls Google's Gemini API via `curl` with structured `imageConfig` parameters for reliable resolution and aspect ratio control. It uses a 3-step model resolution chain:

1. **Primary model** (`gemini-3.1-flash-image-preview` or `gemini-3-pro-image-preview`)
2. **Fallback** (`gemini-2.5-flash-image`) if primary returns 404
3. **Auto-discover** latest available image models as last resort

Prompts are crafted following Gemini-specific best practices:
- Priority-ordered elements (subject first, constraints last)
- JSON structured prompts for complex scenes to prevent concept bleeding
- Text wrapped in quotes for in-image rendering
- `imageConfig` for resolution/aspect ratio (not prompt text)
- Thinking mode for spatial reasoning in complex compositions
- Search grounding for real-world visual accuracy

## License

MIT
