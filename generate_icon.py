from PIL import Image, ImageDraw, ImageFont
import math

# ---- Image Settings ----
size = 512
cx, cy = size // 2, size // 2
img = Image.new("RGBA", (size, size), (30, 30, 60, 255))
draw = ImageDraw.Draw(img)

# ---- Radar Circles ----
for r in range(50, 251, 50):
    draw.ellipse((cx-r, cy-r, cx+r, cy+r), outline=(0,255,0,255), width=2)

# ---- Radar Lines ----
for angle in range(0, 360, 30):
    x = cx + int(240 * 0.9 * math.cos(math.radians(angle)))
    y = cy + int(240 * 0.9 * math.sin(math.radians(angle)))
    draw.line((cx, cy, x, y), fill=(0,255,0,100), width=1)

# ---- Plane Icon ----
plane_size = 40
plane_points = [
    (cx, cy-plane_size),
    (cx-10, cy+10),
    (cx+10, cy+10)
]
draw.polygon(plane_points, fill=(255,0,0,255))

# ---- Text Overlay ----
font_size = 32
try:
    font = ImageFont.truetype("arial.ttf", font_size)
except:
    font = ImageFont.load_default()

text = "SyAviTimePredictor"

# Use textbbox instead of textsize
bbox = draw.textbbox((0,0), text, font=font)
text_w = bbox[2] - bbox[0]
text_h = bbox[3] - bbox[1]

draw.text((cx - text_w//2, cy + 200), text, font=font, fill=(255,255,255,255))

# ---- Save Icon ----
img.save("SyAviTimePredictorIcon_3D.png")
print("✅ Realistic 3D icon generated: SyAviTimePredictorIcon_3D.png")
