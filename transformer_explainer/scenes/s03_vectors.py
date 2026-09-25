import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import *  # noqa: E402,F401,F403


def word_time(b, sub):
    for w, s, e in b.words:
        if sub.lower() in w.lower():
            return b.t0 + s
    raise KeyError(sub)


class S03_Vectors(TScene):
    chapter = ("02", "Words as vectors")

    def construct(self):
        self.wait(0.2)
        self.chapter_intro()

        # ---- b1: a token becomes a vector of 512 numbers
        with self.vo("b1") as b:
            animal = Chip("animal", size=40).move_to(LEFT * 4.2 + UP * 0.2)
            self.sfx("pop_soft", -10)
            self.play(FadeIn(animal, scale=0.9), run_time=0.5)
            # sub-word tokens aside
            tsub = word_time(b, "sub-word")
            wait = tsub - self.now - 0.2
            if wait > 0:
                self.wait(wait)
            whole = Chip("Transformers", size=30).move_to(LEFT * 4.2 + DOWN * 1.9)
            p1 = Chip("Transform", size=30)
            p2 = Chip("ers", size=30)
            parts = VGroup(p1, p2).arrange(RIGHT, buff=0.12).move_to(whole)
            cap = txt("sub-word tokens", 22, INK3).next_to(parts, DOWN, buff=0.25)
            self.play(FadeIn(whole, shift=UP * 0.1), run_time=0.4)
            self.sfx("click", -12)
            self.play(ReplacementTransform(whole, parts), FadeIn(cap), run_time=0.6)
            b.wait_until("vec", lead=0.3)
            vals = [0.21, -1.37, 0.84, 0.05, -0.62, 1.12]
            col = MathTex(r"\begin{bmatrix} 0.21 \\ -1.37 \\ 0.84 \\ 0.05 \\ -0.62 \\ \vdots \\ 1.12 \end{bmatrix}",
                          font_size=40, color=INK)
            col.move_to(RIGHT * 0.2 + UP * 0.2)
            cells = VecCells(np.tanh(np.array(vals + [0.3, -0.2, 0.7, -0.9, 0.1, 0.5])), X_C, cell=0.28, gap=0.05)
            cells.next_to(col, RIGHT, buff=0.6)
            arrow = Arrow(animal.get_right(), col.get_left(), buff=0.25, stroke_width=4).set_color(INK3)
            self.sfx("whoosh_soft", -10)
            self.play(GrowArrow(arrow), FadeIn(col, shift=RIGHT * 0.3), FadeOut(VGroup(parts, cap)), run_time=0.7)
            self.play(LaggedStart(*[FadeIn(c, scale=0.6) for c in cells.cells], lag_ratio=0.06),
                      Create(cells.outline), run_time=0.8)
            b.wait_until("dim", lead=0.2)
            brace = Brace(cells, RIGHT, color=INK3)
            dim = MathTex(r"d_{\text{model}} = 512", font_size=46, color=X_C).next_to(brace, RIGHT, buff=0.2)
            self.sfx("pop", -10)
            self.play(GrowFromCenter(brace), FadeIn(dim, shift=LEFT * 0.2), run_time=0.6)
            vec_group = VGroup(animal, arrow, col, cells, brace, dim)

        # ---- b2: a space of meaning
        with self.vo("b2") as b:
            b.wait_until("space", lead=0.4)
            plane = NumberPlane(x_range=[-7, 7, 1], y_range=[-4, 4, 1],
                                background_line_style={"stroke_color": INK3, "stroke_width": 1, "stroke_opacity": 0.22},
                                axis_config={"stroke_color": INK3, "stroke_opacity": 0.5, "stroke_width": 1.5})
            self.play(FadeOut(vec_group, scale=0.9), FadeIn(plane), run_time=0.7)
            words = {
                "animal": (2.6, 1.9), "cat": (3.3, 1.2), "dog": (2.0, 2.6),
                "street": (-3.2, 1.5), "road": (-3.8, 0.7), "bridge": (-2.4, 2.2),
                "tired": (1.6, -2.4), "sleepy": (2.5, -2.0),
            }
            cols = {"animal": K_C, "cat": K_C, "dog": K_C, "street": Q_C, "road": Q_C, "bridge": Q_C,
                    "tired": V_C, "sleepy": V_C}
            arrows, labels = VGroup(), VGroup()
            for w, (x, y) in words.items():
                a = Arrow(ORIGIN, [x, y, 0], buff=0, stroke_width=4, max_tip_length_to_length_ratio=0.12)
                a.set_color(cols[w])
                lab = txt(w, 24, cols[w], weight="SEMIBOLD")
                lab.next_to(a.get_end(), normalize([x, y, 0]), buff=0.12)
                arrows.add(a)
                labels.add(lab)
            self.sfx("shimmer", -12)
            self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.08),
                      LaggedStart(*[FadeIn(l) for l in labels], lag_ratio=0.08), run_time=1.4)
            b.wait_until("rel", lead=0.2)
            halos = VGroup()
            for grp, c in (((0, 1, 2), K_C), ((3, 4, 5), Q_C), ((6, 7), V_C)):
                pts = [arrows[i].get_end() for i in grp]
                centre = np.mean(pts, axis=0)
                rad = max(np.linalg.norm(p - centre) for p in pts) + 0.75
                halos.add(Circle(radius=rad).move_to(centre).set_fill(c, 0.08).set_stroke(c, 1.5, opacity=0.5))
            note = txt("drawn in 2D  ·  really 512D", 20, INK3).to_corner(DR, buff=0.4)
            self.play(LaggedStart(*[FadeIn(h, scale=0.8) for h in halos], lag_ratio=0.2), FadeIn(note), run_time=1.0)

        # ---- b3: the dot product
        with self.vo("b3") as b:
            b.wait_until("dot", lead=0.4)
            self.play(FadeOut(VGroup(arrows, labels, halos)), plane.animate.shift(LEFT * 2.2), run_time=0.6)
            origin = plane.c2p(0, 0)
            a_vec = np.array([2.0, 0.9, 0])
            theta = ValueTracker(np.arctan2(0.9, 2.0) + 1.9)
            blen = 2.1

            def b_vec():
                t = theta.get_value()
                return np.array([blen * np.cos(t), blen * np.sin(t), 0])

            A = Arrow(origin, origin + a_vec, buff=0, stroke_width=6, max_tip_length_to_length_ratio=0.12).set_color(Q_C)
            B = always_redraw(lambda: Arrow(origin, origin + b_vec(), buff=0, stroke_width=6,
                                            max_tip_length_to_length_ratio=0.12).set_color(K_C))
            la = MathTex(r"\mathbf{a}", font_size=46, color=Q_C).next_to(A.get_end(), RIGHT, buff=0.12)
            lb = always_redraw(lambda: MathTex(r"\mathbf{b}", font_size=46, color=K_C)
                               .move_to(origin + b_vec() * 1.16))
            formula = MathTex(r"\mathbf{a}\cdot\mathbf{b}", r"=", r"\sum_i a_i\, b_i", font_size=52)
            formula[0][0].set_color(Q_C)
            formula[0][2].set_color(K_C)
            formula.move_to(RIGHT * 3.6 + UP * 2.2)
            self.sfx("pop", -10)
            self.play(GrowArrow(A), FadeIn(la), FadeIn(B), FadeIn(lb), Write(formula), run_time=1.0)
            b.wait_until("mult", lead=0.2)
            expand = MathTex(r"= a_1 b_1 + a_2 b_2 + \dots + a_{512} b_{512}", font_size=34, color=INK2)
            expand.next_to(formula, DOWN, buff=0.3)
            if expand.get_right()[0] > 6.7:
                expand.shift(LEFT * (expand.get_right()[0] - 6.7))
            self.play(FadeIn(expand, shift=DOWN * 0.1), run_time=0.6)

            def dotv():
                return float(np.dot(a_vec[:2], b_vec()[:2]))

            def read_color(v):
                if v >= 0:
                    return lerp_color(INK2, GOOD, min(v / 3.5, 1))
                return lerp_color(INK2, BAD, min(-v / 3.5, 1))

            readout = always_redraw(lambda: VGroup(
                MathTex(r"\mathbf{a}\cdot\mathbf{b} =", font_size=48, color=INK2),
                DecimalNumber(dotv(), num_decimal_places=1, include_sign=True, font_size=64,
                              color=read_color(dotv()))).arrange(RIGHT, buff=0.25).move_to(RIGHT * 3.9 + DOWN * 0.4))
            tag = always_redraw(lambda: txt(
                "similar" if dotv() > 2.4 else ("unrelated" if abs(dotv()) < 0.8 else ("opposite" if dotv() < -2.4 else "")),
                30, read_color(dotv()), weight="SEMIBOLD").move_to(RIGHT * 3.9 + DOWN * 1.5))
            self.add(readout, tag)
            b.wait_until("same", lead=0.9)
            self.sfx("tone_up", -12)
            self.play(theta.animate.set_value(np.arctan2(0.9, 2.0) + 0.3), run_time=1.1, rate_func=smooth)
            b.wait_until("perp", lead=0.9)
            self.sfx("tone_down", -12)
            self.play(theta.animate.set_value(np.arctan2(0.9, 2.0) + PI / 2), run_time=1.1, rate_func=smooth)
            b.wait_until("opp", lead=0.9)
            self.sfx("tone_down", -12)
            self.play(theta.animate.set_value(np.arctan2(0.9, 2.0) + PI - 0.08), run_time=1.1, rate_func=smooth)
            b.wait_until("built", lead=0.2)
            box = outline(formula, Q_C, buff=0.2, corner=0.12, width=2)
            self.sfx("chime_soft", -9)
            self.play(Create(box), theta.animate.set_value(np.arctan2(0.9, 2.0) + 0.5), run_time=1.2)
        self.wait(0.4)
        self.end_scene()
