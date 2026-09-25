import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import *  # noqa: E402,F401,F403

TOK = ["the", "animal", "was", "tired"]
LX = [-5.75, -4.4, -3.05, -1.7]
BX, BW = -3.725, 5.3      # block centre x and width
Y_CHIP, Y_X, Y_MHA, Y_AN1, Y_FFN, Y_AN2, Y_OUT = -3.35, -2.55, -1.5, -0.42, 0.62, 1.66, 2.35
RP = 3.6                  # centre of the right-hand explanation panel


def hvec(vals, color, cell=0.17):
    return VecCells(vals, color, cell=cell, gap=0.03, direction=RIGHT)


def nn_diagram(n_in=6, n_hid=12, n_out=6, x0=RP - 2.0, x1=RP, x2=RP + 2.0, h=3.2, y=0.0):
    def col(n, x, spread):
        ys = np.linspace(spread / 2, -spread / 2, n)
        return VGroup(*[Circle(radius=0.1).set_fill(PANEL2, 1).set_stroke(INK3, 1.5).move_to([x, y + yy, 0])
                        for yy in ys])
    a = col(n_in, x0, h * 0.62)
    b = col(n_hid, x1, h)
    c = col(n_out, x2, h * 0.62)
    e1 = VGroup(*[Line(p.get_center(), q.get_center(), buff=0.1).set_stroke(INK3, 0.8, opacity=0.35)
                  for p in a for q in b])
    e2 = VGroup(*[Line(p.get_center(), q.get_center(), buff=0.1).set_stroke(INK3, 0.8, opacity=0.35)
                  for p in b for q in c])
    return VGroup(e1, e2, a, b, c)


class S10_EncoderLayer(TScene):
    chapter = ("09", "Into the network")

    def construct(self):
        self.wait(0.2)
        self.chapter_intro()

        chips = VGroup(*[Chip(t, size=22, min_width=1.1).move_to([x, Y_CHIP, 0]) for t, x in zip(TOK, LX)])
        lanes = VGroup(*[Line([x, Y_CHIP + 0.35, 0], [x, Y_OUT + 0.45, 0]).set_stroke(INK3, 1.5, opacity=0.45)
                         for x in LX])
        xs = VGroup(*[hvec(rvals(5, 500 + i), X_C).move_to([x, Y_X, 0]) for i, x in enumerate(LX)])
        mha = Block("Multi-Head Attention", ATT_C, width=BW, height=0.74, size=26).move_to([BX, Y_MHA, 0])
        an1 = Block("Add & Norm", NORM_C, width=BW, height=0.42, size=20).move_to([BX, Y_AN1, 0])
        ffns = VGroup(*[Block("Feed\nForward", FFN_C, width=1.1, height=0.66, size=16).move_to([x, Y_FFN, 0])
                        for x in LX])
        an2 = Block("Add & Norm", NORM_C, width=BW, height=0.42, size=20).move_to([BX, Y_AN2, 0])
        for m in (mha, an1, an2):
            m.rect.set_fill(opacity=0.22)

        def res_path(y0, y1):
            p = VMobject().set_points_as_corners([[BX + BW / 2 - 0.05, y0, 0], [BX + BW / 2 + 0.4, y0, 0], [BX + BW / 2 + 0.4, y1, 0],
                                                  [BX + BW / 2 + 0.02, y1, 0]])
            p.set_stroke(NORM_C, 2.5)
            tip = ArrowTriangleFilledTip(color=NORM_C).scale(0.6).rotate(PI).move_to([BX + BW / 2 + 0.12, y1, 0])
            return VGroup(p, tip)

        res1 = res_path(Y_MHA - 0.62, Y_AN1)
        res2 = res_path(Y_AN1 + 0.4, Y_AN2)

        # ---- b1: the question
        with self.vo("b1") as b:
            b.wait_until("how", lead=0.3)
            q = txt("How does attention fit into the network?", 40, INK, weight="SEMIBOLD")
            self.play(FadeIn(q, shift=UP * 0.2), run_time=0.7)
            b.wait_until("build", lead=0.3)
            layer_box = DashedVMobject(RoundedRectangle(corner_radius=0.25, width=BW + 1.25, height=(Y_OUT + 0.35) - (Y_MHA - 0.8)),
                                       num_dashes=70).set_stroke(INK3, 1.5)
            layer_box.move_to([BX + 0.3, ((Y_OUT + 0.35) + (Y_MHA - 0.8)) / 2, 0])
            lb_lab = txt("one encoder layer", 22, INK3).next_to(layer_box, UP, buff=0.1).align_to(layer_box, LEFT)
            self.play(FadeOut(q, shift=UP * 0.3), Create(layer_box), FadeIn(lb_lab), run_time=0.9)

        # ---- b2: lanes and attention
        with self.vo("b2") as b:
            b.wait_until("lanes", lead=0.1)
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in chips], lag_ratio=0.1),
                      LaggedStart(*[Create(l) for l in lanes], lag_ratio=0.1), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(x_, shift=UP * 0.3) for x_ in xs], lag_ratio=0.1), run_time=0.7)
            side1 = VGroup(txt("each word's vector travels", 24, INK2), txt("up its own lane", 24, INK2)).arrange(DOWN, buff=0.1)
            side1.move_to([RP, Y_X + 0.3, 0])
            self.play(FadeIn(side1), run_time=0.4)
            b.wait_until("attn", lead=0.25)
            self.sfx("whoosh_soft", -9)
            self.play(FadeIn(mha, shift=UP * 0.2), run_time=0.6)
            b.wait_until("gather", lead=0.25)
            links = VGroup()
            for i in range(4):
                for j in range(4):
                    if i == j:
                        continue
                    a = ArcBetweenPoints([LX[i], Y_MHA - 0.2, 0], [LX[j], Y_MHA - 0.2, 0],
                                         angle=-0.8 if LX[j] > LX[i] else 0.8)
                    a.set_stroke(HEADS[(i + j) % 8], 2.2, opacity=0.85)
                    links.add(a)
            side2 = txt("words exchange information", 24, ATT_C).move_to([RP, Y_MHA, 0])
            self.sfx("shimmer", -10)
            self.play(LaggedStart(*[ShowPassingFlash(l.copy().set_stroke(width=4), time_width=0.6) for l in links],
                                  lag_ratio=0.05),
                      FadeIn(side2), FadeOut(side1), run_time=1.6)

        # ---- b3: residual connection
        with self.vo("b3") as b:
            zs = VGroup(*[hvec(rvals(5, 600 + i) * 0.8, ATT_C).move_to([x, Y_MHA + 0.62, 0]) for i, x in enumerate(LX)])
            b.wait_until("res", lead=0.05)
            self.play(LaggedStart(*[FadeIn(z, shift=UP * 0.25) for z in zs], lag_ratio=0.1), FadeOut(side2), run_time=0.7)
            b.wait_until("added", lead=0.2)
            self.sfx("click", -10)
            self.play(Create(res1), run_time=0.7)
            # worked example on the right
            xa = hvec(xs[1].values, X_C, cell=0.28)
            za = hvec(zs[1].values, ATT_C, cell=0.28)
            sa = hvec(np.clip((np.array(xs[1].values) + np.array(zs[1].values)) / 1.4, -1, 1), INK, cell=0.28)
            eqn = VGroup(xa, MathTex("+", font_size=44), za, MathTex("=", font_size=44), sa).arrange(RIGHT, buff=0.22)
            eqn.move_to([RP, 1.0, 0])
            labs = VGroup(MathTex(r"\mathbf{x}", font_size=36, color=X_C).next_to(xa, UP, buff=0.15),
                          txt("attention output", 20, ATT_C).next_to(za, UP, buff=0.15),
                          txt("new x", 20, INK).next_to(sa, UP, buff=0.15))
            res_lab = txt("residual connection", 26, NORM_C, weight="SEMIBOLD").next_to(eqn, DOWN, buff=0.4)
            self.play(TransformFromCopy(xs[1], xa), TransformFromCopy(zs[1], za), FadeIn(eqn[1]), FadeIn(labs[:2]),
                      run_time=0.8)
            self.play(FadeIn(eqn[3]), FadeIn(sa, shift=RIGHT * 0.2), FadeIn(labs[2]), FadeIn(res_lab), run_time=0.7)
            b.wait_until("doc", lead=0.2)
            doc = RoundedRectangle(corner_radius=0.08, width=1.5, height=1.9).set_fill(PANEL2, 1).set_stroke(INK3, 1.5)
            doc.move_to([RP - 1.7, -1.75, 0])
            lines_ = VGroup(*[Line(LEFT * 0.5, RIGHT * (0.5 - 0.25 * (k % 2))).set_stroke(INK3, 3) for k in range(5)])
            lines_.arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to(doc).shift(UP * 0.15)
            doc_t = txt("a running document", 24, INK2).next_to(doc, RIGHT, buff=0.3).shift(UP * 0.25)
            self.play(FadeIn(doc), FadeIn(lines_), FadeIn(doc_t), run_time=0.6)
            b.wait_until("upd", lead=0.2)
            new_line = Line(LEFT * 0.5, RIGHT * 0.45).set_stroke(ATT_C, 4).next_to(lines_, DOWN, buff=0.2, aligned_edge=LEFT)
            upd_t = txt("+ an update, added in", 24, ATT_C).next_to(doc_t, DOWN, buff=0.25).align_to(doc_t, LEFT)
            self.sfx("pop_soft", -10)
            self.play(Create(new_line), FadeIn(upd_t), run_time=0.6)
            grp3 = VGroup(eqn, labs, res_lab, doc, lines_, doc_t, new_line, upd_t)

        # ---- b4: layer norm
        with self.vo("b4") as b:
            b.wait_until("norm", lead=0.05)
            self.play(FadeOut(grp3), FadeIn(an1, shift=UP * 0.1), run_time=0.6)
            vals = np.array([1.9, 0.4, 2.6, 1.2, 3.1, 0.9, 2.2, 1.5])
            normed = (vals - vals.mean()) / vals.std()
            base = 0.2
            bx0 = RP - 1.4
            bars = VGroup(*[Rectangle(width=0.28, height=abs(v) * 0.45 + 0.01).set_fill(X_C, 0.85).set_stroke(width=0)
                            .move_to([bx0 + 0.4 * k, base, 0], aligned_edge=DOWN if v >= 0 else UP)
                            for k, v in enumerate(vals)])
            zero = DashedLine([bx0 - 0.4, base, 0], [bx0 + 3.2, base, 0], dash_length=0.08).set_stroke(INK3, 1.5)
            ln_t = txt("layer norm: re-centre and rescale", 26, NORM_C, weight="SEMIBOLD").move_to([RP, 2.4, 0])
            self.play(FadeIn(ln_t), Create(zero), LaggedStart(*[GrowFromEdge(bb, DOWN) for bb in bars], lag_ratio=0.05),
                      run_time=0.8)
            nb = VGroup(*[Rectangle(width=0.28, height=abs(v) * 0.6 + 0.01).set_fill(NORM_C, 0.85).set_stroke(width=0)
                          .move_to([bx0 + 0.4 * k, base, 0], aligned_edge=DOWN if v >= 0 else UP)
                          for k, v in enumerate(normed)])
            self.sfx("swish", -12)
            self.play(*[Transform(a_, c_) for a_, c_ in zip(bars, nb)], run_time=0.9)
            stable = txt("numbers stay in a stable range", 22, INK2).next_to(zero, DOWN, buff=1.2)
            self.play(FadeIn(stable), run_time=0.4)
            b.wait_until("formula", lead=0.2)
            fml = MathTex(r"\mathrm{LayerNorm}(", r"x", r"+", r"\mathrm{Sublayer}(x)", r")", font_size=40)
            fml[1].set_color(X_C)
            fml[3].set_color(ATT_C)
            fml.move_to([RP, -2.7, 0])
            self.play(Write(fml), run_time=0.9)
            b.wait_until("an", lead=0.2)
            self.play(Indicate(an1.label, color=NORM_C, scale_factor=1.25), run_time=0.7)
            grp4 = VGroup(bars, zero, ln_t, stable, fml)

        # ---- b5: the feed-forward network
        with self.vo("b5") as b:
            b.wait_until("ffn", lead=0.05)
            self.sfx("whoosh_soft", -9)
            self.play(FadeOut(grp4), LaggedStart(*[FadeIn(f, shift=UP * 0.15) for f in ffns], lag_ratio=0.1),
                      zs.animate.set_opacity(0.25), run_time=0.8)
            b.wait_until("classic", lead=0.3)
            nn = nn_diagram(y=0.1)
            e1, e2, na, nh, no = nn
            call = DashedLine(ffns[3].get_right(), [RP - 2.35, 0.1, 0], dash_length=0.08).set_stroke(FFN_C, 1.5)
            ttl = txt("feed-forward network", 26, FFN_C, weight="SEMIBOLD").move_to([RP, 2.35, 0])
            dims = VGroup(txt("512", 22, INK2).next_to(na, DOWN, buff=0.25), txt("2048", 22, INK2).next_to(nh, DOWN, buff=0.2),
                          txt("512", 22, INK2).next_to(no, DOWN, buff=0.25))
            self.play(ffns[3].rect.animate.set_fill(opacity=0.45), Create(call), FadeIn(ttl), run_time=0.5)
            self.play(Create(e1), Create(e2), FadeIn(na), FadeIn(nh), FadeIn(no), run_time=1.1)
            b.wait_until("up", lead=0.2)
            act_in = rvals(6, 7, 0.2, 1)
            hid = np.random.default_rng(8).uniform(-1, 1, 12)
            self.play(*[c.animate.set_fill(lerp_color(PANEL2, X_C, a), 1) for c, a in zip(na, act_in)],
                      FadeIn(dims[0]), run_time=0.5)
            self.sfx("swish", -12)
            self.play(ShowPassingFlash(e1.copy().set_stroke(FFN_C, 1.6, opacity=1), time_width=0.5),
                      *[c.animate.set_fill(lerp_color(PANEL2, FFN_C, abs(v)) if v > 0 else lerp_color(PANEL2, BAD, abs(v) * 0.7), 1)
                        for c, v in zip(nh, hid)], FadeIn(dims[1]), run_time=1.1)
            up_t = txt("expand", 22, INK3).move_to([RP - 1.0, 2.0, 0])
            self.play(FadeIn(up_t), run_time=0.3)
            b.wait_until("relu", lead=0.2)
            relu_ax = VGroup(Line(LEFT * 0.35, ORIGIN), Line(ORIGIN, UP * 0.35 + RIGHT * 0.35)).set_stroke(Q_C, 3)
            relu_ax.move_to([RP, 1.95, 0])
            relu_l = MathTex(r"\max(0,\cdot)", font_size=28, color=Q_C).next_to(relu_ax, RIGHT, buff=0.15)
            zeros = VGroup(*[MathTex("0", font_size=18, color=INK3).move_to(c) for c, v in zip(nh, hid) if v <= 0])
            self.sfx("click", -9)
            self.play(FadeOut(up_t), FadeIn(relu_ax), FadeIn(relu_l),
                      *[c.animate.set_fill(PANEL, 1).set_stroke(INK3, 1) for c, v in zip(nh, hid) if v <= 0],
                      FadeIn(zeros), run_time=0.7)
            b.wait_until("down", lead=0.2)
            self.play(ShowPassingFlash(e2.copy().set_stroke(FFN_C, 1.6, opacity=1), time_width=0.5),
                      *[c.animate.set_fill(lerp_color(PANEL2, FFN_C, a), 1) for c, a in zip(no, rvals(6, 9, 0.2, 1))],
                      FadeIn(dims[2]), run_time=1.0)
            ffml = MathTex(r"\mathrm{FFN}(x) = \max(0,\, xW_1 + b_1)\,W_2 + b_2", font_size=34, color=INK)
            ffml.move_to([RP, -2.45, 0])
            self.play(Write(ffml), run_time=0.9)
            nn_grp = VGroup(nn, call, ttl, dims, relu_ax, relu_l, zeros, ffml)

        # ---- b6: same network for every position; communication vs computation
        with self.vo("b6") as b:
            b.wait_until("same", lead=0.05)
            shared = DashedLine(ffns[0].get_top() + UP * 0.12, ffns[3].get_top() + UP * 0.12, dash_length=0.1)
            shared.set_stroke(FFN_C, 2)
            sh_l = txt("same weights", 20, FFN_C).next_to(shared, UP, buff=0.05)
            self.play(FadeOut(nn_grp), ffns[3].rect.animate.set_fill(opacity=0.16), run_time=0.5)
            self.play(Create(shared), FadeIn(sh_l), *[Indicate(f, color=FFN_C, scale_factor=1.08) for f in ffns],
                      run_time=0.9)
            b.wait_until("nomove", lead=0.2)
            xs_marks = VGroup(*[txt("✗", 22, BAD, weight="BOLD").move_to([(LX[i] + LX[i + 1]) / 2, Y_FFN, 0])
                                for i in range(3)])
            self.sfx("tick", -10)
            self.play(LaggedStart(*[FadeIn(m, scale=0.5) for m in xs_marks], lag_ratio=0.15), run_time=0.6)
            b.wait_until("div", lead=0.2)
            dl = txt("A division of labour", 32, INK, weight="SEMIBOLD").move_to([RP, 2.3, 0])
            self.play(FadeIn(dl, shift=UP * 0.1), run_time=0.5)
            b.wait_until("comm", lead=0.2)
            c1 = VGroup(txt("Attention", 30, ATT_C, weight="BOLD"), txt("= communication", 30, INK)).arrange(RIGHT, buff=0.2)
            c1s = txt("words exchange information", 22, INK2)
            cg1 = VGroup(c1, c1s).arrange(DOWN, buff=0.15).move_to([RP, 0.9, 0])
            mg = glow(mha.rect, ATT_C, layers=6, width=18, opacity=0.3)
            self.sfx("pop", -9)
            self.play(FadeIn(cg1, shift=LEFT * 0.2), FadeIn(mg), run_time=0.6)
            b.wait_until("comp", lead=0.2)
            c2 = VGroup(txt("Feed-forward", 30, FFN_C, weight="BOLD"), txt("= computation", 30, INK)).arrange(RIGHT, buff=0.2)
            c2s = txt("each word processes what it gathered", 22, INK2)
            cg2 = VGroup(c2, c2s).arrange(DOWN, buff=0.15).move_to([RP, -0.6, 0])
            fg = VGroup(*[glow(f.rect, FFN_C, layers=5, width=14, opacity=0.3) for f in ffns])
            self.sfx("pop", -9)
            self.play(FadeIn(cg2, shift=LEFT * 0.2), FadeOut(mg), FadeIn(fg), run_time=0.6)
            grp6 = VGroup(dl, cg1, cg2)

        # ---- b7: parameters and the key-value memory view
        with self.vo("b7") as b:
            b.wait_until("params", lead=0.2)
            self.play(FadeOut(grp6), FadeOut(fg), FadeOut(xs_marks), run_time=0.4)
            pt = txt("parameters in one encoder layer", 24, INK2).move_to([RP, 2.45, 0])
            total_w = 5.0
            att_seg = Rectangle(width=total_w / 3, height=0.6).set_fill(ATT_C, 0.85).set_stroke(width=0)
            ffn_seg = Rectangle(width=total_w * 2 / 3, height=0.6).set_fill(FFN_C, 0.85).set_stroke(width=0)
            seg = VGroup(att_seg, ffn_seg).arrange(RIGHT, buff=0.04).move_to([RP, 1.8, 0])
            sl1 = VGroup(txt("attention", 20, ATT_C, weight="SEMIBOLD"), MathTex(r"4\times512^2\approx1.0\text{M}", font_size=26,
                                                                                    color=INK2)).arrange(DOWN, buff=0.08)
            sl2 = VGroup(txt("feed-forward", 20, FFN_C, weight="SEMIBOLD"),
                         MathTex(r"2\times512\times2048\approx2.1\text{M}", font_size=26, color=INK2)).arrange(DOWN, buff=0.08)
            sl1.next_to(att_seg, DOWN, buff=0.15)
            sl2.next_to(ffn_seg, DOWN, buff=0.15)
            thirds = txt("≈ 2/3", 30, BG, weight="BOLD").move_to(ffn_seg)
            self.play(FadeIn(pt), GrowFromEdge(att_seg, LEFT), run_time=0.5)
            self.play(GrowFromEdge(ffn_seg, LEFT), FadeIn(sl1), FadeIn(sl2), run_time=0.7)
            self.play(FadeIn(thirds, scale=0.8), run_time=0.4)
            b.wait_until("mem", lead=0.2)
            nn2 = nn_diagram(n_in=5, n_hid=8, n_out=5, x0=RP - 1.5, x1=RP, x2=RP + 1.5, h=1.2, y=-0.85)
            e1b, e2b, nab, nhb, nob = nn2
            memt = txt("later research: a key-value memory", 24, INK).move_to([RP, 0.2, 0])
            cite = txt("Geva et al., 2021", 18, INK3).move_to([RP, -2.6, 0])
            self.play(FadeIn(memt), FadeIn(nn2), FadeIn(cite), run_time=0.7)
            b.wait_until("fk", lead=0.2)
            fk_t = txt("layer 1 ≈ keys: pattern detectors", 22, K_C).move_to([RP, -1.8, 0])
            self.play(e1b.animate.set_stroke(K_C, 1.2, opacity=0.7), nhb.animate.set_stroke(K_C, 2), FadeIn(fk_t), run_time=0.6)
            b.wait_until("fv", lead=0.2)
            fv_t = txt("layer 2 ≈ values: what to write out", 22, V_C).move_to([RP, -2.18, 0])
            self.play(e2b.animate.set_stroke(V_C, 1.2, opacity=0.7), nob.animate.set_stroke(V_C, 2), FadeIn(fv_t), run_time=0.6)
            b.wait_until("again", lead=0.2)
            again = txt("the same idea, frozen into weights", 24, Q_C, weight="SEMIBOLD").move_to([RP, -3.1, 0])
            self.play(FadeIn(again, shift=UP * 0.1), run_time=0.5)
            grp7 = VGroup(pt, seg, sl1, sl2, thirds, nn2, memt, cite, fk_t, fv_t, again)

        # ---- b8: complete layer, stack of six
        with self.vo("b8") as b:
            b.wait_until("add2", lead=0.05)
            outs = VGroup(*[hvec(rvals(5, 700 + i), lerp_color(X_C, V_C, 0.4)).move_to([x, Y_OUT, 0]) for i, x in enumerate(LX)])
            self.play(FadeOut(grp7), FadeIn(an2, shift=UP * 0.1), Create(res2), run_time=0.7)
            self.play(LaggedStart(*[FadeIn(o, shift=UP * 0.2) for o in outs], lag_ratio=0.1), run_time=0.6)
            full = txt("a complete encoder layer", 28, INK, weight="SEMIBOLD").move_to([RP, 0.3, 0])
            self.play(FadeIn(full), layer_box.animate.set_stroke(INK2, 2), run_time=0.5)
            b.wait_until("stack", lead=0.3)
            everything = VGroup(chips, lanes, xs, zs, mha, an1, ffns, an2, outs, res1, res2, layer_box, lb_lab, shared, sh_l, full)
            # compact layer icon
            def layer_icon():
                return VGroup(Block("", ATT_C, width=2.6, height=0.24, size=10),
                              Block("", NORM_C, width=2.6, height=0.12, size=10),
                              VGroup(*[Block("", FFN_C, width=0.56, height=0.24, size=10) for _ in range(4)]).arrange(RIGHT, buff=0.12),
                              Block("", NORM_C, width=2.6, height=0.12, size=10)).arrange(UP, buff=0.06)
            icons = VGroup(*[layer_icon() for _ in range(6)]).arrange(UP, buff=0.2).scale(0.82).move_to([-2.9, -0.55, 0])
            frames = VGroup(*[SurroundingRectangle(ic, buff=0.08, corner_radius=0.08).set_stroke(INK3, 1.2).set_fill(PANEL, 0.6)
                              for ic in icons])
            self.sfx("whoosh", -8)
            self.play(FadeOut(everything, scale=0.6), run_time=0.6)
            self.play(LaggedStart(*[AnimationGroup(FadeIn(f), FadeIn(ic, shift=DOWN * 0.3)) for f, ic in zip(frames, icons)],
                                  lag_ratio=0.15), run_time=1.3)
            nlab = MathTex(r"\times 6", font_size=56, color=INK).next_to(frames, RIGHT, buff=0.35)
            nsub = VGroup(txt("N = 6 layers: same shape,", 22, INK2), txt("each with its own weights", 22, INK2)).arrange(DOWN, buff=0.08)
            nsub.move_to([RP, -2.6, 0])
            self.sfx("thud", -8)
            self.play(FadeIn(nlab, scale=0.7), FadeIn(nsub), run_time=0.5)
            b.wait_until("deep", lead=0.2)
            dots = VGroup(*[Dot(radius=0.07, color=X_C).move_to([-3.9 + 0.65 * k, frames.get_bottom()[1] - 0.3, 0])
                            for k in range(4)])
            self.play(FadeIn(dots), run_time=0.3)
            top_y = frames.get_top()[1] + 0.3
            self.play(*[d.animate.move_to([d.get_center()[0], top_y, 0]).set_color(lerp_color(X_C, V_C, 0.8)) for d in dots],
                      run_time=2.4, rate_func=linear)
            ctx = VGroup(Arrow(DOWN * 1.6, UP * 1.6, buff=0).set_color(INK3),
                         txt("more context", 22, INK2).rotate(PI / 2)).arrange(RIGHT, buff=0.1)
            ctx.next_to(nlab, RIGHT, buff=0.5)
            later = txt("later layers see vectors already", 24, INK).move_to([RP, 1.0, 0])
            later2 = txt("enriched with context", 24, INK).next_to(later, DOWN, buff=0.12)
            self.play(FadeIn(ctx), FadeIn(later), FadeIn(later2), run_time=0.6)
            stack_grp = VGroup(frames, icons, nlab, nsub, dots, ctx, later, later2)

        # ---- b9: everything is learned
        with self.vo("b9") as b:
            b.wait_until("learn", lead=0.05)
            self.play(FadeOut(VGroup(dots, ctx, later, later2, nsub)), run_time=0.4)
            mats = VGroup(*[MathTex(s, font_size=46, color=c) for s, c in
                            ((r"W^Q", Q_C), (r"W^K", K_C), (r"W^V", V_C), (r"W^O", ATT_C), (r"W_1", FFN_C), (r"W_2", FFN_C))])
            mats.arrange_in_grid(2, 3, buff=(0.5, 0.35)).move_to([RP, 1.4, 0])
            ml = txt("every layer's matrices", 26, INK2).next_to(mats, UP, buff=0.35)
            self.play(FadeIn(ml), LaggedStart(*[FadeIn(m, scale=0.7) for m in mats], lag_ratio=0.1), run_time=1.0)
            b.wait_until("bp", lead=0.2)
            loss = VGroup(Circle(radius=0.32).set_fill(BAD, 0.25).set_stroke(BAD, 2), txt("loss", 18, BAD))
            loss[1].move_to(loss[0])
            loss.next_to(frames, UP, buff=0.35)
            self.play(FadeIn(loss, scale=0.7), run_time=0.4)
            pulses = VGroup(*[Line([x, loss.get_bottom()[1], 0], [x, frames.get_bottom()[1], 0]).set_stroke(BAD, 4)
                              for x in (-4.0, -2.9, -1.8)])
            bp_t = txt("backpropagation", 24, BAD, weight="SEMIBOLD").next_to(mats, DOWN, buff=0.5)
            self.sfx("swell", -10)
            self.play(*[ShowPassingFlash(p, time_width=0.35) for p in pulses], FadeIn(bp_t),
                      LaggedStart(*[Indicate(ic, color=BAD, scale_factor=1.04) for ic in reversed(list(icons))], lag_ratio=0.12),
                      run_time=1.6)
            self.play(*[ShowPassingFlash(p.copy(), time_width=0.35) for p in pulses],
                      *[Wiggle(m, scale_value=1.1, rotation_angle=0.03 * TAU) for m in mats], run_time=1.4)
            b.wait_until("sig", lead=0.2)
            sig = VGroup(txt("one training signal:", 22, INK2),
                         txt("predict the next word of", 24, INK), txt("the correct translation", 24, INK)).arrange(DOWN, buff=0.1)
            sig.next_to(bp_t, DOWN, buff=0.45)
            self.play(FadeIn(sig, shift=UP * 0.1), run_time=0.6)
            b.wait_until("nobody", lead=0.2)
            qs = VGroup(*[txt("?", 30, Q_C, weight="BOLD").next_to(ic[0], RIGHT, buff=0.12) for ic in icons[::2]])
            self.play(LaggedStart(*[FadeIn(q_, scale=0.5) for q_ in qs], lag_ratio=0.15), run_time=0.7)
            b.wait_until("emerge", lead=0.2)
            pats = VGroup(*[Heatmap(np.eye(3)[::(-1) ** k] * 0.9 + 0.1, cell=0.1, gap=0.015, hi=HEADS[k % 8]).move_to(q_)
                            for k, q_ in enumerate(qs)])
            self.sfx("chime", -8)
            self.play(*[ReplacementTransform(q_, p_) for q_, p_ in zip(qs, pats)], run_time=0.8)
        self.wait(0.6)
        self.end_scene()
