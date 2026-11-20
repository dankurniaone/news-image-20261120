#!/usr/bin/env python3
"""Render the 20 November 2026 front page to entry.png.

Pillow only, no network, no clock, no randomness: the same news.json
plus the same photos always produce the same bytes. The page is drawn
at double size (1360x2048) and shrunk with LANCZOS to 680x1024 so the
type stays crisp. Photos are real Pexels file photos, credited in the
footer; the layout and typography are drawn in code. Run from the
repo root:

    python3 tools/render20.py
"""
import json
import os

from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

# newsprint palette: warm paper, near-black ink, one red, one grey
PAPER = (250, 246, 236)
INK = (20, 20, 18)
GREY = (104, 98, 88)
RED = (178, 34, 34)
HAIRLINE = (200, 192, 176)

FACTOR = 2
PAGE_W, PAGE_H = 680 * FACTOR, 1024 * FACTOR
EDGE = 36 * FACTOR
INNER = PAGE_W - 2 * EDGE


class Type:
    """Font cache: serif for headlines, sans for kickers and captions."""

    def __init__(self):
        self._cache = {}

    def get(self, family, size, bold=False):
        key = (family, size, bold)
        if key not in self._cache:
            if family == "serif":
                name = "DejaVuSerif-Bold.ttf" if bold else "DejaVuSerif.ttf"
            else:
                name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
            self._cache[key] = ImageFont.truetype(
                os.path.join(FONT_DIR, name), size)
        return self._cache[key]


class FrontPage:
    def __init__(self, copy):
        self.copy = copy
        self.type = Type()
        self.canvas = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
        self.pen = ImageDraw.Draw(self.canvas)
        self.cursor = 0

    # -- low-level helpers -------------------------------------------------
    def split_lines(self, text, font, width):
        """Greedy wrap; returns a list of lines that fit `width`."""
        out, current = [], ""
        for word in text.split():
            candidate = word if not current else current + " " + word
            if self.pen.textlength(candidate, font=font) <= width:
                current = candidate
            else:
                if current:
                    out.append(current)
                current = word
        if current:
            out.append(current)
        return out

    def draw_lines(self, x, y, lines, font, fill, leading):
        for line in lines:
            self.pen.text((x, y), line, font=font, fill=fill)
            y += leading
        return y

    def paragraph(self, x, y, text, font, fill, width, leading):
        return self.draw_lines(
            x, y, self.split_lines(text, font, width), font, fill, leading)

    def centred_line(self, y, text, font, fill):
        width = self.pen.textlength(text, font=font)
        self.pen.text(((PAGE_W - width) / 2, y), text, font=font, fill=fill)
        return y + font.size

    def spaced_centre(self, y, text, font, fill, gap):
        """Centre text with extra space between letters (masthead tag)."""
        widths = [self.pen.textlength(ch, font=font) for ch in text]
        total = sum(widths) + gap * (len(text) - 1)
        x = (PAGE_W - total) / 2
        for ch, w in zip(text, widths):
            self.pen.text((x, y), ch, font=font, fill=fill)
            x += w + gap
        return y + font.size

    def hrule(self, y, weight=2, fill=INK):
        self.pen.line([(EDGE, y), (PAGE_W - EDGE, y)], fill=fill, width=weight)
        return y + weight

    def vrule(self, x, y0, y1, weight=2):
        self.pen.line([(x, y0), (x, y1)], fill=HAIRLINE, width=weight)

    def photo(self, name, x, y, w, h):
        """Paste a photo cropped to fill the box exactly."""
        src = Image.open(os.path.join(ROOT, "assets", name)).convert("RGB")
        fitted = ImageOps.fit(src, (w, h), Image.LANCZOS)
        self.canvas.paste(fitted, (x, y))
        return y + h

    def caption(self, x, y, text, width):
        font = self.type.get("sans", 20)
        return self.paragraph(x, y, text, font, GREY, width, 26)

    def kicker(self, x, y, text):
        self.pen.text((x, y), text, font=self.type.get("sans", 26, bold=True),
                      fill=RED)
        return y + 40

    def headline(self, x, y, text, size, width, leading):
        return self.paragraph(x, y, text, self.type.get("serif", size, bold=True),
                              INK, width, leading)

    def deck(self, x, y, text, width):
        return self.paragraph(x, y, text, self.type.get("serif", 31),
                              INK, width, 42)

    # -- sections ----------------------------------------------------------
    def masthead(self):
        n = self.copy
        y = 40
        self.pen.rectangle([EDGE, y, PAGE_W - EDGE, y + 6], fill=RED)
        y += 22
        y = self.centred_line(y, n["masthead"],
                              self.type.get("serif", 108, bold=True), INK)
        y += 6
        y = self.spaced_centre(y, n["masthead_tag"],
                               self.type.get("sans", 30, bold=True), INK, 14)
        y += 10
        y = self.centred_line(y, n["date"].upper(),
                              self.type.get("sans", 28), GREY)
        y += 12
        y = self.hrule(y)
        y += 14
        y = self.centred_line(y, n["strapline"],
                              self.type.get("serif", 26), GREY)
        return y + 12

    def lead(self, y):
        n = self.copy["lead"]
        y = self.kicker(EDGE, y, n["kicker"])
        y = self.headline(EDGE, y, n["headline"], 64, INNER, 76)
        y += 8
        y = self.deck(EDGE, y, n["deck"], INNER)
        y += 14
        y = self.photo("akvan.jpg", EDGE, y, INNER, 372)
        y += 12
        y = self.caption(EDGE, y, n["photo_caption"], INNER)
        y += 12
        return self.hrule(y) + 14

    def two_columns(self, y):
        n = self.copy
        gap = 40
        col_w = (INNER - gap) // 2
        left_x = EDGE
        right_x = EDGE + col_w + gap
        tops = y
        bottoms = []
        for key, x in (("kyiv", left_x), ("italy", right_x)):
            s = n[key]
            yy = tops
            yy = self.kicker(x, yy, s["kicker"])
            yy = self.headline(x, yy, s["headline"], 36, col_w, 44)
            yy += 8
            yy = self.paragraph(x, yy, s["deck"], self.type.get("serif", 26),
                                INK, col_w, 35)
            yy += 14
            yy = self.photo("kyiv.jpg" if key == "kyiv" else "rome.jpg",
                            x, yy, col_w, 226)
            yy += 10
            yy = self.caption(x, yy, s["photo_caption"], col_w)
            bottoms.append(yy)
        self.vrule(EDGE + col_w + gap // 2, tops, max(bottoms))
        return max(bottoms) + 16

    def markets_strip(self, y):
        n = self.copy["markets"]
        x = EDGE + 24
        # measure the text first so the red bar matches its true height
        body = n["headline"] + " — " + n["deck"]
        lines = self.split_lines(body, self.type.get("serif", 26),
                                 INNER - 24)
        box_h = 8 + 32 + len(lines) * 34 + 10
        self.pen.rectangle([EDGE, y, EDGE + 8, y + box_h], fill=RED)
        yy = y + 8
        self.pen.text((x, yy), n["kicker"],
                      font=self.type.get("sans", 22, bold=True), fill=RED)
        yy += 32
        yy = self.draw_lines(x, yy, lines, self.type.get("serif", 26),
                             INK, 34)
        return y + box_h + 16

    def ticker(self, y):
        n = self.copy["ticker"]
        self.pen.rectangle([EDGE, y, PAGE_W - EDGE, y + 56], fill=RED)
        size = 25
        font = self.type.get("sans", size, bold=True)
        width = self.pen.textlength(n, font=font)
        while width > INNER - 40 and size > 14:
            size -= 1
            font = self.type.get("sans", size, bold=True)
            width = self.pen.textlength(n, font=font)
        self.pen.text(((PAGE_W - width) / 2, y + (56 - size) // 2 - 2),
                      n, font=font, fill=(255, 255, 255))
        return y + 56 + 10

    def footer(self, y):
        y = self.paragraph(EDGE, y, self.copy["footer"],
                           self.type.get("sans", 20), GREY, INNER, 26)
        y += 12
        return self.hrule(y)

    def build(self):
        y = self.masthead()
        y = self.lead(y)
        y = self.two_columns(y)
        y = self.markets_strip(y)
        y = self.ticker(y)
        y = self.footer(y)
        assert y <= PAGE_H - 30, f"page overflow: y={y} of {PAGE_H}"
        final = self.canvas.resize((680, 1024), Image.LANCZOS)
        out = os.path.join(ROOT, "entry.png")
        final.save(out, optimize=True)
        print(f"entry.png: {os.path.getsize(out)} bytes")


def main():
    with open(os.path.join(ROOT, "news.json")) as f:
        copy = json.load(f)
    FrontPage(copy).build()


if __name__ == "__main__":
    main()
