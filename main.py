#!/usr/bin/env python3
"""the-passport-page-of-a-countr-2-20261121-0318 - The Passport Page
of a Country That Isn't There.

Pure Python 3.13 standard library (math, os, struct, zlib only). It
paints a 1024x1024 passport spread for an invented country: the
Republic of Virelia, an island nation in the Meridian Sea that does
not exist. The left page is the holder's data page (coat of arms,
photograph, personal details, signature, machine-readable zone); the
right page is the visa page (a drawn map of the island, arrival and
departure stamps, a granted visa). Deterministic: fixed constants, no
clock, no randomness, no network. Writes /output/entry.png (or
$MAKEFUN_OUTPUT_DIR/entry.png).

The invented country:
  Name:        Republic of Virelia
  Capital:     Aerthys
  Motto:       PER MARE ET STELLAS (by sea and stars)
  Founded:     1927
  Population:  84,213
  Currency:    lumen
  Language:    Virelian
  The holder:  Elara Voss Marlowe, born 14 Mar 1998 in Aerthys,
               passport V-2026-084213, issued 21 Nov 2026.
"""

import math
import os
import struct
import zlib

W = 1024
H = 1024

DESK = (14, 42, 40)
PAGE = (246, 240, 222)
INK = (20, 20, 20)
GOLD = (198, 160, 80)
GOLD_DARK = (150, 116, 52)
WHITE = (255, 255, 255)
GREY = (110, 106, 94)
RED = (178, 34, 24)
BLUE = (30, 70, 130)
NAVY = (16, 34, 64)
SEA = (64, 128, 168)
SEA_DARK = (44, 96, 132)
SAND = (228, 210, 170)
SKY = (150, 170, 200)
VIOLET = (96, 52, 140)
GREEN = (28, 96, 60)

# 5x7 pixel font. Each glyph is seven rows; each row is a 5-bit
# integer, bit 4 first (leftmost pixel), bit 0 last.
FONT = {
    "A": (14, 17, 17, 31, 17, 17, 17),
    "B": (30, 17, 17, 30, 17, 17, 30),
    "C": (14, 17, 16, 16, 16, 17, 14),
    "D": (30, 17, 17, 17, 17, 17, 30),
    "E": (31, 16, 16, 30, 16, 16, 31),
    "F": (31, 16, 16, 30, 16, 16, 16),
    "G": (14, 17, 16, 23, 17, 17, 15),
    "H": (17, 17, 17, 31, 17, 17, 17),
    "I": (14, 4, 4, 4, 4, 4, 14),
    "J": (7, 2, 2, 2, 2, 18, 12),
    "K": (17, 18, 20, 24, 20, 18, 17),
    "L": (16, 16, 16, 16, 16, 16, 31),
    "M": (17, 27, 21, 21, 17, 17, 17),
    "N": (17, 25, 21, 19, 17, 17, 17),
    "O": (14, 17, 17, 17, 17, 17, 14),
    "P": (30, 17, 17, 30, 16, 16, 16),
    "Q": (14, 17, 17, 17, 21, 18, 13),
    "R": (30, 17, 17, 30, 20, 18, 17),
    "S": (15, 16, 16, 14, 1, 1, 30),
    "T": (31, 4, 4, 4, 4, 4, 4),
    "U": (17, 17, 17, 17, 17, 17, 14),
    "V": (17, 17, 17, 17, 17, 10, 4),
    "W": (17, 17, 17, 21, 21, 27, 17),
    "X": (17, 17, 10, 4, 10, 17, 17),
    "Y": (17, 17, 10, 4, 4, 4, 4),
    "Z": (31, 1, 2, 4, 8, 16, 31),
    "0": (14, 17, 19, 21, 25, 17, 14),
    "1": (4, 12, 4, 4, 4, 4, 14),
    "2": (14, 17, 1, 2, 4, 8, 31),
    "3": (31, 2, 4, 2, 1, 17, 14),
    "4": (2, 6, 10, 18, 31, 2, 2),
    "5": (31, 16, 30, 1, 1, 17, 14),
    "6": (6, 8, 16, 30, 17, 17, 14),
    "7": (31, 1, 2, 4, 8, 8, 8),
    "8": (14, 17, 17, 14, 17, 17, 14),
    "9": (14, 17, 17, 15, 1, 2, 12),
    " ": (0, 0, 0, 0, 0, 0, 0),
    ",": (0, 0, 0, 0, 12, 4, 8),
    ".": (0, 0, 0, 0, 0, 12, 12),
    "'": (4, 4, 8, 0, 0, 0, 0),
    "-": (0, 0, 0, 14, 0, 0, 0),
    ":": (0, 12, 12, 0, 12, 12, 0),
    ";": (0, 12, 12, 0, 12, 4, 8),
    "!": (4, 4, 4, 4, 4, 0, 4),
    "?": (14, 17, 1, 2, 4, 0, 4),
    "/": (1, 1, 2, 4, 8, 16, 16),
    "(": (2, 4, 8, 8, 8, 4, 2),
    ")": (8, 4, 2, 2, 2, 4, 8),
    "<": (2, 4, 8, 16, 8, 4, 2),
    ">": (8, 4, 2, 1, 2, 4, 8),
    "+": (0, 4, 4, 31, 4, 4, 0),
    "=": (0, 0, 31, 0, 31, 0, 0),
    '"': (10, 10, 10, 0, 0, 0, 0),
    "$": (4, 15, 20, 14, 5, 30, 4),
    "%": (25, 25, 2, 4, 8, 19, 19),
    "*": (0, 4, 21, 14, 21, 4, 0),
    "_": (0, 0, 0, 0, 0, 0, 31),
}


class Canvas:
    """A plain RGB pixel buffer with small vector drawing helpers."""

    def __init__(self, width, height, bg):
        self.w = width
        self.h = height
        self.px = bytearray(bg) * (width * height)

    def dot(self, x, y, colour):
        if 0 <= x < self.w and 0 <= y < self.h:
            at = (y * self.w + x) * 3
            self.px[at] = colour[0]
            self.px[at + 1] = colour[1]
            self.px[at + 2] = colour[2]

    def rect(self, x, y, w, h, colour):
        stripe = bytes(colour) * w
        left = max(x, 0)
        right = min(x + w, self.w)
        if right <= left:
            return
        for yy in range(max(y, 0), min(y + h, self.h)):
            at = (yy * self.w + left) * 3
            self.px[at:at + 3 * (right - left)] = \
                stripe[3 * (left - x):3 * (right - x)]

    def frame(self, x, y, w, h, colour, thick=2):
        self.rect(x, y, w, thick, colour)
        self.rect(x, y + h - thick, w, thick, colour)
        self.rect(x, y, thick, h, colour)
        self.rect(x + w - thick, y, thick, h, colour)

    def hline(self, x, y, w, colour, thick=1):
        self.rect(x, y, w, thick, colour)

    def vline(self, x, y, h, colour, thick=1):
        self.rect(x, y, thick, h, colour)

    def line(self, x0, y0, x1, y1, colour, thick=1):
        # Bresenham walk; each step stamps a thick square.
        run = abs(x1 - x0)
        rise = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = run + rise
        px, py = x0, y0
        half = thick // 2
        while True:
            self.rect(px - half, py - half, thick, thick, colour)
            if px == x1 and py == y1:
                return
            e2 = 2 * err
            if e2 >= rise:
                err += rise
                px += sx
            if e2 <= run:
                err += run
                py += sy

    def disc(self, cx, cy, r, colour):
        # Filled circle, one horizontal run per row.
        for yy in range(cy - r, cy + r + 1):
            dx = int(math.sqrt(max(0, r * r - (yy - cy) * (yy - cy))))
            self.rect(cx - dx, yy, 2 * dx + 1, 1, colour)

    def ring(self, cx, cy, r, colour, thick=3):
        # Circle outline: pixels whose distance is near r.
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                d2 = (xx - cx) * (xx - cx) + (yy - cy) * (yy - cy)
                if (r - thick) * (r - thick) <= d2 <= r * r:
                    self.dot(xx, yy, colour)

    def tri(self, ax, ay, bx, by, cx, cy, colour):
        # Filled triangle by scanlines between its three edges.
        top = min(ay, by, cy)
        bottom = max(ay, by, cy)
        edges = ((ax, ay, bx, by), (bx, by, cx, cy), (cx, cy, ax, ay))
        for yy in range(top, bottom + 1):
            hits = []
            for (x1, y1, x2, y2) in edges:
                if y1 == y2:
                    continue
                low, high = (y1, y2) if y1 < y2 else (y2, y1)
                if low <= yy < high or (yy == bottom and yy == high):
                    hits.append(x1 + (x2 - x1) * (yy - y1) / (y2 - y1))
            if len(hits) >= 2:
                self.rect(int(min(hits)), yy,
                          int(max(hits)) - int(min(hits)) + 1, 1, colour)

    def four_star(self, cx, cy, r, colour):
        # A four-pointed star: four triangles meeting at the centre.
        self.tri(cx, cy - r, cx + r // 4, cy, cx - r // 4, cy, colour)
        self.tri(cx, cy + r, cx + r // 4, cy, cx - r // 4, cy, colour)
        self.tri(cx - r, cy, cx, cy - r // 4, cx, cy + r // 4, colour)
        self.tri(cx + r, cy, cx, cy - r // 4, cx, cy + r // 4, colour)


def text_w(text, scale):
    # Six pixels per character cell (five glyph pixels plus spacing).
    return len(text) * 6 * scale


def draw_text(cv, x, y, text, scale, colour):
    """Draw uppercase text; a character outside the font is blank."""
    cursor = x
    for ch in text:
        rows = FONT.get(ch) or FONT[" "]
        for row_no, bits in enumerate(rows):
            for col_no in range(5):
                if bits & (16 >> col_no):
                    cv.rect(cursor + col_no * scale,
                            y + row_no * scale, scale, scale, colour)
        cursor += 6 * scale
    return cursor


def draw_centred(cv, x, y, width, text, scale, colour):
    draw_text(cv, x + (width - text_w(text, scale)) // 2,
              y, text, scale, colour)


def wrap(text, max_w, scale):
    """Greedy word wrap into lines that fit max_w pixels at scale."""
    out = []
    for word in text.split(" "):
        if out and text_w(out[-1] + " " + word, scale) <= max_w:
            out[-1] += " " + word
        else:
            out.append(word)
    return out


# ---------------------------------------------------------------- scenes

def coat_of_arms(cv, cx, top):
    """Shield, star and waves: the arms of Virelia."""
    # Four-pointed gold star above the shield.
    cv.four_star(cx, top + 10, 16, GOLD)
    # Shield: blue field, gold border, white stripe, pointed base.
    cv.rect(cx - 34, top + 30, 68, 44, BLUE)
    cv.tri(cx - 34, top + 74, cx + 34, top + 74, cx, top + 98, BLUE)
    cv.frame(cx - 34, top + 30, 68, 44, GOLD, 3)
    cv.line(cx - 34, top + 74, cx, top + 98, GOLD, 3)
    cv.line(cx + 34, top + 74, cx, top + 98, GOLD, 3)
    cv.rect(cx - 34, top + 48, 68, 8, WHITE)
    cv.disc(cx, top + 41, 7, GOLD)
    # Three waves under the shield, for the Meridian Sea.
    for i, wy in enumerate((top + 106, top + 114, top + 122)):
        for k in range(5):
            wx = cx - 44 + k * 20
            cv.line(wx, wy + (4 if k % 2 else 0),
                    wx + 10, wy + (0 if k % 2 else 4), SEA, 2)


def portrait(cv, bx, by, w, h):
    """A passport photograph: silhouette of the holder."""
    cv.rect(bx, by, w, h, SKY)
    # Faint diagonal guilloche lines across the photo, clipped to
    # the box: each line is drawn row by row inside the frame.
    for i in range(-h, w, 14):
        for yy in range(by, by + h):
            xx = bx + i + (yy - by)
            if bx <= xx < bx + w:
                cv.dot(xx, yy, (170, 188, 214))
    # Head and shoulders of the holder, dark silhouette.
    cv.disc(bx + w // 2, by + 62, 32, NAVY)
    cv.tri(bx + w // 2 - 52, by + h, bx + w // 2 + 52, by + h,
           bx + w // 2, by + 96, NAVY)
    cv.rect(bx + w // 2 - 52, by + 138, 104, h - 138, NAVY)
    # A gold hair band and a small earring, the only details.
    cv.line(bx + w // 2 - 30, by + 38, bx + w // 2 + 30, by + 38,
            GOLD, 3)
    cv.disc(bx + w // 2 + 30, by + 66, 3, GOLD)
    cv.frame(bx, by, w, h, INK, 2)


def island_map(cv, bx, by, w, h):
    """The island of Virelia in the Meridian Sea."""
    cv.rect(bx, by, w, h, SEA)
    # A few darker sea swells.
    for (sx, sy, sl) in ((24, 40, 60), (300, 200, 70), (330, 60, 50),
                         (40, 190, 56)):
        cv.line(bx + sx, by + sy, bx + sx + sl, by + sy + 6,
                SEA_DARK, 2)
    # The island: a cluster of sand discs forming one landmass.
    for (ix, iy, ir) in ((150, 130, 62), (210, 110, 52), (120, 170, 46),
                         (240, 160, 48), (180, 180, 56), (270, 120, 30),
                         (110, 120, 34)):
        cv.disc(bx + ix, by + iy, ir, SAND)
    # Coastline ring around the largest disc, for definition.
    cv.ring(bx + 150, by + 130, 62, GOLD_DARK, 2)
    # Mount Solenne, a peak in the island's north.
    cv.tri(bx + 205, by + 78, bx + 225, by + 78, bx + 215, by + 58,
           NAVY)
    cv.tri(bx + 211, by + 68, bx + 219, by + 68, bx + 215, by + 58,
           WHITE)
    draw_text(cv, bx + 120, by + 88, "MT SOLENNE", 2, INK)
    # The capital, Aerthys, marked with a gold star on the coast.
    cv.four_star(bx + 150, by + 150, 12, GOLD)
    cv.ring(bx + 150, by + 150, 16, GOLD_DARK, 2)
    draw_text(cv, bx + 168, by + 144, "AERTHYS", 2, INK)
    # Port Lumen on the southern shore.
    cv.disc(bx + 190, by + 205, 5, RED)
    draw_text(cv, bx + 200, by + 198, "PORT LUMEN", 2, INK)
    # A small northern islet.
    cv.disc(bx + 330, by + 40, 16, SAND)
    draw_text(cv, bx + 286, by + 64, "STAR ISLET", 2, WHITE)
    # Compass rose, lower right, clear of the labels.
    ccx, ccy = bx + w - 44, by + h - 44
    cv.four_star(ccx, ccy, 18, WHITE)
    draw_text(cv, ccx - 6, ccy - 34, "N", 2, WHITE)
    # Sea label, lower left.
    draw_text(cv, bx + 16, by + h - 26, "MERIDIAN SEA", 2, WHITE)
    cv.frame(bx, by, w, h, INK, 2)


def stamp_circle(cv, cx, cy, r, colour, lines):
    """A round border-control stamp with centred text lines."""
    cv.ring(cx, cy, r, colour, 3)
    cv.ring(cx, cy, r - 8, colour, 2)
    step = 18
    top = cy - (len(lines) * step) // 2
    for i, line_text in enumerate(lines):
        draw_centred(cv, cx - r, top + i * step, 2 * r,
                     line_text, 2, colour)


def stamp_visa(cv, x, y, w, h, colour):
    """A rectangular visa sticker, granted by Nordhaven."""
    cv.rect(x, y, w, h, WHITE)
    cv.frame(x, y, w, h, colour, 3)
    cv.frame(x + 8, y + 8, w - 16, h - 16, colour, 1)
    draw_centred(cv, x, y + 16, w, "VISA", 3, colour)
    draw_centred(cv, x, y + 44, w, "NORDHAVEN", 2, colour)
    draw_centred(cv, x, y + 66, w, "GRANTED", 2, colour)
    draw_centred(cv, x, y + 88, w, "90 DAYS", 2, colour)
    # A small crown mark above the word VISA.
    cv.tri(x + w // 2 - 12, y + 12, x + w // 2 + 12, y + 12,
           x + w // 2, y + 2, colour)


# ---------------------------------------------------------------- data

FIELDS = [
    ("TYPE", "P"),
    ("CODE", "VIR"),
    ("NO.", "V-2026-084213"),
    ("SURNAME", "MARLOWE"),
    ("GIVEN NAMES", "ELARA VOSS"),
    ("NATIONALITY", "VIRELIAN"),
    ("BORN", "14 MAR 1998 - F"),
    ("PLACE OF BIRTH", "AERTHYS"),
    ("ISSUED", "21 NOV 2026"),
    ("EXPIRES", "21 NOV 2036"),
]

MRZ = [
    "P<VIRMARLOWE<<ELARA<VOSS<<<<<<",
    "V2026084213VIR9803148F3611210<2",
]


# ---------------------------------------------------------------- layout

def data_page(cv, x0, y0, w, h):
    """The left page: the holder's data page."""
    cv.rect(x0, y0, w, h, PAGE)
    cv.frame(x0, y0, w, h, INK, 2)
    cv.frame(x0 + 8, y0 + 8, w - 16, h - 16, GOLD, 2)
    cx = x0 + w // 2
    draw_centred(cv, x0, y0 + 20, w, "REPUBLIC OF VIRELIA", 3, INK)
    draw_centred(cv, x0, y0 + 54, w, "PASSPORT", 6, RED)
    cv.hline(x0 + 28, y0 + 104, w - 56, GOLD, 3)
    coat_of_arms(cv, cx, y0 + 118)
    draw_centred(cv, x0, y0 + 252, w, "PER MARE ET STELLAS", 2, GREY)
    # Photograph on the left, data fields on the right.
    px, py = x0 + 24, y0 + 282
    portrait(cv, px, py, 140, 186)
    draw_centred(cv, px, py + 192, 140, "PHOTO", 2, GREY)
    fx = x0 + 182
    for i, (label, value) in enumerate(FIELDS):
        fy = y0 + 282 + i * 30
        draw_text(cv, fx, fy, label, 2, GREY)
        draw_text(cv, fx, fy + 14, value, 2, INK)
    # Holder's signature.
    sy = y0 + 596
    cv.hline(x0 + 24, sy, 240, INK, 2)
    draw_text(cv, x0 + 24, sy + 10, "HOLDER'S SIGNATURE", 2, GREY)
    draw_text(cv, x0 + 288, sy - 6, "MINISTRY OF", 2, GREY)
    draw_text(cv, x0 + 288, sy + 10, "THE INTERIOR", 2, GREY)
    # Machine-readable zone, two lines at the foot of the page.
    cv.rect(x0 + 24, y0 + 640, w - 48, 56, WHITE)
    cv.frame(x0 + 24, y0 + 640, w - 48, 56, GREY, 1)
    draw_text(cv, x0 + 36, y0 + 650, MRZ[0], 2, INK)
    draw_text(cv, x0 + 36, y0 + 672, MRZ[1], 2, INK)


def visa_page(cv, x0, y0, w, h):
    """The right page: visas, stamps and the island map."""
    cv.rect(x0, y0, w, h, PAGE)
    cv.frame(x0, y0, w, h, INK, 2)
    cv.frame(x0 + 8, y0 + 8, w - 16, h - 16, GOLD, 2)
    draw_centred(cv, x0, y0 + 20, w, "VISAS", 5, INK)
    draw_centred(cv, x0, y0 + 64, w, "STAMPS OF THE MERIDIAN SEA",
                 2, GREY)
    cv.hline(x0 + 28, y0 + 96, w - 56, GOLD, 3)
    island_map(cv, x0 + 24, y0 + 112, w - 48, 250)
    # Arrival stamp, lower left; granted visa, mid right.
    stamp_circle(cv, x0 + 127, y0 + 472, 62, RED,
                 ["AERTHYS", "ARRIVAL", "21 NOV"])
    stamp_visa(cv, x0 + 217, y0 + 417, 210, 118, BLUE)
    # Departure stamp, bottom left.
    stamp_circle(cv, x0 + 127, y0 + 617, 60, VIOLET,
                 ["PORT", "LUMEN", "DEPARTED"])
    # The fine print at the foot of the page.
    draw_centred(cv, x0, y0 + 692, w, "PER MARE ET STELLAS", 2, GOLD_DARK)
    draw_centred(cv, x0, y0 + 716, w,
                 "THIS PASSPORT REMAINS THE PROPERTY", 2, INK)
    draw_centred(cv, x0, y0 + 734, w,
                 "OF THE REPUBLIC OF VIRELIA", 2, INK)


def compose():
    cv = Canvas(W, H, DESK)
    cv.frame(12, 12, W - 24, H - 24, GOLD, 3)
    cv.frame(20, 20, W - 40, H - 40, GOLD_DARK, 1)
    draw_centred(cv, 0, 34, W, "THE PASSPORT PAGE", 5, GOLD)
    draw_centred(cv, 0, 78, W, "OF A COUNTRY THAT ISN'T THERE", 3, WHITE)
    cv.hline(36, 110, W - 72, GOLD, 2)
    # The open passport: data page left, visa page right.
    data_page(cv, 36, 128, 460, 760)
    visa_page(cv, 528, 128, 460, 760)
    # Gutter shadow between the two pages.
    cv.vline(512, 128, 760, (8, 26, 24), 4)
    cv.vline(520, 128, 760, (8, 26, 24), 2)
    # Footer: the invented country's facts.
    cv.hline(36, 908, W - 72, GOLD, 2)
    draw_centred(cv, 0, 922, W,
                 "REPUBLIC OF VIRELIA - EST. 1927", 2, GOLD)
    draw_centred(cv, 0, 946, W,
                 "POPULATION 84,213 - CAPITAL AERTHYS - CURRENCY LUMEN",
                 2, WHITE)
    draw_centred(cv, 0, 970, W,
                 "AN ISLAND IN THE MERIDIAN SEA - IT ISN'T THERE",
                 2, GREY)
    return cv


def encode_png(cv):
    """Encode the canvas as a 1024x1024 RGB PNG, filter 0 per row."""

    def pack(kind, payload):
        framed = struct.pack(">I", len(payload)) + kind + payload
        return framed + struct.pack(">I", zlib.crc32(kind + payload)
                                    & 0xFFFFFFFF)

    header = struct.pack(">IIBBBBB", cv.w, cv.h, 8, 2, 0, 0, 0)
    raw = bytearray()
    for row_no in range(cv.h):
        raw.append(0)
        raw += cv.px[row_no * cv.w * 3:(row_no + 1) * cv.w * 3]
    return (b"\x89PNG\r\n\x1a\n" + pack(b"IHDR", header)
            + pack(b"IDAT", zlib.compress(bytes(raw), 6))
            + pack(b"IEND", b""))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    data = encode_png(compose())
    path = os.path.join(out_dir, "entry.png")
    with open(path, "wb") as f:
        f.write(data)
    print("wrote %s (%d bytes, %dx%d)" % (path, len(data), W, H))


if __name__ == "__main__":
    main()
