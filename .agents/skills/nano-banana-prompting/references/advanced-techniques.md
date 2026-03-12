# Advanced Prompting Techniques

## Thinking Mode

Nano Banana 2 supports configurable thinking levels that make the model reason through the prompt before rendering. **Recommended: keep OFF by default.** For standard image generation, disabling thinking saves time and cost. Only enable when the model needs help reasoning through complex prompts.

### Thinking Levels

| Level | Behavior | Cost Impact | Use When |
|---|---|---|---|
| Off (recommended default) | Standard generation, no extra reasoning | Baseline | Standard prompts, fast iteration |
| Moderate | Plans layout, multi-subject positioning | +10-20% | Multiple subjects, specific layouts |
| Advanced (High) | Deep reasoning — scene logic, spatial relationships, physics | +20-40% | Complex scenes, precise layouts, interlocking objects |
| Dynamic | Model decides how much reasoning is needed | Variable | Mixed complexity batches |

### When to Enable Thinking

Only turn thinking ON if:
- The model is generating **nonsensical results** and needs help reasoning through the prompt
- Generating **highly complex infographics** with logical data flow
- Combining **complex Image Grounding with spatial reasoning** (e.g., accurate landmark + multi-element scene)
- **Multi-character scenes** with interlocking spatial relationships
- **Text-heavy images** with multiple text elements requiring layout planning

### API Parameter

Set thinking mode via `generationConfig`:

```json
{
  "generationConfig": {
    "responseModalities": ["TEXT", "IMAGE"],
    "thinkingConfig": {
      "thinkingBudget": 8192
    }
  }
}
```

Higher `thinkingBudget` = more reasoning. Use 0 for minimal, 8192+ for advanced.

## Search Grounding & Image Grounding (NB2 Only)

NB2 takes a massive leap beyond text-based search: **Image Grounding**. The model can search the internet for specific images to understand exactly what a real-world subject looks like before generating. This produces dramatically more accurate depictions of specific locations, species, and landmarks.

### Best Practices for Image Grounding

**Specific Locations**: Ask for specific churches, bridges, city squares, or niche buildings:
> "Generate a cinematic, golden-hour photograph of the main historical church in Voiron, France. Ensure the architectural details, the spire, the surrounding square, and the landscape (mountains) are accurate to reality."

**Nature & Species**: Ask for exact animal species, breeds, or insects:
> "Create a realistic picture of a machaon butterfly and a flambé one, and highlight their differences to show how to differentiate them."

**Limitation**: The model **cannot search for people**. Use reference images instead for specific person likeness.

### When to Use
- Real landmarks, buildings, or specific locations
- Brand logos or product designs
- Current events or trending topics
- Specific real-world objects the model might not have in training data
- Factual accuracy matters (maps, flags, uniforms)
- Exact biological species, breeds, or insects

### API Parameter

Add `tools` to the request:

```json
{
  "tools": [{
    "googleSearch": {
      "searchTypes": ["imageSearch", "webSearch"]
    }
  }]
}
```

The response includes `groundingMetadata` with the sources used.

### Cost
- First 1,500 queries/day: Free
- After: $35 per 1,000 grounding queries
- Each search the model executes counts as a separate query

## Conversational Editing Workflow

The official recommended workflow: **edit, don't re-roll**.

### The Pattern

1. **Generate** the initial image
2. **Evaluate** — is it 80%+ correct?
3. If yes → **refine** with conversational follow-ups
4. If no → **regenerate** with an improved prompt

### Effective Edit Commands

Use direct, conversational language:

```
"Change the background to a sunset"
"Make the lighting warmer, like golden hour"
"Remove the person in the background"
"Add a subtle lens flare from the top-right"
"Keep everything the same but change her expression to a smile"
"Update the input image. Do not change the input aspect ratio."
```

### Rules for Conversational Editing
- Be specific about what to change and what to preserve
- If the model changes the aspect ratio, explicitly state: "Do not change the input aspect ratio"
- The model adjusts lighting/reflections automatically to match edits
- For large edits, break into a chain of small steps

### Edit Chaining for Complex Changes

Instead of one massive edit, chain small focused edits:

```
Step 1: "Change the background from indoor to outdoor park"
Step 2: "Update the lighting to match natural outdoor sunlight"
Step 3: "Add autumn leaves on the ground"
Step 4: "Apply warm color grading"
```

Each step is focused, reducing unexpected cross-effects.

## Text-First Hack

For images containing text (posters, signs, infographics), generate the text content first in conversation, then render it.

### Why This Works
The model renders text more accurately when the text concepts are established in the conversation context before image generation.

### The Pattern

```
Step 1 (text): "I need a motivational poster. Help me write a short,
punchy headline and a subtitle."

Model responds: "RISE ABOVE" / "Your only limit is your mindset"

Step 2 (image): "Now generate a motivational poster with the headline
'RISE ABOVE' in bold white sans-serif at the top, and the subtitle
'Your only limit is your mindset' in smaller italic text below.
Dark gradient background, dramatic lighting from below."
```

## Hybrid Workflow: NL → JSON

The recommended professional workflow:

### Phase 1: Explore with Natural Language
Use natural language prompts to explore creative directions quickly:
```
"A cyberpunk street food vendor in a neon-lit alley at night"
```
Iterate 2-3 times to find a direction that works.

### Phase 2: Lock Down with JSON
Once the creative direction is established, convert to JSON for production consistency:
```json
{
  "Subject": ["Street food vendor, middle-aged man, cybernetic arm prosthetic",
              "Cooking at a steaming wok, neon-lit smoke rising"],
  "MadeOutOf": ["Weathered leather apron, oil-stained",
                "Brushed titanium prosthetic arm with blue LED accents"],
  "Lighting": {
    "source": "Multiple neon signs (pink, cyan, amber) from storefronts",
    "quality": "Hard colored lighting with atmospheric haze",
    "color_temperature": "Mixed — warm from wok flame, cool from neon"
  },
  "Camera": {
    "lens": "35mm",
    "aperture": "f/2.0",
    "film_stock": "Cinestill 800T"
  },
  "Background": "Narrow alley with stacked signage in Chinese and English, wet pavement reflecting neon",
  "ColorRestriction": "Cyberpunk palette — cyan, magenta, amber, deep shadows"
}
```

### Why Hybrid Works
- NL is faster for ideation (try many directions quickly)
- JSON is more precise for production (exact reproduction, batch variations)
- Moving from NL → JSON forces deliberate creative decisions
- JSON prompts are reusable and version-controllable

## Multi-Image Composition

Combine multiple input images into a single output:

### Style Transfer
Upload Image A (content) and Image B (style):
```
"Apply the artistic style of Image B to the scene in Image A.
Maintain the composition and subjects from Image A, but render
everything in the visual style of Image B."
```

### Scene Fusion
Upload two concept images:
```
"Combine the subject from Image A with the environment from Image B.
The character should be placed naturally in the new setting with
appropriate lighting and shadows."
```

## Known Limitations

Set expectations for these known issues:

| Limitation | Workaround |
|---|---|
| Small faces may lack detail | Generate at 2K+ resolution, use close-up composition |
| Text spelling can be wrong | Use text-first hack, verify output, regenerate specific text |
| Infographic data may be inaccurate | Always verify numerical data — the model generates visual design, not accurate data |
| Fine details in complex scenes | Use Advanced thinking mode for better spatial reasoning |
| Character consistency isn't pixel-perfect | 90%+ perceptual consistency is achievable with proper techniques |
| Hands/fingers can be distorted | Add constraint: "anatomically correct hands" or crop to avoid |
