#!/usr/bin/env python3
"""Generate the Priscilla Vision contact-sheet JPEG from actual repository photos."""
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "documentation" / "product-images"
OUTPUT = ROOT / "documentation" / "images" / "00-contact-sheet.jpg"
PHOTOS = [
    ("BEFORE  |  TWO RUBBER BANDS", "ghetto_mount.jpg"),
    ("AFTER  |  V2 INSTALLED", "priscilla_vision_1.jpg"),
    ("AFTER  |  SIDE VIEW", "priscilla_vision_2.jpg"),
]
WIDTH, HEIGHT = 1600, 820
BG, PANEL, ACCENT, WHITE, MUTED = "#0c1420", "#182337", "#ff851c", "#f6f7fb", "#b8c7dc"

def font(size, bold=False):
    names = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]
    for name in names:
        if Path(name).exists():
            return ImageFont.truetype(name, size)
    return ImageFont.load_default()

def main():
    missing = [name for _, name in PHOTOS if not (SOURCE / name).exists()]
    if missing:
        raise SystemExit(f"Missing source photo(s): {', '.join(missing)}")
    sheet = Image.new("RGB", (WIDTH, HEIGHT), BG)
    d = ImageDraw.Draw(sheet)
    d.rounded_rectangle((16, 16, WIDTH-16, HEIGHT-16), radius=24, outline=ACCENT, width=5)
    d.text((52, 42), "PRISCILLA VISION", font=font(58, True), fill=WHITE)
    d.text((54, 112), "#FPD  /  Fully Prototyped Dumbassery", font=font(29), fill=ACCENT)
    margin, gap, box_y, box_h = 54, 22, 194, 475
    box_w = (WIDTH - 2*margin - 2*gap)//3
    for i, (label, filename) in enumerate(PHOTOS):
        x = margin + i*(box_w+gap)
        d.rounded_rectangle((x, box_y, x+box_w, box_y+box_h), radius=15, fill=PANEL)
        with Image.open(SOURCE / filename) as im:
            im = ImageOps.exif_transpose(im).convert("RGB")
            photo = ImageOps.fit(im, (box_w-14, box_h-74), method=Image.Resampling.LANCZOS, centering=(0.5, 0.48))
            sheet.paste(photo, (x+7, box_y+7))
        d.text((x+12, box_y+box_h-54), label, font=font(19, True), fill=WHITE)
    d.text((55, 706), "We designed, prototyped, documented, and published an entire", font=font(25, True), fill=WHITE)
    d.text((55, 742), "engineering project to replace two rubber bands.", font=font(25, True), fill=WHITE)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(OUTPUT, quality=87, optimize=True, subsampling=0)
    print(f"Generated {OUTPUT.relative_to(ROOT)} ({WIDTH}x{HEIGHT})")

if __name__ == "__main__":
    main()
