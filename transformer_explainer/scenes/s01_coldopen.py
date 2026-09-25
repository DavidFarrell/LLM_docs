import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import *  # noqa: E402,F401,F403


def chip_hl(chip, color, fill=0.24, width=2.6):
    return chip.box.animate.set_stroke(color, width).set_fill(lerp_color(PANEL, color, fill), 1)


def chip_reset(chip):
    return chip.box.animate.set_stroke(EDGE, 1.6).set_fill(PANEL, 1)


class S01_ColdOpen(TScene):
    def construct(self):
        self.wait(0.4)
        chips = chip_row(SENT, size=34, gap=0.13)
        chips.scale_to_fit_width(12.4).move_to(UP * 0.1)

        # ---- b1: the sentence appears word by word
        with self.vo("b1") as b:
            b.wait_until("w0", lead=0.05)
            b.schedule([(b.t(f"w{i}") - self.now, FadeIn(chips[i], shift=UP * 0.18, scale=0.92), 0.3,
                         "tick", -15) for i in range(len(SENT))])

        # ---- b2: 'it' -> animal, then swap tired -> wide, 'it' -> street
        with self.vo("b2") as b:
            b.wait_until("it", lead=0.15)
            it = chips[IT]
            it_glow = glow(it.box, Q_C, width=18, opacity=0.35)
            arc = attn_arc(it, chips[ANIMAL], 0.95, Q_C, angle=0.62 * PI)
            arc_glow = glow(arc, Q_C, layers=5, width=22, opacity=0.25)
            self.sfx("chime_soft", -8)
            self.play(chip_hl(it, Q_C), FadeIn(it_glow), run_time=0.35)
            self.play(Create(arc), FadeIn(arc_glow), chip_hl(chips[ANIMAL], K_C, 0.18),
                      run_time=0.8, rate_func=smooth)
            b.wait_until("wide", lead=0.1)
            wide = Chip("wide.", size=34).scale(chips[0].height / Chip("The", size=34).height)
            wide.move_to(chips[10]).align_to(chips[10], LEFT)
            self.sfx("click", -8)
            self.play(FadeOut(chips[10], shift=UP * 0.25), FadeIn(wide, shift=UP * 0.25), run_time=0.4)
            chips.submobjects[10] = wide
            b.wait_until("now", lead=0.25)
            arc2 = attn_arc(it, chips[STREET], 0.95, Q_C, angle=0.62 * PI)
            arc2_glow = glow(arc2, Q_C, layers=5, width=22, opacity=0.25)
            self.sfx("blip", -9)
            self.play(Transform(arc, arc2), Transform(arc_glow, arc2_glow),
                      chip_reset(chips[ANIMAL]), chip_hl(chips[STREET], K_C, 0.18),
                      run_time=0.7, rate_func=smooth)

        # ---- b3: every word looks at every other word; the paper
        with self.vo("b3") as b:
            b.wait_until("look", lead=0.2)
            rng = np.random.default_rng(3)
            w_it = np.array([.02, .10, .03, .05, .02, .62, .03, .0, .02, .02, .09])
            arcs_it = VGroup(*[attn_arc(it, chips[j], w_it[j], Q_C, angle=0.62 * PI)
                               for j in range(len(SENT)) if j not in (IT, STREET)])
            web = VGroup()
            for i in range(len(SENT)):
                for j in range(i + 1, len(SENT)):
                    if IT in (i, j):
                        continue
                    web.add(attn_arc(chips[i], chips[j], rng.uniform(0.0, 0.25), INK2,
                                     angle=0.62 * PI, base=0.6, span=3, min_op=0.06))
            self.sfx("shimmer", -9)
            self.play(LaggedStart(*[Create(a) for a in arcs_it], lag_ratio=0.08), run_time=1.2)
            self.play(LaggedStart(*[Create(a) for a in web], lag_ratio=0.01), run_time=1.4)
            b.wait_until("year", lead=0.35)
            sentence_group = VGroup(chips, arc, arc_glow, it_glow, arcs_it, web)
            page = paper_card(os.path.join(PAPER, "page1.png"), height=7.0, oversample=1.7)
            page.move_to(RIGHT * 3.4 + DOWN * 0.1)
            year = txt("2017", 120, Q_C, weight="BOLD")
            venue = txt("NIPS 2017  ·  Long Beach", 26, INK2)
            org = txt("Google Brain  ·  Google Research", 26, INK2)
            left = VGroup(year, venue, org).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
            left.move_to(LEFT * 3.6)
            self.sfx("whoosh", -6)
            self.play(sentence_group.animate.scale(0.5).set_opacity(0).shift(DOWN * 2.5),
                      FadeIn(page, shift=LEFT * 1.2), run_time=0.9, rate_func=smooth)
            self.remove(sentence_group)
            self.play(FadeIn(year, shift=UP * 0.3), run_time=0.6)
            self.play(FadeIn(venue, shift=UP * 0.2), FadeIn(org, shift=UP * 0.2), run_time=0.6)
            # slow push-in on the paper's title line
            img = page[2]
            title_pt = img.get_top() + DOWN * img.height * 0.197
            push = b.t("title") - 3.0 - self.now
            if push > 0:
                self.wait(push)
            self.sfx("riser", -10)
            self.play(FadeOut(left, shift=LEFT * 0.5),
                      self.camera.frame.animate.set(width=config.frame_width / 1.7).move_to(title_pt),
                      run_time=b.rt("title", lead=0.05), rate_func=smooth)
            title = txt("Attention Is All You Need", 78, INK, weight="SEMIBOLD")
            top_rule = Line(LEFT, RIGHT).set_stroke(INK, 7).set_width(title.width + 0.6)
            bot_rule = Line(LEFT, RIGHT).set_stroke(INK, 2.5).set_width(title.width + 0.6)
            top_rule.next_to(title, UP, buff=0.45)
            bot_rule.next_to(title, DOWN, buff=0.45)
            head = VGroup(top_rule, title, bot_rule).move_to(ORIGIN)
            tglow = glow(title, Q_C, layers=6, width=10, opacity=0.18)
            self.sfx("impact", -4)
            self.remove(page)
            self.camera.frame.set(width=config.frame_width).move_to(ORIGIN)
            flash = FullScreenRectangle().set_fill(INK, 0.22).set_stroke(width=0)
            self.add(flash)
            self.play(FadeOut(flash), FadeIn(title, scale=1.08), FadeIn(tglow), GrowFromCenter(top_rule),
                      GrowFromCenter(bot_rule), run_time=0.6, rate_func=smooth)

        # ---- b4: the T in GPT
        with self.vo("b4") as b:
            b.wait_until("transformer", lead=0.2)
            the_t = txt("the", 40, INK2)
            tf = txt("Transformer", 96, Q_C, weight="BOLD")
            tf_glow = glow(tf, Q_C, layers=6, width=10, opacity=0.16)
            self.sfx("whoosh_soft", -8)
            self.play(VGroup(head, tglow).animate.scale(0.5).to_edge(UP, buff=0.5),
                      FadeIn(tf, shift=UP * 0.3), FadeIn(tf_glow), run_time=0.7)
            b.wait_until("gpt", lead=0.1)
            gpt = VGroup(txt("G", 70, INK2, weight="BOLD"), txt("P", 70, INK2, weight="BOLD"),
                         txt("T", 70, Q_C, weight="BOLD")).arrange(RIGHT, buff=0.06)
            gpt.next_to(tf, DOWN, buff=0.9)
            expl = VGroup(txt("Generative", 26, INK2), txt("Pre-trained", 26, INK2),
                          txt("Transformer", 26, Q_C, weight="SEMIBOLD")).arrange(RIGHT, buff=0.2)
            expl.next_to(gpt, DOWN, buff=0.3)
            uline = Line(LEFT, RIGHT).set_stroke(Q_C, 2.5).set_width(expl[2].width)
            uline.next_to(expl[2], DOWN, buff=0.08)
            self.sfx("pop", -8)
            self.play(FadeIn(gpt, shift=UP * 0.2), run_time=0.4)
            self.play(FadeIn(expl, shift=UP * 0.1), gpt[2].animate.scale(1.15), run_time=0.6)
            self.play(Create(uline), run_time=0.4)
            b.wait_until("llm", lead=0.3)
            icons = VGroup()
            for k in range(24):
                stack = VGroup(*[RoundedRectangle(corner_radius=0.03, width=0.42, height=0.09)
                                 .set_fill(HEADS[(k + r) % 8], 0.8).set_stroke(width=0) for r in range(4)])
                stack.arrange(UP, buff=0.04)
                icons.add(stack)
            left_grid = VGroup(*icons[:12]).arrange_in_grid(4, 3, buff=(0.4, 0.5)).move_to(LEFT * 5.85 + DOWN * 0.3)
            right_grid = VGroup(*icons[12:]).arrange_in_grid(4, 3, buff=(0.4, 0.5)).move_to(RIGHT * 5.85 + DOWN * 0.3)
            pos = [ic.get_center() for ic in icons]
            order = sorted(range(len(icons)), key=lambda k: abs(pos[k][0]))
            self.sfx("sparkle", -10)
            self.play(LaggedStart(*[FadeIn(icons[k], scale=0.5) for k in order], lag_ratio=0.06),
                      run_time=1.6)

        # ---- b5: the two goals
        with self.vo("b5") as b:
            self.play(*[FadeOut(m) for m in [head, tglow, tf, tf_glow, gpt, expl, uline, icons]],
                      run_time=0.6)
            goals = txt("Two goals", 30, INK2, weight="SEMIBOLD").to_edge(UP, buff=0.9)
            self.play(FadeIn(goals, shift=DOWN * 0.1), run_time=0.4)

            def card(inner, caption, color):
                box = RoundedRectangle(corner_radius=0.22, width=5.6, height=4.2)
                box.set_fill(PANEL, 0.92).set_stroke(color, 2)
                inner.move_to(box.get_center() + UP * 0.45)
                cap = txt(caption, 28, INK, weight="SEMIBOLD")
                if cap.width > 5.0:
                    cap.scale_to_fit_width(5.0)
                cap.move_to(box.get_center() + DOWN * 1.35)
                return VGroup(box, inner, cap)

            qkv = VGroup(txt("Q", 110, Q_C, weight="BOLD"), txt("K", 110, K_C, weight="BOLD"),
                         txt("V", 110, V_C, weight="BOLD")).arrange(RIGHT, buff=0.45)
            c1 = card(qkv, "Why these three nouns?", Q_C).move_to(LEFT * 3.2 + DOWN * 0.25)
            # network glyph: an attention block plugged into a stack
            att = Block("Attention", ATT_C, width=3.4, height=0.62, size=24)
            ff = Block("Feed-forward", FFN_C, width=3.4, height=0.62, size=24)
            nm1 = Block("Add & Norm", NORM_C, width=3.4, height=0.4, size=18)
            nm2 = Block("Add & Norm", NORM_C, width=3.4, height=0.4, size=18)
            net = VGroup(att, nm1, ff, nm2).arrange(UP, buff=0.14)
            c2 = card(net, "How does it plug into the network?", ATT_C).move_to(RIGHT * 3.2 + DOWN * 0.25)
            b.wait_until("one", lead=0.2)
            self.sfx("pop", -7)
            self.play(FadeIn(c1[0], shift=UP * 0.3), LaggedStart(*[FadeIn(l, scale=0.6) for l in qkv],
                      lag_ratio=0.2), FadeIn(c1[2]), run_time=0.9)
            b.wait_until("two", lead=0.2)
            self.sfx("pop", -7)
            self.play(FadeIn(c2[0], shift=UP * 0.3), FadeIn(c2[2]),
                      LaggedStart(*[FadeIn(m, shift=UP * 0.2) for m in net], lag_ratio=0.15), run_time=0.9)
        self.wait(0.4)
        self.sfx("whoosh", -8)
        self.end_scene()
