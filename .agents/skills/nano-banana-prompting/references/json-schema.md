# Nano Banana JSON Prompt Schema

## Complete Schema Structure

```json
{
  "label": "internal-name-for-prompt",
  "tags": ["high-level", "aesthetic", "keywords"],

  "Subject": [
    "Primary subject description — physical traits",
    "Clothing, accessories, distinguishing features",
    "Expression, mood, energy"
  ],

  "MadeOutOf": [
    "Material 1 with texture detail (e.g., 'cotton camisole with visible weave')",
    "Material 2 (e.g., 'matte skin with subtle freckles')",
    "Material 3 (e.g., 'brushed leather belt, slightly worn')"
  ],

  "Arrangement": "Subject placement, pose, spatial relationships. E.g., 'Subject sits centered, cross-legged, facing camera at three-quarter angle'",

  "Lighting": {
    "source": "Light type and position (e.g., 'single tungsten key light, camera-left')",
    "quality": "Hard/soft, direction (e.g., 'hard directional with soft fill bounce')",
    "color_temperature": "Kelvin value (e.g., '3200K warm')",
    "secondary": "Optional fill/accent lights"
  },

  "Camera": {
    "lens": "Focal length (e.g., '85mm prime')",
    "aperture": "F-stop (e.g., 'f/1.8')",
    "iso": "Sensitivity (e.g., '400')",
    "film_stock": "Optional film simulation (e.g., 'Kodak Portra 400')",
    "shutter_speed": "Optional (e.g., '1/125s')"
  },

  "ColorRestriction": "Palette constraints (e.g., 'Warm earth tones only — navy, amber, cream. No bright saturated colors.')",

  "Background": "Environment description with depth cues (e.g., 'Blurred urban street at dusk, bokeh from streetlights')",

  "Text": {
    "content": "Exact text to render (e.g., 'Happy Birthday')",
    "style": "Typography description (e.g., 'bold serif, white with drop shadow')",
    "placement": "Where in the image (e.g., 'centered top third')"
  },

  "Constraints": [
    "no extra people",
    "no watermark",
    "no deformed hands",
    "no heavy blur"
  ],

  "Style": "Overall artistic direction (e.g., 'cinematic photography', 'studio product shot', 'editorial fashion')",

  "AspectRatio": "1:1",
  "Resolution": "2K"
}
```

## Field Details

### Subject (Array of Strings)
Break the subject description into separate lines rather than one long sentence. Each line should address a different attribute: physical appearance, clothing, expression. This prevents attributes from bleeding into each other.

### MadeOutOf (Array of Strings)
Explicitly define materials and textures. This prevents generic "plastic-looking" outputs. Specifying "cotton camisole" vs "spandex top" changes how light reflects and the overall feel.

### Lighting (Object)
Controls the entire mood. Key parameters:
- `source`: Where light comes from (natural, studio, practical)
- `quality`: Hard creates drama, soft creates flattering portraits
- `color_temperature`: 2700K (warm/golden) to 6500K (cool/daylight)

### Camera (Object)
Simulates virtual photography gear:
- **Wide lenses** (24-35mm): Environmental portraits, landscapes, architecture
- **Standard** (50mm): Natural perspective, street photography
- **Telephoto** (85-200mm): Portraits with background compression, bokeh
- **Aperture**: Lower f-stop = more bokeh. f/1.4-2.0 for portraits, f/8-11 for landscapes

### ColorRestriction (String)
Prevents visual chaos. Define what's allowed AND what's excluded. Effective patterns:
- "Monochromatic blue palette with white accents"
- "Warm earth tones only — no cool colors"
- "Muted pastels, nothing saturated"

## Multi-Subject Scenes

For scenes with multiple subjects, use an array:

```json
{
  "Subjects": [
    {
      "id": "subject_1",
      "description": ["Tall man, mid-30s, dark hair", "Wearing charcoal suit"],
      "position": "Standing left of frame"
    },
    {
      "id": "subject_2",
      "description": ["Woman, late 20s, red hair", "Wearing emerald dress"],
      "position": "Seated right of frame"
    }
  ],
  "Interaction": "Subject_1 is handing a gift box to subject_2"
}
```

## Batch Variation Patterns

### Style Variations
Keep everything constant except `Style`:
```json
// Variation 1
{ "Style": "oil painting, impressionist" }
// Variation 2
{ "Style": "watercolor, loose brushstrokes" }
// Variation 3
{ "Style": "digital art, hyperrealistic" }
```

### Lighting Variations
Swap lighting block only:
```json
// Dawn
{ "Lighting": { "source": "natural sunrise", "color_temperature": "3000K" } }
// Noon
{ "Lighting": { "source": "overhead sun", "color_temperature": "5500K" } }
// Golden hour
{ "Lighting": { "source": "low sun, camera-left", "color_temperature": "3200K" } }
```

### Aspect Ratio Variations
Same content, different crops for different platforms:
```json
// Instagram post
{ "AspectRatio": "1:1", "Resolution": "2K" }
// Instagram story
{ "AspectRatio": "9:16", "Resolution": "2K" }
// YouTube thumbnail
{ "AspectRatio": "16:9", "Resolution": "2K" }
```

## Meta Token Boosters

For maximum quality output, add a quality enhancement field:

```json
{
  "quality_boost": "Nano-detail, 8k crisp, sub-surface scattering, rule of thirds, diffraction spikes, insane detail, pure textures, professional color grading"
}
```

Use sparingly — only when the user explicitly wants maximum quality. Overuse can lead to over-processed results.

## Common Pitfalls

1. **Contradictory constraints**: Don't specify "minimal white background" AND "dense complex background" in the same prompt
2. **Over-specifying**: Too many fields can constrain the model. Start with Subject + Lighting + Camera, add fields as needed
3. **Vague MadeOutOf**: "nice fabric" tells the model nothing. "Raw silk with visible texture grain" is specific and useful
4. **Missing ColorRestriction**: Without palette constraints, the model may introduce jarring colors that don't match the mood
