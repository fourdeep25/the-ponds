"""
The Ponds — Floor Plan Generator
Original work, drawn programmatically. © 2026 Matt Farrar.
Generates: floorplan-the-ponds.pdf, floorplan-the-ponds.png (high-res)
"""
from PIL import Image, ImageDraw, ImageFont
import os

# ============================================================
# CONFIG
# ============================================================
DPI = 300                            # print-quality
PAGE_W = int(16.5 * DPI)             # ~A2 landscape width
PAGE_H = int(11.7 * DPI)             # ~A2 landscape height
BG = (250, 248, 244)                 # warm off-white (matches site palette)
WALL = (26, 24, 21)                  # near-black (--color-text)
WALL_THIN = (60, 58, 55)
ROOM_FILL = (235, 230, 220)
ROOM_FILL_ALT = (224, 219, 209)
LABEL_COLOR = (26, 24, 21)
DIM_COLOR = (90, 88, 85)
ACCENT = (166, 137, 74)              # gold accent
WALL_W = 12
THIN_W = 4

# Fonts
def load_font(size, bold=False):
    paths_bold = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ]
    paths_reg = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for p in (paths_bold if bold else paths_reg):
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

F_TITLE = load_font(110, bold=True)
F_FLOOR = load_font(70, bold=True)
F_ROOM = load_font(36, bold=True)
F_DIM = load_font(28)
F_FOOT = load_font(26)
F_DISC = load_font(22)

# ============================================================
# CANVAS
# ============================================================
canvas = Image.new("RGB", (PAGE_W, PAGE_H), BG)
draw = ImageDraw.Draw(canvas)

# Title bar
draw.text((PAGE_W // 2, 90), "THE PONDS", fill=WALL, font=F_TITLE, anchor="mt")
draw.text((PAGE_W // 2, 220), "118 Main Road, Goostrey, Cheshire CW4 8JR", fill=DIM_COLOR, font=F_FOOT, anchor="mt")

# Decorative accent line
ACCENT_Y = 290
draw.line([(PAGE_W // 2 - 200, ACCENT_Y), (PAGE_W // 2 + 200, ACCENT_Y)], fill=ACCENT, width=4)

# Three-floor layout
PANEL_TOP = 380
PANEL_BOTTOM = PAGE_H - 480
PANEL_H = PANEL_BOTTOM - PANEL_TOP
PANEL_W = PAGE_W // 3
COLS = [
    ("GROUND FLOOR", 0),
    ("FIRST FLOOR", 1),
    ("SECOND FLOOR", 2),
]

# Floor labels
for label, idx in COLS:
    cx = PANEL_W * idx + PANEL_W // 2
    draw.text((cx, PANEL_TOP - 20), label, fill=WALL, font=F_FLOOR, anchor="mb")
    # Underline
    draw.line([(cx - 180, PANEL_TOP - 5), (cx + 180, PANEL_TOP - 5)], fill=ACCENT, width=2)


# ============================================================
# DRAWING HELPERS
# ============================================================
def panel_origin(idx):
    """Top-left corner of the panel for floor idx."""
    return PANEL_W * idx + 100, PANEL_TOP + 40


def room(idx, x, y, w, h, name, dims, fill=ROOM_FILL, name_size=None):
    """Draw a room rectangle with wall outline, name, and dimensions.
    Centered both name and dims as separate lines."""
    px, py = panel_origin(idx)
    x1, y1 = px + x, py + y
    x2, y2 = x1 + w, y1 + h
    # Fill
    draw.rectangle([x1, y1, x2, y2], fill=fill, outline=WALL, width=WALL_W)
    # Label
    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
    f = name_size or F_ROOM

    name_lines = (name or "").split("\n") if name else []
    dim_lines = (dims or "").split("\n") if dims else []
    NAME_LH = 42 if f is F_ROOM else 32
    DIM_LH = 32

    total_h = len(name_lines) * NAME_LH + (16 if name_lines and dim_lines else 0) + len(dim_lines) * DIM_LH
    start_y = cy - total_h // 2

    cur_y = start_y
    for nl in name_lines:
        draw.text((cx, cur_y), nl, fill=LABEL_COLOR, font=f, anchor="mt")
        cur_y += NAME_LH
    if name_lines and dim_lines:
        cur_y += 16
    for dl in dim_lines:
        draw.text((cx, cur_y), dl, fill=DIM_COLOR, font=F_DIM, anchor="mt")
        cur_y += DIM_LH


def line(idx, x1, y1, x2, y2, color=WALL, w=WALL_W):
    px, py = panel_origin(idx)
    draw.line([(px + x1, py + y1), (px + x2, py + y2)], fill=color, width=w)


def text_at(idx, x, y, text, color=LABEL_COLOR, font=F_ROOM, anchor="mm"):
    px, py = panel_origin(idx)
    draw.text((px + x, py + y), text, fill=color, font=font, anchor=anchor)


# ============================================================
# GROUND FLOOR (panel 0)
# Re-imagined in clean orthogonal blocks. Approximate proportions.
# ============================================================
G = 0
# Living Room (top-left)
room(G, 50, 60, 460, 540, "LIVING ROOM", "5.39m × 4.86m\n17'8\" × 15'11\"", fill=ROOM_FILL_ALT, name_size=F_ROOM)
# Media Room (bottom-left)
room(G, 50, 620, 460, 480, "MEDIA ROOM", "6.20m × 4.99m\n20'4\" × 16'4\"", fill=ROOM_FILL)
# Kitchen (centre, large)
room(G, 530, 280, 700, 820, "KITCHEN", "8.56m × 5.06m\n28'1\" × 16'7\"", fill=ROOM_FILL_ALT)
# Dining Room (top-centre)
room(G, 530, 60, 700, 200, "DINING ROOM", "6.71m × 3.94m\n22'0\" × 12'11\"", fill=ROOM_FILL)
# Hall + boot/utility narrow strip
room(G, 1250, 60, 240, 200, "BOOT\nROOM", "", fill=ROOM_FILL, name_size=F_DIM)
# Double Garage (right)
room(G, 1250, 280, 240, 540, "DOUBLE\nGARAGE", "5.53m × 5.52m\n18'2\" × 18'1\"", fill=ROOM_FILL_ALT, name_size=F_ROOM)
# Pantry / utility under garage
room(G, 1250, 840, 240, 260, "UTILITY", "", fill=ROOM_FILL, name_size=F_DIM)


# ============================================================
# FIRST FLOOR (panel 1)
# ============================================================
F1 = 1
# Principal Bedroom (top-left)
room(F1, 50, 60, 540, 380, "PRINCIPAL\nBEDROOM", "5.40m × 4.93m\n17'9\" × 16'2\"", fill=ROOM_FILL_ALT)
# Balcony stripe under principal
room(F1, 50, 460, 540, 80, "BALCONY", "", fill=BG, name_size=F_DIM)
# Ensuite (centre-left mid)
room(F1, 50, 560, 270, 220, "ENSUITE", "", fill=ROOM_FILL, name_size=F_DIM)
# Laundry (mid-bottom)
room(F1, 340, 560, 250, 220, "LAUNDRY", "", fill=ROOM_FILL, name_size=F_DIM)
# Bedroom 4 (bottom-left)
room(F1, 50, 800, 540, 300, "BEDROOM 4", "4.90m × 4.30m\n16'1\" × 14'1\"", fill=ROOM_FILL)
# Landing (centre)
room(F1, 610, 380, 320, 360, "LANDING", "", fill=ROOM_FILL, name_size=F_ROOM)
# Library (centre-right)
room(F1, 940, 540, 290, 200, "LIBRARY", "", fill=ROOM_FILL, name_size=F_DIM)
# Bedroom 3 (bottom-centre)
room(F1, 610, 760, 320, 340, "BEDROOM 3", "4.86m × 3.18m\n15'11\" × 10'5\"", fill=ROOM_FILL)
# Bedroom 5 (top-right)
room(F1, 950, 60, 540, 320, "BEDROOM 5", "4.89m × 3.88m\n16'1\" × 12'8\"", fill=ROOM_FILL_ALT)
# Bedroom 2 (mid-right) — single large room
room(F1, 940, 400, 550, 340, "BEDROOM 2", "5.68m × 5.43m\n18'9\" × 17'10\"", fill=ROOM_FILL_ALT)
# Ensuite to Bedroom 2 (bottom-right of F1)
room(F1, 940, 760, 550, 340, "ENSUITE 2", "", fill=ROOM_FILL, name_size=F_ROOM)


# ============================================================
# SECOND FLOOR (panel 2)
# ============================================================
F2 = 2
# Bedroom 6 (top, full width)
room(F2, 50, 60, 1000, 320, "BEDROOM 6", "4.82m × 3.96m\n15'10\" × 13'0\"", fill=ROOM_FILL_ALT)
# Mezzanine annotation panel (right side, separate)
room(F2, 1080, 60, 360, 320, "MEZZANINE OVER\nBEDROOM 2", "3.69m × 2.27m\n12'1\" × 7'5\"", fill=BG, name_size=F_DIM)
# Dressing Room (bottom-left, large)
room(F2, 50, 400, 540, 700, "DRESSING ROOM", "8.94m × 4.06m\n29'4\" × 13'4\"", fill=ROOM_FILL_ALT)
# Study (mid-right)
room(F2, 600, 400, 440, 380, "STUDY", "4.85m × 4.40m\n15'11\" × 14'5\"", fill=ROOM_FILL)
# Ensuite (bottom-right)
room(F2, 600, 800, 440, 300, "ENSUITE", "", fill=ROOM_FILL, name_size=F_ROOM)


# ============================================================
# FOOTER
# ============================================================
FOOTER_Y = PAGE_H - 380
draw.line([(200, FOOTER_Y - 30), (PAGE_W - 200, FOOTER_Y - 30)], fill=ACCENT, width=2)

draw.text(
    (PAGE_W // 2, FOOTER_Y + 10),
    "APPROXIMATE NET INTERNAL AREA  5,301 SQ FT  |  492.52 SQ M",
    fill=WALL,
    font=F_FOOT,
    anchor="mt",
)

# Disclaimer
disc = (
    "This floor plan is for illustrative purposes only. Measurements and dimensions are approximate.\n"
    "Whilst every care has been taken to ensure accuracy, no responsibility is assumed for any error or omission.\n"
    "Services, systems and appliances shown have not been tested and no guarantee of operability is given."
)
# Center each line manually since multiline_text doesn't support anchor
for i, _line in enumerate(disc.split("\n")):
    draw.text(
        (PAGE_W // 2, FOOTER_Y + 110 + i * 36),
        _line,
        fill=DIM_COLOR,
        font=F_DISC,
        anchor="mt",
    )

# Copyright
draw.text(
    (PAGE_W // 2, PAGE_H - 80),
    "© 2026 The Ponds  |  www.the-ponds.co.uk",
    fill=ACCENT,
    font=F_DISC,
    anchor="mt",
)

# ============================================================
# OUTPUT
# ============================================================
OUT_DIR = "/home/user/workspace/the-ponds/assets/images"
os.makedirs(OUT_DIR, exist_ok=True)

# High-res PNG
png_path = f"{OUT_DIR}/floorplan.png"
canvas.save(png_path, "PNG", optimize=True, dpi=(DPI, DPI))
print(f"PNG saved: {png_path} ({os.path.getsize(png_path) / 1024:.0f} KB)")

# PDF
pdf_path = "/home/user/workspace/the-ponds-floorplan.pdf"
canvas.save(pdf_path, "PDF", resolution=DPI, save_all=True)
print(f"PDF saved: {pdf_path} ({os.path.getsize(pdf_path) / 1024:.0f} KB)")

# JPG for OffAgent (some platforms prefer JPG)
jpg_path = "/home/user/workspace/the-ponds-floorplan.jpg"
canvas.save(jpg_path, "JPEG", quality=92, dpi=(DPI, DPI))
print(f"JPG saved: {jpg_path} ({os.path.getsize(jpg_path) / 1024:.0f} KB)")
