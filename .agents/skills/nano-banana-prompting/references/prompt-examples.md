# Prompt Examples by Category

## Portraits

### Natural Language
> A confident young woman with short curly hair and warm brown skin, wearing a vintage denim jacket, standing against a weathered brick wall in soft afternoon light, shot on 85mm f/1.8, shallow depth of field, warm cinematic tones

### JSON
```json
{
  "Subject": [
    "Young woman, early 20s, short curly hair, warm brown skin",
    "Confident expression, slight smile, direct eye contact",
    "Wearing vintage denim jacket, white t-shirt underneath"
  ],
  "MadeOutOf": [
    "Worn denim with faded indigo, visible stitching",
    "Soft cotton t-shirt, slightly creased",
    "Matte skin with natural highlights"
  ],
  "Arrangement": "Subject standing, leaning slightly against wall, three-quarter turn",
  "Lighting": {
    "source": "Natural afternoon sun, camera-right",
    "quality": "Soft directional, warm fill from wall bounce",
    "color_temperature": "4500K"
  },
  "Camera": {
    "lens": "85mm prime",
    "aperture": "f/1.8",
    "film_stock": "Kodak Portra 400"
  },
  "Background": "Weathered red brick wall, slightly out of focus",
  "ColorRestriction": "Warm earth tones — denim blue, brick red, cream, amber"
}
```

## Product Photography

### Natural Language
> A sleek matte black wireless earbud case sitting on a polished marble surface, studio lighting with a single softbox from above-left, clean white background with subtle shadow, product photography style, 100mm macro lens

### JSON
```json
{
  "Subject": ["Wireless earbud case, matte black finish", "Lid slightly open, revealing one earbud"],
  "MadeOutOf": ["Matte black polycarbonate with soft-touch coating", "Polished white Carrara marble surface"],
  "Arrangement": "Product centered, angled 15 degrees for dimension",
  "Lighting": {
    "source": "Single softbox, above-left at 45 degrees",
    "quality": "Soft, even, with subtle gradient shadow",
    "color_temperature": "5500K daylight"
  },
  "Camera": {
    "lens": "100mm macro",
    "aperture": "f/8",
    "iso": "100"
  },
  "Background": "Clean white gradient, subtle drop shadow",
  "ColorRestriction": "Monochrome — black, white, grey only",
  "Style": "Studio product photography, e-commerce ready"
}
```

## Landscapes

### Natural Language
> A misty mountain valley at sunrise, layers of green pine forests fading into fog, a winding river reflecting golden light, shot with a 24mm wide-angle lens at f/11, deep depth of field, National Geographic style

## Logos & Branding

### Natural Language
> A minimalist logo for a coffee shop called "Brew Lab", featuring a stylized coffee cup merged with a laboratory flask, clean vector lines on white background, modern sans-serif typography, the text "BREW LAB" below the icon

### JSON (for text rendering control)
```json
{
  "Subject": ["Minimalist logo icon — coffee cup merged with laboratory flask"],
  "Style": "Clean vector illustration, flat design, modern",
  "Text": {
    "content": "BREW LAB",
    "style": "Modern sans-serif, bold weight, dark charcoal color",
    "placement": "Centered below the icon"
  },
  "Background": "Pure white",
  "ColorRestriction": "Two-tone — dark charcoal (#333) and warm brown (#8B4513)",
  "Constraints": ["no gradients", "no shadows", "no 3D effects", "no extra text"]
}
```

## Social Media Graphics

### Natural Language
> An Instagram story graphic with a vibrant gradient background from coral to purple, bold white text saying "NEW DROP", modern streetwear aesthetic, 9:16 aspect ratio

## UI Mockups

### Natural Language
> A clean mobile app login screen with a dark theme, email and password fields with rounded corners, a gradient blue login button, subtle background pattern, iPhone 15 Pro frame, 9:16 aspect ratio

## Infographics

### Natural Language
> A vertical infographic about coffee brewing methods, showing 4 methods (Pour Over, French Press, Espresso, Cold Brew) with illustrated icons for each, brewing time and temperature listed, clean modern design with coffee-brown color palette, the title "The Art of Coffee" at the top
