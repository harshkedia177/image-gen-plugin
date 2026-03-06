# Character Consistency Techniques

## The Core Challenge

Maintaining a consistent character across different images is one of the hardest tasks in AI generation. Anchor strings alone produce drift. These techniques achieve 90%+ perceptual consistency.

## The 360-Degree Character Sheet

The most reliable approach. Two-step process:

### Step 1: Generate the Character Sheet

Prompt the model to show the character from multiple angles in a single generation:

```
Generate a character sheet showing a young woman with short black hair,
round glasses, and a green hoodie. Show her from three angles:
front-facing, three-quarter view looking left, and profile looking right.
Clean white background, consistent lighting across all views.
```

### Step 2: Use as Reference

Upload the character sheet as a reference image for all subsequent generations:

```
Using the character from the reference image, place her in a cozy
coffee shop, sitting at a wooden table with a laptop. Maintain exact
facial features, hair, and clothing from the reference.
```

## Identity Locking Prompts

Explicit instructions that anchor the model to preserve identity:

### Strong Identity Lock Phrases
- "Keep the person's facial features exactly the same as Image 1"
- "Maintain identical facial structure, hair style, and distinguishing marks"
- "The character must look like the same person — same face, same build"
- "Preserve all character details (hair, glasses, clothing) but change expression to [X]"

### Weak (Avoid These)
- "Similar looking person" — too vague, allows drift
- "Same style character" — preserves style, not identity
- "Like the previous image" — ambiguous reference

## Character Naming / Tokens

Assign distinctive identifiers to characters for multi-character scenes:

```json
{
  "Characters": {
    "Maya": "Woman, early 30s, short black hair, round silver glasses, small scar above left eyebrow",
    "Jin": "Man, mid-20s, tall, rectangular silver glasses, angular jaw, navy peacoat"
  },
  "Scene": "Maya and Jin standing outside a bookshop, Maya holding a paper bag, Jin pointing at the window display"
}
```

Naming prevents the model from blending attributes between characters.

## Multi-Image Reference Roles

Nano Banana supports up to 14 reference images (6 with high fidelity). Assign explicit roles to each:

### Role Assignment Prompt Pattern

```
I'm uploading 4 reference images:
- Image 1: Use for CHARACTER IDENTITY (face, body, hair)
- Image 2: Use for POSE and body positioning
- Image 3: Use for LIGHTING and atmosphere
- Image 4: Use for BACKGROUND environment

Generate a new image combining these elements. The character must look
exactly like Image 1, posed like Image 2, lit like Image 3, in the
environment of Image 4.
```

### Available Roles
| Role | What It Controls |
|---|---|
| Identity/Character | Face, body type, distinguishing features |
| Pose/Composition | Body position, gesture, spatial arrangement |
| Style/Aesthetic | Color palette, visual treatment, artistic approach |
| Lighting/Atmosphere | Light direction, mood, environmental tone |
| Environment/Background | Setting, location, context |
| Clothing/Outfit | Specific wardrobe for the character |

## Storyboarding with Consistency

For creating image sequences (comics, storyboards, tutorials):

```
Generate panel 3 of a 6-panel comic. Same character from panels 1-2
(upload previous panels as reference). The identity and attire of all
characters must stay consistent throughout.

In this panel: Maya enters the library, looking surprised.
Wide shot, warm interior lighting.
```

## Troubleshooting Character Drift

| Problem | Solution |
|---|---|
| Face changes between images | Upload original as reference, use identity lock phrase |
| Clothing drifts | Explicitly re-describe clothing in every prompt |
| Hair/glasses disappear | List distinguishing features: "same round silver glasses, same short black hair" |
| Character blends with another | Use character naming tokens, separate descriptions |
| Details get softer over iterations | Reduce reference count to 3-4 highly consistent images, generate at 2K+ |
| Character drifts too far | Re-upload one of the original reference images to reset |

## Best Practices Summary

1. **Build a character sheet first** — front, three-quarter, profile views
2. **Use identity lock phrases** in every follow-up prompt
3. **Name characters** in multi-character scenes to prevent attribute blending
4. **Assign roles** to reference images explicitly
5. **Re-describe key features** (don't assume the model remembers)
6. **Chain small edits** — expression change → outfit change → background change
7. **Re-upload originals** if consistency drifts too far
