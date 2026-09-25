import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import *  # noqa: E402,F401,F403

EN = ["The", "cat", "sat", "on", "the", "mat"]
DE = ["<s>", "Die", "Katze", "saß", "auf", "der", "Matte"]
FIG1_W, FIG1_H = 967, 1384
FIG1_BOXES = [  # (label, cx, cy, w, h) in figure pixels
    ("Input Embedding", 321, 1160, 218, 88), ("Output Embedding", 645, 1160, 218, 88),
    ("Positional Encoding", 270, 1062, 150, 76), ("Positional Encoding", 700, 1066, 150, 76),
    ("Multi-Head Attention", 321, 868, 218, 88), ("Add & Norm", 321, 793, 218, 40),
    ("Feed Forward", 321, 647, 218, 88), ("Add & Norm", 321, 572, 218, 40),
    ("Masked Multi-Head Attention", 645, 851, 218, 122), ("Multi-Head Attention", 645, 614, 218, 88),
    ("Feed Forward", 645, 426, 218, 88), ("Linear", 645, 256, 218, 40), ("Softmax", 645, 171, 218, 40),
]


class S11_Decoder(TScene):
    chapter = ("10", "The decoder")

    def construct(self):
        self.wait(0.2)
        self.chapter_intro()

        # ---- b1: translation set-up
        with self.vo("b1") as b:
            en = VGroup(*[Chip(w, size=24) for w in EN]).arrange(RIGHT, buff=0.1).move_to([-3.6, -2.7, 0])
            enc = Block("Encoder  × 6", INK2, width=5.2, height=1.1, size=30, fill_op=0.12).move_to([-3.6, -0.95, 0])
            dec = Block("Decoder  × 6", INK2, width=4.8, height=1.1, size=30, fill_op=0.12).move_to([3.5, -0.95, 0])
            title = VGroup(txt("English", 30, INK, weight="SEMIBOLD"), txt("→", 30, INK3),
                           txt("German", 30, INK, weight="SEMIBOLD")).arrange(RIGHT, buff=0.25).move_to(UP * 2.6)
            b.wait_until("en", lead=0.2)
            self.play(FadeIn(title, shift=DOWN * 0.1), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in en], lag_ratio=0.08),
                      run_time=0.8)
            b.wait_until("enc", lead=0.1)
            enc_out = VGroup(*[VGroup(VecCells(rvals(3, 800 + i), K_C, cell=0.15, gap=0.03),
                                      VecCells(rvals(3, 850 + i), V_C, cell=0.15, gap=0.03)).arrange(RIGHT, buff=0.04)
                               for i in range(6)])
            for c, o in zip(en, enc_out):
                o.move_to([c.get_center()[0], 0.55, 0])
            up = VGroup(*[Arrow([c.get_center()[0], -2.3, 0], [c.get_center()[0], -1.55, 0], buff=0, stroke_width=2,
                                max_tip_length_to_length_ratio=0.3).set_color(INK3) for c in en])
            self.sfx("whoosh_soft", -9)
            self.play(FadeIn(enc, shift=UP * 0.1), LaggedStart(*[GrowArrow(a) for a in up], lag_ratio=0.05), run_time=0.7)
            self.play(LaggedStart(*[FadeIn(o, shift=UP * 0.3) for o in enc_out], lag_ratio=0.08), run_time=0.9)
            ctx_l = txt("context-rich vectors", 22, INK2).next_to(enc_out, UP, buff=0.25)
            self.play(FadeIn(ctx_l), run_time=0.4)
            b.wait_until("dec", lead=0.2)
            self.play(FadeIn(dec, shift=UP * 0.1), run_time=0.5)
            ins = VGroup()
            outs = VGroup()
            xs_ = [1.7 + 1.2 * k for k in range(4)]
            for k in range(3):
                ic = Chip(DE[k], size=24).move_to([xs_[k], -2.7, 0])
                oc = Chip(DE[k + 1], size=24).move_to([xs_[k], 0.55, 0])
                ins.add(ic)
                outs.add(oc)
            self.play(FadeIn(ins[0], shift=UP * 0.2), run_time=0.3)
            per = max(0.5, (b.t0 + b.dur - self.now - 0.2) / 3)
            for k in range(3):
                self.sfx("pop_soft", -11)
                self.play(Indicate(dec.rect, color=Q_C, scale_factor=1.03), FadeIn(outs[k], shift=UP * 0.3), run_time=per * 0.55)
                if k < 2:
                    self.play(TransformFromCopy(outs[k], ins[k + 1], path_arc=-0.8), run_time=per * 0.45)
            grp1 = VGroup(title, en, enc, dec, enc_out, up, ctx_l, ins, outs)

        # ---- b2: masked self-attention
        with self.vo("b2") as b:
            self.play(FadeOut(grp1, shift=UP * 0.2), run_time=0.5)
            toks = DE[:6]
            n = 6
            M = np.random.default_rng(4).uniform(0.2, 1.0, (n, n))
            hm = Heatmap(np.full((n, n), 0.12), cell=0.62, gap=0.06, hi=Q_C).move_to([-1.2, -0.75, 0])
            rl = VGroup(*[txt(t, 24, INK2).next_to(hm.cell(i, 0), LEFT, buff=0.25) for i, t in enumerate(toks)])
            cl = VGroup(*[txt(t, 22, INK2).rotate(PI / 3).next_to(hm.cell(0, j), UP, buff=0.18) for j, t in enumerate(toks)])
            mtitle = txt("masked self-attention", 32, ATT_C, weight="SEMIBOLD").move_to([4.0, 2.4, 0])
            self.play(FadeIn(hm), FadeIn(rl), FadeIn(cl), FadeIn(mtitle), run_time=0.8)
            b.wait_until("mask", lead=0.2)
            r = 2
            ro = outline(hm.row(r), Q_C, buff=0.05, corner=0.06, width=3)
            seen = VGroup(*[hm.cell(r, j) for j in range(r + 1)])
            future = VGroup(*[hm.cell(r, j) for j in range(r + 1, n)])
            note1 = VGroup(txt("'Katze' may look at", 24, INK), txt("itself and earlier words only", 24, INK)).arrange(DOWN, buff=0.1)
            note1.move_to([4.0, 1.2, 0])
            self.play(Create(ro), seen.animate.set_fill(heat_color(0.85), 1), future.animate.set_fill(PANEL, 1),
                      FadeIn(note1), run_time=0.8)
            fut_l = txt("future", 22, BAD).next_to(future, DOWN, buff=0.15)
            self.play(FadeIn(fut_l), run_time=0.3)
            b.wait_until("inf", lead=0.2)
            upper = [(i, j) for i in range(n) for j in range(n) if j > i]
            infs = VGroup(*[MathTex(r"-\infty", font_size=22, color=BAD).move_to(hm.cell(i, j)) for i, j in upper])
            self.sfx("glitch", -12)
            self.play(*[hm.cell(i, j).animate.set_fill(lerp_color(PANEL, BAD, 0.25), 1) for i, j in upper],
                      LaggedStart(*[FadeIn(t, scale=0.6) for t in infs], lag_ratio=0.03), FadeOut(fut_l),
                      run_time=0.9)
            note2 = MathTex(r"\text{score} \leftarrow -\infty \;\;\text{before softmax}", font_size=34, color=BAD)
            note2.next_to(note1, DOWN, buff=0.5)
            self.play(FadeIn(note2), run_time=0.4)
            b.wait_until("zero", lead=0.2)
            W = np.zeros((n, n))
            for i in range(n):
                row = M[i, :i + 1]
                W[i, :i + 1] = softmax(row * 3)
            Wn = W / W.max(axis=1, keepdims=True)
            zeros = VGroup(*[MathTex("0", font_size=24, color=INK3).move_to(hm.cell(i, j)) for i, j in upper])
            note3 = MathTex(r"e^{-\infty} = 0 \;\Rightarrow\; \text{weight} = 0", font_size=34, color=INK)
            note3.next_to(note2, DOWN, buff=0.35)
            self.sfx("chime_soft", -10)
            self.play(*[hm.cell(i, j).animate.set_fill(PANEL, 1) for i, j in upper],
                      *[ReplacementTransform(a, z) for a, z in zip(infs, zeros)],
                      *[hm.cell(i, j).animate.set_fill(heat_color(0.1 + 0.85 * Wn[i, j]), 1) for i in range(n) for j in range(i + 1)],
                      FadeIn(note3), run_time=1.0)
            grp2 = VGroup(hm, rl, cl, mtitle, ro, note1, note2, note3, zeros)

        # ---- b3: encoder-decoder (cross) attention
        with self.vo("b3") as b:
            b.wait_until("cross", lead=0.0)
            self.play(FadeOut(grp2, shift=UP * 0.2), run_time=0.4)
            ctitle = txt("encoder-decoder attention", 32, ATT_C, weight="SEMIBOLD").move_to(UP * 3.05)
            en2 = VGroup(*[Chip(w, size=26, min_width=1.1) for w in EN]).arrange(RIGHT, buff=0.35).move_to([0, 0.95, 0])
            kvs = VGroup(*[VGroup(VecCells(rvals(3, 800 + i), K_C, cell=0.17, gap=0.03),
                                  VecCells(rvals(3, 850 + i), V_C, cell=0.17, gap=0.03)).arrange(RIGHT, buff=0.05)
                           .next_to(c, UP, buff=0.25) for i, c in enumerate(en2)])
            enc_tag = txt("English sentence (encoder side)", 22, INK3).next_to(en2, DOWN, buff=0.25)
            de_row = VGroup(Chip("<s>", size=26), Chip("Die", size=26), Chip("?", size=26, color=Q_C, stroke=Q_C))
            de_row.arrange(RIGHT, buff=0.3).move_to([0, -2.8, 0])
            dec_tag = txt("German so far (decoder)", 22, INK3).next_to(de_row, LEFT, buff=0.5)
            self.play(FadeIn(ctitle, shift=DOWN * 0.1), FadeIn(en2), FadeIn(kvs), FadeIn(de_row), FadeIn(enc_tag),
                      FadeIn(dec_tag), run_time=0.8)
            b.wait_until("dq", lead=0.2)
            qv = VecCells(rvals(4, 901), Q_C, cell=0.22, gap=0.04).next_to(de_row[1], UP, buff=0.45)
            qb = bubble("next word: what in the English matters?", Q_C, 22)
            qb = VGroup(qb[0], qb[3]).next_to(qv, RIGHT, buff=0.25)
            if qb.get_right()[0] > 6.9:
                qb.shift(LEFT * (qb.get_right()[0] - 6.9))
            self.sfx("pop", -9)
            self.play(FadeIn(qv, shift=UP * 0.2), run_time=0.5)
            self.play(FadeIn(qb, shift=RIGHT * 0.1), run_time=0.5)
            ql = txt("query from the decoder", 22, Q_C).next_to(qv, LEFT, buff=0.3)
            self.play(FadeIn(ql), run_time=0.4)
            b.wait_until("ek", lead=0.2)
            kl = txt("keys & values from the encoder", 22, INK2).next_to(kvs, UP, buff=0.3)
            self.play(LaggedStart(*[Indicate(k, scale_factor=1.12, color=None) for k in kvs], lag_ratio=0.08), FadeIn(kl),
                      run_time=0.9)
            b.wait_until("ans", lead=0.2)
            w = np.array([0.04, 0.78, 0.06, 0.03, 0.03, 0.06])
            lines = VGroup(*[Line(qv.get_top(), kv[0].get_bottom() + DOWN * 0.45, buff=0.05)
                             .set_stroke(Q_C, 1 + 7 * wi, opacity=0.25 + 0.75 * wi) for kv, wi in zip(kvs, w)])
            self.sfx("whoosh_soft", -9)
            self.play(FadeOut(qb), LaggedStart(*[Create(l) for l in lines], lag_ratio=0.05), run_time=0.7)
            flows = VGroup(*[kv[1].copy().set_opacity(0.2 + 0.8 * wi) for kv, wi in zip(kvs, w)])
            katze = Chip("Katze", size=26, color=INK).move_to(de_row[2])
            self.play(*[f.animate.move_to(qv).scale(0.5).set_opacity(0) for f in flows], en2[1].box.animate.set_stroke(K_C, 2.8),
                      run_time=0.8)
            self.remove(flows)
            self.sfx("ding", -8)
            self.play(ReplacementTransform(de_row[2], katze), run_time=0.5)
            grp3 = VGroup(ctitle, en2, kvs, enc_tag, de_row[:2], katze, dec_tag, qv, ql, kl, lines)
            b.wait_until(None, lead=0.4)
            self.play(FadeOut(grp3, shift=UP * 0.2), run_time=0.35)

        # ---- b4: the decoder layer
        with self.vo("b4") as b:
            dx = -3.3
            m1 = Block("Masked Multi-Head Attention", ATT_C, width=4.2, height=0.62, size=22)
            a1 = Block("Add & Norm", NORM_C, width=4.2, height=0.34, size=17)
            m2 = Block("Multi-Head Attention", ATT_C, width=4.2, height=0.62, size=22)
            a2 = Block("Add & Norm", NORM_C, width=4.2, height=0.34, size=17)
            ff = Block("Feed Forward", FFN_C, width=4.2, height=0.62, size=22)
            a3 = Block("Add & Norm", NORM_C, width=4.2, height=0.34, size=17)
            stack = VGroup(m1, a1, m2, a2, ff, a3).arrange(UP, buff=0.14).move_to([dx, -0.35, 0])
            for blk in (m1, m2, a1, a2, a3):
                blk.rect.set_fill(opacity=0.22)
            from_enc = Arrow(m2.get_left() + LEFT * 1.3, m2.get_left(), buff=0.05, stroke_width=3).set_color(K_C)
            fe_l = txt("from encoder", 18, K_C).next_to(from_enc, UP, buff=0.05)
            self.play(FadeIn(m1, shift=UP * 0.1), FadeIn(m2, shift=UP * 0.1), GrowArrow(from_enc), FadeIn(fe_l), run_time=0.3)
            self.play(FadeIn(ff, shift=UP * 0.1), run_time=0.4)
            b.wait_until("an", lead=0.2)
            self.sfx("click", -11)
            self.play(LaggedStart(FadeIn(a1), FadeIn(a2), FadeIn(a3), lag_ratio=0.2), run_time=0.7)
            b.wait_until("six", lead=0.2)
            br = Brace(stack, RIGHT, color=INK3)
            six = MathTex(r"\times 6", font_size=50, color=INK).next_to(br, RIGHT, buff=0.15)
            self.sfx("thud", -9)
            self.play(GrowFromCenter(br), FadeIn(six), run_time=0.5)

        # ---- b5: output probabilities
        with self.vo("b5") as b:
            lin = Block("Linear", LIN_C, width=2.4, height=0.55, size=22).move_to([dx, 2.6, 0])
            smx = Block("Softmax", SMX_C, width=2.4, height=0.55, size=22).move_to([0.3, 2.6, 0])
            ar1 = Arrow(stack.get_top(), lin.get_bottom(), buff=0.08, stroke_width=3).set_color(INK3)
            ar2 = Arrow(lin.get_right(), smx.get_left(), buff=0.08, stroke_width=3).set_color(INK3)
            b.wait_until("lin", lead=0.05)
            self.play(GrowArrow(ar1), FadeIn(lin), run_time=0.45)
            self.play(GrowArrow(ar2), FadeIn(smx), run_time=0.45)
            cands = [("Katze", 0.74), ("Kater", 0.07), ("Tier", 0.05), ("Hund", 0.03), ("Maus", 0.02)]
            bars = VGroup()
            for k, (word, p) in enumerate(cands):
                lab = txt(word, 24, INK).move_to([2.5, 1.2 - 0.62 * k, 0], aligned_edge=RIGHT)
                bar = Rectangle(width=max(0.03, 3.6 * p), height=0.38).set_fill(Q_C, 0.35 + 0.6 * p).set_stroke(width=0)
                bar.next_to(lab, RIGHT, buff=0.2)
                pct = txt(f"{100 * p:.0f}%", 20, INK2).next_to(bar, RIGHT, buff=0.12)
                bars.add(VGroup(lab, bar, pct))
            dots = txt("⋮", 30, INK3).next_to(bars, DOWN, buff=0.12).align_to(bars[0][1], LEFT)
            ar3 = Arrow(smx.get_bottom(), bars.get_top() + UP * 0.05 + LEFT * 0.3, buff=0.08, stroke_width=3).set_color(INK3)
            self.play(GrowArrow(ar3), LaggedStart(*[FadeIn(bb, shift=RIGHT * 0.2) for bb in bars], lag_ratio=0.1),
                      FadeIn(dots), run_time=1.0)
            b.wait_until("vocab", lead=0.2)
            voc = txt("over ≈ 37,000 tokens", 24, INK2).next_to(dots, DOWN, buff=0.15).align_to(bars[0][1], LEFT)
            self.play(FadeIn(voc), run_time=0.4)
            b.wait_until("pick", lead=0.1)
            pg = glow(bars[0][1], Q_C, layers=5, width=14, opacity=0.35)
            self.sfx("ding", -8)
            self.play(FadeIn(pg), Indicate(bars[0][0], color=Q_C, scale_factor=1.2), run_time=0.6)
            b.wait_until("app", lead=0.1)
            loop_chip = Chip("Katze", size=24).move_to([dx, -3.35, 0])
            inp_l = txt("appended to the decoder's input", 22, INK2).next_to(loop_chip, RIGHT, buff=0.4)
            self.sfx("swish", -9)
            self.play(TransformFromCopy(bars[0][0], loop_chip, path_arc=-1.0), run_time=0.8)
            self.play(FadeIn(inp_l), run_time=0.4)
            grp5 = VGroup(stack, from_enc, fe_l, br, six, lin, smx, ar1, ar2, ar3, bars, dots, voc, pg, loop_chip, inp_l)

        # ---- b6: parallel training with the mask
        with self.vo("b6") as b:
            self.play(FadeOut(grp5, shift=UP * 0.2), run_time=0.4)
            ins = VGroup(*[Chip(t, size=24, min_width=1.25) for t in DE]).arrange(RIGHT, buff=0.16).move_to([0, -2.3, 0])
            outs = VGroup(*[Chip(t, size=24, min_width=1.25, color=Q_C, stroke=Q_C) for t in DE[1:] + ["</s>"]])
            for o, i_ in zip(outs, ins):
                o.move_to([i_.get_center()[0], 1.6, 0])
            dblk = Block("Decoder (masked)", INK2, width=ins.width + 0.4, height=1.1, size=28, fill_op=0.12).move_to([0, -0.35, 0])
            in_l = txt("the correct German, shifted right", 22, INK3).next_to(ins, DOWN, buff=0.2)
            out_l = txt("targets: each next word", 22, Q_C).next_to(outs, UP, buff=0.2)
            b.wait_until("train", lead=0.1)
            self.play(FadeIn(ins, shift=UP * 0.1), FadeIn(in_l), FadeIn(dblk), run_time=0.7)
            b.wait_until("mask2", lead=0.2)
            self.sfx("power_up", -10)
            self.play(LaggedStart(*[FadeIn(o, shift=UP * 0.2) for o in outs], lag_ratio=0.0), FadeIn(out_l), run_time=0.7)
            all_l = txt("every position predicted at once", 28, INK, weight="SEMIBOLD").move_to(UP * 2.75)
            self.play(FadeIn(all_l, shift=DOWN * 0.1), run_time=0.5)
            b.wait_until("fast", lead=0.2)
            fast = txt("→ far faster to train than a recurrent network", 26, GOOD).next_to(in_l, DOWN, buff=0.35)
            self.play(FadeIn(fast, shift=UP * 0.1), run_time=0.5)
            grp6 = VGroup(ins, outs, dblk, in_l, out_l, all_l, fast)

        # ---- b7: the paper's Figure 1
        with self.vo("b7") as b:
            self.play(FadeOut(grp6), run_time=0.3)
            card = paper_card(os.path.join(PAPER, "fig1.png"), height=7.0, pad=0.12).move_to(DOWN * 0.15)
            img = card[2]
            cap = txt("Vaswani et al. 2017, Figure 1", 20, INK3).next_to(card, RIGHT, buff=0.3).align_to(card, DOWN)
            self.sfx("whoosh_soft", -8)
            self.play(FadeIn(card, scale=0.95), FadeIn(cap), run_time=0.7)
            b.wait_until("every", lead=0.1)

            def fbox(cx, cy, w, h, col):
                p = img.get_corner(UL) + RIGHT * (cx / FIG1_W * img.width) + DOWN * (cy / FIG1_H * img.height)
                r = RoundedRectangle(corner_radius=0.05, width=w / FIG1_W * img.width + 0.08,
                                     height=h / FIG1_H * img.height + 0.08).move_to(p)
                return r.set_stroke(col, 4).set_fill(opacity=0)

            items = []
            for k, (label, cx, cy, w_, h_) in enumerate(FIG1_BOXES):
                r = fbox(cx, cy, w_, h_, Q_C)
                items.append((0.28 * k, Succession(Create(r, run_time=0.2), FadeOut(r, run_time=0.5)), 0.7, "tick", -13))
            b.schedule(items)
        self.wait(1.4)
        self.end_scene()
