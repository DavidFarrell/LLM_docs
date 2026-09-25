import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import *  # noqa: E402,F401,F403

WORDS = ["The", "animal", "didn't", "cross", "the", "street", "because", "it"]


def orb(color, r=0.13):
    core = Circle(radius=r).set_fill(color, 1).set_stroke(width=0)
    halo = VGroup(*[Circle(radius=r * k).set_fill(color, 0.10 / k).set_stroke(width=0)
                    for k in (1.6, 2.2, 3.0)])
    return VGroup(halo, core)


class S02_Recurrence(TScene):
    chapter = ("01", "Why not recurrence?")

    def construct(self):
        self.wait(0.2)
        self.chapter_intro()
        n = len(WORDS)
        xs = [-5.25 + 1.5 * i for i in range(n)]
        cells = VGroup(*[RoundedRectangle(corner_radius=0.14, width=0.86, height=0.86)
                         .set_fill(PANEL, 1).set_stroke(INK3, 2).move_to([x, 0.35, 0]) for x in xs])
        cell_lbl = VGroup(*[mono("RNN", 16, INK3).move_to(c) for c in cells])
        harrows = VGroup(*[Arrow(cells[i].get_right(), cells[i + 1].get_left(), buff=0.06,
                                 stroke_width=3, max_tip_length_to_length_ratio=0.25)
                           .set_color(INK3) for i in range(n - 1)])
        chips = VGroup(*[Chip(w, size=24).move_to([x, -1.55, 0]) for w, x in zip(WORDS, xs)])
        up_arrows = VGroup(*[Arrow(chips[i].get_top(), cells[i].get_bottom(), buff=0.08, stroke_width=2.5,
                                   max_tip_length_to_length_ratio=0.3).set_color(INK3) for i in range(n)])
        title = txt("Recurrent neural network", 30, INK2, weight="SEMIBOLD").move_to(UP * 2.3)

        # ---- b1
        with self.vo("b1") as b:
            b.wait_until("rnn", lead=0.3)
            self.sfx("whoosh_soft", -9)
            self.play(FadeIn(title, shift=DOWN * 0.1),
                      LaggedStart(*[FadeIn(VGroup(c, l), scale=0.8) for c, l in zip(cells, cell_lbl)],
                                  lag_ratio=0.08),
                      LaggedStart(*[GrowArrow(a) for a in harrows], lag_ratio=0.08), run_time=1.3)
            b.wait_until("one", lead=0.1)
            h = orb(X_C).move_to(cells[0].get_left() + LEFT * 0.45)
            self.play(FadeIn(h, scale=0.5), run_time=0.2)
            step = (b.t("hidden") - self.now + 0.4) / n
            for i in range(n):
                self.sfx("tick", -15)
                self.play(FadeIn(chips[i], shift=UP * 0.15), GrowArrow(up_arrows[i]),
                          h.animate.move_to(cells[i]),
                          cells[i].animate.set_stroke(X_C, 2.5).set_fill(lerp_color(PANEL, X_C, 0.18), 1),
                          run_time=step * 0.75)
                self.play(cells[i].animate.set_stroke(INK3, 2).set_fill(PANEL, 1), run_time=step * 0.25)
            hl = txt("hidden state", 24, X_C, weight="SEMIBOLD").next_to(cells[-1], UP, buff=0.45)
            self.play(FadeIn(hl, shift=DOWN * 0.1), Indicate(h, color=X_C, scale_factor=1.4), run_time=0.7)

        # ---- b2: distance
        with self.vo("b2") as b:
            b.wait_until("dist", lead=0.2)
            p1 = txt("Problem 1:  distance", 30, INK, weight="SEMIBOLD").move_to(UP * 2.3)
            self.play(FadeOut(title, shift=UP * 0.2), FadeIn(p1, shift=UP * 0.2), FadeOut(hl), FadeOut(h),
                      run_time=0.6)
            b.wait_until("pass", lead=0.3)
            a_orb = orb(K_C, 0.16).move_to(cells[ANIMAL])
            self.play(chips[ANIMAL].box.animate.set_stroke(K_C, 2.5),
                      chips[7].box.animate.set_stroke(Q_C, 2.5), FadeIn(a_orb, scale=0.4), run_time=0.4)
            counter = VGroup(txt("hand-offs:", 24, INK2), txt("0", 24, INK, weight="SEMIBOLD", font=MONO))
            counter.arrange(RIGHT, buff=0.15).move_to(DOWN * 2.8)
            self.play(FadeIn(counter), run_time=0.25)
            hops = 6
            hop_t = max(0.3, (b.t("far") - self.now) / hops)
            for k in range(hops):
                i = ANIMAL + k + 1
                new_num = txt(str(k + 1), 24, INK, weight="SEMIBOLD", font=MONO).move_to(counter[1])
                fade = 1 - (k + 1) / (hops + 1.2)
                self.sfx("blip_down", -14 - k)
                self.play(a_orb.animate.move_to(cells[i]).set_opacity(max(fade, 0.12)).scale(0.86),
                          Transform(counter[1], new_num),
                          Indicate(cells[i], color=K_C, scale_factor=1.06), run_time=hop_t)
            brace = BraceBetweenPoints(cells[ANIMAL].get_top() + UP * 0.1, cells[7].get_top() + UP * 0.1,
                                       direction=UP).set_color(INK3)
            bt = txt("the further apart, the weaker the link", 24, INK2).next_to(brace, UP, buff=0.12)
            b.wait_until("far", lead=-0.2)
            self.play(GrowFromCenter(brace), FadeIn(bt, shift=UP * 0.1), run_time=0.6)

        # ---- b3: speed
        with self.vo("b3") as b:
            p2 = txt("Problem 2:  speed", 30, INK, weight="SEMIBOLD").move_to(UP * 2.3)
            chain = VGroup(cells, cell_lbl, harrows, chips, up_arrows)
            self.play(FadeOut(VGroup(p1, brace, bt, counter, a_orb)), FadeIn(p2, shift=UP * 0.2),
                      chips[ANIMAL].box.animate.set_stroke(EDGE, 1.6), chips[7].box.animate.set_stroke(EDGE, 1.6),
                      chain.animate.scale(0.62).move_to(LEFT * 2.9 + DOWN * 0.3), run_time=0.7)
            gpu = VGroup(*[RoundedRectangle(corner_radius=0.03, width=0.24, height=0.24)
                           .set_fill(PANEL2, 1).set_stroke(EDGE, 1) for _ in range(80)])
            gpu.arrange_in_grid(8, 10, buff=0.07).move_to(RIGHT * 4.3 + DOWN * 0.3)
            gpu_lbl = txt("GPU cores", 24, INK2).next_to(gpu, UP, buff=0.25)
            idle = txt("mostly idle", 22, INK3).next_to(gpu, DOWN, buff=0.25)
            timeline = Arrow(LEFT, RIGHT, buff=0).set_color(INK3).set_width(chain.width)
            timeline.next_to(chain, DOWN, buff=0.35)
            tl = txt("time", 20, INK3).next_to(timeline, DOWN, buff=0.08)
            self.play(GrowArrow(timeline), FadeIn(tl), run_time=0.5)
            shown = False
            per = 0.42
            for i in range(n):
                anims = [cells[i].animate.set_fill(lerp_color(PANEL, Q_C, 0.35), 1).set_stroke(Q_C, 2.5)]
                if i > 0:
                    anims.append(cells[i - 1].animate.set_fill(PANEL, 1).set_stroke(INK3, 2))
                if shown:
                    anims += [gpu[(i - 1) % 80].animate.set_fill(PANEL2, 1),
                              gpu[i % 80].animate.set_fill(Q_C, 1)]
                self.sfx("tick", -16)
                self.play(*anims, run_time=per)
                if not shown and self.now >= b.t("gpu") - 0.5:
                    self.sfx("pop_soft", -12)
                    self.play(FadeIn(gpu, lag_ratio=0.01), FadeIn(gpu_lbl), FadeIn(idle), run_time=0.5)
                    self.play(gpu[i % 80].animate.set_fill(Q_C, 1), run_time=0.15)
                    shown = True
            if not shown:
                self.play(FadeIn(gpu, lag_ratio=0.01), FadeIn(gpu_lbl), FadeIn(idle), run_time=0.5)
            self.play(cells[n - 1].animate.set_fill(PANEL, 1).set_stroke(INK3, 2), run_time=0.2)

        # ---- b4: the transformer's answer
        with self.vo("b4") as b:
            b.wait_until("drop", lead=0.3)
            self.sfx("whoosh", -8)
            self.play(FadeOut(VGroup(cells, cell_lbl, harrows, up_arrows), scale=0.8),
                      FadeOut(VGroup(timeline, tl, p2)), run_time=0.7)
            row = chips.copy()
            row.arrange(RIGHT, buff=0.16).scale_to_fit_width(8.4).move_to(LEFT * 2.3 + DOWN * 1.0)
            self.play(Transform(chips, row), run_time=0.7)
            b.wait_until("all", lead=0.2)
            rng = np.random.default_rng(5)
            web = VGroup()
            for i in range(n):
                for j in range(i + 1, n):
                    web.add(attn_arc(chips[i], chips[j], rng.uniform(0.05, 0.35), INK2, angle=0.7 * PI,
                                     base=0.8, span=3.0, min_op=0.18))
            new_t = txt("Every word looks at every other word, at once", 28, INK, weight="SEMIBOLD")
            new_t.move_to(UP * 2.6)
            self.sfx("shimmer", -8)
            self.play(LaggedStart(*[Create(a) for a in web], lag_ratio=0.0), FadeIn(new_t, shift=DOWN * 0.1),
                      run_time=1.0)
            b.wait_until("onestep", lead=0.2)
            key = attn_arc(chips[7], chips[ANIMAL], 0.9, Q_C, angle=0.7 * PI)
            kg = glow(key, Q_C, layers=5, width=20, opacity=0.25)
            one = txt("1 step", 26, Q_C, weight="SEMIBOLD").next_to(key, UP, buff=0.12)
            path_t = VGroup(txt("longest path between words", 24, INK2),
                            MathTex(r"O(n)\;\rightarrow\;O(1)", font_size=42, color=INK)).arrange(RIGHT, buff=0.3)
            path_t.next_to(chips, DOWN, buff=0.5)
            self.sfx("chime_soft", -8)
            self.play(web.animate.set_stroke(opacity=0.12), Create(key), FadeIn(kg), FadeIn(one),
                      chips[7].box.animate.set_stroke(Q_C, 2.6), chips[ANIMAL].box.animate.set_stroke(K_C, 2.6),
                      FadeIn(path_t, shift=UP * 0.1), run_time=0.8)
            b.wait_until("par", lead=0.1)
            seq_t = VGroup(txt("sequential steps", 24, INK2),
                           MathTex(r"O(n)\;\rightarrow\;O(1)", font_size=42, color=INK)).arrange(RIGHT, buff=0.3)
            seq_t.next_to(gpu, DOWN, buff=0.35)
            self.sfx("power_up", -8)
            self.play(LaggedStart(*[c.animate.set_fill(HEADS[k % 8], 1) for k, c in enumerate(gpu)], lag_ratio=0.004),
                      FadeOut(idle), FadeIn(seq_t, shift=UP * 0.1), run_time=0.9)
            tag = txt("paper, Table 1", 18, INK3).next_to(seq_t, DOWN, buff=0.15)
            self.play(FadeIn(tag), run_time=0.3)
        self.wait(0.6)
        self.sfx("whoosh", -9)
        self.end_scene()
