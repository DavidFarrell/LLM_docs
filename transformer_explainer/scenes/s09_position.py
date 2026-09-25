import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import *  # noqa: E402,F401,F403

FREQS = [1.0, 0.55, 0.3, 0.16, 0.085]


def pe_image():
    path = os.path.join(BUILD, "pe_heatmap2.png")
    if os.path.exists(path):
        return path
    npos, d = 100, 128
    pos = np.arange(npos)[:, None]
    i = np.arange(d // 2)[None, :]
    ang = pos / (10000 ** (2 * i / d))
    pe = np.concatenate([np.sin(ang), np.cos(ang)], axis=1)  # sin dims, then cos dims
    lo = np.array([124, 58, 237]) * 0.95
    mid = np.array([20, 25, 42])
    hi = np.array([255, 200, 87])
    t = pe[..., None]
    rgb = np.where(t >= 0, mid + (hi - mid) * t, mid + (lo - mid) * (-t))
    img = Image.fromarray(np.clip(rgb.transpose(1, 0, 2), 0, 255).astype(np.uint8), "RGB")
    img.save(path)
    return path


class S09_Position(TScene):
    chapter = ("08", "Word order")

    def construct(self):
        self.wait(0.2)
        self.chapter_intro()

        # ---- b1: attention ignores order
        with self.vo("b1") as b:
            b.wait_until("order", lead=0.3)
            words = ["dog", "bites", "man"]
            chips = VGroup(*[Chip(w, size=36, min_width=1.6) for w in words]).arrange(RIGHT, buff=0.9)
            chips.move_to(DOWN * 0.8)
            outs = VGroup(*[VecCells(rvals(5, 300 + i), [V_C, INK2, K_C][i], cell=0.22, gap=0.04)
                            .next_to(c, UP, buff=0.4) for i, c in enumerate(chips)])
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in chips], lag_ratio=0.15), run_time=0.7)
            self.play(LaggedStart(*[FadeIn(o, shift=UP * 0.2) for o in outs], lag_ratio=0.15), run_time=0.7)
            olab = txt("attention outputs", 22, INK3).next_to(outs, UP, buff=0.3)
            self.play(FadeIn(olab), run_time=0.3)
            b.wait_until("shuf", lead=0.2)
            g0, g2 = VGroup(chips[0], outs[0]), VGroup(chips[2], outs[2])
            p0, p2 = g0.get_center(), g2.get_center()
            self.sfx("swish", -9)
            self.play(g0.animate.move_to(p2), g2.animate.move_to(p0), path_arc=PI / 2, run_time=1.0)
            same = txt("same vectors, just in new slots", 26, INK2).next_to(chips, DOWN, buff=0.5)
            self.play(FadeIn(same, shift=UP * 0.1), run_time=0.5)
            b.wait_until("dog", lead=0.3)
            left = VGroup(*[Chip(w, size=28) for w in ["dog", "bites", "man"]]).arrange(RIGHT, buff=0.15)
            right = VGroup(*[Chip(w, size=28) for w in ["man", "bites", "dog"]]).arrange(RIGHT, buff=0.15)
            eqv = MathTex(r"\equiv", font_size=64, color=Q_C)
            row = VGroup(left, eqv, right).arrange(RIGHT, buff=0.6).move_to(DOWN * 0.3)
            note = txt("…to attention alone, without position information", 24, INK3).next_to(row, DOWN, buff=0.5)
            self.play(FadeOut(VGroup(chips, outs, olab, same)), run_time=0.4)
            self.sfx("pop", -9)
            self.play(FadeIn(left, shift=RIGHT * 0.2), FadeIn(right, shift=LEFT * 0.2), FadeIn(eqv, scale=0.6),
                      run_time=0.6)
            self.play(FadeIn(note), run_time=0.4)
            grp1 = VGroup(left, right, eqv, note)

        # ---- b2: positional encodings
        with self.vo("b2") as b:
            self.play(FadeOut(VGroup(right, eqv, note)), left.animate.scale(1.25).move_to(DOWN * 0.2), run_time=0.5)
            badges = VGroup(*[VGroup(Circle(radius=0.24).set_fill(POS_C, 0.25).set_stroke(POS_C, 2),
                                     txt(str(k), 22, POS_C, weight="BOLD")) for k in range(3)])
            for k, bd in enumerate(badges):
                bd[1].move_to(bd[0])
                bd.next_to(left[k], UP, buff=0.3)
            self.sfx("pop", -10)
            self.play(LaggedStart(*[FadeIn(bd, scale=0.5) for bd in badges], lag_ratio=0.2), run_time=0.8)
            b.wait_until("add", lead=0.45)
            self.play(FadeOut(VGroup(left, badges), shift=UP * 0.2), run_time=0.4)
            words = ["dog", "bites", "man"]
            cols = VGroup()
            for i, w in enumerate(words):
                c = Chip(w, size=28, min_width=1.3)
                e = VecCells(rvals(5, 400 + i), X_C, cell=0.22, gap=0.04)
                p = VecCells([np.sin(i * f) if k % 2 == 0 else np.cos(i * f) for k, f in enumerate(FREQS)],
                             POS_C, cell=0.22, gap=0.04)
                s_ = VecCells(np.clip((rvals(5, 400 + i) + np.array(p.values)) / 1.6, -1, 1), INK, cell=0.22,
                              gap=0.04)
                plus = MathTex("+", font_size=40, color=INK2)
                eq = MathTex("=", font_size=40, color=INK2)
                grp = VGroup(e, plus, p, eq, s_).arrange(RIGHT, buff=0.18)
                c.next_to(grp, DOWN, buff=0.35)
                cols.add(VGroup(grp, c))
            cols.arrange(RIGHT, buff=0.9).move_to(DOWN * 0.3)
            def key(col, label):
                sq = RoundedRectangle(corner_radius=0.04, width=0.22, height=0.22).set_fill(col, 1).set_stroke(width=0)
                return VGroup(sq, txt(label, 24, col)).arrange(RIGHT, buff=0.15)
            hdr = VGroup(key(X_C, "word embedding"), MathTex("+", font_size=36, color=INK2),
                         key(POS_C, "positional encoding"), MathTex("=", font_size=36, color=INK2),
                         key(INK, "input to layer 1")).arrange(RIGHT, buff=0.3)
            hdr.next_to(cols, UP, buff=0.7)
            b.wait_until("add", lead=0.3)
            self.play(LaggedStart(*[FadeIn(c[1]) for c in cols], lag_ratio=0.1),
                      LaggedStart(*[FadeIn(c[0][0]) for c in cols], lag_ratio=0.1), FadeIn(hdr[0]), run_time=0.7)
            self.sfx("pop_soft", -10)
            self.play(LaggedStart(*[AnimationGroup(FadeIn(c[0][1]), FadeIn(c[0][2], shift=DOWN * 0.2)) for c in cols],
                                  lag_ratio=0.12), FadeIn(hdr[1:3]), run_time=0.8)
            self.play(LaggedStart(*[AnimationGroup(FadeIn(c[0][3]), FadeIn(c[0][4], shift=LEFT * 0.2)) for c in cols],
                                  lag_ratio=0.12), FadeIn(hdr[3:]), run_time=0.8)
            b.wait_until("waves", lead=0.3)
            self.play(FadeOut(VGroup(cols, hdr), shift=UP * 0.2), run_time=0.45)
            # stacked sinusoids
            x0, x1 = -6.2, 1.6
            npos = 20.0
            strip_h = 0.95
            waves = VGroup()
            labels = VGroup()
            base_ys = [2.0 - i * 1.05 for i in range(len(FREQS))]
            for i, (f, y0) in enumerate(zip(FREQS, base_ys)):
                fn = (lambda f_, i_: (lambda p: np.sin(f_ * p) if i_ % 2 == 0 else np.cos(f_ * p)))(f, i)
                curve = ParametricFunction(lambda t, fn=fn, y0=y0: np.array(
                    [x0 + (x1 - x0) * t / npos, y0 + 0.36 * fn(t), 0]), t_range=[0, npos, 0.05])
                curve.set_stroke(lerp_color(POS_C, INK, i / 6), 3)
                base = Line([x0, y0, 0], [x1, y0, 0]).set_stroke(INK3, 1, opacity=0.5)
                waves.add(VGroup(base, curve))
                labels.add(MathTex(f"i={i}", font_size=26, color=INK3).next_to(base, LEFT, buff=0.15))
            poslab = txt("position  →", 22, INK3).next_to(waves, DOWN, buff=0.3)
            self.sfx("whoosh_soft", -10)
            self.play(LaggedStart(*[Create(w) for w in waves], lag_ratio=0.1), FadeIn(labels), FadeIn(poslab),
                      run_time=1.2)
            P = ValueTracker(2.0)

            def xpos(p):
                return x0 + (x1 - x0) * p / npos

            def vals(p):
                return [np.sin(f * p) if k % 2 == 0 else np.cos(f * p) for k, f in enumerate(FREQS)]

            scan = always_redraw(lambda: DashedLine([xpos(P.get_value()), 2.6, 0],
                                                    [xpos(P.get_value()), base_ys[-1] - 0.5, 0], dash_length=0.08)
                                 .set_stroke(Q_C, 2))
            dots = always_redraw(lambda: VGroup(*[Dot([xpos(P.get_value()), y0 + 0.36 * v, 0], radius=0.07,
                                                      color=Q_C) for y0, v in zip(base_ys, vals(P.get_value()))]))
            vec = always_redraw(lambda: VecCells(vals(P.get_value()), POS_C, cell=0.34, gap=0.07)
                                .move_to([2.9, 0.0, 0]))
            vlab = always_redraw(lambda: MathTex(r"PE(" + f"{P.get_value():.0f}" + r")", font_size=34, color=POS_C)
                                 .next_to(vec, UP, buff=0.25))
            # clock
            clock_c = np.array([5.3, 0.0, 0])
            face = Circle(radius=1.05).move_to(clock_c).set_stroke(INK3, 2).set_fill(PANEL, 0.8)
            ticks = VGroup(*[Line(clock_c + 0.92 * np.array([np.cos(a), np.sin(a), 0]),
                                  clock_c + 1.02 * np.array([np.cos(a), np.sin(a), 0])).set_stroke(INK3, 2)
                             for a in np.linspace(0, TAU, 12, endpoint=False)])
            hands = always_redraw(lambda: VGroup(*[
                Line(clock_c, clock_c + L * np.array([np.sin(f * P.get_value()), np.cos(f * P.get_value()), 0]))
                .set_stroke(c, w) for f, L, c, w in ((FREQS[0], 0.9, Q_C, 2.5), (FREQS[2], 0.7, POS_C, 4),
                                                     (FREQS[4], 0.5, INK, 6))]))
            self.add(scan, dots)
            self.play(FadeIn(vec), FadeIn(vlab), FadeIn(face), FadeIn(ticks), FadeIn(hands), run_time=0.6)
            b.wait_until("fast", lead=0.3)
            self.play(P.animate.set_value(6.0), waves[0].animate.set_stroke(width=5), waves[1].animate.set_stroke(width=5),
                      run_time=1.4)
            b.wait_until("slow", lead=0.3)
            self.play(P.animate.set_value(11.0), waves[0].animate.set_stroke(width=3), waves[1].animate.set_stroke(width=3),
                      waves[3].animate.set_stroke(width=5), waves[4].animate.set_stroke(width=5), run_time=1.6)
            b.wait_until("sig", lead=0.3)
            self.play(P.animate.set_value(17.0), run_time=1.2)
            self.remove(scan, dots, vec, vlab, hands)
            hm = ImageMobject(pe_image())
            hm.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
            hm.height = 4.6
            hm.stretch_to_fit_width(9.5)
            hm.move_to(DOWN * 0.2)
            frame = SurroundingRectangle(hm, buff=0.04, corner_radius=0.04).set_stroke(INK3, 1.5).set_fill(opacity=0)
            xlab = txt("position  →", 22, INK3).next_to(hm, DOWN, buff=0.2)
            ylab = VGroup(txt("sin dims", 20, INK3), txt("cos dims", 20, INK3))
            ylab[0].next_to(hm, LEFT, buff=0.2).shift(UP * hm.height / 4)
            ylab[1].next_to(hm, LEFT, buff=0.2).shift(DOWN * hm.height / 4)
            divider = DashedLine(hm.get_left(), hm.get_right(), dash_length=0.1).set_stroke(INK, 1, opacity=0.5)
            uniq = txt("every position gets a unique signature", 28, INK, weight="SEMIBOLD").next_to(hm, UP, buff=0.3)
            self.sfx("shimmer", -10)
            self.play(FadeOut(VGroup(waves, labels, poslab, face, ticks)), FadeIn(hm), Create(frame),
                      FadeIn(xlab), FadeIn(ylab), FadeIn(divider), run_time=0.8)
            self.play(FadeIn(uniq, shift=UP * 0.1), run_time=0.5)
            grp2 = Group(hm, frame, xlab, ylab, uniq, divider)
            b.wait_until(None, lead=0.3)
            self.play(FadeOut(grp2), run_time=0.3)

        # ---- b3: shifting is linear (a rotation)
        with self.vo("b3") as b:
            c0 = np.array([-3.6, -0.3, 0])
            R = 1.8
            circle = Circle(radius=R).move_to(c0).set_stroke(INK3, 2)
            axes_ = VGroup(Line(c0 + LEFT * 2.2, c0 + RIGHT * 2.2), Line(c0 + DOWN * 2.2, c0 + UP * 2.2)).set_stroke(INK3, 1)
            a0, dk = 0.5, 1.1
            p1 = Dot(c0 + R * np.array([np.cos(a0), np.sin(a0), 0]), radius=0.11, color=POS_C)
            p2 = Dot(c0 + R * np.array([np.cos(a0 + dk), np.sin(a0 + dk), 0]), radius=0.11, color=Q_C)
            l1 = MathTex(r"PE(pos)", font_size=30, color=POS_C).next_to(p1, RIGHT, buff=0.15)
            l2 = MathTex(r"PE(pos{+}k)", font_size=30, color=Q_C).next_to(p2, UP + RIGHT * 0.3, buff=0.1)
            arc = Arc(radius=R + 0.35, start_angle=a0, angle=dk, arc_center=c0).set_stroke(Q_C, 3)
            arc.add_tip(tip_length=0.18)
            lab = txt("one sine/cosine pair", 22, INK3).next_to(circle, DOWN, buff=0.35)
            b.wait_until("lin", lead=0.1)
            self.play(Create(axes_), Create(circle), FadeIn(lab), FadeIn(p1), FadeIn(l1), run_time=0.8)
            self.sfx("swish", -10)
            self.play(Create(arc), TransformFromCopy(p1, p2), FadeIn(l2), run_time=0.9)
            mat = MathTex(r"PE_{pos+k} =", r"\begin{bmatrix} \cos k\omega & \sin k\omega \\ -\sin k\omega & \cos k\omega "
                          r"\end{bmatrix}", r"PE_{pos}", font_size=40)
            mat[0].set_color(Q_C)
            mat[2].set_color(POS_C)
            mat.move_to(RIGHT * 2.9 + UP * 0.9)
            rot = txt("a fixed rotation: a linear map", 26, INK2).next_to(mat, DOWN, buff=0.4)
            self.play(Write(mat), run_time=1.2)
            self.play(FadeIn(rot, shift=UP * 0.1), run_time=0.5)
            b.wait_until("rel", lead=0.2)
            relt = VGroup(txt("→ relative positions should be easy to learn", 26, Q_C, weight="SEMIBOLD"),
                          txt("(the authors' hypothesis)", 22, INK3)).arrange(DOWN, buff=0.15)
            relt.next_to(rot, DOWN, buff=0.5)
            self.play(FadeIn(relt, shift=UP * 0.1), run_time=0.6)
        self.wait(0.5)
        self.end_scene()
