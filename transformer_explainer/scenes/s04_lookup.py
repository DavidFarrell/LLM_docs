import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import *  # noqa: E402,F401,F403


class S04_Lookup(TScene):
    chapter = ("03", "Query, key, value")

    def construct(self):
        self.wait(0.2)
        self.chapter_intro()

        # ---- b1
        with self.vo("b1") as b:
            b.wait_until("qkv", lead=0.2)
            words = VGroup(txt("Query", 84, Q_C, weight="BOLD"), txt("Key", 84, K_C, weight="BOLD"),
                           txt("Value", 84, V_C, weight="BOLD")).arrange(RIGHT, buff=0.8)
            b.schedule([(0.0, FadeIn(words[0], shift=UP * 0.3), 0.45, "pop", -8),
                        (0.35, FadeIn(words[1], shift=UP * 0.3), 0.45, "pop", -8),
                        (0.7, FadeIn(words[2], shift=UP * 0.3), 0.45, "pop", -8)])
            b.wait_until("lookup", lead=0.3)
            sub = txt("…all borrowed from looking something up", 32, INK2).next_to(words, DOWN, buff=0.6)
            self.play(FadeIn(sub, shift=UP * 0.1), run_time=0.6)

        # ---- b2: a dictionary lookup
        with self.vo("b2") as b:
            self.play(FadeOut(words, shift=UP * 0.3), FadeOut(sub), run_time=0.45)
            rows = [("Japan", "Tokyo"), ("Kenya", "Nairobi"), ("France", "Paris"), ("Peru", "Lima")]
            head = mono("capital = {", 30, INK2)
            lines = VGroup()
            for k, v in rows:
                kt = mono(f'"{k}"', 30, INK)
                col = mono(":", 30, INK3)
                vt = mono(f'"{v}"', 30, INK)
                ln = VGroup(kt, col, vt)
                lines.add(ln)
            tail = mono("}", 30, INK2)
            # align columns
            kx = -4.6
            for i, ln in enumerate(lines):
                ln[0].move_to([kx, 1.2 - i * 0.75, 0], aligned_edge=LEFT)
                ln[1].move_to([kx + 2.15, 1.2 - i * 0.75, 0])
                ln[2].move_to([kx + 2.55, 1.2 - i * 0.75, 0], aligned_edge=LEFT)
            head.move_to([kx - 0.45, 2.0, 0], aligned_edge=LEFT)
            tail.move_to([kx - 0.45, 1.2 - 4 * 0.75 + 0.05, 0], aligned_edge=LEFT)
            panel = RoundedRectangle(corner_radius=0.2, width=6.6, height=4.6).set_fill(PANEL, 0.95)
            panel.set_stroke(EDGE, 1.5).move_to([kx + 2.2, 0.35, 0])
            dy = -0.45
            VGroup(panel, head, lines, tail).shift(UP * dy)
            self.play(FadeIn(panel), run_time=0.3)
            items = [(0.0, FadeIn(head), 0.25, "type", -14)]
            for i, ln in enumerate(lines):
                items.append((0.18 + 0.2 * i, FadeIn(ln, shift=RIGHT * 0.1), 0.25, "type", -14))
            items.append((1.1, FadeIn(tail), 0.2))
            b.schedule(items)
            b.wait_until("key", lead=0.15)
            keys = VGroup(*[ln[0] for ln in lines])
            vals = VGroup(*[ln[2] for ln in lines])
            klab = pill("keys", K_C, 22).next_to(panel, UP, buff=0.15).align_to(keys, LEFT)
            self.play(keys.animate.set_color(K_C), FadeIn(klab, shift=DOWN * 0.1), run_time=0.5)
            b.wait_until("val", lead=0.15)
            vlab = pill("values", V_C, 22).next_to(panel, UP, buff=0.15).align_to(vals, LEFT)
            self.play(vals.animate.set_color(V_C), FadeIn(vlab, shift=DOWN * 0.1), run_time=0.5)
            b.wait_until("q", lead=0.1)
            qchip = Chip('"France"', size=32, font=MONO, color=Q_C, stroke=Q_C).move_to(RIGHT * 3.6 + UP * 1.6)
            qlab = pill("query", Q_C, 22).next_to(qchip, UP, buff=0.25)
            code = mono('capital["France"]', 26, INK2).next_to(qchip, DOWN, buff=0.35)
            self.sfx("pop", -9)
            self.play(FadeIn(qchip, shift=LEFT * 0.4), FadeIn(code), run_time=0.5)
            b.wait_until("query", lead=0.1)
            self.play(FadeIn(qlab, shift=DOWN * 0.1), Indicate(qchip, color=Q_C, scale_factor=1.08), run_time=0.6)
            b.wait_until("cmp", lead=0.1)
            marks = VGroup()
            per = max(0.3, (b.t("match") - self.now) / 3)
            for i in range(3):
                target = lines[i][0]
                line = DashedLine(qchip.get_left(), target.get_right() + RIGHT * 0.1, dash_length=0.08)
                line.set_stroke(Q_C, 2, opacity=0.8)
                ok = i == 2
                sym = txt("✓" if ok else "✗", 30, GOOD if ok else BAD, weight="BOLD")
                sym.next_to(lines[i][2], RIGHT, buff=0.35)
                if ok:
                    break
                self.sfx("tick", -12)
                self.play(Create(line), run_time=per * 0.45)
                self.play(FadeIn(sym, scale=0.6), FadeOut(line), run_time=per * 0.55)
                marks.add(sym)
            b.wait_until("match", lead=0.15)
            line = DashedLine(qchip.get_left(), lines[2][0].get_right() + RIGHT * 0.1, dash_length=0.08)
            line.set_stroke(Q_C, 2.5)
            hl = outline(lines[2], Q_C, buff=0.12, corner=0.1, width=2.5)
            self.sfx("ding", -8)
            self.play(Create(line), Create(hl), FadeIn(sym, scale=0.6), run_time=0.5)
            marks.add(sym)
            b.wait_until("ret", lead=0.1)
            result = Chip('"Paris"', size=32, font=MONO, color=V_C, stroke=V_C).move_to(RIGHT * 3.6 + DOWN * 1.6)
            rlab = txt("returned", 22, INK3).next_to(result, DOWN, buff=0.2)
            self.sfx("whoosh_soft", -8)
            self.play(TransformFromCopy(lines[2][2], result, path_arc=-0.6), FadeOut(line), run_time=0.8)
            self.play(FadeIn(rlab), run_time=0.3)

        # ---- b3: key and value are different things
        with self.vo("b3") as b:
            b.wait_until("k", lead=0.2)
            k_note = txt("how the entry is found", 24, K_C).next_to(panel, DOWN, buff=0.35).align_to(panel, LEFT)
            kbox = outline(lines[2][0], K_C, buff=0.08, corner=0.08, width=2.5)
            self.play(Create(kbox), FadeIn(k_note, shift=UP * 0.1), run_time=0.6)
            b.wait_until("v", lead=0.2)
            vbox = outline(lines[2][2], V_C, buff=0.08, corner=0.08, width=2.5)
            v_note = txt("what the entry gives you", 24, V_C).next_to(k_note, DOWN, buff=0.15).align_to(k_note, LEFT)
            self.play(Create(vbox), FadeIn(v_note, shift=UP * 0.1), run_time=0.6)
            b.wait_until("sep", lead=0.2)
            trio = VGroup(pill("query", Q_C, 26), pill("key", K_C, 26), pill("value", V_C, 26))
            trio.arrange(RIGHT, buff=0.5).move_to(RIGHT * 3.6 + UP * 0.05)
            self.play(FadeOut(code), run_time=0.3)
            arr1 = Arrow(trio[0].get_right(), trio[1].get_left(), buff=0.08, stroke_width=3).set_color(INK3)
            arr2 = Arrow(trio[1].get_right(), trio[2].get_left(), buff=0.08, stroke_width=3).set_color(INK3)
            three = txt("three roles", 22, INK2).next_to(trio, DOWN, buff=0.25)
            self.sfx("pop", -9)
            self.play(LaggedStart(FadeIn(trio[0]), GrowArrow(arr1), FadeIn(trio[1]), GrowArrow(arr2),
                                  FadeIn(trio[2]), lag_ratio=0.25), FadeIn(three), run_time=1.1)

        # ---- b4: make it soft
        with self.vo("b4") as b:
            everything = VGroup(panel, head, lines, tail, klab, vlab, qchip, qlab, marks, hl, result, rlab,
                                kbox, vbox, k_note, v_note, trio, arr1, arr2, three)
            hard_t = txt("hard lookup:  one match, one value", 28, INK2).move_to(UP * 2.7)
            self.play(FadeOut(everything, shift=DOWN * 0.3), FadeIn(hard_t), run_time=0.6)
            n = 4
            xs = [-1.6 + 1.9 * i for i in range(n)]
            bars_base = -0.2
            hard_w = [0, 0, 1, 0]
            bars = VGroup(*[Rectangle(width=0.8, height=max(0.02, 2.2 * w)).set_fill(Q_C, 0.85).set_stroke(width=0)
                            .move_to([x, bars_base, 0], aligned_edge=DOWN) for x, w in zip(xs, hard_w)])
            axis = Line([xs[0] - 0.8, bars_base, 0], [xs[-1] + 0.8, bars_base, 0]).set_stroke(INK3, 2)
            klbls = VGroup(*[txt(k, 24, K_C).next_to([x, bars_base, 0], DOWN, buff=0.25)
                             for (k, _), x in zip(rows, xs)])
            self.play(Create(axis), FadeIn(klbls), LaggedStart(*[GrowFromEdge(bb, DOWN) for bb in bars], lag_ratio=0.1),
                      run_time=0.8)
            b.wait_until("soft", lead=0.3)
            soft_t = txt("soft lookup:  score every key, blend every value", 28, INK).move_to(UP * 2.7)
            self.sfx("whoosh_soft", -9)
            self.play(FadeOut(VGroup(bars, axis, klbls)), ReplacementTransform(hard_t, soft_t), run_time=0.6)
            # query vector + key/value pairs
            qv = VecCells([0.8, -0.3, 0.6, 0.9], Q_C, cell=0.3, gap=0.05).move_to(LEFT * 5.2 + DOWN * 0.3)
            ql = MathTex(r"\mathbf{q}", font_size=44, color=Q_C).next_to(qv, UP, buff=0.2)
            keys_v, vals_v = VGroup(), VGroup()
            kx0 = -2.4
            kvals = [[0.7, -0.2, 0.5, 0.8], [-0.5, 0.6, -0.2, 0.1], [0.1, 0.9, -0.8, -0.4], [0.5, 0.1, 0.2, 0.6]]
            vv = [[0.9, -0.6, 0.3, 0.7], [-0.2, 0.8, 0.5, -0.9], [0.6, 0.2, -0.7, 0.1], [-0.8, 0.4, 0.9, 0.3]]
            for i in range(n):
                k = VecCells(kvals[i], K_C, cell=0.26, gap=0.045).move_to([kx0 + 1.45 * i, 0.55, 0])
                v = VecCells(vv[i], V_C, cell=0.26, gap=0.045).move_to([kx0 + 1.45 * i, -1.3, 0])
                keys_v.add(k)
                vals_v.add(v)
            kl = MathTex(r"\mathbf{k}_i", font_size=40, color=K_C).next_to(keys_v, LEFT, buff=0.35)
            vl = MathTex(r"\mathbf{v}_i", font_size=40, color=V_C).next_to(vals_v, LEFT, buff=0.35)
            self.play(FadeIn(qv), FadeIn(ql), LaggedStart(*[FadeIn(k, shift=UP * 0.1) for k in keys_v], lag_ratio=0.1),
                      LaggedStart(*[FadeIn(v, shift=UP * 0.1) for v in vals_v], lag_ratio=0.1),
                      FadeIn(kl), FadeIn(vl), run_time=1.0)
            b.wait_until("score", lead=0.2)
            scores = [2.1, 0.4, -0.6, 1.3]
            links = VGroup(*[Line(qv.get_right(), k.get_left(), buff=0.1).set_stroke(Q_C, 2, opacity=0.6)
                             for k in keys_v])
            sc_t = VGroup(*[MathTex(f"{s:+.1f}", font_size=34, color=Q_C).next_to(k, UP, buff=0.25)
                            for s, k in zip(scores, keys_v)])
            sclab = txt("score = q · k", 22, INK2).next_to(sc_t, UP, buff=0.3)
            self.sfx("blip", -10)
            self.play(LaggedStart(*[Create(l) for l in links], lag_ratio=0.15), run_time=0.7)
            self.play(LaggedStart(*[FadeIn(s, shift=UP * 0.1) for s in sc_t], lag_ratio=0.15), FadeIn(sclab),
                      run_time=0.8)
            b.wait_until("w", lead=0.2)
            w = softmax(scores)
            w_t = VGroup(*[MathTex(f"{x:.2f}", font_size=34, color=INK).move_to(s) for x, s in zip(w, sc_t)])
            wlab = txt("weights (softmax): sum to 1", 22, INK2).move_to(sclab)
            self.sfx("shimmer", -11)
            self.play(*[ReplacementTransform(a, c) for a, c in zip(sc_t, w_t)], ReplacementTransform(sclab, wlab),
                      *[k.animate.set_opacity(0.3 + 0.7 * x / w.max()) for k, x in zip(keys_v, w)], run_time=0.8)
            b.wait_until("blend", lead=0.2)
            out = VecCells(np.clip(np.array(vv).T @ w, -1, 1), V_C, cell=0.3, gap=0.05).move_to(RIGHT * 5.0 + DOWN * 1.3)
            ol = txt("output", 24, V_C, weight="SEMIBOLD").next_to(out, UP, buff=0.25)
            osum = MathTex(r"\sum_i w_i\,\mathbf{v}_i", font_size=40, color=V_C).next_to(out, DOWN, buff=0.3)
            copies = VGroup(*[v.copy().set_opacity(0.25 + 0.75 * x / w.max()) for v, x in zip(vals_v, w)])
            self.play(*[vv_.animate.set_opacity(0.25 + 0.75 * x / w.max()) for vv_, x in zip(vals_v, w)], run_time=0.4)
            self.sfx("whoosh_soft", -9)
            self.play(*[Transform(c, out.copy().set_opacity(0.0)) for c in copies], FadeIn(out, scale=0.9),
                      run_time=0.9)
            self.remove(copies)
            self.sfx("chime_soft", -10)
            self.play(FadeIn(ol), FadeIn(osum), run_time=0.5)
            soft_group = VGroup(soft_t, qv, ql, keys_v, vals_v, kl, vl, links, w_t, wlab, out, ol, osum)

        # ---- b5: the paper's definition
        with self.vo("b5") as b:
            self.play(FadeOut(soft_group, shift=UP * 0.2), run_time=0.5)
            q_lines = [
                "“An attention function can be described as mapping a query",
                "and a set of key-value pairs to an output, where the query, keys,",
                "values, and output are all vectors. The output is computed as a",
                "weighted sum of the values, where the weight assigned to each",
                "value is computed by a compatibility function of the query",
                "with the corresponding key.”",
            ]
            import re as _re

            def t2c_words(line):
                out = {}
                for m in _re.finditer(r"\b(query|keys?|values?)\b", line):
                    w = m.group(1)
                    c = Q_C if w.startswith("q") else (K_C if w.startswith("k") else V_C)
                    out[f"[{m.start()}:{m.end()}]"] = c
                return out

            quote = VGroup(*[Text(l, font=FONT, font_size=32, color=INK, weight="NORMAL", slant=ITALIC,
                                  t2c=t2c_words(l)) for l in q_lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
            if quote.width > 11.4:
                quote.scale_to_fit_width(11.4)
            quote.move_to(UP * 0.3 + RIGHT * 0.2)
            src = txt("Vaswani et al., 2017  ·  Section 3.2", 22, INK3).next_to(quote, DOWN, buff=0.5).align_to(quote, RIGHT)
            bar = Line(quote.get_corner(UL) + LEFT * 0.3, quote.get_corner(DL) + LEFT * 0.3).set_stroke(Q_C, 4)
            b.wait_until("quote", lead=0.5)
            self.play(Create(bar), LaggedStart(*[FadeIn(l, shift=UP * 0.08) for l in quote], lag_ratio=0.18),
                      run_time=1.6)
            self.play(FadeIn(src), run_time=0.4)
            b.wait_until("ws", lead=0.1)
            u1 = Underline(VGroup(quote[3][0:16]), buff=0.05).set_stroke(V_C, 3)
            self.play(Create(u1), run_time=0.5)
            b.wait_until("compat", lead=0.1)
            u2 = Underline(VGroup(quote[4][30:]), buff=0.05).set_stroke(Q_C, 3)
            u3 = Underline(VGroup(quote[5][:-2]), buff=0.05).set_stroke(Q_C, 3)
            self.play(Create(u2), run_time=0.45)
            self.play(Create(u3), run_time=0.35)
            quote_group = VGroup(quote, src, bar, u1, u2, u3)

        # ---- b6: why soft? differentiable
        with self.vo("b6") as b:
            self.play(FadeOut(quote_group, shift=UP * 0.2), run_time=0.5)
            ax1 = Axes(x_range=[-1, 1, 1], y_range=[0, 1, 1], x_length=4.2, y_length=2.4,
                       axis_config={"stroke_color": INK3, "include_ticks": False, "stroke_width": 2})
            ax2 = ax1.copy()
            ax1.move_to(LEFT * 3.4 + DOWN * 0.3)
            ax2.move_to(RIGHT * 3.4 + DOWN * 0.3)
            soft_curve = ax1.plot(lambda x: 1 / (1 + np.exp(-5 * x)), color=GOOD, stroke_width=5)
            hard_curve = VGroup(ax2.plot(lambda x: 0.0, x_range=[-1, 0], color=BAD, stroke_width=5),
                                ax2.plot(lambda x: 1.0, x_range=[0, 1], color=BAD, stroke_width=5),
                                DashedLine(ax2.c2p(0, 0), ax2.c2p(0, 1)).set_stroke(BAD, 2, opacity=0.5))
            t1 = txt("soft: weights shift smoothly", 26, GOOD, weight="SEMIBOLD").next_to(ax1, UP, buff=0.4)
            t2 = txt("hard: all or nothing", 26, BAD, weight="SEMIBOLD").next_to(ax2, UP, buff=0.4)
            xl1 = txt("query nudged  →", 20, INK3).next_to(ax1, DOWN, buff=0.2)
            xl2 = txt("query nudged  →", 20, INK3).next_to(ax2, DOWN, buff=0.2)
            yl1 = txt("weight", 20, INK3).rotate(PI / 2).next_to(ax1, LEFT, buff=0.15)
            yl2 = txt("weight", 20, INK3).rotate(PI / 2).next_to(ax2, LEFT, buff=0.15)
            b.wait_until("diff", lead=0.3)
            self.play(Create(ax1), FadeIn(xl1), FadeIn(yl1), FadeIn(t1), run_time=0.7)
            self.play(Create(soft_curve), run_time=0.8)
            b.wait_until("nudge", lead=0.2)
            x = ValueTracker(-0.6)
            dot = always_redraw(lambda: Dot(ax1.c2p(x.get_value(), 1 / (1 + np.exp(-5 * x.get_value()))),
                                            radius=0.1, color=Q_C))
            tang = always_redraw(lambda: TangentLine(soft_curve, alpha=(x.get_value() + 1) / 2, length=1.6)
                                 .set_stroke(Q_C, 3))
            self.add(tang, dot)
            self.sfx("tone_up", -13)
            self.play(x.animate.set_value(0.35), run_time=1.6, rate_func=there_and_back_with_pause)
            self.play(x.animate.set_value(0.1), run_time=0.8)
            b.wait_until("learn", lead=0.2)
            grad = txt("slope ≠ 0  →  gradient descent can learn", 24, INK).next_to(ax1, DOWN, buff=0.75)
            self.play(FadeIn(grad, shift=UP * 0.1), run_time=0.5)
            b.wait_until("hard", lead=0.3)
            self.play(Create(ax2), FadeIn(xl2), FadeIn(yl2), FadeIn(t2), run_time=0.6)
            self.sfx("click", -10)
            self.play(Create(hard_curve), run_time=0.7)
            flat = txt("slope = 0 almost everywhere", 24, INK2).next_to(ax2, DOWN, buff=0.75)
            self.play(FadeIn(flat, shift=UP * 0.1), run_time=0.5)
        self.wait(0.3)
        self.end_scene()
