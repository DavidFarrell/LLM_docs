import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import *  # noqa: E402,F401,F403


class S13_Recap(TScene):
    chapter = ("12", "Recap")

    def construct(self):
        self.wait(0.2)
        self.chapter_intro(hold=0.8)
        chips = sentence_layout(SENT, y=-2.9, size=26, width=11.6).shift(LEFT * 0.5)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in chips], lag_ratio=0.04), run_time=0.7)

        # ---- b1: Q, K, V once more
        with self.vo("b1") as b:
            b.wait_until("q", lead=0.2)
            q = VecCells(rvals(4, 17), Q_C, cell=0.2, gap=0.04).next_to(chips[IT], UP, buff=0.35)
            ql = VGroup(txt("query", 30, Q_C, weight="BOLD"), txt("what I'm looking for", 26, INK2)).arrange(RIGHT, buff=0.25)
            ql.move_to([0, 2.7, 0])
            self.sfx("pop", -9)
            self.play(FadeIn(q, shift=UP * 0.2), chips[IT].box.animate.set_stroke(Q_C, 2.6), FadeIn(ql, shift=DOWN * 0.1),
                      run_time=0.6)
            b.wait_until("k", lead=0.2)
            ks = VGroup(*[VecCells(rvals(3, 60 + i), K_C, cell=0.15, gap=0.03).next_to(c, UP, buff=0.25)
                          for i, c in enumerate(chips) if i != IT])
            kl = VGroup(txt("key", 30, K_C, weight="BOLD"), txt("what I contain", 26, INK2)).arrange(RIGHT, buff=0.25)
            kl.next_to(ql, DOWN, buff=0.25)
            self.sfx("pop", -9)
            self.play(LaggedStart(*[FadeIn(k, shift=UP * 0.15) for k in ks], lag_ratio=0.04), FadeIn(kl, shift=DOWN * 0.1),
                      run_time=0.8)
            b.wait_until("v", lead=0.2)
            vs = VGroup(*[VecCells(rvals(3, 90 + i), V_C, cell=0.15, gap=0.03).next_to(k, RIGHT, buff=0.05) for i, k in enumerate(ks)])
            vl = VGroup(txt("value", 30, V_C, weight="BOLD"), txt("what I share", 26, INK2)).arrange(RIGHT, buff=0.25)
            vl.next_to(kl, DOWN, buff=0.25)
            self.sfx("pop", -9)
            self.play(LaggedStart(*[FadeIn(v, shift=UP * 0.15) for v in vs], lag_ratio=0.04), FadeIn(vl, shift=DOWN * 0.1),
                      run_time=0.8)
            b.wait_until("attn", lead=0.2)
            others = [i for i in range(len(SENT)) if i != IT]
            w = np.array([.02, .62, .03, .04, .02, .12, .03, .02, .02, .08])
            arcs = VGroup(*[attn_arc(q, ks[k], wk, Q_C, angle=0.5 * PI, base=1, span=8) for k, wk in enumerate(w)])
            self.sfx("shimmer", -9)
            self.play(LaggedStart(*[Create(a) for a in arcs], lag_ratio=0.04), run_time=0.9)
            flows = VGroup(*[v.copy().set_opacity(0.15 + 0.85 * wk / w.max()) for v, wk in zip(vs, w)])
            qg = glow(q.outline, V_C, layers=5, width=14, opacity=0.35)
            self.play(*[f.animate.move_to(q).set_opacity(0) for f in flows], run_time=0.9)
            self.remove(flows)
            self.play(q.animate.set_values(rvals(4, 23), color=V_C), FadeIn(qg), run_time=0.5)
            grp1 = VGroup(ql, kl, vl, arcs, ks, vs)

        # ---- b2: FFN, residuals, stack
        with self.vo("b2") as b:
            b.wait_until("ffn", lead=0.05)
            self.play(FadeOut(grp1), FadeOut(qg), q.animate.set_opacity(0), run_time=0.4)
            att = Block("attention", ATT_C, width=chips.width, height=0.3, size=16).next_to(chips, UP, buff=0.2)
            ffs = VGroup(*[Block("", FFN_C, width=c.width * 0.9, height=0.26, size=8).next_to(c, UP, buff=0.62) for c in chips])
            f_l = txt("feed-forward: each word processes what it gathered", 24, FFN_C).move_to(UP * 2.7)
            self.play(FadeIn(att), LaggedStart(*[FadeIn(f, shift=UP * 0.1) for f in ffs], lag_ratio=0.04), FadeIn(f_l),
                      run_time=0.8)
            b.wait_until("res", lead=0.2)
            res = VGroup(*[Line(c.get_top() + UP * 0.05, [c.get_center()[0], ffs[0].get_top()[1] + 0.12, 0])
                           .set_stroke(NORM_C, 2, opacity=0.8) for c in chips])
            r_l = txt("residual connections: a running record", 24, NORM_C).next_to(f_l, DOWN, buff=0.2)
            self.play(LaggedStart(*[Create(r) for r in res], lag_ratio=0.03), FadeIn(r_l), run_time=0.7)
            b.wait_until("stack", lead=0.2)
            layer = VGroup(att, ffs, res)
            copies = VGroup(*[layer.copy().set_opacity(0.9 - 0.12 * k) for k in range(5)])
            for k, c in enumerate(copies):
                c.shift(UP * 0.86 * (k + 1))
            self.play(FadeOut(VGroup(f_l, r_l)), run_time=0.3)
            self.sfx("thud", -10)
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.3) for c in copies], lag_ratio=0.2), run_time=1.5)
            x6 = MathTex(r"\times 6", font_size=52, color=INK).next_to(VGroup(layer, copies), RIGHT, buff=0.3)
            self.play(FadeIn(x6), run_time=0.4)
            glowline = VGroup(*[Line(c.get_top(), [c.get_center()[0], copies[-1].get_top()[1] + 0.2, 0])
                                .set_stroke(lerp_color(X_C, V_C, 0.6), 3) for c in chips])
            self.play(*[ShowPassingFlash(g, time_width=0.5) for g in glowline], run_time=1.2)
            grp2 = VGroup(chips, layer, copies, x6, q)

        # ---- b3: close
        with self.vo("b3") as b:
            b.wait_until("end", lead=0.05)
            self.play(FadeOut(grp2, scale=0.95), FadeOut(self.chapter_mob), run_time=0.6)
            title = txt("Attention Is All You Need", 76, INK, weight="SEMIBOLD")
            top_rule = Line(LEFT, RIGHT).set_stroke(INK, 7).set_width(title.width + 0.6).next_to(title, UP, buff=0.45)
            bot_rule = Line(LEFT, RIGHT).set_stroke(INK, 2.5).set_width(title.width + 0.6).next_to(title, DOWN, buff=0.45)
            head = VGroup(top_rule, title, bot_rule).move_to(UP * 0.4)
            self.sfx("impact_soft", -8)
            self.play(FadeIn(title, scale=1.05), GrowFromCenter(top_rule), GrowFromCenter(bot_rule), run_time=0.8)
            # "wasn't quite all you need"
            gap_x = (title[10].get_right()[0] + title[11].get_left()[0]) / 2
            almost = txt("almost", 34, Q_C, weight="SEMIBOLD", slant=ITALIC).next_to(top_rule, UP, buff=0.18)
            almost.set_x(gap_x)
            pointer = Line([gap_x, almost.get_bottom()[1] - 0.04, 0], [gap_x, title.get_top()[1] + 0.02, 0])
            pointer.set_stroke(Q_C, 2.5)
            almost = VGroup(almost, pointer)
            wt = b.t("but") - 1.4 - self.now
            if wt > 0:
                self.wait(wt)
            caret = txt("^", 30, Q_C).next_to(title[11], UP, buff=-0.05).shift(LEFT * 0.2)
            self.play(FadeIn(almost, shift=DOWN * 0.1), run_time=0.5)
            b.wait_until("but", lead=0.1)
            sub = txt("but it was the idea that changed everything", 32, INK2).next_to(head, DOWN, buff=0.6)
            self.play(FadeIn(sub, shift=UP * 0.1), run_time=0.8)
        self.wait(1.2)
        self.sfx("whoosh_soft", -10)
        self.play(FadeOut(VGroup(head, almost, sub)), run_time=0.8)
        credits = VGroup(
            txt("Based on", 22, INK3),
            txt("Vaswani, Shazeer, Parmar, Uszkoreit, Jones, Gomez, Kaiser & Polosukhin", 26, INK),
            txt("“Attention Is All You Need”  ·  NIPS 2017  ·  arXiv:1706.03762", 26, INK2),
            txt("Paper figures reproduced with attribution, as permitted for scholarly use.", 20, INK3),
            txt("Narration: Kokoro-82M, run locally  ·  Animation: Manim  ·  Sound: synthesised", 20, INK3),
        ).arrange(DOWN, buff=0.28)
        credits[2].shift(DOWN * 0.05)
        credits[3].shift(DOWN * 0.3)
        credits[4].shift(DOWN * 0.3)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in credits], lag_ratio=0.15), run_time=1.4)
        self.wait(4.0)
        self.play(FadeOut(credits), run_time=1.0)
        self.wait(0.8)
