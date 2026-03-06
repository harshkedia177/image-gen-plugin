---
name: prompt-optimizer
description: This skill should be used when the user asks to "optimize my image prompt", "improve this prompt", "make this prompt better", "rewrite my prompt for Gemini", "enhance my image description", "fix my prompt", "why isn't my prompt working", "optimize for Nano Banana", "convert my Midjourney prompt", "translate my DALL-E prompt", or when the user provides a rough/vague image description that needs transformation into a production-quality Nano Banana prompt. Also triggers when a generated image doesn't match expectations and the prompt needs debugging.
version: 0.1.0
---

# Nano Banana Prompt Optimizer

## Purpose

Transform rough, vague, or underperforming image prompts into optimized Nano Banana (Gemini) prompts. Analyze the user's intent, diagnose prompt weaknesses, and rewrite applying Gemini-specific best practices. Input goes in, optimized prompt comes out.

## When to Use

- User provides a raw image description that needs optimization
- A generated image didn't match expectations — prompt needs debugging
- User wants to improve, enhance, rewrite, or fix an image prompt
- Converting a prompt from another model (Midjourney, DALL-E, Stable Diffusion, Flux) to Nano Banana
- User describes an abstract concept that needs grounding into a concrete visual

## The Optimization Process

Follow these phases in order. Do not skip phases.

### Phase 1: Analyze the Input Prompt

Read the user's prompt and diagnose weaknesses. Check for these problems:

| Problem | Symptom | Example |
|---|---|---|
| **Keyword soup** | Comma-separated tags, not narrative | "cat, cute, fluffy, sitting, garden, sunny, 8k, masterpiece" |
| **Over-prompting** | Spam quality tags that add nothing | "4K, trending on Artstation, masterpiece, best quality, ultra detailed" |
| **Missing subject priority** | Key subject buried late in prompt | "In a garden with flowers, there's a bench, and a woman sits on it" |
| **Vague style** | No medium, look, or reference | "a cool looking city" |
| **No composition** | Missing camera angle, framing, lens | "a portrait of a woman" |
| **Contradictions** | Conflicting instructions | "dark moody lighting in a bright sunny room" |
| **Config in prompt text** | Resolution/ratio in words not API params | "in 16:9 widescreen format at 4K resolution" |
| **Missing constraints** | No exclusions for common artifacts | No "no watermark", "no text", "no extra fingers" |
| **Foreign model syntax** | Midjourney/SD/Flux-specific syntax | "cyberpunk city --ar 16:9 --v 6 --style raw" |
| **Text without quotes** | In-image text not wrapped in quotes | "a sign saying Welcome Home" |
| **Overloaded prompt** | 10+ competing concepts in one prompt | Everything plus the kitchen sink |
| **Abstract concepts** | Non-visual ideas used as subjects | "freedom", "innovation", "chaos" |
| **Conversational preamble** | Polite filler before the actual prompt | "Please create an image of...", "I would like to see..." |
| **Isolated subject** | No scene, environment, or context | "a businessman smiling" |

**Assess complexity:**
- **Simple** (1 subject, basic scene) → optimize as natural language
- **Complex** (3+ subjects, precise camera/lighting, text, multi-element) → optimize as JSON structured prompt

Report the diagnosis to the user before rewriting.

### Phase 2: Extract and Reorder Elements

Decompose the prompt into Nano Banana's priority order. **Elements listed first carry the most weight in generation** — this is confirmed by Google's own documentation.

Reorder to the **5-pillar framework** (Google's recommended structure):

1. **Subject** — who/what, count, age, materials, physical traits, clothing
2. **Action & Composition** — what they're doing, camera angle, framing, lens
3. **Setting/Location** — place, time of day, weather, environment
4. **Style & Medium** — photo/illustration/3D/watercolor, film stock, realism level
5. **Constraints** — exclusions ("no text", "no watermark", "anatomically correct hands")

**Infer missing elements** from context:
- "portrait" → 85mm lens, f/1.8-f/2.0, shallow DoF, head-and-shoulders, soft directional light
- "product shot" → 100mm macro, f/8, studio softbox lighting, clean background
- "landscape" → 24mm wide-angle, f/11, deep DoF, golden hour if unspecified
- "logo" → flat vector design, clean white background, "no gradients", "no shadows", "no 3D"
- "cinematic" → 35mm anamorphic, f/2.0, CineStill 800T film stock, letterbox framing
- "vintage" → Kodak Portra 400 film stock, warm tones, slight grain, soft focus
- "street photography" → 35mm lens, f/5.6, natural light, candid framing

### Phase 3: Apply Nano Banana Optimizations

**1. Narrative over keywords** — Gemini's core strength is deep language understanding. Describe the scene, don't list tags:
```
Bad:  "cat, fluffy, orange, garden, sunny, sitting, flowers, 8k, masterpiece"
Good: "A fluffy orange tabby cat sitting among wildflowers in a sunlit cottage garden,
       soft afternoon light filtering through the petals, shallow depth of field"
```

**2. Priority ordering** — put the main subject first, always:
```
Bad:  "In a neon-lit alley at night, rain falling, there's a food vendor cooking"
Good: "A street food vendor cooking at a steaming wok in a narrow neon-lit alley at night,
       rain-slicked pavement reflecting pink and cyan neon signs"
```

**3. Specificity injection** — add concrete, sensory details where the prompt is vague:
```
Bad:  "a woman in a city"
Good: "A 30-year-old woman with dark braided hair wearing a camel overcoat,
       walking through a rainy Tokyo intersection at dusk, captured with a 50mm lens"
```

**4. Film stock anchoring** — for photographic style, reference a specific film stock to anchor the entire aesthetic:
- **Kodak Portra 400**: Warm, clean, natural skin tones — ideal for portraits
- **CineStill 800T**: Cinematic halation, tungsten glow — ideal for night/neon scenes
- **Kodak Ektar 100**: Vivid saturated colors, fine grain — ideal for landscapes
- **Fuji Velvia 50**: Ultra-saturated, deep contrast — ideal for nature/travel
- **Ilford HP5**: Classic black & white, medium grain — ideal for street photography

**5. Abstract → concrete conversion** — ground non-visual concepts into specific imagery:
```
Bad:  "An image representing freedom"
Good: "A woman with arms outstretched standing on a cliff edge overlooking an endless
       turquoise ocean at sunrise, wind catching her white linen dress, shot from below
       with a wide-angle lens, warm golden light"
```

**6. Text rendering optimization** — Nano Banana excels at text but has limits:
- Wrap all in-image text in double quotes: `a sign that says "OPEN"`
- Specify typography: font style, weight, color, placement
- Keep text under 25 characters for reliable rendering
- For long text: use the **text-first hack** — generate the text content in conversation first, confirm wording, then render
- Enable advanced thinking mode for multi-text layouts

**7. Constraint injection** — add exclusions to prevent common artifacts:
- Portraits with visible hands: add "anatomically correct hands"
- Logos/icons: add "no gradients", "no shadows", "no 3D effects", "no extra text"
- Clean professional shots: add "no watermark", "no text overlay"
- Product photography: add "no people", "no branding" if unwanted
- Any image: add "no extra fingers" if hands are present

**8. Strip over-prompting** — remove spam quality tags that add nothing:
- Remove: "4K", "8K", "masterpiece", "best quality", "trending on Artstation", "ultra HD", "hyperrealistic"
- Nano Banana understands natural language — it doesn't need these crutches
- Resolution is controlled via `imageConfig.imageSize`, not prompt text
- Instead of "hyperrealistic", describe *what makes it look real*: specific lens, lighting, material textures

**9. Remove conversational preamble:**
```
Bad:  "Please create an image of a cat sitting in a garden"
Good: "A cat sitting in a garden"
(Or better: "A fluffy ginger cat sitting in a sunlit English cottage garden...")
```

**10. Config extraction** — move these OUT of prompt text into `imageConfig` API parameters:
- Aspect ratio mentions → `imageConfig.aspectRatio` (14 options: 1:1 through 8:1)
- Resolution mentions → `imageConfig.imageSize` (512px, 0.5K, 1K, 2K, 4K)
- These are more reliably controlled via structured API parameters than prompt text

### Phase 4: Select Format

**Natural language** (simple prompts):
Present the rewritten prompt as a clean narrative paragraph. Use for: single subject, basic scene, exploration, quick iteration.

**JSON structured** (complex prompts):
Convert to JSON schema to prevent concept bleeding. Use for: 3+ subjects, precise camera/lighting, text rendering, batch generation, production work.

```json
{
  "Subject": ["primary description", "secondary details"],
  "MadeOutOf": ["material/texture descriptions"],
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
  "Text": {
    "content": "exact text in quotes",
    "style": "font, weight, color",
    "placement": "where in the image"
  },
  "Constraints": ["no text", "no watermark", "anatomically correct hands"]
}
```

JSON prompts deliver 60-80% improved accuracy for complex multi-element scenes vs natural language — they prevent concept bleeding and are reproducible for batch work.

### Phase 5: Recommend Settings

Based on the optimized prompt, recommend API configuration:

| Setting | How to Decide |
|---|---|
| **Model** | NB2 (`gemini-3.1-flash-image-preview`) for most work; Pro (`gemini-3-pro-image-preview`) for professional photography, complex multi-subject scenes, or maximum quality |
| **Aspect ratio** | Match use case: 1:1 Instagram, 16:9 desktop/YouTube, 9:16 Stories/Reels/TikTok, 3:2 standard photo, 21:9 cinematic |
| **Resolution** | 1K for iteration, 2K for quality output, 4K for print/professional. Use 2K+ when faces are small or fine detail matters |
| **Thinking mode** | Off for simple prompts. Moderate (2048) for multiple subjects. Advanced (8192+) for spatial reasoning, text layouts, interlocking objects. Advanced costs 20-40% more |
| **Search grounding** | On for real landmarks, logos, products, current events. NB2 only. 1500 free queries/day |

### Phase 6: Present the Result

Always present:

1. **Diagnosis** — what was wrong with the original prompt (bullet list)
2. **Optimized prompt** — the rewritten prompt (NL or JSON)
3. **What changed** — specific improvements with reasoning
4. **Recommended settings** — model, aspect ratio, resolution, thinking, grounding
5. **Variations** — 1-2 alternative directions if the intent was ambiguous

## Cross-Model Prompt Translation

When converting prompts from other models, strip platform-specific syntax and rebuild:

| Source | Syntax to Strip | Conversion Notes |
|---|---|---|
| **Midjourney** | `--ar`, `--v`, `--style`, `--chaos`, `--sref`, `--oref`, `::` weights, `/imagine` | Expand keyword shorthand into full descriptions. Convert `::` weights into priority ordering (higher weight = earlier in prompt). Convert `--ar` to `imageConfig.aspectRatio` |
| **DALL-E / GPT** | "I NEED...", "Create an image of...", system instruction leaks, `size:` | Remove conversational preamble. DALL-E prompts are already natural language — focus on adding Gemini-specific detail (lens, film stock, constraints) |
| **Stable Diffusion** | `(emphasis:1.5)`, `[negative]`, `steps:`, `cfg:`, `sampler:`, LORA/checkpoint names, `<lora:name:weight>` | Remove all technical parameters. Convert emphasis `(word:1.5)` into position priority. Move negative prompt content into Constraints array. Replace LORA style names with descriptive style language |
| **Flux** | Similar to SD but prefers short prompts | Expand short Flux prompts into descriptive Gemini-style narratives. Flux prompts are often too terse for Gemini |

## Prompt Debugging

When a generated image doesn't match the prompt:

1. **Compare intent vs output** — list what's different
2. **Identify the failure mode:**

| Failure | Root Cause | Fix |
|---|---|---|
| Wrong subject | Subject wasn't prioritized first | Move subject to beginning of prompt |
| Wrong style | Style descriptor too weak or contradicted | Be more specific: name a film stock, art movement, or medium |
| Missing elements | Prompt overloaded, elements competed | Reduce to 3-5 key elements, use JSON for complex scenes |
| Wrong composition | No camera/framing specified | Add lens focal length, shot type, angle |
| Bad text rendering | Text not in quotes, no typography | Wrap in quotes, specify font, keep under 25 chars |
| Artifacts/distortions | Missing constraints | Add "anatomically correct hands", "no extra fingers" |
| Wrong lighting | Lighting described vaguely | Specify source direction, quality (hard/soft), color temp |
| Generic/flat result | Over-prompted with spam tags | Remove "masterpiece/8K/best quality", add real detail instead |
| Aspect ratio wrong | Ratio in prompt text not imageConfig | Move to `imageConfig.aspectRatio` parameter |

3. **Apply targeted fix** — surgical change to the failing element only
4. **Don't rewrite everything** — preserve what worked, fix what didn't
5. **If 80%+ correct** → use conversational editing instead of regenerating

## Editing Prompt Optimization

When optimizing prompts for editing (not generating from scratch):

- Focus on **what changes and what stays the same** — editing is different from generating
- Be explicit about preservation: "Keep everything the same but change X"
- For **semantic masking** (inpainting): describe the target area and the change clearly
- For **style transfer**: "Apply the artistic style of [reference] to this image while maintaining the composition and subjects"
- For **multi-reference composition**: use the formula `[References] + [Relationship instruction] + [New scenario]`
- If the model changes aspect ratio: add "Do not change the input aspect ratio"
- Chain large edits into small steps: background → lighting → color grading → detail

## Additional Resources

Consult these reference files from the nano-banana-prompting skill for detailed guidance:
- **`references/json-schema.md`** — Complete JSON prompt schema
- **`references/prompt-examples.md`** — Curated examples by category (before/after)
- **`references/advanced-techniques.md`** — Thinking mode, search grounding, text-first hack
- **`references/character-consistency.md`** — Character sheets, identity locking

Sources that informed this skill:
- [Google DeepMind Prompt Guide](https://deepmind.google/models/gemini-image/prompt-guide/)
- [Google Cloud Ultimate Prompting Guide for Nano Banana](https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-nano-banana)
- [Nano Banana Pro Prompt Tips — Google Blog](https://blog.google/products/gemini/prompting-tips-nano-banana-pro/)
- [Google Developers Blog — Gemini 2.5 Flash Image Prompting](https://developers.googleblog.com/how-to-prompt-gemini-2-5-flash-image-generation-for-the-best-results/)
- [pauhu/gemini-image-prompting-handbook — JSON Schema](https://github.com/pauhu/gemini-image-prompting-handbook)
- [NeurIPS 2023 — Optimizing Prompts for Text-to-Image Generation](https://arxiv.org/abs/2212.09611)
