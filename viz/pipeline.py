"""Manim: how one book is copied on its way into Claude (Order on Fair Use, pp. 4-7)."""
from manim import *

BG, INK, MUTED = "#0F1420", "#E8ECF4", "#AEB7C7"
RED, GREEN, AMBER, BLUE = "#FF6B6B", "#4FD1A5", "#F5B84B", "#6EA8FE"
FONT = "Apple SD Gothic Neo"
config.background_color = BG


def T(s, size=30, color=INK, weight=NORMAL):
    return Text(s, font=FONT, font_size=size, color=color, weight=weight)


def box(title, sub, color, w=2.7, h=1.5):
    r = RoundedRectangle(corner_radius=0.15, width=w, height=h, stroke_color=color, stroke_width=4,
                         fill_color=color, fill_opacity=0.10)
    t = T(title, 28, INK, BOLD)
    s = T(sub, 20, MUTED)
    VGroup(t, s).arrange(DOWN, buff=0.16).move_to(r)
    return VGroup(r, t, s)


class Pipeline(Scene):
    def construct(self):
        title = T("책 한 권이 클로드에 들어가기까지", 40, INK, BOLD).to_edge(UP, buff=0.45)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.8)

        pir = box("해적판", "Books3·LibGen·PiLiMi", RED, 3.0, 1.2)
        buy = box("구매·스캔", "종이 원본은 폐기", GREEN, 3.0, 1.2)
        src = VGroup(pir, buy).arrange(DOWN, buff=0.5).to_edge(LEFT, buff=0.5).shift(DOWN * 0.2)
        lib = box("중앙 도서관", "\"영원히 보관\"", AMBER, 2.8, 1.6).next_to(src, RIGHT, buff=1.0)
        self.play(LaggedStart(FadeIn(pir, shift=RIGHT), FadeIn(buy, shift=RIGHT), lag_ratio=0.3), run_time=1.0)
        a1 = Arrow(pir.get_right(), lib.get_left() + UP * 0.3, color=MUTED, buff=0.1, stroke_width=4)
        a2 = Arrow(buy.get_right(), lib.get_left() + DOWN * 0.3, color=MUTED, buff=0.1, stroke_width=4)
        self.play(GrowArrow(a1), GrowArrow(a2), FadeIn(lib), run_time=1.0)

        steps = [("① 작업 사본", "학습용 묶음에 복사"), ("② 정제본", "머리글·쪽번호 제거"),
                 ("③ 토큰화", "글자 → 숫자 배열"), ("④ 모델 안 압축", "거의 그대로 '암기'")]
        chips = VGroup(*[box(a, b, BLUE, 2.55, 1.05) for a, b in steps]).arrange(DOWN, buff=0.18)
        chips.next_to(lib, RIGHT, buff=1.0)
        arr = Arrow(lib.get_right(), chips.get_left(), color=MUTED, buff=0.1, stroke_width=4)
        self.play(GrowArrow(arr), run_time=0.5)
        for c in chips:
            self.play(FadeIn(c, shift=LEFT * 0.3), run_time=0.45)

        tok = T("  [ 4821, 917, 30442, 118, 7765, ... ]", 22, BLUE).next_to(chips[2], RIGHT, buff=0.15)
        self.play(Write(tok), run_time=0.8)
        self.play(FadeOut(tok), run_time=0.3)

        filt = box("필터", "입·출력 검사", MUTED, 1.9, 1.3).next_to(chips, RIGHT, buff=0.9)
        out = VGroup(T("침해 출력", 26, GREEN, BOLD), T("없음", 26, GREEN, BOLD)).arrange(DOWN, buff=0.1).next_to(filt, DOWN, buff=0.8)
        a4 = Arrow(filt.get_bottom(), out.get_top(), color=MUTED, buff=0.08, stroke_width=4)
        a3 = Arrow(chips[3].get_right(), filt.get_left(), color=MUTED, buff=0.1, stroke_width=4)
        self.play(GrowArrow(a3), FadeIn(filt), run_time=0.7)
        self.play(GrowArrow(a4), FadeIn(out, shift=DOWN * 0.2), run_time=0.6)

        note = T("원고들은 '출력'이 아니라 '입력(학습)'만 문제 삼았다", 28, AMBER, BOLD).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(note, shift=UP * 0.2), Indicate(chips, color=AMBER, scale_factor=1.03), run_time=1.2)
        self.wait(1.5)
