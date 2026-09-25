"""Shared design system and timing helpers for every scene."""
import json
import os

import numpy as np
from manim import *  # noqa: F401,F403
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(ROOT, "build")
ASSETS = os.path.join(ROOT, "assets")
PAPER = os.path.join(ASSETS, "paper")

with open(os.path.join(BUILD, "vo", "manifest.json")) as f:
    MANIFEST = json.load(f)

# ---------------------------------------------------------------- palette
BG = "#0B0F1A"
INK = "#EEF1F7"
INK2 = "#A3ADC2"
INK3 = "#5B6682"
PANEL = "#141B2B"
PANEL2 = "#1B2338"
EDGE = "#2C3752"

Q_C = "#FFC857"   # query  - gold
K_C = "#3DD6C6"   # key    - teal
V_C = "#FF6B9A"   # value  - pink
X_C = "#8AA4FF"   # embedding - periwinkle
POS_C = "#C084FC"  # positional encoding - purple
ATT_C = "#FFA657"  # attention block - orange (as in the paper's Figure 1)
FFN_C = "#79C0FF"  # feed-forward block - blue
NORM_C = "#E3F29A"  # add & norm - yellow-green
LIN_C = "#C4B5FD"  # linear - lavender
SMX_C = "#86EFAC"  # softmax - green
GOOD = "#7EE787"
BAD = "#FF7B72"
HEADS = ["#FFC857", "#3DD6C6", "#FF6B9A", "#8AA4FF", "#FFA657", "#86EFAC", "#C084FC", "#79C0FF"]

FONT = "Inter"
MONO = "JetBrains Mono"

SENT = ["The", "animal", "didn't", "cross", "the", "street", "because", "it", "was", "too", "tired."]
IT = 7
ANIMAL = 1
STREET = 5


# ---------------------------------------------------------------- text
def txt(s, size=30, color=INK, weight="MEDIUM", font=FONT, **kw):
    return Text(s, font=font, font_size=size, color=color, weight=weight, **kw)


def mono(s, size=26, color=INK, weight="MEDIUM", **kw):
    return Text(s, font=MONO, font_size=size, color=color, weight=weight, **kw)


def tex(s, size=44, color=INK, **kw):
    return MathTex(s, font_size=size, color=color, **kw)


def base_text(s, size=30, color=INK, weight="MEDIUM", font=FONT):
    """Text whose glyphs keep a consistent baseline: returns (glyphs, ref_H)."""
    full = Text("H" + s, font=font, font_size=size, color=color, weight=weight)
    return VGroup(*full[1:]), full[0]


def cap_height(size, font=FONT, weight="MEDIUM"):
    return Text("H", font=font, font_size=size, weight=weight).height


# ---------------------------------------------------------------- shapes
class Chip(VGroup):
    """A word token: rounded panel with baseline-aligned text."""

    def __init__(self, word, size=30, color=INK, fill=PANEL, stroke=EDGE, padx=0.2,
                 height=None, min_width=0.0, weight="MEDIUM", font=FONT, stroke_width=1.6):
        glyphs, H = base_text(word, size, color, weight, font)
        ch = H.height
        h = height or ch * 2.35
        w = max(glyphs.width + 2 * padx, min_width, h * 0.9)
        box = RoundedRectangle(corner_radius=min(0.13, h / 2.2), width=w, height=h)
        box.set_fill(fill, 1).set_stroke(stroke, stroke_width)
        # place glyphs: baseline at centre - ch/2
        dy = (box.get_center()[1] - ch / 2) - H.get_bottom()[1]
        glyphs.shift(UP * dy)
        glyphs.set_x(box.get_center()[0])
        super().__init__(box, glyphs)
        self.box, self.label, self.word = box, glyphs, word

    def lit(self, color, fill_op=0.22):
        """Return an animation-ready copy target that is highlighted."""
        self.box.set_fill(interpolate_color(ManimColor(PANEL), ManimColor(color), fill_op), 1)
        self.box.set_stroke(color, 2.4)
        return self


def chip_row(words, size=30, gap=0.14, **kw):
    chips = VGroup(*[Chip(w, size=size, **kw) for w in words])
    chips.arrange(RIGHT, buff=gap)
    return chips


def outline(mob, color, buff=0.1, corner=0.1, width=2.4):
    return stroke_around(mob, buff=buff, corner=corner).set_stroke(color, width)


def lerp_color(a, b, t):
    return interpolate_color(ManimColor(a), ManimColor(b), float(np.clip(t, 0, 1)))


class StrokeRect(RoundedRectangle):
    """Rounded rectangle that never takes a fill (safe under group-wide set_opacity)."""

    def set_fill(self, color=None, opacity=None, family=True):
        return super().set_fill(color, 0.0, family)


def stroke_around(mob, buff=0.1, corner=0.1):
    r = StrokeRect(corner_radius=corner, width=mob.width + 2 * buff, height=mob.height + 2 * buff)
    return r.move_to(mob)


class VecCells(VGroup):
    """A vector drawn as a strip of cells; brightness encodes value in [-1, 1]."""

    def __init__(self, values, color, cell=0.2, gap=0.035, direction=DOWN, corner=0.035,
                 outline=True, lo=None):
        super().__init__()
        self.vcolor = color
        self.lo_color = lo or PANEL2
        cells = VGroup()
        for v in values:
            sq = RoundedRectangle(corner_radius=corner, width=cell, height=cell)
            sq.set_stroke(width=0)
            sq.set_fill(self.shade(v), 1)
            cells.add(sq)
        cells.arrange(direction, buff=gap)
        self.add(cells)
        self.cells = cells
        self.values = list(values)
        if outline:
            ol = stroke_around(cells, buff=0.05, corner=0.06)
            ol.set_stroke(color, 1.4, opacity=0.8)
            self.add(ol)
            self.outline = ol
        else:
            self.outline = None

    def shade(self, v):
        return lerp_color(self.lo_color, self.vcolor, 0.18 + 0.82 * (float(v) + 1) / 2)

    def set_opacity(self, opacity, family=True):
        for c in self.cells:
            c.set_fill(opacity=opacity)
        if self.outline is not None:
            self.outline.set_stroke(opacity=0.8 * opacity).set_fill(opacity=0)
        return self

    def set_values(self, values, color=None):
        if color is not None:
            self.vcolor = color
            if self.outline is not None:
                self.outline.set_stroke(color)
        for sq, v in zip(self.cells, values):
            sq.set_fill(self.shade(v), 1)
        self.values = list(values)
        return self


def rvals(n, seed, lo=-1, hi=1):
    return np.random.default_rng(seed).uniform(lo, hi, n)


def glow(mob, color=None, layers=7, width=16, opacity=0.28):
    """Soft halo made of widening transparent strokes (placed behind mob)."""
    col = color or mob.get_stroke_color()
    g = VGroup()
    for i in range(layers, 0, -1):
        c = mob.copy()
        c.set_fill(opacity=0)
        c.set_stroke(col, width=width * i / layers, opacity=opacity * (1 - (i - 1) / layers) ** 1.6)
        g.add(c)
    return g


def attn_arc(a, b, w, color=Q_C, angle=0.55 * PI, base=1.2, span=9.0, min_op=0.12, above=True):
    """Arc between the tops (or bottoms) of two mobjects; weight sets thickness/opacity."""
    if above:
        p1, p2 = a.get_top() + UP * 0.06, b.get_top() + UP * 0.06
        ang = -angle if p2[0] > p1[0] else angle
    else:
        p1, p2 = a.get_bottom() + DOWN * 0.06, b.get_bottom() + DOWN * 0.06
        ang = angle if p2[0] > p1[0] else -angle
    arc = ArcBetweenPoints(p1, p2, angle=ang)
    arc.set_stroke(color, width=base + span * w, opacity=min_op + (1 - min_op) * min(1, w * 1.6))
    return arc


class Block(VGroup):
    """Architecture block (rounded rectangle + label)."""

    def __init__(self, label, color, width=3.4, height=0.78, size=26, fill_op=0.16,
                 label_color=INK, weight="SEMIBOLD", corner=0.14, stroke_width=2.2):
        r = RoundedRectangle(corner_radius=corner, width=width, height=height)
        r.set_fill(color, fill_op).set_stroke(color, stroke_width)
        lines = label.split("\n")
        t = VGroup(*[txt(l, size, label_color, weight=weight) for l in lines]).arrange(DOWN, buff=0.08)
        if t.width > width - 0.25:
            t.scale_to_fit_width(width - 0.25)
        t.move_to(r)
        super().__init__(r, t)
        self.rect, self.label, self.bcolor = r, t, color


def pill(label, color, size=22, weight="SEMIBOLD", padx=0.18, pady=0.09, fill_op=0.16):
    t = txt(label, size, color, weight=weight)
    r = RoundedRectangle(corner_radius=(t.height + 2 * pady) / 2, width=t.width + 2 * padx,
                         height=t.height + 2 * pady)
    r.set_fill(color, fill_op).set_stroke(color, 1.4)
    t.move_to(r)
    return VGroup(r, t)


def heat_color(v, lo=PANEL2, hi=Q_C, top="#FFF4D6"):
    v = float(np.clip(v, 0, 1))
    if v < 0.75:
        return lerp_color(lo, hi, v / 0.75)
    return lerp_color(hi, top, (v - 0.75) / 0.25)


class Heatmap(VGroup):
    def __init__(self, M, cell=0.42, gap=0.05, lo=PANEL2, hi=Q_C, corner=0.05):
        M = np.asarray(M, float)
        cells = VGroup()
        for i in range(M.shape[0]):
            for j in range(M.shape[1]):
                sq = RoundedRectangle(corner_radius=corner, width=cell, height=cell)
                sq.set_stroke(width=0).set_fill(heat_color(M[i, j], lo, hi), 1)
                cells.add(sq)
        cells.arrange_in_grid(M.shape[0], M.shape[1], buff=gap)
        super().__init__(cells)
        self.M = M
        self.lo, self.hi = lo, hi
        self.cells = cells
        self.n, self.m = M.shape

    def cell(self, i, j):
        return self.cells[i * self.m + j]

    def row(self, i):
        return VGroup(*[self.cell(i, j) for j in range(self.m)])

    def col(self, j):
        return VGroup(*[self.cell(i, j) for i in range(self.n)])

    def recolor(self, M, lo=None, hi=None):
        M = np.asarray(M, float)
        lo, hi = lo or self.lo, hi or self.hi
        for i in range(M.shape[0]):
            for j in range(M.shape[1]):
                self.cell(i, j).set_fill(heat_color(M[i, j], lo, hi), 1)
        self.M = M
        return self


def softmax(x, axis=-1):
    x = np.asarray(x, float)
    e = np.exp(x - np.max(x, axis=axis, keepdims=True))
    return e / e.sum(axis=axis, keepdims=True)


def scaled_image(path, height_units, oversample=1.0):
    """Pre-scale a raster with Lanczos so Manim's (non-antialiased) transform stays crisp."""
    px = int(round(height_units / config.frame_height * config.pixel_height * oversample))
    base = os.path.splitext(os.path.basename(path))[0]
    out = os.path.join(BUILD, "scaled", f"{base}_{px}.png")
    if not os.path.exists(out):
        os.makedirs(os.path.dirname(out), exist_ok=True)
        im = Image.open(path).convert("RGBA")
        w = int(round(im.width * px / im.height))
        im.resize((w, px), Image.LANCZOS).save(out)
    return out


def paper_card(path, height=5.6, pad=0.18, corner=0.12, oversample=1.0):
    """A paper figure on a light card with a soft shadow."""
    img = ImageMobject(scaled_image(path, height, oversample))
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bicubic"])
    img.height = height
    card = RoundedRectangle(corner_radius=corner, width=img.width + 2 * pad, height=img.height + 2 * pad)
    card.set_fill("#FBFAF7", 1).set_stroke(width=0)
    shadow = card.copy().set_fill(BLACK, 0.45).shift(DOWN * 0.08 + RIGHT * 0.05)
    shadow.set_stroke(BLACK, 12, opacity=0.18)
    img.move_to(card)
    return Group(shadow, card, img)


def make_bg(w, h):
    path = os.path.join(BUILD, f"bg_{w}x{h}.png")
    if os.path.exists(path):
        return path
    y, x = np.mgrid[0:h, 0:w].astype(np.float32)
    cx, cy = w * 0.5, h * 0.42
    r = np.sqrt(((x - cx) / w) ** 2 + ((y - cy) / h) ** 2 * 0.8)
    base = np.array([9, 12, 21], np.float32)
    centre = np.array([22, 29, 47], np.float32)
    t = np.clip(r / 0.72, 0, 1) ** 1.35
    img = centre * (1 - t)[..., None] + base * t[..., None]
    img += np.random.default_rng(0).normal(0, 0.9, img.shape)
    img = np.clip(img, 0, 255).astype(np.uint8)
    Image.fromarray(img, "RGB").convert("RGBA").save(path)
    return path


# ---------------------------------------------------------------- timing
class Beat:
    """Context manager tying a narration clip to the scene timeline."""

    def __init__(self, scene, key, gap):
        self.s, self.key, self.gap = scene, key, gap
        d = scene.vo_data[key]
        self.dur, self.marks, self.words, self.file = d["dur"], d["marks"], d["words"], d["file"]

    def __enter__(self):
        self.t0 = self.s.now
        self.s.events.append({"type": "vo", "key": self.key, "file": self.file, "t": self.t0,
                              "dur": self.dur})
        return self

    def t(self, mark):
        return self.t0 + self.marks[mark]

    def word_t(self, i):
        return self.t0 + self.words[i][1]

    def left(self, mark=None, lead=0.0):
        target = self.t0 + self.dur if mark is None else self.t(mark)
        return target - lead - self.s.now

    def wait_until(self, mark=None, lead=0.0):
        r = self.left(mark, lead)
        if r > 1.0 / 60:
            self.s.wait(r)
        elif r < -0.12:
            print(f"[timing] {self.s.__class__.__name__}/{self.key}: overran '{mark}' by {-r:.2f}s")

    def rt(self, mark=None, lead=0.0, lo=0.25, hi=None):
        """Run time that ends exactly at `mark` (clamped)."""
        r = self.left(mark, lead)
        r = max(lo, r)
        return min(r, hi) if hi else r

    def schedule(self, items):
        """Play several animations in one call, each starting at its own mark.

        items: (mark_or_offset, animation, run_time[, sfx_name, gain]).
        A string is a bookmark; a float is seconds from now."""
        start = self.s.now
        anims, end = [], start
        for it in items:
            m, anim, rt = it[:3]
            t = self.t(m) if isinstance(m, str) else start + m
            d = max(0.0, t - start)
            anim.run_time = rt
            anims.append(Succession(Wait(run_time=d), anim) if d > 1.0 / 120 else anim)
            if len(it) > 3 and it[3]:
                self.s.sfx(it[3], it[4] if len(it) > 4 else 0.0, dt=d)
            end = max(end, start + d + rt)
        self.s.play(AnimationGroup(*anims), run_time=end - start)

    def __exit__(self, *exc):
        if exc[0] is None:
            self.wait_until(None)
            if self.gap > 0:
                self.s.wait(self.gap)


class TScene(MovingCameraScene):
    chapter = None  # (number, title)

    def setup(self):
        super().setup()
        self.camera.background_image = make_bg(config.pixel_width, config.pixel_height)
        self.camera.init_background()
        self.events = []
        self.vo_data = MANIFEST[self.__class__.__name__]
        self.chapter_mob = None

    @property
    def now(self):
        return self.renderer.time

    def sfx(self, name, gain=0.0, dt=0.0):
        self.events.append({"type": "sfx", "name": name, "t": self.now + dt, "gain": gain})

    def vo(self, key, gap=0.35):
        return Beat(self, key, gap)

    def chapter_intro(self, hold=1.1):
        """Centre title card that settles into the top-left corner."""
        num, title = self.chapter
        n = txt(num, 30, Q_C, weight="SEMIBOLD", font=MONO)
        t = txt(title, 54, INK, weight="SEMIBOLD")
        bar = Line(LEFT, RIGHT).set_stroke(Q_C, 3)
        bar.set_width(t.width * 0.25)
        grp = VGroup(n, t, bar).arrange(DOWN, buff=0.28)
        self.sfx("whoosh_soft", -6)
        self.play(FadeIn(n, shift=UP * 0.2), FadeIn(t, shift=UP * 0.25), GrowFromCenter(bar),
                  run_time=0.7, rate_func=smooth)
        self.wait(hold)
        small_n = txt(num, 18, Q_C, weight="SEMIBOLD", font=MONO)
        small_t = txt(title, 20, INK2, weight="SEMIBOLD")
        small = VGroup(small_n, small_t).arrange(RIGHT, buff=0.2)
        small.to_corner(UL, buff=0.42)
        self.sfx("swish", -10)
        self.play(ReplacementTransform(n, small_n), ReplacementTransform(t, small_t),
                  FadeOut(bar, shift=UP * 0.3), run_time=0.7, rate_func=smooth)
        self.chapter_mob = small

    def clear_all(self, run_time=0.6, keep=()):
        mobs = [m for m in self.mobjects if m not in keep and m is not self.chapter_mob]
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=run_time)

    def end_scene(self, run_time=0.7, tail=0.35):
        mobs = list(self.mobjects)
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=run_time)
        self.wait(tail)

    def tear_down(self):
        super().tear_down()
        os.makedirs(os.path.join(BUILD, "events"), exist_ok=True)
        with open(os.path.join(BUILD, "events", f"{self.__class__.__name__}.json"), "w") as f:
            json.dump({"scene": self.__class__.__name__, "duration": self.now,
                       "fps": config.frame_rate, "events": self.events}, f, indent=1)


def bubble(text, color, size=24, width=None, pointer="down", slant=ITALIC):
    """Speech-bubble label with a small pointer triangle."""
    t = Text(text, font=FONT, font_size=size, color=color, weight="MEDIUM", slant=slant)
    if width and t.width > width:
        t.scale_to_fit_width(width)
    r = RoundedRectangle(corner_radius=0.14, width=t.width + 0.4, height=t.height + 0.3)
    r.set_fill(PANEL2, 0.96).set_stroke(color, 1.8)
    t.move_to(r)
    tri = Triangle().set_fill(PANEL2, 0.96).set_stroke(color, 1.8).scale(0.09)
    if pointer == "down":
        tri.rotate(PI).next_to(r, DOWN, buff=-0.035)
    else:
        tri.next_to(r, UP, buff=-0.035)
    cover = Line(tri.get_corner(UL if pointer == "down" else DL) + RIGHT * 0.02,
                 tri.get_corner(UR if pointer == "down" else DR) + LEFT * 0.02).set_stroke(PANEL2, 3)
    return VGroup(r, tri, cover, t)


def sentence_layout(words, y=-3.05, size=26, min_width=1.02, width=12.8):
    chips = VGroup(*[Chip(w, size=size, min_width=min_width) for w in words]).arrange(RIGHT, buff=0.1)
    if chips.width > width:
        chips.scale_to_fit_width(width)
    chips.move_to([0, y, 0])
    return chips
