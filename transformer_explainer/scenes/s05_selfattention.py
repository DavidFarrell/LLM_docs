import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import *  # noqa: E402,F401,F403

# raw attention scores from 'it' to each word (illustrative)
SCORES = np.array([0.3, 3.4, 0.1, 0.6, 0.2, 1.7, 0.4, 1.1, 0.2, 0.1, 1.5])


class S05_SelfAttention(TScene):
    chapter = ("04", "Self-attention")

    def make_triplets(self, chips):
        trips = VGroup()
        for i, c in enumerate(chips):
            q = VecCells(rvals(4, 10 + i), Q_C, cell=0.15, gap=0.03)
            k = VecCells(rvals(4, 40 + i), K_C, cell=0.15, gap=0.03)
            v = VecCells(rvals(4, 70 + i), V_C, cell=0.15, gap=0.03)
            t = VGroup(q, k, v).arrange(RIGHT, buff=0.05).move_to([c.get_center()[0], -1.35, 0])
            trips.add(t)
        return trips

    def construct(self):
        self.wait(0.2)
        self.chapter_intro()
        chips = sentence_layout(SENT, y=-2.45)
        trips = self.make_triplets(chips)
        Qs = VGroup(*[t[0] for t in trips])
        Ks = VGroup(*[t[1] for t in trips])
        Vs = VGroup(*[t[2] for t in trips])

        legend = VGroup()
        for name, desc, col in (("query", "what am I looking for?", Q_C), ("key", "what do I contain?", K_C),
                                ("value", "what will I pass on?", V_C)):
            dot = RoundedRectangle(corner_radius=0.04, width=0.2, height=0.2).set_fill(col, 1).set_stroke(width=0)
            row = VGroup(dot, txt(name, 28, col, weight="SEMIBOLD"), txt(desc, 28, INK2))
            row.arrange(RIGHT, buff=0.2)
            legend.add(row)
        legend.arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to(UP * 1.3)

        # ---- b1: every word plays all three roles
        with self.vo("b1") as b:
            b.wait_until("sent", lead=0.3)
            self.sfx("swish", -12)
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in chips], lag_ratio=0.05), run_time=0.9)
            for key, group, row in (("q", Qs, legend[0]), ("k", Ks, legend[1]), ("v", Vs, legend[2])):
                b.wait_until(key, lead=0.15)
                self.sfx("pop_soft", -11)
                self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.25) for m in group], lag_ratio=0.04),
                          FadeIn(row, shift=RIGHT * 0.2), run_time=0.9)

        # ---- b2: cartoon intuitions
        with self.vo("b2") as b:
            b.wait_until("it", lead=0.25)
            others = [i for i in range(len(SENT)) if i != IT]
            q_it = Qs[IT]
            qglow = glow(q_it.outline, Q_C, layers=5, width=14, opacity=0.35)
            self.play(legend.animate.set_opacity(0.0),
                      *[chips[i].animate.set_opacity(0.3) for i in others],
                      *[trips[i].animate.set_opacity(0.2) for i in others],
                      Ks[IT].animate.set_opacity(0.2), Vs[IT].animate.set_opacity(0.2),
                      chips[IT].box.animate.set_stroke(Q_C, 2.6), FadeIn(qglow), run_time=0.6)
            self.remove(legend)
            b_it = bubble("Which noun do I refer to?", Q_C, 26).next_to(q_it, UP, buff=0.3)
            b_it.shift(RIGHT * (b_it.width / 2 - 0.45))
            for part in (b_it[1], b_it[2]):
                part.set_x(q_it.get_center()[0])
            self.sfx("pop", -9)
            self.play(FadeIn(b_it, shift=UP * 0.15, scale=0.9), run_time=0.45)
            b.wait_until("ak", lead=0.2)
            k_an = Ks[ANIMAL]
            b_k = bubble("singular noun · a creature · can get tired", K_C, 24).next_to(k_an, UP, buff=0.3)
            b_k.shift(RIGHT * (b_k.width / 2 - 0.5))
            b_k[1].move_to([k_an.get_center()[0], b_k[1].get_center()[1], 0])
            b_k[2].move_to([k_an.get_center()[0], b_k[2].get_center()[1], 0])
            self.sfx("pop", -9)
            self.play(chips[ANIMAL].animate.set_opacity(1), k_an.animate.set_opacity(1),
                      FadeIn(b_k, shift=UP * 0.15, scale=0.9), run_time=0.5)
            b.wait_until("av", lead=0.2)
            v_an = Vs[ANIMAL]
            b_v = bubble("what 'animal' means", V_C, 24).next_to(b_k, UP, buff=0.35)
            b_v.align_to(b_k, LEFT)
            vline = Line(v_an.get_top() + UP * 0.05, b_v.get_bottom() + DOWN * 0.02).set_stroke(V_C, 2)
            vline.put_start_and_end_on(v_an.get_top() + UP * 0.05,
                                       [v_an.get_center()[0], b_v.get_bottom()[1], 0])
            self.sfx("pop", -9)
            self.play(v_an.animate.set_opacity(1), FadeIn(b_v, shift=UP * 0.15, scale=0.9), Create(vline),
                      b_k.animate.shift(RIGHT * 0.0), run_time=0.5)

        # ---- b3: cartoons -> learned matrices
        with self.vo("b3") as b:
            stamp_t = txt("CARTOONS", 34, BAD, weight="BOLD")
            stamp = VGroup(outline(stamp_t, BAD, buff=0.18, corner=0.08, width=3), stamp_t).rotate(0.1)
            stamp.move_to(UP * 2.3 + LEFT * 1.0)
            self.play(FadeIn(stamp, scale=1.3), Wiggle(b_it, scale_value=1.05), Wiggle(b_k, scale_value=1.05),
                      Wiggle(b_v, scale_value=1.05), run_time=0.9)
            b.wait_until("nobody", lead=0.1)
            self.sfx("swish", -10)
            self.play(*[FadeOut(m, scale=1.25) for m in (b_it, b_k, b_v, vline, stamp)], run_time=0.5)
            b.wait_until("mat", lead=0.35)
            sent_group = VGroup(chips, trips, qglow)
            self.play(sent_group.animate.set_opacity(0).shift(DOWN * 0.5), run_time=0.5)
            self.remove(sent_group)
            # projection diagram for one word
            xchip = Chip("animal", size=30).move_to(LEFT * 5.6 + UP * 0.0)
            xv = VecCells(rvals(8, 3), X_C, cell=0.26, gap=0.045).next_to(xchip, RIGHT, buff=0.45)
            xl = MathTex(r"\mathbf{x}", font_size=44, color=X_C).next_to(xv, UP, buff=0.2)
            mats = VGroup()
            mlabels = VGroup()
            for j, (col, name) in enumerate(((Q_C, "W^Q"), (K_C, "W^K"), (V_C, "W^V"))):
                vals = np.random.default_rng(100 + j).uniform(0, 1, (6, 4))
                grid = VGroup(*[RoundedRectangle(corner_radius=0.02, width=0.2, height=0.2).set_stroke(width=0)
                                .set_fill(lerp_color(PANEL2, col, 0.15 + 0.6 * vals[r, c]), 1)
                                for r in range(6) for c in range(4)])
                grid.arrange_in_grid(6, 4, buff=0.035)
                frame = outline(grid, col, buff=0.07, corner=0.08, width=2)
                m = VGroup(grid, frame).move_to([-0.6, 2.35 - 2.35 * j, 0])
                mats.add(m)
                lab = MathTex(name, font_size=42, color=col).next_to(m, LEFT, buff=0.3)
                mlabels.add(lab)
            in_arrows = VGroup(*[Arrow(xv.get_right(), m.get_left(), buff=0.15, stroke_width=2.5)
                                 .set_color(INK3) for m in mats])
            self.sfx("whoosh_soft", -9)
            self.play(FadeIn(xchip, shift=RIGHT * 0.2), FadeIn(xv), FadeIn(xl), FadeIn(in_arrows),
                      *[FadeIn(m[1]) for m in mats], *[m[0].animate.set_opacity(0.25) for m in mats], run_time=0.8)
            for key, j in (("wq", 0), ("wk", 1), ("wv", 2)):
                b.wait_until(key, lead=0.1)
                self.sfx("tick", -12)
                self.play(mats[j][0].animate.set_opacity(1), FadeIn(mlabels[j], shift=RIGHT * 0.1), run_time=0.35)
            b.wait_until("mul", lead=0.05)
            outs = VGroup()
            olabels = VGroup()
            for j, (col, name, seed) in enumerate(((Q_C, r"\mathbf{q} = \mathbf{x}W^Q", 11 + ANIMAL),
                                                   (K_C, r"\mathbf{k} = \mathbf{x}W^K", 41 + ANIMAL),
                                                   (V_C, r"\mathbf{v} = \mathbf{x}W^V", 71 + ANIMAL))):
                o = VecCells(rvals(4, seed), col, cell=0.24, gap=0.045).move_to([2.2, mats[j].get_center()[1], 0])
                outs.add(o)
                olabels.add(MathTex(name, font_size=38, color=col).next_to(o, RIGHT, buff=0.45))
            flows = VGroup(*[xv.copy() for _ in range(3)])
            self.sfx("whoosh", -10)
            self.play(*[f.animate.rotate(-PI / 2).scale(0.8).move_to(mats[j]).set_opacity(0)
                        for j, f in enumerate(flows)], run_time=0.8)
            self.remove(flows)
            arrows = VGroup(*[Arrow(mats[j].get_right(), outs[j].get_left(), buff=0.15, stroke_width=3)
                              .set_color(INK3) for j in range(3)])
            self.sfx("blip", -10)
            self.play(LaggedStart(*[AnimationGroup(GrowArrow(arrows[j]), FadeIn(outs[j], shift=RIGHT * 0.3))
                                    for j in range(3)], lag_ratio=0.25), run_time=1.0)
            self.play(LaggedStart(*[FadeIn(l, shift=RIGHT * 0.1) for l in olabels], lag_ratio=0.2), run_time=0.8)
            proj = VGroup(xchip, xv, xl, mats, mlabels, outs, olabels, arrows, in_arrows)

        # ---- b4: scores
        with self.vo("b4") as b:
            self.play(FadeOut(proj, shift=UP * 0.3), run_time=0.45)
            sent_group.shift(UP * 0.5)
            for c in chips:
                c.set_opacity(1)
            for t in trips:
                for vec in t:
                    vec.set_opacity(1)
            others = [i for i in range(len(SENT)) if i != IT]
            for i in others:
                trips[i][0].set_opacity(0.25)
                trips[i][2].set_opacity(0.25)
            trips[IT][1].set_opacity(0.25)
            trips[IT][2].set_opacity(0.25)
            chips[IT].box.set_stroke(Q_C, 2.6)
            qglow = glow(Qs[IT].outline, Q_C, layers=5, width=14, opacity=0.35)
            self.play(FadeIn(chips), FadeIn(trips), FadeIn(qglow), run_time=0.6)
            b.wait_until("dot", lead=0.2)
            qbig = VecCells(Qs[IT].values, Q_C, cell=0.22, gap=0.04).move_to(UP * 2.45)
            qbl = MathTex(r"\mathbf{q}_{\text{it}}", font_size=40, color=Q_C).next_to(qbig, LEFT, buff=0.25)
            self.play(TransformFromCopy(Qs[IT], qbig), FadeIn(qbl), run_time=0.6)
            lines = VGroup(*[Line(qbig.get_bottom() + DOWN * 0.05, Ks[j].get_top() + UP * 0.05)
                             .set_stroke(Q_C, 1.6, opacity=0.55) for j in range(len(SENT))])
            self.sfx("shimmer", -12)
            self.play(LaggedStart(*[Create(l) for l in lines], lag_ratio=0.06),
                      LaggedStart(*[Indicate(Ks[j], color=Q_C, scale_factor=1.15) for j in range(len(SENT))],
                                  lag_ratio=0.06), run_time=1.4)
            dot_lab = MathTex(r"\mathbf{q}_{\text{it}}\cdot\mathbf{k}_j", font_size=38, color=INK2)
            dot_lab.next_to(qbig, RIGHT, buff=0.5)
            self.play(FadeIn(dot_lab), run_time=0.4)
            b.wait_until("scores", lead=0.2)
            base_y = -0.55
            hmax = 1.55
            bars = VGroup()
            nums = VGroup()
            for j in range(len(SENT)):
                h = max(0.03, hmax * SCORES[j] / SCORES.max())
                bar = Rectangle(width=0.5, height=h).set_fill(Q_C, 0.8).set_stroke(width=0)
                bar.move_to([chips[j].get_center()[0], base_y, 0], aligned_edge=DOWN)
                bars.add(bar)
                nums.add(DecimalNumber(SCORES[j], num_decimal_places=1, font_size=26, color=INK)
                         .next_to(bar, UP, buff=0.08))
            self.play(FadeOut(lines), LaggedStart(*[GrowFromEdge(bb, DOWN) for bb in bars], lag_ratio=0.04),
                      LaggedStart(*[FadeIn(nn) for nn in nums], lag_ratio=0.04), run_time=1.0)
            b.wait_until("high", lead=0.1)
            bglow = glow(bars[ANIMAL], Q_C, layers=5, width=16, opacity=0.35)
            self.sfx("ding", -10)
            self.play(FadeIn(bglow), Indicate(nums[ANIMAL], color=Q_C), chips[ANIMAL].box.animate.set_stroke(K_C, 2.6),
                      run_time=0.6)

        # ---- b5: softmax
        with self.vo("b5") as b:
            b.wait_until("soft", lead=0.15)
            w = softmax(SCORES)
            sm = pill("softmax", SMX_C, 26).move_to([-5.3, 1.75, 0])
            new_bars = VGroup()
            new_nums = VGroup()
            for j in range(len(SENT)):
                h = max(0.03, hmax * w[j] / w.max())
                nb = Rectangle(width=0.5, height=h).set_fill(Q_C, 0.35 + 0.6 * w[j] / w.max()).set_stroke(width=0)
                nb.move_to([chips[j].get_center()[0], base_y, 0], aligned_edge=DOWN)
                new_bars.add(nb)
                new_nums.add(txt(f"{100 * w[j]:.0f}%", 22, INK).next_to(nb, UP, buff=0.08))
            sum1 = txt("weights sum to 100%", 24, INK2).move_to([4.9, 1.75, 0])
            self.sfx("shimmer", -9)
            self.play(FadeIn(sm, shift=RIGHT * 0.2), FadeOut(dot_lab), run_time=0.35)
            self.play(*[Transform(bars[j], new_bars[j]) for j in range(len(SENT))],
                      *[Transform(nums[j], new_nums[j]) for j in range(len(SENT))],
                      Transform(bglow, glow(new_bars[ANIMAL], Q_C, layers=5, width=16, opacity=0.35)),
                      FadeIn(sum1), run_time=0.9)
            b.wait_until("most", lead=0.1)
            self.play(Indicate(nums[ANIMAL], color=Q_C, scale_factor=1.3), run_time=0.7)

        # ---- b6: weighted sum of values
        with self.vo("b6") as b:
            b.wait_until("scale", lead=0.05)
            self.play(*[Vs[j].animate.set_opacity(0.12 + 0.88 * w[j] / w.max()) for j in range(len(SENT))],
                      *[Ks[j].animate.set_opacity(0.25) for j in range(len(SENT))],
                      bars.animate.set_opacity(0.35), run_time=0.7)
            b.wait_until("sum", lead=0.1)
            vals = np.array([Vs[j].values for j in range(len(SENT))])
            new_it = np.clip((w[:, None] * vals).sum(0) * 1.4, -1, 1)
            out = VecCells(new_it, V_C, cell=0.22, gap=0.04).move_to([chips[IT].get_center()[0], 2.35, 0])
            copies = VGroup(*[Vs[j].copy() for j in range(len(SENT))])
            self.sfx("whoosh_soft", -8)
            self.play(*[c.animate.move_to(out).set_opacity(0.0) for c in copies], FadeIn(out, scale=0.8),
                      FadeOut(qbig), FadeOut(qbl), FadeOut(sum1), run_time=1.1)
            self.remove(copies)
            b.wait_until("new", lead=0.1)
            og = glow(out.outline, V_C, layers=5, width=14, opacity=0.35)
            ol = txt("new vector for 'it'", 26, V_C, weight="SEMIBOLD").next_to(out, LEFT, buff=0.35)
            arrow = Arrow(chips[IT].get_top() + UP * 1.0, out.get_bottom(), buff=0.1, stroke_width=2).set_color(INK3)
            self.sfx("chime", -9)
            self.play(FadeIn(og), FadeIn(ol, shift=LEFT * 0.1), chips[IT].box.animate.set_stroke(V_C, 2.6),
                      run_time=0.6)
            b.wait_until("ctx", lead=0.2)
            ctx = VGroup(txt("it", 26, INK, weight="SEMIBOLD"), txt("+ context from", 24, INK2),
                         txt("animal", 26, K_C, weight="SEMIBOLD")).arrange(RIGHT, buff=0.15)
            ctx.next_to(ol, DOWN, buff=0.2).align_to(ol, RIGHT)
            self.play(FadeIn(ctx, shift=UP * 0.1), run_time=0.5)

        # ---- b7: every word at once
        with self.vo("b7") as b:
            outs = VGroup()
            for j in range(len(SENT)):
                o = VecCells(rvals(4, 200 + j), V_C, cell=0.13, gap=0.025)
                o.move_to([chips[j].get_center()[0], 0.35, 0])
                outs.add(o)
            rng = np.random.default_rng(9)
            web = VGroup()
            for i in range(len(SENT)):
                for j in range(i + 1, len(SENT)):
                    web.add(attn_arc(chips[i], chips[j], rng.uniform(0.02, 0.4), INK2, angle=0.28 * PI,
                                     base=0.6, span=3.0, min_op=0.1, above=False))
            self.play(FadeOut(VGroup(bars, nums, bglow, sm, out, og, ol, ctx)),
                      *[Vs[j].animate.set_opacity(1) for j in range(len(SENT))],
                      *[Ks[j].animate.set_opacity(1) for j in range(len(SENT))],
                      *[Qs[j].animate.set_opacity(1) for j in range(len(SENT))],
                      chips[IT].box.animate.set_stroke(EDGE, 1.6), FadeOut(qglow), run_time=0.5)
            self.sfx("shimmer", -8)
            self.play(LaggedStart(*[Create(a) for a in web], lag_ratio=0.0),
                      LaggedStart(*[FadeIn(o, shift=UP * 0.3) for o in outs], lag_ratio=0.03), run_time=1.3)
            b.wait_until("sa", lead=0.25)
            title = txt("Self-attention", 64, INK, weight="BOLD").move_to(UP * 2.4)
            tg = glow(title, Q_C, layers=6, width=10, opacity=0.18)
            self.sfx("impact_soft", -8)
            self.play(FadeIn(title, scale=1.1), FadeIn(tg), run_time=0.6)
        self.wait(0.6)
        self.end_scene()
