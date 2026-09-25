import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import *  # noqa: E402,F401,F403

W5 = ["animal", "street", "it", "tired", "cross"]
SYM = np.array([[1.0, .30, .35, .40, .25],
                [.30, 1.0, .30, .15, .45],
                [.35, .30, 1.0, .20, .20],
                [.40, .15, .20, 1.0, .10],
                [.25, .45, .20, .10, 1.0]])
ASYM = np.array([[.08, .30, .05, .50, .35],
                 [.20, .08, .05, .12, .55],
                 [.95, .35, .05, .25, .10],
                 [.62, .10, .12, .05, .08],
                 [.55, .50, .05, .05, .08]])


class S06_WhyThree(TScene):
    chapter = ("05", "Why three projections?")

    def construct(self):
        self.wait(0.2)
        self.chapter_intro()

        # ---- b1
        with self.vo("b1") as b:
            f1 = MathTex(r"\text{score}(i,j)", r"=", r"\mathbf{x}_i \cdot \mathbf{x}_j", font_size=60)
            f1[2].set_color(X_C)
            qm = txt("?", 80, Q_C, weight="BOLD").next_to(f1, RIGHT, buff=0.3)
            self.play(FadeIn(f1, shift=UP * 0.2), run_time=0.7)
            b.wait_until("direct", lead=0.2)
            self.sfx("pop", -9)
            self.play(FadeIn(qm, scale=0.5), run_time=0.4)

        # ---- b2: two problems
        with self.vo("b2") as b:
            self.play(VGroup(f1, qm).animate.scale(0.7).move_to(UP * 2.75 + LEFT * 2.6), run_time=0.6)
            hm = Heatmap(SYM, cell=0.68, gap=0.06, hi=X_C).move_to(LEFT * 2.6 + DOWN * 0.75)
            rl = VGroup(*[txt(w, 24, INK2).next_to(hm.cell(i, 0), LEFT, buff=0.25) for i, w in enumerate(W5)])
            cl = VGroup(*[txt(w, 22, INK2).rotate(PI / 2.6).next_to(hm.cell(0, j), UP, buff=0.18)
                          for j, w in enumerate(W5)])
            self.play(LaggedStart(*[FadeIn(c, scale=0.7) for c in hm.cells], lag_ratio=0.02),
                      FadeIn(rl), FadeIn(cl), run_time=1.1)
            b.wait_until("self", lead=0.2)
            diag = VGroup(*[outline(hm.cell(i, i), INK, buff=0.03, corner=0.06, width=2.5) for i in range(5)])
            n1 = VGroup(txt("1", 26, Q_C, weight="BOLD", font=MONO),
                        txt("every word matches itself best", 26, INK)).arrange(RIGHT, buff=0.25)
            n1.move_to(RIGHT * 3.3 + UP * 1.3)
            self.sfx("tick", -10)
            self.play(LaggedStart(*[Create(d) for d in diag], lag_ratio=0.12), FadeIn(n1, shift=LEFT * 0.2),
                      run_time=0.9)
            b.wait_until("sym", lead=0.2)
            c1 = outline(hm.cell(2, 0), Q_C, buff=0.03, corner=0.06, width=3)
            c2 = outline(hm.cell(0, 2), Q_C, buff=0.03, corner=0.06, width=3)
            mirror = DashedLine(hm.cell(0, 0).get_corner(UL), hm.cell(4, 4).get_corner(DR), dash_length=0.1)
            mirror.set_stroke(INK3, 2)
            n2 = VGroup(txt("2", 26, Q_C, weight="BOLD", font=MONO),
                        MathTex(r"\text{symmetric: } \mathbf{x}_i\cdot\mathbf{x}_j = \mathbf{x}_j\cdot\mathbf{x}_i",
                                font_size=36, color=INK)).arrange(RIGHT, buff=0.25)
            n2.next_to(n1, DOWN, buff=0.45).align_to(n1, LEFT)
            self.sfx("tick", -10)
            self.play(FadeOut(diag), Create(mirror), Create(c1), Create(c2), FadeIn(n2, shift=LEFT * 0.2),
                      run_time=0.9)
            b.wait_until("asym", lead=0.2)
            it_c = Chip("it", size=26)
            an_c = Chip("animal", size=26)
            pair = VGroup(it_c, an_c).arrange(RIGHT, buff=2.2).move_to(RIGHT * 3.3 + DOWN * 1.1)
            a1 = CurvedArrow(it_c.get_top() + UP * 0.05, an_c.get_top() + UP * 0.05, angle=-PI / 2.5)
            a1.set_stroke(Q_C, 6).set_fill(Q_C)
            a2 = CurvedArrow(an_c.get_bottom() + DOWN * 0.05, it_c.get_bottom() + DOWN * 0.05, angle=-PI / 2.5)
            a2.set_stroke(INK3, 1.6).set_fill(INK3)
            l1 = txt("needs it a lot", 22, Q_C).next_to(a1, UP, buff=0.1)
            l2 = txt("barely", 22, INK3).next_to(a2, DOWN, buff=0.1)
            self.sfx("whoosh_soft", -10)
            self.play(FadeIn(pair), Create(a1), FadeIn(l1), run_time=0.8)
            self.play(Create(a2), FadeIn(l2), run_time=0.6)
            one_way = txt("relevance is one-directional", 26, INK, weight="SEMIBOLD").next_to(pair, DOWN, buff=1.0)
            self.play(FadeIn(one_way, shift=UP * 0.1), run_time=0.5)

        # ---- b3: separate W_Q and W_K fix both
        with self.vo("b3") as b:
            b.wait_until("fix", lead=0.4)
            f2 = MathTex(r"\text{score}(i \to j)", r"=", r"(\mathbf{x}_i W^Q)", r"\cdot", r"(\mathbf{x}_j W^K)",
                         font_size=44)
            f2[2].set_color(Q_C)
            f2[4].set_color(K_C)
            f2.move_to(UP * 2.75 + LEFT * 2.0)
            self.sfx("chime_soft", -9)
            self.play(ReplacementTransform(VGroup(f1, qm), f2), FadeOut(VGroup(mirror, c1, c2)),
                      FadeOut(VGroup(n1, n2)), hm.animate.recolor(ASYM, hi=Q_C), run_time=1.1)
            c3 = outline(hm.cell(2, 0), Q_C, buff=0.03, corner=0.06, width=3)
            c4 = outline(hm.cell(0, 2), INK3, buff=0.03, corner=0.06, width=2)
            lab3 = txt("it → animal", 22, Q_C).next_to(hm, DOWN, buff=0.3).align_to(hm, LEFT)
            lab4 = txt("animal → it", 22, INK3).next_to(lab3, RIGHT, buff=0.6)
            self.play(Create(c3), Create(c4), FadeIn(lab3), FadeIn(lab4), run_time=0.6)
            learned = txt("learned  ·  one-way", 26, Q_C, weight="SEMIBOLD").move_to(RIGHT * 3.3 + UP * 1.3)
            self.play(FadeIn(learned, shift=LEFT * 0.2), run_time=0.5)
            b.wait_until("val", lead=0.3)
            self.play(FadeOut(VGroup(pair, a1, a2, l1, l2, one_way)), run_time=0.4)
            xa = VecCells(rvals(6, 3), X_C, cell=0.22, gap=0.04).move_to(RIGHT * 1.2 + DOWN * 0.8)
            xal = txt("animal", 22, X_C).next_to(xa, DOWN, buff=0.15)
            kk = VecCells(rvals(4, 42), K_C, cell=0.22, gap=0.04).move_to(RIGHT * 3.3 + UP * 0.1)
            vv = VecCells(rvals(4, 72), V_C, cell=0.22, gap=0.04).move_to(RIGHT * 3.3 + DOWN * 1.7)
            ak = Arrow(xa.get_right(), kk.get_left(), buff=0.12, stroke_width=3).set_color(K_C)
            av = Arrow(xa.get_right(), vv.get_left(), buff=0.12, stroke_width=3).set_color(V_C)
            lk = MathTex("W^K", font_size=30, color=K_C).next_to(ak.get_center(), UP, buff=0.12)
            lv = MathTex("W^V", font_size=30, color=V_C).next_to(av.get_center(), DOWN, buff=0.12)
            tk = txt("what it advertises", 22, K_C).next_to(kk, RIGHT, buff=0.25)
            tv = txt("what it hands over", 22, V_C).next_to(vv, RIGHT, buff=0.25)
            self.play(FadeIn(xa), FadeIn(xal), run_time=0.4)
            self.sfx("blip", -10)
            self.play(GrowArrow(ak), GrowArrow(av), FadeIn(lk), FadeIn(lv), FadeIn(kk), FadeIn(vv), run_time=0.8)
            self.play(FadeIn(tk, shift=LEFT * 0.1), FadeIn(tv, shift=LEFT * 0.1), run_time=0.5)
            grp3 = VGroup(f2, hm, rl, cl, c3, c4, lab3, lab4, learned, xa, xal, kk, vv, ak, av, lk, lv, tk, tv)

        # ---- b4: summary
        with self.vo("b4") as b:
            self.play(FadeOut(grp3, shift=UP * 0.2), run_time=0.45)
            rows = VGroup()
            for name, desc, col in (("Query", "what I'm looking for", Q_C), ("Key", "what I can be found by", K_C),
                                    ("Value", "what I give when I'm found", V_C)):
                n = txt(name, 50, col, weight="BOLD")
                d = txt(desc, 38, INK)
                rows.add(VGroup(n, d))
            for r in rows:
                r[0].move_to([-3.0, 0, 0], aligned_edge=RIGHT)
                r[1].move_to([-2.4, 0, 0], aligned_edge=LEFT)
            for i, r in enumerate(rows):
                r.shift(UP * (1.6 - 1.2 * i))
            for key, r in zip(("q", "k", "v"), rows):
                b.wait_until(key, lead=0.15)
                self.sfx("pop", -9)
                self.play(FadeIn(r[0], shift=RIGHT * 0.3), FadeIn(r[1], shift=RIGHT * 0.15), run_time=0.5)
            b.wait_until("names", lead=0.2)
            chain = VGroup(pill("a database lookup", INK2, 26), txt("→", 30, INK3),
                           pill("made soft", Q_C, 26), txt("→", 30, INK3), pill("made learnable", K_C, 26))
            chain.arrange(RIGHT, buff=0.3).move_to(DOWN * 2.3)
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in chain], lag_ratio=0.3), run_time=1.6)
        self.wait(0.5)
        self.sfx("chime_soft", -12)
        self.end_scene()
