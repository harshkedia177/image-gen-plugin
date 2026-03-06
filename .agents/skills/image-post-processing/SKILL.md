---
name: image-post-processing
description: This skill should be used when the user asks to "remove background", "make transparent", "make a logo transparent", "create a sticker with no background", "convert to PNG", "convert to JPEG", "convert to WebP", "export as", "convert image format", "post-process image", "remove bg", or when an image needs background removal or format conversion after generation.
version: 0.1.0
---

# Image Post-Processing

## Purpose

Handle post-generation image processing tasks including background removal for transparent PNGs and format conversion. Uses `rembg` for reliable alpha-channel transparency.

## Background Removal

### When to Use
- User explicitly requests transparent background
- User asks for a PNG with no background
- Generating logos, icons, stickers, or assets intended for overlay

### Tool: rembg

`rembg` is a Python library for automatic background removal using deep learning. It produces true alpha-channel transparency — not white or solid-color backgrounds.

### Prerequisites
Verify Python and rembg are available before attempting background removal:

```bash
python3 -c "import rembg; print('rembg available')" 2>/dev/null
```

If not installed, inform the user:
```
Background removal requires rembg. Install with: pip install rembg
```

### Usage

Run the background removal script at `${CLAUDE_PLUGIN_ROOT}/scripts/remove-bg.py`:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/remove-bg.py input.png output.png
```

The script:
1. Reads the input image
2. Removes the background using rembg's U2NET model
3. Saves as PNG with alpha channel
4. Reports success/failure

### Best Practices for Background Removal
- Generate images with clean, simple backgrounds for best removal results
- Solid or gradient backgrounds remove more cleanly than complex scenes
- Add prompt guidance: "on a clean white background" or "on a solid colored background" to improve removal quality
- Always save the result as PNG (JPEG does not support transparency)

## Format Conversion

### Supported Conversions
- PNG → JPEG (lossy, smaller file, no transparency)
- PNG → WebP (modern format, good compression, supports transparency)
- JPEG → PNG (lossless, larger file)

### When Format Matters
- **PNG**: Transparency needed, logos, icons, UI assets
- **JPEG**: Photos, social media posts, web images where file size matters
- **WebP**: Modern web usage, best compression-to-quality ratio

To convert formats, run remove-bg.py with the `--convert` flag:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/remove-bg.py input.png output.webp --convert webp
```

Supported `--convert` values: `jpeg` (or `jpg`), `webp`, `png` (default). Note: converting to JPEG strips transparency since JPEG does not support alpha channels.

## Workflow Integration

The typical post-processing flow:

1. Image generated and saved as PNG
2. If user wants transparent background → run remove-bg.py
3. If user wants different format → convert
4. Update the markdown sidecar with post-processing notes
