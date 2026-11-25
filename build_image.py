#!/usr/bin/env python3
"""Render entry.png for make.fun news-image-20261125 (Wednesday 25 November 2026).

Flat editorial illustration drawn with PIL shapes only. No photos, no AI images.
Layout follows the winning superskie template: serif masthead, UTC strip +
numbers strip at the top, 3 illustrated leads with number banners, 10 fully
illustrated tiles with verification badges, world map + dense 3-column index +
DATE CHECK at the bottom.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
M = 14                      # outer margin
CW = W - 2 * M              # content width = 996

# ---------- palette ----------
PAPER = (246, 241, 231)
INK = (22, 22, 22)
MUTED = (90, 86, 78)
RED = (179, 32, 44)
NAVY = (30, 58, 95)
TEAL = (15, 118, 110)
GOLD = (184, 134, 11)
GREEN = (30, 125, 50)
GREY = (100, 116, 139)
LINE = (200, 192, 176)
CARD = (255, 255, 255)
SKY = (244, 217, 160)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SERIF = os.path.join(FONT_DIR, "DejaVuSerif.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")

_cache = {}


def font(size, bold=False, serif=False):
    key = (size, bold, serif)
    if key not in _cache:
        path = SERIF_B if (serif and bold) else SERIF if serif else SANS_B if bold else SANS
        _cache[key] = ImageFont.truetype(path, size)
    return _cache[key]


def wrap(d, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(d, x, y, lines, fnt, fill, lh, align="left", width=None):
    for ln in lines:
        if align == "center":
            d.text((x + (width - d.textlength(ln, font=fnt)) / 2, y), ln, font=fnt, fill=fill)
        else:
            d.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def badge(d, x, y, kind):
    """Verification pill. Returns width used."""
    colors = {"OFFICIAL": GREEN, "CONFIRMED": NAVY, "REPORTED": GREY}
    fnt = font(8, bold=True)
    label = kind
    tw = d.textlength(label, font=fnt)
    w = int(tw) + 10
    h = 13
    d.rounded_rectangle([x, y, x + w, y + h], radius=6, fill=colors[kind])
    d.text((x + 5, y + 2), label, font=fnt, fill=(255, 255, 255))
    return w


# ---------- region colours ----------
REGION_COLOR = {
    "Middle East": RED,
    "East Asia": NAVY,
    "China": GOLD,
    "South Asia": TEAL,
    "Oceania": (46, 125, 50),
    "SE Asia": (230, 126, 34),
    "Africa": (106, 61, 154),
    "N. America": (74, 111, 165),
    "Europe": (100, 116, 139),
    "Global": (156, 163, 175),
}

# ---------- content (all verified 25 Nov 2026, cross-checked 2+ outlets unless REPORTED) ----------
LEADS = [
    {
        "banner": "2 DRONES DOWNED", "band": RED,
        "headline": "COALITION STRIKES HODEIDAH",
        "sub": "Saudi-led jets hit Yemen's Red Sea port after an evacuation warning; Houthis threaten Jeddah and every Saudi Red Sea port.",
        "badge": "CONFIRMED", "region": "Middle East", "art": "port",
    },
    {
        "banner": "-2.9%", "band": NAVY,
        "headline": "NIKKEI TUMBLES 2.9%",
        "sub": "SoftBank -13%, Advantest -13% as tariff threats and a US tech slide hammer Asian markets; the yen sits near 159.2.",
        "badge": "CONFIRMED", "region": "East Asia", "art": "chart",
    },
    {
        "banner": "90+ EXPERIMENTS", "band": TEAL,
        "headline": "SHENZHOU-24 LIFTS OFF",
        "sub": "China launches its crewed mission to Tiangong with the first foreign astronaut: Pakistani payload specialist Zeeshan Ali, 40.",
        "badge": "OFFICIAL", "region": "China", "art": "rocket",
    },
]

UTC_STRIP = [
    ("00:18", "SHENZHOU-24 LIFTS OFF"),
    ("00:19", "NIKKEI OPENS -2.8%"),
    ("00:20", "HODEIDAH STRIKES REPORTED"),
    ("01:36", "SENATE PASSES DUTY OF CARE"),
    ("01:45", "NIKKEI -2.41%, SOFTBANK -13%"),
    ("02:00", "ASIAN STOCKS TUMBLE"),
    ("03:20", "HOUTHIS THREATEN JEDDAH"),
]

NUMBERS_STRIP = [
    ("-2.9%", "NIKKEI'S WEDNESDAY FALL"),
    ("-13%", "SOFTBANK'S DROP"),
    ("4.3%", "AUSTRALIA'S INFLATION"),
    ("90+", "EXPERIMENTS ON SHENZHOU-24"),
    ("$86,050", "BITCOIN ON WEDNESDAY"),
    ("Rs 15,000 CR", "INDIA'S AID TO NEPAL"),
]

TILES = [
    ("DUTY OF CARE PASSES", "Australia's Senate votes 36-23; fines up to 5% of global revenue", "OFFICIAL", "Oceania", "shield"),
    ("SHANGHAI PLEDGES LOYALTY", "City party chiefs back Beijing after Chen Jining probe", "CONFIRMED", "China", "tower"),
    ("IRAN ORDERS HORMUZ CLOSED", "Army chief: close it 'further day by day'", "REPORTED", "Middle East", "strait"),
    ("INFLATION JUMPS TO 4.3%", "Treasurer Chalmers calls it 'a very serious moment'", "CONFIRMED", "Oceania", "prices"),
    ("SOLOMONS SECURITY PACT", "Australia signs historic treaty to block China", "CONFIRMED", "Oceania", "flags"),
    ("US READIES TARIFF RISES", "16 economies in scope, incl. China, Japan, EU", "REPORTED", "East Asia", "tariffs"),
    ("BJP-SAD REUNION DRAWS FIRE", "CM-face row as Punjab allies reunite", "REPORTED", "South Asia", "ballot"),
    ("INDIA AIDS NEPAL: Rs 15,000 CR", "Development assistance announced for Kathmandu", "REPORTED", "South Asia", "mountain"),
    ("72 ORANGUTANS RESCUED", "Saved from West Kalimantan wildfires since August", "REPORTED", "SE Asia", "orangutan"),
    ("PALACE REJECTS DUTERTE CLAIMS", "No abuse in ex-president's ICC arrest, Manila says", "REPORTED", "SE Asia", "court"),
]

# index: (headline, fact, region, badge)
INDEX = [
    ("JAPAN SERVICES PPI +4.2%", "Highest since March 1990", "East Asia", "CONFIRMED"),
    ("NIKKEI POLL: 65,000 BY JUNE", "Reuters poll sees 67,500 by year-end", "East Asia", "CONFIRMED"),
    ("ASX SNAPS 8-DAY LOSING STREAK", "Nvidia rally lifts Sydney shares", "Oceania", "REPORTED"),
    ("BITCOIN $86,050, DOWN 1.3%", "Wednesday slide in Asia hours", "N. America", "CONFIRMED"),
    ("US 10-YEAR YIELD 4.02%", "Steady as Asia trades", "N. America", "CONFIRMED"),
    ("MSCI WORLD EDGES +0.1% HIGHER", "Global stocks hold up", "Global", "CONFIRMED"),
    ("DOLLAR/YEN NEAR 159.2", "Yen weak as Nikkei falls", "East Asia", "CONFIRMED"),
    ("STOXX 50 FUTURES -0.4%", "Europe set to open lower", "Europe", "CONFIRMED"),
    ("LABOR-GREENS HEALTH DEAL", "Pensioner exemption; A$3bn saving halved", "Oceania", "REPORTED"),
    ("ONE NATION VOWS REPEAL", "Hanson: all four senators voted no", "Oceania", "REPORTED"),
    ("SMALL BUSINESS SITES EXEMPT", "Duty-of-care duties waived", "Oceania", "REPORTED"),
    ("NSW POLICE + CYBER COMMAND", "Joint centre pilot begins", "Oceania", "REPORTED"),
    ("CENSUS: WEST SYDNEY +79,600", "Professionals surge in five years", "Oceania", "REPORTED"),
    ("EX-COP MURDER VERDICT", "Beau Lamarre-Condon trial, Sydney", "Oceania", "REPORTED"),
    ("MELANOMA SURVIVAL RECORD HIGH", "Cancer Council data", "Oceania", "REPORTED"),
    ("KARNATAKA MOVES ON CAUVERY", "Asks top court on river-linking", "South Asia", "REPORTED"),
    ("INDONESIA SEEKS UK TRADE DEAL", "Comprehensive pact pushed", "SE Asia", "REPORTED"),
    ("MANILA BUDGETS PHP35.2BN", "Embassy upkeep plan for 2027", "SE Asia", "REPORTED"),
    ("THAILAND DEFERS THB20BN SCHEME", "Civil-service retirement plan delayed", "SE Asia", "REPORTED"),
    ("BANGKOK RAIL SIGN-UP DEC 15", "Common ticket via Paotang app", "SE Asia", "REPORTED"),
    ("GUINEA UNVEILS NEW DOCTRINE", "PM sets course for government", "Africa", "REPORTED"),
    ("COMOROS REOPENS HISTORIC LYCEE", "Said Mohamed Cheikh school inaugurated", "Africa", "REPORTED"),
]

DATE_CHECK_EXCLUDED = ("EXCLUDED AS EARLIER NEWS: COP31 collapse (22 Nov) · Hamas security chief killed (24 Nov) · "
                       "Houthi drone on Riyadh (24 Nov) · Nepal quake (24 Nov) · EU sanctions (23 Nov) · "
                       "Trump turkey pardon (24 Nov)")
DATE_CHECK_NOTYET = ("NOT YET: US core PCE data due 13:30 UTC - US markets closed Thu for Thanksgiving - "
                     "ESA Hera's first Dimorphos close-ups - Shenzhou-24 docking with Tiangong")
DATE_CHECK_SURE = "HOW SURE: OFFICIAL = primary source  -  CONFIRMED = 2+ outlets  -  REPORTED = single outlet or claim"

# world map bitmap (52 x 24), '#' = land
WORLD_MAP = [
    "....########..........................#############....",
    "...##########......##.................###############.",
    "..############....####......##.........################",
    "..###########.....#####....###.........################",
    "...##########.....####....###..........###############.",
    "....########......###....###...........##############..",
    ".....######.......###....###...........#############...",
    "......####........###....####..........############....",
    ".......###........###....#####.........###########.....",
    "........##........###....######.........#########......",
    ".........##.......####...######.........#######........",
    ".........###......####...######.........######.........",
    "..........####....####...#####..........#####..........",
    "..........#####...####...#####..........####...........",
    "...........#####..####....####.........###.............",
    "...........#####..####....###..........................",
    "............####..####................................",
    "............###...###.........................######...",
    ".............##..............................#######..",
    ".............................................######...",
    "..............................................####....",
    "......................................................",
    "......................................................",
    "......................................................",
]
MAP_PINS = [  # (grid col, grid row, number)
    (31, 8, "1"),   # Hodeidah, Yemen
    (45, 6, "2"),   # Tokyo
    (38, 4, "3"),   # Jiuquan
    (41, 6, "4"),   # Shanghai
    (45, 18, "5"),  # Canberra
    (34, 7, "6"),   # New Delhi
    (39, 12, "7"),  # Jakarta
    (24, 11, "8"),  # Conakry
]
MAP_KEY = ["1 HODEIDAH - 2 TOKYO - 3 JIUQUAN - 4 SHANGHAI",
           "5 CANBERRA - 6 DELHI - 7 JAKARTA - 8 CONAKRY"]

# ---------- lead illustrations (flat shapes only) ----------

def art_port(d, x, y, w, h):
    """Hodeidah port at dawn: sky, sea, cargo ship, cranes, smoke, blast."""
    d.rectangle([x, y, x + w, y + h], fill=(244, 217, 160))
    d.ellipse([x + w - 66, y + 10, x + w - 26, y + 50], fill=(232, 161, 60))
    # sea
    d.rectangle([x, y + h - 46, x + w, y + h], fill=(46, 95, 138))
    d.line([x + 6, y + h - 34, x + w - 6, y + h - 34], fill=(120, 170, 205), width=2)
    d.line([x + 20, y + h - 20, x + w - 20, y + h - 20], fill=(120, 170, 205), width=2)
    # cranes (left)
    for cx in (x + 26, x + 66):
        d.line([cx, y + 26, cx, y + h - 46], fill=(31, 41, 55), width=4)
        d.line([cx - 22, y + 30, cx + 30, y + 30], fill=(31, 41, 55), width=3)
        d.line([cx + 30, y + 30, cx + 44, y + 58], fill=(31, 41, 55), width=2)
    # cargo ship
    sx, sy = x + w - 210, y + h - 78
    d.polygon([(sx, sy + 22), (sx + 180, sy + 22), (sx + 168, sy + 44), (sx + 12, sy + 44)],
              fill=(31, 41, 55))
    cols = [(179, 32, 44), (15, 118, 110), (201, 162, 39), (30, 58, 95)]
    for i, c in enumerate(cols):
        d.rectangle([sx + 14 + i * 42, sy - 6, sx + 52 + i * 42, sy + 22], fill=c)
    # blast + smoke (right) — keep every shape inside the art box
    bx, by = x + w - 46, y + 62
    d.polygon([(bx, by - 26), (bx + 8, by - 8), (bx + 26, by - 12), (bx + 14, by + 4),
               (bx + 28, by + 14), (bx + 8, by + 12), (bx, by + 28), (bx - 8, by + 12),
               (bx - 28, by + 14), (bx - 14, by + 4), (bx - 26, by - 12), (bx - 8, by - 8)],
              fill=(232, 126, 34))
    d.ellipse([bx - 10, by - 10, bx + 10, by + 10], fill=(251, 191, 36))
    for ox, oy, r in ((bx - 36, by - 34, 10), (bx - 14, by - 46, 12), (bx + 10, by - 36, 9)):
        d.ellipse([ox - r, oy - r, ox + r, oy + r], fill=(120, 120, 120))


def art_chart(d, x, y, w, h):
    """Nikkei selloff: dark board, grid, falling red line, candlesticks, down arrow."""
    d.rectangle([x, y, x + w, y + h], fill=(22, 35, 58))
    for gy in range(y + 22, y + h, 26):
        d.line([x + 8, gy, x + w - 8, gy], fill=(48, 66, 96), width=1)
    for gx in range(x + 24, x + w, 44):
        d.line([gx, y + 8, gx, y + h - 8], fill=(48, 66, 96), width=1)
    # candlesticks
    sticks = [(x + 30, 26, 12, (34, 197, 94)), (x + 66, 44, 14, (239, 68, 68)),
              (x + 102, 62, 12, (239, 68, 68)), (x + 138, 78, 16, (239, 68, 68)),
              (x + 176, 92, 12, (34, 197, 94)), (x + 212, 104, 14, (239, 68, 68))]
    for sx, top, bh, c in sticks:
        d.rectangle([sx, y + top, sx + 16, y + top + bh], fill=c)
        d.line([sx + 8, y + top - 8, sx + 8, y + top + bh + 8], fill=c, width=2)
    # falling line
    pts = [(x + 16, y + 18), (x + 70, y + 42), (x + 120, y + 58), (x + 170, y + 88),
           (x + 225, y + 100), (x + 275, y + 122), (x + w - 14, y + 138)]
    d.line(pts, fill=(239, 68, 68), width=4, joint="curve")
    for px, py in pts:
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(251, 191, 36))
    # down arrow (right)
    ax, ay = x + w - 58, y + h - 52
    d.polygon([(ax + 14, ay), (ax + 30, ay + 22), (ax + 20, ay + 22), (ax + 20, ay + 40),
               (ax + 8, ay + 40), (ax + 8, ay + 22), (ax - 2, ay + 22)], fill=(239, 68, 68))


def art_rocket(d, x, y, w, h):
    """Shenzhou-24 liftoff: night sky, stars, moon, rocket, flame, tower."""
    d.rectangle([x, y, x + w, y + h], fill=(11, 30, 58))
    for sx, sy, r in ((x + 24, y + 18, 2), (x + 60, y + 34, 1), (x + 96, y + 12, 2),
                      (x + 150, y + 26, 1), (x + 210, y + 14, 2), (x + 250, y + 40, 1),
                      (x + 290, y + 18, 2), (x + 30, y + 60, 1), (x + 280, y + 70, 1)):
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(255, 255, 255))
    d.ellipse([x + w - 74, y + 12, x + w - 34, y + 52], fill=(240, 230, 200))
    d.ellipse([x + w - 66, y + 8, x + w - 30, y + 44], fill=(11, 30, 58))
    # ground
    d.rectangle([x, y + h - 22, x + w, y + h], fill=(45, 55, 45))
    # launch tower (left of rocket)
    tx = x + w // 2 - 74
    d.rectangle([tx, y + 40, tx + 12, y + h - 22], fill=(120, 125, 130))
    for by in range(y + 52, y + h - 30, 18):
        d.line([tx, by, tx + 12, by], fill=(90, 95, 100), width=3)
    d.line([tx + 12, y + 46, tx + 44, y + 46], fill=(120, 125, 130), width=3)
    # rocket
    rx = x + w // 2 - 14
    d.polygon([(rx, y + 30), (rx + 14, y + 8), (rx + 28, y + 30)], fill=(179, 32, 44))
    d.rectangle([rx, y + 30, rx + 28, y + 96], fill=(245, 245, 240))
    d.rectangle([rx, y + 52, rx + 28, y + 60], fill=(179, 32, 44))
    d.polygon([(rx - 12, y + 96), (rx, y + 78), (rx, y + 96)], fill=(179, 32, 44))
    d.polygon([(rx + 28, y + 96), (rx + 28, y + 78), (rx + 40, y + 96)], fill=(179, 32, 44))
    # flame + smoke
    d.polygon([(rx + 4, y + 96), (rx + 14, y + h - 22), (rx + 24, y + 96)], fill=(232, 126, 34))
    d.polygon([(rx + 9, y + 96), (rx + 14, y + h - 30), (rx + 19, y + 96)], fill=(251, 191, 36))
    for ox, oy, r in ((rx - 22, y + h - 30, 12), (rx + 50, y + h - 28, 14), (rx + 62, y + h - 38, 10)):
        d.ellipse([ox - r, oy - r, ox + r, oy + r], fill=(200, 200, 200))


LEAD_ART = {"port": art_port, "chart": art_chart, "rocket": art_rocket}


# ---------- tile illustrations (small full-colour scenes) ----------

def tile_shield(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 58, 95))
    cx = x + w // 2
    d.polygon([(cx, y + 3), (cx + 30, y + 8), (cx + 30, y + h - 12),
               (cx, y + h - 2), (cx - 30, y + h - 12), (cx - 30, y + 8)], fill=(255, 255, 255))
    d.line([(cx - 12, y + h // 2), (cx - 2, y + h // 2 + 9),
            (cx + 14, y + h // 2 - 9)], fill=(30, 125, 50), width=4)


def tile_tower(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(244, 217, 160))
    d.ellipse([x + w - 34, y + 4, x + w - 6, y + 32], fill=(232, 126, 34))
    for bx, bw, bh in ((x + 6, 26, 30), (x + 120, 30, 36), (x + 152, 24, 26)):
        d.rectangle([bx, y + h - bh, bx + bw, y + h], fill=(90, 90, 95))
    cx = x + w // 2
    d.rectangle([cx - 3, y + 8, cx + 3, y + h], fill=(31, 41, 55))
    d.ellipse([cx - 12, y + 6, cx + 12, y + 22], fill=(179, 32, 44))
    d.ellipse([cx - 9, y + 22, cx + 9, y + 34], fill=(179, 32, 44))
    d.rectangle([cx - 16, y + 36, cx + 16, y + 40], fill=(31, 41, 55))


def tile_strait(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(46, 95, 138))
    d.polygon([(x, y), (x + 52, y), (x + 40, y + h), (x, y + h)], fill=(210, 180, 140))
    d.polygon([(x + w, y), (x + w - 52, y), (x + w - 40, y + h), (x + w, y + h)], fill=(210, 180, 140))
    d.rectangle([x + 62, y + h // 2 - 4, x + w - 62, y + h // 2 + 10], fill=(31, 41, 55))
    d.rectangle([x + w // 2 - 8, y + h // 2 - 14, x + w // 2 + 8, y + h // 2 - 4], fill=(179, 32, 44))
    d.polygon([(x + w - 30, y + 4), (x + w - 16, y + 24), (x + w - 44, y + 24)], fill=(251, 191, 36))
    d.text((x + w - 34, y + 10), "!", font=font(10, bold=True), fill=(22, 22, 22))


def tile_prices(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 248, 220))
    for cx, cy in ((x + 22, y + h - 12), (x + 44, y + h - 10), (x + 66, y + h - 12)):
        d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=(201, 162, 39))
        d.text((cx - 3, cy - 6), "$", font=font(10, bold=True), fill=(120, 90, 10))
    d.polygon([(x + w - 58, y + 8), (x + w - 8, y + 8), (x + w - 8, y + 30),
               (x + w - 58, y + 30), (x + w - 66, y + 19)], fill=(251, 191, 36))
    d.ellipse([x + w - 56, y + 15, x + w - 48, y + 23], fill=(255, 248, 220))
    # clean up arrow: vertical shaft + triangle head
    ax = x + w // 2 - 6
    d.rectangle([ax, y + 16, ax + 12, y + h - 8], fill=(179, 32, 44))
    d.polygon([(ax - 7, y + 16), (ax + 19, y + 16), (ax + 6, y + 2)], fill=(179, 32, 44))


def tile_flags(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(230, 240, 250))
    # Australia flag (left)
    d.rectangle([x + 8, y + 8, x + 82, y + h - 8], fill=(0, 40, 104))
    d.rectangle([x + 8, y + 8, x + 40, y + 20], fill=(255, 255, 255))
    d.line([x + 8, y + 14, x + 40, y + 14], fill=(179, 32, 44), width=3)
    d.line([x + 24, y + 8, x + 24, y + 20], fill=(179, 32, 44), width=3)
    for sx, sy in ((x + 66, y + 16), (x + 56, y + 28), (x + 72, y + 30)):
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 255, 255))
    # Solomon Islands flag (right)
    d.rectangle([x + w - 82, y + 8, x + w - 8, y + h - 8], fill=(0, 80, 160))
    d.polygon([(x + w - 82, y + h - 8), (x + w - 82, y + 8), (x + w - 8, y + 8)], fill=(0, 140, 70))
    for sx, sy in ((x + w - 66, y + 14), (x + w - 50, y + 16), (x + w - 70, y + 26),
                   (x + w - 56, y + 30), (x + w - 40, y + 14)):
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 255, 255))
    # shield between
    cx = x + w // 2
    d.polygon([(cx, y + h - 12), (cx + 10, y + h - 22), (cx + 10, y + h - 34),
               (cx, y + h - 28), (cx - 10, y + h - 34), (cx - 10, y + h - 22)], fill=(201, 162, 39))


def tile_tariffs(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 58, 95))
    d.rectangle([x + 10, y + h - 18, x + w - 60, y + h - 8], fill=(31, 41, 55))
    for i, c in enumerate(((179, 32, 44), (201, 162, 39), (15, 118, 110))):
        d.rectangle([x + 14 + i * 26, y + h - 34, x + 36 + i * 26, y + h - 18], fill=c)
    d.ellipse([x + w - 56, y + 4, x + w - 4, y + 40], fill=(179, 32, 44))
    d.text((x + w - 46, y + 12), "16", font=font(16, bold=True), fill=(255, 255, 255))


def tile_ballot(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(245, 235, 210))
    d.line([x + 30, y + 10, x + 30, y + 26], fill=(120, 90, 60), width=3)
    d.polygon([(x + 30, y + 8), (x + 56, y + 14), (x + 30, y + 20)], fill=(255, 153, 51))
    d.line([x + w - 40, y + 10, x + w - 40, y + 26], fill=(120, 90, 60), width=3)
    d.polygon([(x + w - 40, y + 8), (x + w - 66, y + 14), (x + w - 40, y + 20)], fill=(30, 58, 95))
    d.rectangle([x + w // 2 - 34, y + 22, x + w // 2 + 34, y + h - 6], fill=(30, 58, 95))
    d.rectangle([x + w // 2 - 20, y + 18, x + w // 2 + 20, y + 24], fill=(22, 22, 22))
    d.line([(x + w // 2 - 16, y + 32), (x + w // 2 - 4, y + 40), (x + w // 2 + 18, y + 26)],
           fill=(255, 255, 255), width=3)


def tile_mountain(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(200, 230, 245))
    d.ellipse([x + w - 30, y + 4, x + w - 8, y + 26], fill=(251, 191, 36))
    d.polygon([(x, y + h), (x + 50, y + 8), (x + 100, y + h)], fill=(120, 125, 130))
    d.polygon([(x + 50, y + 8), (x + 66, y + 24), (x + 34, y + 24)], fill=(255, 255, 255))
    d.polygon([(x + 80, y + h), (x + 140, y + 16), (x + w, y + h)], fill=(90, 95, 100))
    d.polygon([(x + 140, y + 16), (x + 152, y + 28), (x + 128, y + 28)], fill=(255, 255, 255))
    d.line([(x + 14, y + h - 10), (x + w - 14, y + 10)], fill=(30, 125, 50), width=3)
    d.polygon([(x + w - 26, y + 6), (x + w - 10, y + 10), (x + w - 20, y + 20)], fill=(30, 125, 50))


def tile_orangutan(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(34, 120, 60))
    for lx, ly, r in ((x + 12, y + 8, 10), (x + 30, y + 4, 8), (x + w - 16, y + 10, 10),
                      (x + w - 34, y + 4, 8), (x + 8, y + 26, 8)):
        d.ellipse([lx - r, ly - r, lx + r, ly + r], fill=(20, 90, 45))
    d.line([x + 10, y + h - 12, x + w - 10, y + h - 20], fill=(120, 90, 60), width=5)
    cx, cy = x + w // 2 + 14, y + h // 2 + 2
    d.ellipse([cx - 20, cy - 16, cx + 20, cy + 18], fill=(200, 100, 30))       # body
    d.ellipse([cx - 11, cy - 26, cx + 11, cy - 6], fill=(220, 130, 60))       # head
    d.ellipse([cx - 7, cy - 20, cx + 7, cy - 8], fill=(245, 210, 170))        # face
    d.ellipse([cx - 4, cy - 17, cx - 1, cy - 14], fill=(22, 22, 22))
    d.ellipse([cx + 1, cy - 17, cx + 4, cy - 14], fill=(22, 22, 22))
    d.line([cx - 20, cy - 8, cx - 34, cy + 10], fill=(200, 100, 30), width=5)  # arms
    d.line([cx + 20, cy - 8, cx + 34, cy - 12], fill=(200, 100, 30), width=5)


def tile_court(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(235, 228, 210))
    d.polygon([(x + w // 2 - 52, y + 12), (x + w // 2 + 52, y + 12), (x + w // 2, y + 2)], fill=(120, 100, 70))
    for i in range(3):
        cx = x + w // 2 - 34 + i * 34
        d.rectangle([cx - 5, y + 14, cx + 5, y + h - 12], fill=(245, 240, 225))
    d.rectangle([x + 12, y + h - 12, x + w - 12, y + h - 6], fill=(120, 100, 70))
    d.line([x + w - 44, y + 8, x + w - 20, y + 26], fill=(120, 90, 60), width=4)  # gavel
    d.rectangle([x + w - 48, y + 24, x + w - 16, y + 30], fill=(120, 90, 60))


TILE_ART = {"shield": tile_shield, "tower": tile_tower, "strait": tile_strait,
            "prices": tile_prices, "flags": tile_flags, "tariffs": tile_tariffs,
            "ballot": tile_ballot, "mountain": tile_mountain, "orangutan": tile_orangutan,
            "court": tile_court}


def draw_world_map(d, x, y, w, h):
    """Dot-matrix world map with numbered pins."""
    d.rectangle([x, y, x + w, y + h], fill=(220, 235, 245))
    cols, rows = 52, 24
    cw, ch = w / cols, h / rows
    for r, row in enumerate(WORLD_MAP):
        for c, ch2 in enumerate(row):
            if ch2 == "#":
                cx, cy = x + c * cw + cw / 2, y + r * ch + ch / 2
                d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=NAVY)
    for pc, pr, num in MAP_PINS:
        cx, cy = x + pc * cw + cw / 2, y + pr * ch + ch / 2
        d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=RED, outline=(255, 255, 255), width=1)
        fnt = font(8, bold=True)
        tw = d.textlength(num, font=fnt)
        d.text((cx - tw / 2, cy - 5), num, font=fnt, fill=(255, 255, 255))

# ---------- layout / render ----------

def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ===== masthead =====
    d.rectangle([M, 8, M + CW, 11], fill=RED)
    draw_lines(d, M, 14, ["WEDNESDAY 25 NOVEMBER 2026"], font(40, bold=True, serif=True),
               INK, 44, align="center", width=CW)
    draw_lines(d, M, 62, ["ONE DAY OF WORLD NEWS, ONE PICTURE"], font(15, bold=True),
               INK, 18, align="center", width=CW)
    draw_lines(d, M, 82, ["35 STORIES  ·  9 REGIONS  ·  19 FIELDS  ·  EVERY ONE FROM THIS WEDNESDAY"],
               font(12), MUTED, 15, align="center", width=CW)
    d.line([M, 100, M + CW, 100], fill=LINE, width=1)

    # ===== THE DAY IN UTC =====
    y = 106
    d.text((M, y), "THE DAY IN UTC", font=font(11, bold=True), fill=RED)
    cell_w = CW / 7
    for i, (t, txt) in enumerate(UTC_STRIP):
        cx = M + i * cell_w
        d.text((cx, y + 13), t, font=font(12, bold=True), fill=RED)
        lines = wrap(d, txt, font(10), cell_w - 8)[:2]
        draw_lines(d, cx, y + 27, lines, font(10), INK, 11)
        if i:
            d.line([cx - 4, y + 13, cx - 4, y + 49], fill=LINE, width=1)
    d.line([M, 158, M + CW, 158], fill=LINE, width=1)

    # ===== THE DAY IN NUMBERS =====
    y = 164
    d.text((M, y), "THE DAY IN NUMBERS", font=font(11, bold=True), fill=RED)
    cell_w = CW / 6
    for i, (num, label) in enumerate(NUMBERS_STRIP):
        cx = M + i * cell_w
        d.text((cx, y + 13), num, font=font(22, bold=True), fill=NAVY)
        lines = wrap(d, label, font(9), cell_w - 8)[:2]
        draw_lines(d, cx, y + 37, lines, font(9), MUTED, 10)
        if i:
            d.line([cx - 4, y + 13, cx - 4, y + 49], fill=LINE, width=1)
    d.line([M, 224, M + CW, 224], fill=LINE, width=1)

    # ===== 3 leads =====
    lead_w, lead_gap = 324, 12
    y0 = 230
    for i, lead in enumerate(LEADS):
        lx = M + i * (lead_w + lead_gap)
        d.rectangle([lx, y0, lx + lead_w, y0 + 316], fill=CARD, outline=LINE, width=1)
        # number banner (adaptive size so it never collides with the region tag)
        d.rectangle([lx + 1, y0 + 1, lx + lead_w - 1, y0 + 40], fill=lead["band"])
        rf = font(10, bold=True)
        rtxt = lead["region"].upper()
        rtw = d.textlength(rtxt, font=rf)
        bsize = 24
        while bsize > 18 and d.textlength(lead["banner"], font=font(bsize, bold=True)) > lead_w - 24 - rtw - 16:
            bsize -= 2
        d.text((lx + 12, y0 + 8), lead["banner"], font=font(bsize, bold=True), fill=(255, 255, 255))
        d.text((lx + lead_w - 12 - rtw, y0 + 14), rtxt, font=rf, fill=(255, 255, 255))
        # illustration
        LEAD_ART[lead["art"]](d, lx + 1, y0 + 41, lead_w - 2, 146)
        # headline + sub + badge
        hl = wrap(d, lead["headline"], font(15, bold=True, serif=True), lead_w - 24)[:2]
        draw_lines(d, lx + 12, y0 + 193, hl, font(15, bold=True, serif=True), INK, 18)
        sub = wrap(d, lead["sub"], font(11), lead_w - 24)[:3]
        draw_lines(d, lx + 12, y0 + 193 + len(hl) * 18 + 4, sub, font(11), MUTED, 14)
        badge(d, lx + 12, y0 + 316 - 22, lead["badge"])

    # ===== 10 tiles (2 rows x 5) =====
    tile_w, tile_h, tile_gap = 194, 91, 6
    ty0 = 552
    for i, (head, sub, bdg, region, art) in enumerate(TILES):
        row, col = divmod(i, 5)
        tx = M + col * (tile_w + tile_gap)
        ty = ty0 + row * (tile_h + 6)
        d.rectangle([tx, ty, tx + tile_w, ty + tile_h], fill=CARD, outline=LINE, width=1)
        TILE_ART[art](d, tx + 1, ty + 1, tile_w - 2, 42)
        hl = wrap(d, head, font(11, bold=True), tile_w - 12)[:2]
        draw_lines(d, tx + 6, ty + 47, hl, font(11, bold=True), INK, 13)
        badge(d, tx + 6, ty + tile_h - 18, bdg)
        rf = font(9)
        rtxt = region.upper()
        d.text((tx + tile_w - 6 - d.textlength(rtxt, font=rf), ty + tile_h - 17), rtxt,
               font=rf, fill=MUTED)

    # ===== bottom band: map + index =====
    yb = 746
    d.text((M, yb), "WHERE IT HAPPENED", font=font(11, bold=True), fill=RED)
    draw_world_map(d, M, yb + 16, 286, 140)
    kf = font(8)
    draw_lines(d, M, yb + 160, MAP_KEY, kf, MUTED, 11)

    ix = M + 294
    iw = W - M - ix
    d.text((ix, yb), "ALSO ON WEDNESDAY  -  22 MORE STORIES", font=font(11, bold=True), fill=RED)
    col_w = (iw - 16) / 3
    cols = [INDEX[0:8], INDEX[8:15], INDEX[15:22]]
    for ci, items in enumerate(cols):
        cx = ix + ci * (col_w + 8)
        iy = yb + 16
        for head, fact, region, bdg in items:
            # region dot + headline + mini badge
            d.ellipse([cx, iy + 3, cx + 6, iy + 9], fill=REGION_COLOR[region])
            bf = font(7, bold=True)
            btw = d.textlength(bdg, font=bf) + 8
            hw = col_w - 10 - btw - 4
            hlines = wrap(d, head, font(9, bold=True), hw)
            htxt = hlines[0]
            d.text((cx + 10, iy), htxt, font=font(9, bold=True), fill=INK)
            bx = cx + 10 + d.textlength(htxt, font=font(9, bold=True)) + 4
            # mini badge pill (7px)
            bcol = {"OFFICIAL": GREEN, "CONFIRMED": NAVY, "REPORTED": GREY}[bdg]
            d.rounded_rectangle([bx, iy - 1, bx + btw, iy + 11], radius=5, fill=bcol)
            d.text((bx + 4, iy + 1), bdg, font=bf, fill=(255, 255, 255))
            d.text((cx + 10, iy + 12), fact, font=font(9), fill=MUTED)
            iy += 24

    # ===== DATE CHECK =====
    dy = 956
    d.rectangle([M, dy, M + CW, 1012], outline=RED, width=2)
    d.text((M + 10, dy + 5), "DATE CHECK", font=font(10, bold=True), fill=RED)
    df = font(9)
    lines = []
    for txt in (DATE_CHECK_EXCLUDED, DATE_CHECK_NOTYET, DATE_CHECK_SURE):
        lines.extend(wrap(d, txt, df, CW - 20))
    draw_lines(d, M + 10, dy + 19, lines, df, INK, 11)

    img.save(OUT, optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    render()
