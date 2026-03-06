#!/usr/bin/env python3
"""Remove background from an image using rembg.

Usage:
    python3 remove-bg.py input.png output.png
    python3 remove-bg.py input.png output.png --convert webp
"""

import sys
import os


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 remove-bg.py <input> <output> [--convert format]")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    convert_format = None
    if "--convert" in sys.argv:
        idx = sys.argv.index("--convert")
        if idx + 1 < len(sys.argv):
            convert_format = sys.argv[idx + 1].lower()

    if not os.path.exists(input_path):
        print(f"Error: Input file not found: {input_path}")
        sys.exit(1)

    try:
        from rembg import remove
        from PIL import Image
    except ImportError:
        print("Error: rembg is not installed. Install with: pip install rembg")
        sys.exit(1)

    try:
        with open(input_path, "rb") as f:
            input_data = f.read()

        output_data = remove(input_data)

        img = Image.open(__import__("io").BytesIO(output_data))

        if convert_format:
            if convert_format in ("jpg", "jpeg"):
                img = img.convert("RGB")
                img.save(output_path, "JPEG", quality=95)
            elif convert_format == "webp":
                img.save(output_path, "WEBP", quality=95)
            else:
                img.save(output_path, "PNG")
        else:
            img.save(output_path, "PNG")

        print(f"Success: Background removed and saved to {output_path}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
