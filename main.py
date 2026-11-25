#!/usr/bin/env python3
"""News-image entry for Wednesday 25 November 2026.

Draws a one-page broadsheet summarising the day's world news and writes it
to /output/entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png for local runs).
Python standard library only; no network; deterministic output.
"""
import os
import struct
import zlib

W = 1024
H = 1024

PAPER = (250, 246, 236)
INK = (24, 24, 30)
RED = (178, 34, 34)
NAVY = (27, 48, 92)
TEAL = (16, 105, 102)
GOLD = (176, 124, 22)
GREY = (90, 88, 84)
RULE = (196, 188, 172)
CARD = (255, 253, 247)
BAND = (27, 48, 92)
BANDTX = (250, 246, 236)

# 5x7 bitmap glyphs, rows top to bottom, '#' = ink.
GLYPHS = {
    "A": [".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "B": ["####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."],
    "C": [".####", "#....", "#....", "#....", "#....", "#....", ".####"],
    "D": ["####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."],
    "E": ["#####", "#....", "#....", "####.", "#....", "#....", "#####"],
    "F": ["#####", "#....", "#....", "####.", "#....", "#....", "#...."],
    "G": [".####", "#....", "#....", "#.###", "#...#", "#...#", ".###."],
    "H": ["#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "I": ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "#####"],
    "J": ["#####", "....#", "....#", "....#", "....#", "#...#", ".###."],
    "K": ["#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"],
    "L": ["#....", "#....", "#....", "#....", "#....", "#....", "#####"],
    "M": ["#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"],
    "N": ["#...#", "##..#", "#.#.#", "#..##", "#...#", "#...#", "#...#"],
    "O": [".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "P": ["####.", "#...#", "#...#", "####.", "#....", "#....", "#...."],
    "Q": [".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"],
    "R": ["####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"],
    "S": [".####", "#....", "#....", ".###.", "....#", "....#", "####."],
    "T": ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."],
    "U": ["#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "V": ["#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."],
    "W": ["#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"],
    "X": ["#...#", ".#.#.", "..#..", "..#..", "..#..", ".#.#.", "#...#"],
    "Y": ["#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."],
    "Z": ["#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"],
    "0": [".###.", "#..##", "#.#.#", "##..#", "#...#", "#...#", ".###."],
    "1": ["..#..", ".##..", "..#..", "..#..", "..#..", "..#..", "#####"],
    "2": [".###.", "#...#", "....#", "...#.", "..#..", ".#...", "#####"],
    "3": ["#####", "...#.", "..#..", "...#.", "....#", "#...#", ".###."],
    "4": ["...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."],
    "5": ["#####", "#....", "####.", "....#", "....#", "#...#", ".###."],
    "6": [".###.", "#....", "#....", "####.", "#...#", "#...#", ".###."],
    "7": ["#####", "....#", "...#.", "..#..", "..#..", "..#..", "..#.."],
    "8": [".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."],
    "9": [".###.", "#...#", "#...#", ".####", "....#", "....#", ".###."],
    " ": [".....", ".....", ".....", ".....", ".....", ".....", "....."],
    ".": [".....", ".....", ".....", ".....", ".....", ".##..", ".##.."],
    ",": [".....", ".....", ".....", ".....", ".##..", ".##..", ".#..."],
    ":": [".....", ".##..", ".##..", ".....", ".##..", ".##..", "....."],
    ";": [".....", ".##..", ".##..", ".....", ".##..", ".##..", ".#..."],
    "-": [".....", ".....", ".....", "#####", ".....", ".....", "....."],
    "+": [".....", "..#..", "..#..", "#####", "..#..", "..#..", "....."],
    "/": ["....#", "....#", "...#.", "..#..", ".#...", "#....", "#...."],
    "'": ["..#..", "..#..", ".#...", ".....", ".....", ".....", "....."],
    "(": ["...#.", "..#..", ".#...", ".#...", ".#...", "..#..", "...#."],
    ")": [".#...", "..#..", "...#.", "...#.", "...#.", "..#..", ".#..."],
    "%": ["##..#", "##.#.", "....#", "...#.", "..#..", ".#...", "#..##"],
    "$": ["..#..", ".####", "#.#..", ".###.", "..#.#", "####.", "..#.."],
    "&": [".##..", "#..#.", "#.#..", ".#...", "#.#.#", "#..#.", ".##.#"],
    "?": [".###.", "#...#", "....#", "...#.", "..#..", ".....", "..#.."],
    "!": ["..#..", "..#..", "..#..", "..#..", "..#..", ".....", "..#.."],
    "*": [".....", "#.#.#", ".###.", "#####", ".###.", "#.#.#", "....."],
    "=": [".....", ".....", "#####", ".....", "#####", ".....", "....."],
    "<": ["...#.", "..#..", ".#...", "#....", ".#...", "..#..", "...#."],
    ">": [".#...", "..#..", "...#.", "....#", "...#.", "..#..", ".#..."],
}


def clean(text):
    out = []
    for ch in text.upper():
        out.append(ch if ch in GLYPHS else " ")
    return "".join(out)


class Canvas:
    def __init__(self):
        self.px = bytearray(W * H * 3)
        self.fill_rect(0, 0, W, H, PAPER)

    def set_px(self, x, y, color):
        if 0 <= x < W and 0 <= y < H:
            i = (y * W + x) * 3
            self.px[i] = color[0]
            self.px[i + 1] = color[1]
            self.px[i + 2] = color[2]

    def fill_rect(self, x, y, w, h, color):
        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(W, x + w)
        y1 = min(H, y + h)
        if x1 <= x0 or y1 <= y0:
            return
        row = bytes(color) * (x1 - x0)
        for yy in range(y0, y1):
            i = (yy * W + x0) * 3
            self.px[i:i + len(row)] = row

    def frame(self, x, y, w, h, color, t=1):
        self.fill_rect(x, y, w, t, color)
        self.fill_rect(x, y + h - t, w, t, color)
        self.fill_rect(x, y, t, h, color)
        self.fill_rect(x + w - t, y, t, h, color)

    def line(self, x0, y0, x1, y1, color, t=1):
        steps = max(abs(x1 - x0), abs(y1 - y0), 1)
        for s in range(steps + 1):
            x = x0 + (x1 - x0) * s // steps
            y = y0 + (y1 - y0) * s // steps
            self.fill_rect(x, y, t, t, color)

    def disc(self, cx, cy, r, color):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                if (xx - cx) * (xx - cx) + (yy - cy) * (yy - cy) <= r * r:
                    self.set_px(xx, yy, color)

    def ring(self, cx, cy, r, color, t=2):
        for yy in range(cy - r - t, cy + r + t + 1):
            for xx in range(cx - r - t, cx + r + t + 1):
                d2 = (xx - cx) * (xx - cx) + (yy - cy) * (yy - cy)
                if (r - t) * (r - t) <= d2 <= (r + t) * (r + t):
                    self.set_px(xx, yy, color)

    def text(self, x, y, s, color=INK, scale=2):
        cx = x
        for ch in clean(s):
            glyph = GLYPHS[ch]
            for gy in range(7):
                row = glyph[gy]
                for gx in range(5):
                    if row[gx] == "#":
                        self.fill_rect(cx + gx * scale, y + gy * scale, scale, scale, color)
            cx += 6 * scale
        return cx

    def text_w(self, s, scale=2):
        return len(clean(s)) * 6 * scale

    def text_c(self, cx, y, s, color=INK, scale=2):
        self.text(cx - self.text_w(s, scale) // 2, y, s, color, scale)

    def wrap(self, x, y, s, max_w, color=INK, scale=2, leading=None, max_lines=4):
        if leading is None:
            leading = 7 * scale + 4
        words = clean(s).split()
        lines = []
        cur = ""
        for word in words:
            trial = (cur + " " + word).strip()
            if self.text_w(trial, scale) <= max_w or not cur:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
        for i, ln in enumerate(lines[:max_lines]):
            self.text(x, y + i * leading, ln, color, scale)
        return y + min(len(lines), max_lines) * leading


def icon_ship(c, x, y, color):
    c.fill_rect(x + 6, y + 26, 44, 8, color)
    c.line(x + 6, y + 26, x + 14, y + 34, color, 2)
    c.line(x + 50, y + 26, x + 42, y + 34, color, 2)
    c.fill_rect(x + 16, y + 14, 10, 12, color)
    c.fill_rect(x + 30, y + 18, 12, 8, color)
    for i in range(3):
        c.line(x + 4 + i * 18, y + 40, x + 16 + i * 18, y + 40, TEAL, 2)


def icon_chart(c, x, y, color):
    c.line(x + 4, y + 4, x + 4, y + 40, color, 2)
    c.line(x + 4, y + 40, x + 52, y + 40, color, 2)
    c.line(x + 8, y + 10, x + 24, y + 22, RED, 3)
    c.line(x + 24, y + 22, x + 34, y + 18, RED, 3)
    c.line(x + 34, y + 18, x + 48, y + 34, RED, 3)
    c.fill_rect(x + 12, y + 30, 6, 8, color)
    c.fill_rect(x + 24, y + 26, 6, 12, color)
    c.fill_rect(x + 36, y + 32, 6, 6, color)


def icon_rocket(c, x, y, color):
    c.line(x + 28, y + 2, x + 20, y + 22, color, 3)
    c.line(x + 28, y + 2, x + 36, y + 22, color, 3)
    c.fill_rect(x + 21, y + 20, 14, 14, color)
    c.disc(x + 28, y + 26, 3, PAPER)
    c.line(x + 21, y + 30, x + 12, y + 40, color, 3)
    c.line(x + 35, y + 30, x + 44, y + 40, color, 3)
    c.line(x + 24, y + 36, x + 28, y + 46, GOLD, 3)
    c.line(x + 32, y + 36, x + 28, y + 46, GOLD, 3)


def draw():
    c = Canvas()
    margin = 22
    inner = W - 2 * margin

    # Masthead
    c.fill_rect(0, 0, W, 118, BAND)
    c.text_c(W // 2, 14, "THE WORLD TODAY", BANDTX, 6)
    c.text_c(W // 2, 64, "WEDNESDAY 25 NOVEMBER 2026", (255, 214, 120), 4)
    c.text_c(W // 2, 94, "ONE DAY OF WORLD NEWS IN ONE IMAGE", BANDTX, 2)

    # Date-check strip
    y = 118
    c.fill_rect(0, y, W, 26, RED)
    c.text_c(W // 2, y + 6, "DATE CHECK: EVERY STORY BELOW HAPPENED OR WAS FIRST REPORTED ON 25 NOV 2026", (255, 255, 255), 2)

    # Heroes
    heroes = [
        ("HORMUZ", "IRAN SAYS 2 TANKERS HIT MINES",
         "Iran's Revolutionary Guards said an LNG carrier and an oil tanker hit naval mines and caught fire.",
         icon_ship, RED),
        ("TRADE WAR", "US PROPOSES TARIFFS ON 14 ECONOMIES",
         "USTR Greer proposed tariffs on 14 partners incl. China at 20%, EU capped at 15%. India: 25%, or 17% with a deal.",
         icon_chart, NAVY),
        ("SPACE FIRST", "PAKISTAN'S FIRST ASTRONAUT ORBITS",
         "Shenzhou-24 left Jiuquan at 00:18 UTC with Muhammad Zeeshan Ali, 40 - first Pakistani in orbit. Docked 03:56 UTC.",
         icon_rocket, TEAL),
    ]
    hy = 156
    hw = (inner - 16) // 3
    hh = 180
    for i, (kicker, head, body, icon, accent) in enumerate(heroes):
        x = margin + i * (hw + 8)
        c.fill_rect(x, hy, hw, hh, CARD)
        c.frame(x, hy, hw, hh, INK, 2)
        c.fill_rect(x, hy, hw, 24, accent)
        c.text(x + 10, hy + 6, kicker, (255, 255, 255), 2)
        icon(c, x + 12, hy + 34, INK)
        yy = c.wrap(x + 76, hy + 34, head, hw - 86, INK, 2, 19, 4)
        c.wrap(x + 10, yy + 6, body, hw - 20, INK, 2, 17, 5)

    # Markets strip
    my = hy + hh + 10
    c.fill_rect(margin, my, inner, 48, (232, 226, 208))
    c.frame(margin, my, inner, 48, INK, 1)
    c.text(margin + 10, my + 5, "MARKETS 25 NOV", RED, 2)
    c.text(margin + 10, my + 24,
           "S+P 500 -2.2%  NIKKEI -2.8%  KOSPI -6.2%  SOFTBANK -15%  BRENT $89.73",
           INK, 2)

    # Grid of short cards: 4 columns x 8 rows = 32 stories
    stories = [
        ("HOUTHIS HIT SAUDI REFINERY", "Houthis claimed an attack on Ras Tanura refinery; Riyadh said drones were downed."),
        ("HUAWEI CONVICTED IN NEW YORK", "A US jury found Huawei guilty of bank fraud and stealing trade secrets; racketeering acquitted."),
        ("TECH SHARES TUMBLE ON AI DOUBTS", "AI spending fears hit shares: Nvidia fell about 6%, Nasdaq slid near 4% early."),
        ("490,334 RUSSIAN WAR DEAD - LEAK", "Leaked statistics analysed by the BBC put Russian military deaths in Ukraine at 490,334+."),
        ("UKRAINE HITS RUSSIAN REFINERIES", "Drones reportedly set Syzran and Kuibyshev refineries ablaze; one killed."),
        ("GAZA STRIKE KILLS HAMAS CHIEF", "An Israeli strike in Gaza City killed Hamas's interior security chief, medics said."),
        ("US WEIGHS STRIKES ON IRAN LEADERS", "Reports say Washington weighs strikes on senior Iranian leaders; Tehran warned of reply."),
        ("NVIDIA ROW OVER HUANG RETURN", "Lawmakers probed Trump's role in reinstating CEO Jensen Huang. Trump: pardon an option."),
        ("POUNDLAND COLLAPSES IN UK", "Poundland entered administration after no buyer was found; 11,000+ jobs at risk."),
        ("UK ENERGY CAP TO RISE 26%", "Ofgem: cap rises 26% on 1 January, typical bill 1,723 to 2,166 pounds."),
        ("OIL DOWN OVER 20% IN NOVEMBER", "Brent fell below $90, down over 20% this month as US crude stocks rose."),
        ("US GROWS 4.3%, INFLATION 3.8%", "US grew 4.3% in Q3, fastest in three years; Fed inflation gauge hit 3.8%."),
        ("COLOMBIA FREES ALL HOSTAGES", "Forces freed about 20 hostages in Cartagena after a 17-hour siege. One gunman killed."),
        ("IOWA BLAST: 5 TONS OF EXPLOSIVE", "The US Army detonated about 5 tons of degraded lead azide at an Iowa plant."),
        ("ABREGO GARCIA LEAVES FOR SPAIN", "Kilmar Abrego Garcia left the US for Spain after his wrongful 2025 deportation fight."),
        ("POLAND PLANS BORDER NO-FLY ZONE", "After a Russian drone entered Polish airspace, Warsaw plans a border no-fly zone."),
        ("MERZ: RUSSIA WANTS MORE", "Chancellor Merz told the Bundestag Russia 'wants more than Ukraine'."),
        ("KNESSET ADVANCES OCT 7 INQUIRY", "Israel's parliament backed a state inquiry into the 7 October attacks, preliminarily."),
        ("SOLOMONS-AUSTRALIA TREATY", "Solomons named Australia primary security partner, barring foreign bases."),
        ("CHINA PROBES SHANGHAI CHIEF", "Politburo member Chen Jining is under investigation, the fourth probed since 2025."),
        ("BANGLADESH WAGES RISE 36%", "Garment minimum wage rose 36% to 17,000 taka amid protests; factories closed."),
        ("ARGENTINA IN RECESSION", "The economy shrank a second quarter; September activity fell 1.2% year on year."),
        ("CUBA LIFE EXPECTANCY FALLS", "WHO: life expectancy fell from 78.8 years in 2020 to 74.4 in 2025."),
        ("UNAIDS WARNS HIV GAINS AT RISK", "Funding cuts may push new HIV infections up in 2027, UNAIDS warned."),
        ("WOLBACHIA CUTS VIRUSES 68%", "In Brazil, Wolbachia mosquitoes cut viral infections 68% among schoolchildren."),
        ("SUDAN DRONES KILL 19 CIVILIANS", "RSF drone strikes in Blue Nile killed at least 19 civilians, wounded 20."),
        ("ENGLAND RECORD HEAT DEATHS", "An estimated 5,200 heat-linked deaths in England this year, twice the record."),
        ("SPAIN HEADS TO SNAP ELECTION", "Spain faces a snap vote; 2,100 migrants reached the Canaries in 24 hours."),
        ("EU UNVEILS 50BN EURO TECH FUND", "The EU announced up to 50 billion euros for AI and quantum computing."),
        ("DANGOTE IPO: AFRICA'S BIGGEST", "Dangote refinery plans a $1.6 billion listing, Africa's most valuable firm."),
        ("SENEGAL RESTORED AS CHAMPIONS", "Sport's top court reinstated Senegal as Africa Cup champions after 11 months."),
        ("DR CONGO EBOLA TOLL TOPS 5,800", "Ebola in eastern DR Congo has killed more than 5,800 since May."),
    ]
    gy = my + 58
    cols = 4
    cw = (inner - (cols - 1) * 8) // cols
    chh = 62
    accents = [RED, NAVY, TEAL, GOLD]
    for idx, (head, body) in enumerate(stories):
        col = idx % cols
        row = idx // cols
        x = margin + col * (cw + 8)
        y = gy + row * (chh + 6)
        c.fill_rect(x, y, cw, chh, CARD)
        c.frame(x, y, cw, chh, RULE, 1)
        c.fill_rect(x, y, 6, chh, accents[idx % 4])
        yy = c.wrap(x + 12, y + 4, head, cw - 20, INK, 2, 16, 2)
        c.wrap(x + 12, yy + 1, body, cw - 20, (52, 50, 48), 1, 10, 3)

    # In-brief ticker
    by = gy + 8 * (chh + 6) + 4
    c.fill_rect(margin, by, inner, 52, BAND)
    c.text(margin + 10, by + 5, "ALSO ON 25 NOVEMBER", (255, 214, 120), 2)
    briefs = [
        "RAMAPHOSA WINS COURT FIGHT IN SOUTH AFRICA",
        "AUSTRALIA INFLATION 4.9%",
        "NORTH KOREA EXPELS SWISS DIPLOMAT",
        "VENEZUELA DEBT $237.5BN REVEALED",
        "COP31 ENDS WITH NO FOSSIL-FUEL DEAL; POPE LEO XIV CONCERNED",
        "BOGOR MINE FLOOD: TOLL 6, ABOUT 20 TRAPPED",
    ]
    line1 = "  *  ".join(briefs[:3])
    line2 = "  *  ".join(briefs[3:])
    c.text(margin + 10, by + 24, line1[:160], BANDTX, 1)
    c.text(margin + 10, by + 38, line2[:160], BANDTX, 1)

    # Footer
    fy = by + 56
    c.text_c(W // 2, fy, "SOURCES: REUTERS, AP, BBC, FRANCE 24, AL JAZEERA, CNBC - AS REPORTED 25 NOV 2026. IRAN AND HOUTHI CLAIMS ARE REPORTED AS CLAIMS.", GREY, 1)
    return c


def png_bytes(canvas):
    raw = bytearray()
    for yy in range(H):
        raw.append(0)
        raw.extend(canvas.px[yy * W * 3:(yy + 1) * W * 3])
    compressed = zlib.compress(bytes(raw), 9)

    def chunk(tag, data):
        body = tag + data
        return struct.pack(">I", len(data)) + body + struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF)

    ihdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)
    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) + chunk(b"IDAT", compressed) + chunk(b"IEND", b"")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    data = png_bytes(draw())
    with open(os.path.join(out_dir, "entry.png"), "wb") as fh:
        fh.write(data)


if __name__ == "__main__":
    main()
