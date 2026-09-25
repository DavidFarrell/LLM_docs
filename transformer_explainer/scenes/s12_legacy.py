import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import *  # noqa: E402,F401,F403

TABLE2 = [("ByteNet", 23.75), ("GNMT + RL", 24.6), ("ConvS2S", 25.16), ("MoE", 26.03),
          ("GNMT + RL ensemble", 26.30), ("ConvS2S ensemble", 26.36),
          ("Transformer (base)", 27.3), ("Transformer (big)", 28.4)]


def stack_icon(kind, layers=3, w=1.6):
    blocks = VGroup()
    for _ in range(layers):
        if kind == "enc":
            lay = VGroup(Block("", ATT_C, width=w, height=0.2, size=8), Block("", FFN_C, width=w, height=0.2, size=8))
        else:
            lay = VGroup(Block("", ATT_C, width=w, height=0.2, size=8), Block("", FFN_C, width=w, height=0.2, size=8))
            lay[0].rect.set_stroke(BAD, 2)
        lay.arrange(UP, buff=0.05)
        blocks.add(lay)
    blocks.arrange(UP, buff=0.12)
    frame = SurroundingRectangle(blocks, buff=0.12, corner_radius=0.1).set_stroke(INK3, 1.5).set_fill(PANEL, 0.7)
    return VGroup(frame, blocks)


class S12_Legacy(TScene):
    chapter = ("11", "Impact")

    def construct(self):
        self.wait(0.2)
        self.chapter_intro()

        # ---- b1: results
        with self.vo("b1") as b:
            ttl = txt("English → German translation  ·  BLEU on newstest2014", 28, INK, weight="SEMIBOLD").move_to(UP * 2.75)
            x0, x1, v0, v1 = -2.9, 2.6, 20.0, 29.0

            def xv(v):
                return x0 + (x1 - x0) * (v - v0) / (v1 - v0)

            rows = VGroup()
            for k, (name, v) in enumerate(TABLE2):
                y = 1.75 - 0.58 * k
                is_t = name.startswith("Transformer")
                lab = txt(name, 24, Q_C if is_t else INK2, weight="SEMIBOLD" if is_t else "MEDIUM").move_to([x0 - 0.25, y, 0],
                                                                                                          aligned_edge=RIGHT)
                bar = Rectangle(width=xv(v) - x0, height=0.4).set_fill(Q_C if is_t else INK3, 0.9 if is_t else 0.7)
                bar.set_stroke(width=0).move_to([x0, y, 0], aligned_edge=LEFT)
                val = txt(f"{v:g}", 22, INK if is_t else INK2).next_to(bar, RIGHT, buff=0.12)
                rows.add(VGroup(lab, bar, val))
            axis = Line([x0, -2.75, 0], [x1, -2.75, 0]).set_stroke(INK3, 1.5)
            ticks = VGroup(*[VGroup(Line([xv(t), -2.75, 0], [xv(t), -2.85, 0]).set_stroke(INK3, 1.5),
                                    txt(str(t), 18, INK3).move_to([xv(t), -3.05, 0])) for t in range(20, 30, 2)])
            note = txt("(axis starts at 20)", 18, INK3).next_to(axis, DOWN, buff=0.45).align_to(axis, RIGHT)
            b.wait_until("bleu", lead=0.3)
            self.play(FadeIn(ttl, shift=DOWN * 0.1), Create(axis), FadeIn(ticks), FadeIn(note), run_time=0.6)
            self.play(LaggedStart(*[AnimationGroup(FadeIn(r[0]), GrowFromEdge(r[1], LEFT), FadeIn(r[2]))
                                    for r in rows], lag_ratio=0.18), run_time=2.4)
            b.wait_until("two", lead=0.2)
            ya, yb = rows[5][1].get_right(), rows[7][1].get_right()
            gap = VGroup(DashedLine([ya[0], ya[1], 0], [ya[0], yb[1], 0], dash_length=0.06).set_stroke(GOOD, 2),
                         Line([ya[0], yb[1], 0], [yb[0], yb[1], 0]).set_stroke(GOOD, 3))
            plus = VGroup(txt("+2.0 BLEU", 30, GOOD, weight="BOLD"), txt("over the best ensemble", 22, GOOD)).arrange(DOWN, buff=0.08)
            plus.move_to([4.75, 1.25, 0])
            self.sfx("ding", -8)
            self.play(Create(gap), FadeIn(plus, shift=LEFT * 0.1), run_time=0.8)
            b.wait_until("days", lead=0.2)
            gpus = VGroup(*[RoundedRectangle(corner_radius=0.04, width=0.3, height=0.42).set_fill(PANEL2, 1)
                            .set_stroke(GOOD, 1.5) for _ in range(8)]).arrange(RIGHT, buff=0.08)
            days = VGroup(gpus, txt("3.5 days on 8 GPUs", 24, INK, weight="SEMIBOLD")).arrange(RIGHT, buff=0.3)
            days = VGroup(gpus, txt("3.5 days on 8 GPUs", 24, INK, weight="SEMIBOLD")).arrange(DOWN, buff=0.2)
            days.move_to([4.75, -0.45, 0])
            cheap = VGroup(txt("a fraction of the", 22, INK2), txt("previous training cost", 22, INK2)).arrange(DOWN, buff=0.06)
            cheap.next_to(days, DOWN, buff=0.15)
            self.play(LaggedStart(*[FadeIn(g, scale=0.6) for g in gpus], lag_ratio=0.06), FadeIn(days[1]), run_time=0.8)
            self.play(FadeIn(cheap), run_time=0.4)
            grp1 = VGroup(ttl, rows, axis, ticks, note, gap, plus, days, cheap)

        # ---- b2: legacy
        with self.vo("b2") as b:
            b.wait_until("later", lead=0.05)
            self.play(FadeOut(grp1, shift=UP * 0.2), run_time=0.45)
            tl = Line(LEFT * 6.0, RIGHT * 6.0).set_stroke(INK3, 2).move_to(DOWN * 2.9)
            marks = VGroup()
            for x, lab in ((-4.6, "2017"), (-0.6, "2018"), (4.2, "today")):
                marks.add(VGroup(Dot([x, -2.9, 0], radius=0.07, color=INK2), txt(lab, 22, INK2).move_to([x, -3.3, 0])))
            orig = VGroup(stack_icon("enc", 2, 1.2), stack_icon("dec", 2, 1.2)).arrange(RIGHT, buff=0.25).move_to([-4.6, -0.9, 0])
            orig_l = txt("Transformer", 22, Q_C, weight="SEMIBOLD").next_to(orig, UP, buff=0.2)
            self.play(Create(tl), FadeIn(marks), FadeIn(orig, shift=UP * 0.2), FadeIn(orig_l), run_time=0.8)
            b.wait_until("bert", lead=0.2)
            bert = stack_icon("enc", 3, 1.4).move_to([-1.6, -0.6, 0])
            bert_l = VGroup(txt("BERT", 26, ATT_C, weight="BOLD"), txt("encoder stack", 20, INK2)).arrange(DOWN, buff=0.08)
            bert_l.next_to(bert, UP, buff=0.2)
            self.sfx("pop", -9)
            self.play(TransformFromCopy(orig[0], bert), FadeIn(bert_l), run_time=0.7)
            b.wait_until("gpt", lead=0.2)
            gpt = stack_icon("dec", 3, 1.4).move_to([0.6, -0.6, 0])
            gpt_l = VGroup(txt("GPT", 26, FFN_C, weight="BOLD"), txt("decoder stack", 20, INK2)).arrange(DOWN, buff=0.08)
            gpt_l.next_to(gpt, UP, buff=0.2)
            self.sfx("pop", -9)
            self.play(TransformFromCopy(orig[1], gpt), FadeIn(gpt_l), run_time=0.7)
            b.wait_until("scale", lead=0.2)
            big = stack_icon("dec", 9, 2.6).move_to([4.2, -0.35, 0])
            big.scale_to_fit_height(5.0).move_to([4.2, -0.2, 0])
            big_l = txt("today's language models", 24, INK, weight="SEMIBOLD").next_to(big, UP, buff=0.2)
            self.sfx("riser", -10)
            self.play(TransformFromCopy(gpt, big), run_time=1.4)
            self.play(FadeIn(big_l), run_time=0.4)
            b.wait_until("core", lead=0.3)
            self.play(FadeOut(VGroup(orig, orig_l, bert, bert_l, gpt, gpt_l, tl, marks, big_l)),
                      big.animate.scale(0.75).move_to([4.6, -0.3, 0]), run_time=0.6)
            centre = np.array([-1.6, -0.2, 0])
            R = 1.9
            names = [("attend", ATT_C, PI / 2), ("compute", FFN_C, PI / 2 - TAU / 3), ("repeat", Q_C, PI / 2 + TAU / 3)]
            nodes = VGroup()
            for nm, col, ang in names:
                p = centre + R * np.array([np.cos(ang), np.sin(ang), 0])
                nodes.add(pill(nm, col, 30, padx=0.3, pady=0.14).move_to(p))
            arcs = VGroup()
            for k in range(3):
                a0 = names[k][2] - 0.42
                arc = Arc(radius=R, start_angle=a0, angle=-(TAU / 3 - 0.84), arc_center=centre).set_stroke(INK3, 3)
                arc.add_tip(tip_length=0.2)
                arcs.add(arc)
            self.play(LaggedStart(*[Create(a) for a in arcs], lag_ratio=0.2), FadeIn(nodes), run_time=1.0)
            for key, k in (("attend", 0), ("compute", 1), ("repeat", 2)):
                b.wait_until(key, lead=0.05)
                self.sfx("tick", -9)
                self.play(nodes[k][0].animate.set_fill(names[k][1], 0.55), Indicate(nodes[k], color=names[k][1], scale_factor=1.12),
                          run_time=0.4)
        self.wait(0.8)
        self.end_scene()
