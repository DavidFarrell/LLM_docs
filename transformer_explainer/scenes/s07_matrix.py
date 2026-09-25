import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import *  # noqa: E402,F401,F403

T8 = ["animal", "didn't", "cross", "street", "because", "it", "was", "tired"]
IT8, AN8 = 5, 0
rng = np.random.default_rng(21)
RAW = rng.uniform(-1.0, 1.2, (8, 8))
RAW[IT8] = [3.2, -0.4, 0.2, 1.4, 0.1, 0.6, -0.2, 1.1]
RAW[AN8] = [0.5, 0.2, 1.3, 0.9, -0.3, 0.1, 0.4, 1.6]
for i in range(8):
    RAW[i, i] += 0.6
SCALED = RAW / 1.6
W8 = softmax(SCALED * 1.6, axis=1)


def mat_block(n, m, color, cell=0.4, gap=0.05, seed=0):
    vals = np.random.default_rng(seed).uniform(0, 1, (n, m))
    g = VGroup(*[RoundedRectangle(corner_radius=0.04, width=cell, height=cell).set_stroke(width=0)
                 .set_fill(lerp_color(PANEL2, color, 0.2 + 0.75 * vals[r, c]), 1)
                 for r in range(n) for c in range(m)])
    g.arrange_in_grid(n, m, buff=gap)
    return g


class S07_Matrix(TScene):
    chapter = ("06", "The equation")

    def construct(self):
        self.wait(0.2)
        self.chapter_intro()
        cell, gap = 0.4, 0.05
        n = 8
        grid = Heatmap(np.zeros((n, n)), cell=cell, gap=gap).move_to([-0.2, -1.25, 0])
        grid.set_opacity(0)
        row_y = [grid.cell(i, 0).get_center()[1] for i in range(n)]
        rl = VGroup(*[txt(w, 22, INK2).move_to([-2.35, y, 0], aligned_edge=RIGHT) for w, y in zip(T8, row_y)])
        cl = VGroup(*[txt(w, 20, INK2).rotate(PI / 2).next_to(grid.cell(0, j), UP, buff=0.15)
                      for j, w in enumerate(T8)])
        for c in cl:
            c.align_to(grid, DOWN).shift(UP * (grid.height + 0.15))
        Qm = mat_block(n, 4, Q_C, cell, gap, seed=1)
        Qm.move_to([-4.85, grid.get_center()[1], 0])
        Km = mat_block(n, 4, K_C, cell, gap, seed=2).move_to([3.35, grid.get_center()[1], 0])
        Vm = mat_block(n, 4, V_C, cell, gap, seed=3).move_to([5.55, grid.get_center()[1], 0])
        Ql = MathTex("Q", font_size=48, color=Q_C).next_to(Qm, UP, buff=0.25)
        Kl = MathTex("K", font_size=48, color=K_C).next_to(Km, UP, buff=0.25)
        Vl = MathTex("V", font_size=48, color=V_C).next_to(Vm, UP, buff=0.25)

        # ---- b1: stack queries into Q, keys into K, values into V
        with self.vo("b1") as b:
            rows = [VGroup(*Qm[4 * r:4 * r + 4]) for r in range(n)]
            yc = Qm.get_center()[1]
            targets = [r.get_center() for r in rows]
            for r in rows:
                r.shift(LEFT * 0.6)
                for k, cell_ in enumerate(r):
                    cell_.shift(LEFT * 0.06 * (3 - k))
            qlab = txt("each word's query", 22, Q_C).next_to(VGroup(*rows), UP, buff=0.3).align_to(VGroup(*rows), LEFT)
            self.play(LaggedStart(*[FadeIn(l, shift=RIGHT * 0.2) for l in rl], lag_ratio=0.08),
                      LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows], lag_ratio=0.08),
                      FadeIn(qlab), run_time=1.3)
            b.wait_until("stack", lead=0.3)
            self.sfx("swish", -12)
            finals = []
            for r, tg in zip(rows, targets):
                fr = r.copy()
                fr.arrange(RIGHT, buff=gap).move_to(tg)
                finals.append(fr)
            self.play(LaggedStart(*[Transform(r, fr) for r, fr in zip(rows, finals)], lag_ratio=0.08),
                      FadeOut(qlab), FadeIn(Ql), run_time=1.3)
            self.sfx("click", -12)
            b.wait_until("kv", lead=0.2)
            self.play(LaggedStart(*[FadeIn(VGroup(*Km[4 * r:4 * r + 4]), shift=LEFT * 0.4) for r in range(n)],
                                  lag_ratio=0.06), FadeIn(Kl), run_time=0.9)
            self.play(LaggedStart(*[FadeIn(VGroup(*Vm[4 * r:4 * r + 4]), shift=LEFT * 0.4) for r in range(n)],
                                  lag_ratio=0.06), FadeIn(Vl), run_time=0.9)

        # ---- b2: Q K^T
        with self.vo("b2") as b:
            formula = MathTex(r"Q", r"K^{\top}", font_size=56).move_to(UP * 2.9 + RIGHT * 3.0)
            formula[0].set_color(Q_C)
            formula[1].set_color(K_C)
            self.play(FadeIn(formula, shift=DOWN * 0.1), FadeIn(cl), grid.animate.set_opacity(0.35), run_time=0.6)
            # one cell explicitly: 'it' row of Q with 'animal' row of K
            qrow = VGroup(*Qm[4 * IT8:4 * IT8 + 4])
            krow = VGroup(*Km[4 * AN8:4 * AN8 + 4])
            qo = outline(qrow, Q_C, buff=0.05, corner=0.06, width=2.5)
            ko = outline(krow, K_C, buff=0.05, corner=0.06, width=2.5)
            target = grid.cell(IT8, AN8)
            self.play(Create(qo), Create(ko), run_time=0.5)
            qc, kc = qrow.copy(), krow.copy()
            self.sfx("blip", -9)
            self.play(qc.animate.move_to(target).scale(0.25).set_opacity(0),
                      kc.animate.move_to(target).scale(0.25).set_opacity(0),
                      target.animate.set_fill(heat_color(0.95), 1).set_opacity(1), run_time=0.8)
            self.remove(qc, kc)
            dot_note = MathTex(r"\mathbf{q}_{\text{it}}\cdot\mathbf{k}_{\text{animal}}", font_size=34, color=INK2)
            dot_note.next_to(grid, DOWN, buff=0.35)
            self.play(FadeIn(dot_note), run_time=0.4)
            b.wait_until("grid", lead=0.3)
            norm_raw = (RAW - RAW.min()) / (RAW.max() - RAW.min())
            order = sorted([(i, j) for i in range(n) for j in range(n)], key=lambda p: p[0] + p[1])
            self.sfx("shimmer", -9)
            self.sfx("ticks_fast", -14)
            self.play(LaggedStart(*[grid.cell(i, j).animate.set_fill(heat_color(norm_raw[i, j]), 1).set_opacity(1)
                                    for i, j in order], lag_ratio=0.012), FadeOut(qo), FadeOut(ko),
                      FadeOut(dot_note), run_time=1.1)
            grid.M = norm_raw
            b.wait_until("rows", lead=0.2)
            ro = outline(grid.row(IT8), Q_C, buff=0.05, corner=0.06, width=3)
            rtxt = txt("each row: a word asking", 24, Q_C).next_to(grid, DOWN, buff=0.35)
            self.play(Create(ro), FadeIn(rtxt, shift=UP * 0.1), rl[IT8].animate.set_color(Q_C), run_time=0.6)
            b.wait_until("cols", lead=0.2)
            co = outline(grid.col(AN8), K_C, buff=0.05, corner=0.06, width=3)
            ctxt = txt("each column: a word being asked", 24, K_C).next_to(rtxt, DOWN, buff=0.12)
            self.play(Create(co), FadeIn(ctxt, shift=UP * 0.1), cl[AN8].animate.set_color(K_C), run_time=0.6)

        # ---- b3: scale, softmax, times V
        with self.vo("b3") as b:
            b.wait_until("div", lead=0.1)
            f_div = MathTex(r"{", r"Q", r"K^{\top}", r"\over", r"\sqrt{d_k}", r"}", font_size=52)
            f_div[1].set_color(Q_C)
            f_div[2].set_color(K_C)
            f_div.move_to(formula)
            soft_raw = 0.15 + 0.7 * norm_raw
            self.play(TransformMatchingTex(formula, f_div), grid.animate.recolor(soft_raw),
                      FadeOut(VGroup(rtxt, ctxt)), run_time=0.8)
            b.wait_until("sm", lead=0.2)
            f_sm = MathTex(r"\mathrm{softmax}\!\Big(", r"{", r"Q", r"K^{\top}", r"\over", r"\sqrt{d_k}", r"}",
                           r"\Big)", font_size=48)
            f_sm[2].set_color(Q_C)
            f_sm[3].set_color(K_C)
            f_sm[0].set_color(SMX_C)
            f_sm[7].set_color(SMX_C)
            f_sm.move_to(formula).shift(LEFT * 0.4)
            wn = W8 / W8.max(axis=1, keepdims=True)
            sums = VGroup(*[MathTex(r"\Sigma{=}1", font_size=26, color=INK2).next_to(grid.cell(i, n - 1), RIGHT, buff=0.12)
                            for i in range(n)])
            self.sfx("shimmer", -9)
            self.play(TransformMatchingTex(f_div, f_sm), run_time=0.6)
            self.play(LaggedStart(*[AnimationGroup(*[grid.cell(i, j).animate.set_fill(heat_color(0.08 + 0.9 * wn[i, j]), 1)
                                                     for j in range(n)]) for i in range(n)], lag_ratio=0.12),
                      LaggedStart(*[FadeIn(s_) for s_ in sums], lag_ratio=0.12), run_time=1.3)
            b.wait_until("v", lead=0.2)
            f_v = MathTex(r"\mathrm{softmax}\!\Big(", r"{", r"Q", r"K^{\top}", r"\over", r"\sqrt{d_k}", r"}",
                          r"\Big)", r"V", font_size=48)
            f_v[2].set_color(Q_C)
            f_v[3].set_color(K_C)
            f_v[0].set_color(SMX_C)
            f_v[7].set_color(SMX_C)
            f_v[8].set_color(V_C)
            f_v.move_to(f_sm)
            self.play(FadeOut(VGroup(Km, Kl)), FadeOut(sums), run_time=0.4)
            self.play(VGroup(Vm, Vl).animate.move_to([2.95, Vm.get_center()[1] + 0.33, 0]),
                      TransformMatchingTex(f_sm, f_v), run_time=0.7)
            Vl.next_to(Vm, UP, buff=0.25)
            b.wait_until("out", lead=0.2)
            Zm = mat_block(n, 4, V_C, cell, gap, seed=9)
            Zm.move_to([5.4, Vm.get_center()[1], 0])
            eq = MathTex("=", font_size=48, color=INK2).move_to([(Vm.get_right()[0] + Zm.get_left()[0]) / 2,
                                                                  Vm.get_center()[1], 0])
            Zl = txt("output", 26, V_C, weight="SEMIBOLD").next_to(Zm, UP, buff=0.25)
            self.sfx("whoosh_soft", -9)
            self.play(FadeIn(eq), LaggedStart(*[FadeIn(VGroup(*Zm[4 * r:4 * r + 4]), shift=RIGHT * 0.3) for r in range(n)],
                                              lag_ratio=0.06), FadeIn(Zl), run_time=1.0)
            zo = outline(VGroup(*Zm[4 * IT8:4 * IT8 + 4]), V_C, buff=0.05, corner=0.06, width=3)
            zt = txt("context-aware 'it'", 22, V_C).next_to(Zm, DOWN, buff=0.3)
            self.play(Create(zo), FadeIn(zt), run_time=0.6)
            mats_group = VGroup(Qm, Ql, rl, cl, grid, ro, co, Vm, Vl, eq, Zm, Zl, zo, zt)

        # ---- b4: the equation
        with self.vo("b4") as b:
            big = MathTex(r"\mathrm{Attention}(Q,K,V)", r"=", r"\mathrm{softmax}\!\left(", r"{Q", r"K^{\top}",
                          r"\over", r"\sqrt{d_k}}", r"\right)", r"V", font_size=64)
            big[2].set_color(SMX_C)
            big[7].set_color(SMX_C)
            big[3].set_color(Q_C)
            big[4].set_color(K_C)
            big[8].set_color(V_C)
            big.move_to(UP * 0.2)
            cap = txt("Scaled dot-product attention  ·  equation (1)", 28, INK2).next_to(big, DOWN, buff=0.6)
            self.sfx("impact_soft", -7)
            self.play(FadeOut(mats_group, scale=0.9), ReplacementTransform(f_v, big[2:]), FadeIn(big[:2]),
                      run_time=1.0)
            self.play(FadeIn(cap, shift=UP * 0.1), run_time=0.5)
            b.wait_until("every", lead=0.1)
            items = [(0.0, Indicate(big[3], color=Q_C, scale_factor=1.2), 0.5, "tick", -12),
                     (0.35, Indicate(big[4], color=K_C, scale_factor=1.2), 0.5, "tick", -12),
                     (0.7, Indicate(big[6], color=INK, scale_factor=1.2), 0.5, "tick", -12),
                     (1.05, Indicate(big[2], color=SMX_C, scale_factor=1.1), 0.5, "tick", -12),
                     (1.4, Indicate(big[8], color=V_C, scale_factor=1.25), 0.5, "tick", -12)]
            b.schedule(items)

        # ---- b5: why sqrt(d_k): variance
        with self.vo("b5") as b:
            self.play(big.animate.scale(0.5).to_edge(UP, buff=0.35).shift(RIGHT * 2.8), FadeOut(cap), run_time=0.6)
            ttl = VGroup(txt("Why divide by", 36, INK, weight="SEMIBOLD"), MathTex(r"\sqrt{d_k}", font_size=50),
                         txt("?", 36, INK, weight="SEMIBOLD")).arrange(RIGHT, buff=0.2).move_to(UP * 2.3 + LEFT * 3.0)
            self.play(FadeIn(ttl, shift=UP * 0.1), run_time=0.4)
            ax = Axes(x_range=[-30, 30, 10], y_range=[0, 0.22, 0.1], x_length=9.5, y_length=3.4,
                      axis_config={"stroke_color": INK3, "stroke_width": 2, "include_ticks": True,
                                   "tick_size": 0.05},
                      x_axis_config={"numbers_to_include": [-24, -16, -8, 0, 8, 16, 24], "font_size": 22,
                                     "numbers_with_elongated_ticks": []}).move_to(DOWN * 0.9)
            ax.y_axis.set_opacity(0)
            sig = ValueTracker(2.0)
            curve = always_redraw(lambda: ax.plot(
                lambda x: np.exp(-x ** 2 / (2 * sig.get_value() ** 2)) / (sig.get_value() * np.sqrt(2 * PI)),
                x_range=[-30, 30, 0.1], color=Q_C, stroke_width=4))
            area = always_redraw(lambda: ax.get_area(curve, x_range=[-30, 30], color=Q_C, opacity=0.18))
            info = always_redraw(lambda: VGroup(
                MathTex(r"d_k = " + f"{int(round(sig.get_value() ** 2))}", font_size=40, color=INK),
                MathTex(r"\sigma = \sqrt{d_k} = " + f"{sig.get_value():.0f}", font_size=40, color=Q_C)
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to(RIGHT * 4.3 + UP * 1.3))
            xl = txt("dot product q · k of random vectors", 22, INK3).next_to(ax, DOWN, buff=0.45)
            self.play(Create(ax), FadeIn(xl), run_time=0.6)
            self.add(area, curve, info)
            b.wait_until("var", lead=0.1)
            vnote = MathTex(r"\mathrm{Var}(\mathbf{q}\cdot\mathbf{k}) = d_k", font_size=40, color=INK2)
            vnote.next_to(ttl, DOWN, buff=0.35).align_to(ttl, LEFT)
            self.play(FadeIn(vnote), run_time=0.4)
            self.sfx("riser_short", -12)
            self.play(sig.animate.set_value(4.0), run_time=1.3)
            b.wait_until("sd", lead=1.2)
            self.play(sig.animate.set_value(8.0), run_time=1.3)
            m1 = DashedLine(ax.c2p(-8, 0), ax.c2p(-8, 0.07)).set_stroke(Q_C, 2)
            m2 = DashedLine(ax.c2p(8, 0), ax.c2p(8, 0.07)).set_stroke(Q_C, 2)
            pm = MathTex(r"\pm 8", font_size=40, color=Q_C).next_to(ax.c2p(8, 0.07), UP + RIGHT, buff=0.1)
            self.play(Create(m1), Create(m2), FadeIn(pm), run_time=0.6)
            grp5 = VGroup(ttl, vnote, ax, xl, m1, m2, pm)

        # ---- b6: softmax saturates
        with self.vo("b6") as b:
            self.remove(area, curve, info)
            self.play(FadeOut(grp5), run_time=0.35)
            s_raw = np.array([9.0, -4.0, 13.0, 2.0, -7.0, 5.0])
            p_raw = softmax(s_raw)
            p_fix = softmax(s_raw / 8)
            xs = [-4.4 + 1.25 * i for i in range(6)]
            base = -2.2
            hmax = 3.6
            bars = VGroup(*[Rectangle(width=0.8, height=max(0.02, hmax * p)).set_fill(Q_C, 0.85).set_stroke(width=0)
                            .move_to([x, base, 0], aligned_edge=DOWN) for x, p in zip(xs, p_raw)])
            axis = Line([xs[0] - 0.7, base, 0], [xs[-1] + 0.7, base, 0]).set_stroke(INK3, 2)
            sc_l = VGroup(*[MathTex(f"{s:+.0f}", font_size=30, color=INK2).next_to([x, base, 0], DOWN, buff=0.2)
                            for x, s in zip(xs, s_raw)])
            lab = txt("softmax(raw scores)", 28, INK, weight="SEMIBOLD").move_to(UP * 2.3 + LEFT * 1.3)
            pct = VGroup(*[txt(f"{100 * p:.0f}%", 22, INK).next_to(bb, UP, buff=0.1) for bb, p in zip(bars, p_raw)])
            b.wait_until("sat", lead=0.1)
            self.play(Create(axis), FadeIn(sc_l), FadeIn(lab), LaggedStart(*[GrowFromEdge(bb, DOWN) for bb in bars],
                                                                             lag_ratio=0.1), run_time=0.9)
            self.play(FadeIn(pct), run_time=0.3)
            satl = txt("saturated: almost one-hot", 26, BAD).move_to(RIGHT * 4.4 + UP * 1.0)
            self.play(FadeIn(satl, shift=LEFT * 0.1), run_time=0.5)
            b.wait_until("grad", lead=0.1)
            gl = txt("gradients ≈ 0", 30, BAD, weight="SEMIBOLD").next_to(satl, DOWN, buff=0.35)
            self.sfx("fail", -12)
            self.play(FadeIn(gl, shift=UP * 0.1), Wiggle(gl), run_time=0.8)
            b.wait_until("fix", lead=0.2)
            lab2 = MathTex(r"\mathrm{softmax}(\text{scores} \div \sqrt{64})", font_size=44, color=INK).move_to(lab)
            sc_l2 = VGroup(*[MathTex(f"{s / 8:+.2f}", font_size=30, color=INK2).move_to(l) for l, s in zip(sc_l, s_raw)])
            new_bars = VGroup(*[Rectangle(width=0.8, height=max(0.02, hmax * p)).set_fill(Q_C, 0.85).set_stroke(width=0)
                                .move_to([x, base, 0], aligned_edge=DOWN) for x, p in zip(xs, p_fix)])
            pct2 = VGroup(*[txt(f"{100 * p:.0f}%", 22, INK).next_to(bb, UP, buff=0.1) for bb, p in zip(new_bars, p_fix)])
            okl = txt("healthy gradients", 30, GOOD, weight="SEMIBOLD").move_to(gl)
            self.sfx("chime_soft", -9)
            self.play(ReplacementTransform(lab, lab2), *[Transform(a, c) for a, c in zip(sc_l, sc_l2)],
                      *[Transform(a, c) for a, c in zip(bars, new_bars)], *[Transform(a, c) for a, c in zip(pct, pct2)],
                      FadeOut(satl), ReplacementTransform(gl, okl), run_time=1.2)
        self.wait(0.5)
        self.end_scene()
