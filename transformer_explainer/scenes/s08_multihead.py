import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import *  # noqa: E402,F401,F403


def pattern(kind, n=8, seed=0):
    rng = np.random.default_rng(seed)
    M = rng.uniform(0, 0.12, (n, n))
    if kind == "prev":
        for i in range(1, n):
            M[i, i - 1] = 1
        M[0, 0] = 1
    elif kind == "next":
        for i in range(n - 1):
            M[i, i + 1] = 1
        M[n - 1, n - 1] = 1
    elif kind == "self":
        for i in range(n):
            M[i, i] = 1
    elif kind == "first":
        M[:, 0] = 0.9
    elif kind == "last":
        M[:, n - 1] = 0.9
    elif kind == "coref":
        M[5, 1] = 1
        M[6, 1] = 0.7
        M[3, 1] = 0.6
        for i in range(n):
            M[i, i] = max(M[i, i], 0.35)
    elif kind == "broad":
        M = rng.uniform(0.25, 0.55, (n, n))
    elif kind == "verb":
        M[3, 1] = 1
        M[2, 1] = 0.8
        M[7, 5] = 0.9
        M[1, 3] = 0.6
    return np.clip(M, 0, 1)


class S08_MultiHead(TScene):
    chapter = ("07", "Multi-head attention")

    def construct(self):
        self.wait(0.2)
        self.chapter_intro()
        chips = sentence_layout(SENT, y=-0.4, size=26)

        # ---- b1: many relationships at once
        with self.vo("b1") as b:
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.12) for c in chips], lag_ratio=0.04), run_time=0.8)
            b.wait_until("ex1", lead=0.2)
            a1 = attn_arc(chips[IT], chips[ANIMAL], 0.9, Q_C, angle=0.6 * PI)
            l1 = txt("pronoun → noun", 24, Q_C, weight="SEMIBOLD").next_to(a1, UP, buff=0.1)
            self.sfx("blip", -10)
            self.play(Create(a1), FadeIn(l1), run_time=0.6)
            b.wait_until("ex2", lead=0.2)
            prev = VGroup(*[attn_arc(chips[i], chips[i - 1], 0.5, K_C, angle=0.9 * PI, above=False)
                            for i in range(1, len(SENT))])
            l2 = txt("previous word", 24, K_C, weight="SEMIBOLD").next_to(chips, DOWN, buff=0.75)
            self.sfx("blip", -10)
            self.play(LaggedStart(*[Create(a) for a in prev], lag_ratio=0.05), FadeIn(l2), run_time=0.8)
            b.wait_until("ex3", lead=0.2)
            a3 = attn_arc(chips[3], chips[ANIMAL], 0.8, V_C, angle=0.75 * PI)
            l3 = txt("verb → subject", 22, V_C, weight="SEMIBOLD")
            l3.move_to([-5.35, a3.get_top()[1] + 0.4, 0])
            self.sfx("blip", -10)
            self.play(Create(a3), FadeIn(l3), run_time=0.6)
            rel_group = VGroup(chips, a1, l1, prev, l2, a3, l3)

        # ---- b2: several heads in parallel
        with self.vo("b2") as b:
            kinds = ["prev", "coref", "next", "broad", "verb", "self", "first", "last"]
            panels = VGroup()
            for h, kind in enumerate(kinds):
                hm = Heatmap(pattern(kind, seed=h), cell=0.17, gap=0.022, hi=HEADS[h])
                box = RoundedRectangle(corner_radius=0.14, width=hm.width + 0.5, height=hm.height + 0.95)
                box.set_fill(PANEL, 0.95).set_stroke(HEADS[h], 1.8)
                hm.move_to(box.get_center() + DOWN * 0.18)
                lab = txt(f"head {h + 1}", 22, HEADS[h], weight="SEMIBOLD").next_to(hm, UP, buff=0.12)
                panels.add(VGroup(box, hm, lab))
            panels.arrange_in_grid(2, 4, buff=(0.35, 0.42)).move_to(DOWN * 0.35)
            b.wait_until("heads", lead=0.2)
            self.sfx("whoosh", -9)
            self.play(FadeOut(rel_group, scale=0.8), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(p, scale=0.85) for p in panels], lag_ratio=0.08), run_time=1.3)
            b.wait_until("own", lead=0.2)
            trios = VGroup()
            for p in panels:
                t = VGroup(*[RoundedRectangle(corner_radius=0.03, width=0.2, height=0.2).set_stroke(width=0)
                             .set_fill(c, 0.9) for c in (Q_C, K_C, V_C)]).arrange(RIGHT, buff=0.06)
                t.next_to(p[0], DOWN, buff=0.1)
                trios.add(t)
            own = VGroup(txt("each head: its own", 24, INK2), MathTex(r"W^Q_i,\;W^K_i,\;W^V_i", font_size=36))
            own.arrange(RIGHT, buff=0.2).move_to(UP * 3.1)
            own[1].set_color_by_tex("W", INK)
            self.sfx("tick", -12)
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.1) for t in trios], lag_ratio=0.05), FadeIn(own),
                      run_time=0.9)
            b.wait_until("eight", lead=0.2)
            eight = MathTex(r"h = 8 \text{ heads}, \quad d_k = d_v = 64", font_size=40, color=Q_C)
            eight.to_edge(DOWN, buff=0.22)
            self.play(FadeIn(eight, shift=UP * 0.1), run_time=0.5)

        # ---- b3: concat and W^O
        with self.vo("b3") as b:
            b.wait_until("cat", lead=0.05)
            segs = VGroup(*[Rectangle(width=0.32, height=1.6).set_fill(HEADS[h], 0.85).set_stroke(width=0)
                            for h in range(8)])
            segs.arrange(RIGHT, buff=0.0).move_to(LEFT * 3.0 + DOWN * 0.3)
            srcs = [p[1].copy() for p in panels]
            self.sfx("click", -10)
            self.play(FadeOut(VGroup(own, trios, eight)), *[ReplacementTransform(srcs[h], segs[h]) for h in range(8)],
                      panels.animate.set_opacity(0.15), run_time=1.0)
            cat_l = MathTex(r"\mathrm{Concat}:\; 8 \times 64 = 512", font_size=36, color=INK).next_to(segs, UP, buff=0.35)
            self.play(FadeIn(cat_l), FadeOut(panels), run_time=0.5)
            b.wait_until("wo", lead=0.2)
            wo = VGroup(*[RoundedRectangle(corner_radius=0.02, width=0.16, height=0.16).set_stroke(width=0)
                          .set_fill(lerp_color(PANEL2, INK2, v), 1)
                          for v in np.random.default_rng(5).uniform(0.1, 0.8, 64)]).arrange_in_grid(8, 8, buff=0.03)
            wo_box = VGroup(wo, outline(wo, INK2, buff=0.08, corner=0.08, width=2)).move_to(RIGHT * 0.6 + DOWN * 0.3)
            wo_l = MathTex("W^O", font_size=44, color=INK).next_to(wo_box, UP, buff=0.3)
            out = Rectangle(width=2.56, height=1.6).set_stroke(width=0)
            out.set_fill(color=[HEADS[0], HEADS[3], HEADS[2]], opacity=0.9)
            out.move_to(RIGHT * 4.3 + DOWN * 0.3)
            out_l = txt("multi-head output (512)", 24, INK2).next_to(out, UP, buff=0.3)
            a1 = Arrow(segs.get_right(), wo_box.get_left(), buff=0.2, stroke_width=3).set_color(INK3)
            a2 = Arrow(wo_box.get_right(), out.get_left(), buff=0.2, stroke_width=3).set_color(INK3)
            self.sfx("whoosh_soft", -9)
            self.play(GrowArrow(a1), FadeIn(wo_box), FadeIn(wo_l), run_time=0.6)
            self.play(GrowArrow(a2), FadeIn(out, shift=RIGHT * 0.2), FadeIn(out_l), run_time=0.7)
            b.wait_until("cost", lead=0.2)
            cmp_l = VGroup(Rectangle(width=0.32 * 8, height=0.5).set_fill(PANEL2, 1).set_stroke(INK3, 1.5),
                           txt("8 heads × 64 dims", 22, INK2)).arrange(DOWN, buff=0.15)
            cmp_r = VGroup(Rectangle(width=0.32 * 8, height=0.5).set_fill(PANEL2, 1).set_stroke(INK3, 1.5),
                           txt("1 head × 512 dims", 22, INK2)).arrange(DOWN, buff=0.15)
            approx = MathTex(r"\approx", font_size=56, color=Q_C)
            cmpg = VGroup(cmp_l, approx, cmp_r).arrange(RIGHT, buff=0.5).move_to(DOWN * 2.7)
            cost_l = txt("same total cost", 24, Q_C, weight="SEMIBOLD").next_to(cmpg, RIGHT, buff=0.4)
            self.play(FadeIn(cmpg, shift=UP * 0.1), FadeIn(cost_l), run_time=0.7)
            grp3 = VGroup(segs, cat_l, wo_box, wo_l, out, out_l, a1, a2, cmpg, cost_l)

        # ---- b4: evidence from the paper
        with self.vo("b4") as b:
            self.play(FadeOut(grp3, shift=UP * 0.2), run_time=0.45)
            head_t = txt("Heads specialise", 40, INK, weight="SEMIBOLD").move_to(LEFT * 3.6 + UP * 1.9)
            self.play(FadeIn(head_t, shift=UP * 0.1), run_time=0.5)
            b.wait_until("fig", lead=0.4)
            card = paper_card(os.path.join(PAPER, "fig4_its.png"), height=6.2, pad=0.15)
            card.move_to(RIGHT * 3.3 + DOWN * 0.05)
            img = card[2]
            W, H = 1045, 1627

            def px(x, y):
                return img.get_corner(UL) + RIGHT * (x / W * img.width) + DOWN * (y / H * img.height)

            cap = txt("Vaswani et al. 2017, Figure 4  ·  encoder layer 5 of 6", 20, INK3)
            cap.next_to(card, DOWN, buff=0.12)
            self.sfx("whoosh_soft", -9)
            self.play(FadeIn(card, shift=LEFT * 0.5), FadeIn(cap), run_time=0.8)
            sub = txt("two heads resolving a pronoun", 26, INK2).next_to(head_t, DOWN, buff=0.3).align_to(head_t, LEFT)
            self.play(FadeIn(sub), run_time=0.4)
            b.wait_until("its", lead=0.15)
            its_box = RoundedRectangle(corner_radius=0.06, width=(1040 - 737) / W * img.width,
                                       height=(548 - 492) / H * img.height).move_to(px(888, 520))
            its_box.set_stroke(Q_C, 3).set_fill(opacity=0)
            self.sfx("tick", -9)
            self.play(Create(its_box), run_time=0.4)
            b.wait_until("law", lead=0.15)
            law_box = RoundedRectangle(corner_radius=0.06, width=(343 - 187) / W * img.width + 0.1,
                                       height=(135 - 80) / H * img.height + 0.06).move_to(px(265, 107))
            law_box.set_stroke(K_C, 3).set_fill(opacity=0)
            link = Line(px(737, 520), px(343, 107)).set_stroke(Q_C, 4, opacity=0.9)
            lg = glow(link, Q_C, layers=4, width=14, opacity=0.3)
            self.sfx("ding", -9)
            self.play(Create(law_box), Create(link), FadeIn(lg), run_time=0.6)
            anno = VGroup(txt("'its'", 30, Q_C, weight="SEMIBOLD"), txt("→", 30, INK3),
                          txt("'Law'", 30, K_C, weight="SEMIBOLD")).arrange(RIGHT, buff=0.25)
            anno.next_to(sub, DOWN, buff=0.45).align_to(sub, LEFT)
            self.play(FadeIn(anno, shift=UP * 0.1), run_time=0.4)
            b.wait_until("just", lead=0.2)
            mini = VGroup(Chip("animal", size=24), Chip("…", size=24), Chip("it", size=24)).arrange(RIGHT, buff=0.15)
            mini.next_to(anno, DOWN, buff=1.3).align_to(anno, LEFT)
            marc = attn_arc(mini[2], mini[0], 0.9, Q_C, angle=0.7 * PI)
            ours = txt("our example", 20, INK3).next_to(mini, DOWN, buff=0.15)
            self.play(FadeIn(mini), Create(marc), FadeIn(ours), run_time=0.7)
        self.wait(0.5)
        self.end_scene()
