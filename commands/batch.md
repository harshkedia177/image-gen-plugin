---
name: batch
description: Generate multiple image variations — different styles, aspect ratios, or creative directions from a single concept.
argument-hint: "[optional: concept description and variation instructions]"
allowed-tools: ["Read", "Write", "Bash", "Glob", "Grep", "Agent", "AskUserQuestion"]
---

# Batch Image Generation Command

Generate multiple image variations from a single concept.

## Workflow

### 1. Load Settings

Read `.claude/image-gen.local.md` for user preferences (same as generate command).

### 2. Gather Requirements

If arguments provided, use as starting point. Otherwise, ask the user:
- **What to generate**: The core concept/subject
- **How many variations**: Number of images to generate (default: 3)
- **What should vary**: Style, lighting, color palette, aspect ratio, mood, or a combination

Common batch patterns:
- **Style variations**: Same subject in different artistic styles
- **Aspect ratio variations**: Same image cropped for different platforms (Instagram, YouTube, Story)
- **Color/mood variations**: Same scene with different lighting or color palettes
- **Composition variations**: Same subject from different angles or distances
- **Custom variations**: User-defined variation parameters

### 3. Plan the Batch

Create a generation plan showing all variations before executing. Present to user for approval:

```
Batch Plan: [Concept]
─────────────────────
1. [Variation 1 description] — [model, resolution, aspect]
2. [Variation 2 description] — [model, resolution, aspect]
3. [Variation 3 description] — [model, resolution, aspect]
```

Wait for user confirmation before proceeding.

### 4. Craft Prompts

For batch generation, prefer JSON structured prompting — it enables clean systematic variations by swapping specific fields while keeping the base prompt constant.

Create a base prompt, then generate variations by modifying only the relevant fields (Style, Lighting, ColorRestriction, etc.). For aspect ratio variations, change `imageConfig.aspectRatio` in the API request — not the prompt text.

### 5. Generate Images

**IMPORTANT**: Use `curl` via Bash to call the Gemini API. WebFetch does NOT support POST requests.

Follow the same API calling pattern as the generate command:
- Resolve the model ID by listing available models (see `/image-gen:generate` for the discovery command)
- Use `curl` with proper `imageConfig` parameters (aspectRatio, imageSize)
- Pipe response through python to extract and save base64 image data

For each variation sequentially (to respect rate limits):
1. Build the curl request with variation-specific prompt and `imageConfig`
2. For complex variations, enable thinking mode: `"thinkingConfig": {"thinkingBudget": 2048}`
3. If generating real-world subjects, enable search grounding (NB2 only)
4. Execute curl, extract and save the image
5. Report progress: "Generated 2/5..."

### 6. Post-Processing

Apply any post-processing (background removal, format conversion) to all generated images if requested.

### 7. Save Output

Save all images to a subdirectory within the output directory:
```
generated-images/
└── batch-[concept]-[timestamp]/
    ├── variation-1-[descriptor].png
    ├── variation-2-[descriptor].png
    ├── variation-3-[descriptor].png
    └── batch-summary.md
```

Create a `batch-summary.md` sidecar that documents all variations:

```markdown
# Batch: [Concept]

## Overview
- **Variations**: [count]
- **Model**: [model used]
- **Date**: YYYY-MM-DD

## Variations

### 1. [Variation Name]
- **File**: variation-1-[descriptor].png
- **Prompt**: [prompt used]
- **Settings**: [resolution, aspect ratio]

### 2. [Variation Name]
...
```

### 8. Present Results

Show the user:
- The batch directory path
- Summary of all generated images
- Key differences between variations
- Option to regenerate any specific variation
