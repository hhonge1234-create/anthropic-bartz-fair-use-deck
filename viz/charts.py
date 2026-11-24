"""Charts for the deck. Every number is taken from the court documents (see PLAN.md)."""
import sys
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "assets")
OUT.mkdir(parents=True, exist_ok=True)

fm.fontManager.addfont("/System/Library/Fonts/AppleSDGothicNeo.ttc")
plt.rcParams.update({
    "font.family": "Apple SD Gothic Neo",
    "axes.unicode_minus": False,
    "text.color": "#111827", "axes.labelcolor": "#4B5563",
    "xtick.color": "#111827", "ytick.color": "#111827",
    "axes.edgecolor": "#D1D5DB", "font.size": 15,
})
INK, MUTED, GRID = "#111827", "#4B5563", "#E5E7EB"
RED, GREEN, AMBER, BLUE = "#B91C1C", "#1E3A8A", "#1E3A8A", "#6B7280"


def save(fig, name):
    fig.savefig(OUT / name, dpi=200, transparent=True, bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)


def clean(ax):
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)


# A. Pirated books downloaded (Order on Fair Use, pp. 2-3)
fig, ax = plt.subplots(figsize=(9.6, 4.2))
rows = [("Books3\n2021년 1~2월", 196_640, "196,640권"),
        ("LibGen\n2021년 6월", 5_000_000, "최소 500만 권"),
        ("PiLiMi\n2022년 7월", 2_000_000, "최소 200만 권")]
labels = [r[0] for r in rows][::-1]
vals = [r[1] for r in rows][::-1]
txt = [r[2] for r in rows][::-1]
bars = ax.barh(labels, vals, color="#1E3A8A", height=0.56)
for b, t in zip(bars, txt):
    ax.text(b.get_width() + 80_000, b.get_y() + b.get_height() / 2, t,
            va="center", fontsize=17, fontweight="bold", color=INK)
ax.set_xlim(0, 6_300_000)
ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v/1e6:.0f}백만" if v else "0"))
ax.grid(axis="x", color="#CBD5E1", lw=1)
ax.set_axisbelow(True)
ax.tick_params(axis="y", length=0, labelsize=17)
ax.tick_params(axis="x", labelsize=15, colors=INK)
clean(ax)
save(fig, "chart_pirated.png")

# B. Per-work settlement vs statutory damages range (Final Approval Order pp. 4, 10)
fig, ax = plt.subplots(figsize=(10, 4.4))
pts = [(200, "무과실 침해\n법정 최저", MUTED), (750, "통상 침해\n법정 최저", MUTED),
       (3000, "작품당 합의금\n(비용 공제 전)", GREEN), (150_000, "법정\n최고", MUTED)]
ax.set_xscale("log")
ax.set_xlim(100, 300_000)
ax.set_ylim(-1, 1.4)
ax.hlines(0, 200, 150_000, color="#D1D5DB", lw=10, capstyle="round")
for v, lab, c in pts:
    big = c == GREEN
    ax.scatter([v], [0], s=520 if big else 220, color=c, zorder=3, edgecolor="white", lw=2)
    ax.text(v, 0.42, f"${v:,}", ha="center", fontsize=24 if big else 18, fontweight="bold", color=c if big else INK)
    ax.text(v, -0.42, lab, ha="center", va="top", fontsize=15, color=c if big else INK, linespacing=1.3)
ax.annotate("", xy=(3000, 0.95), xytext=(750, 0.95),
            arrowprops=dict(arrowstyle="->", color=AMBER, lw=2))
ax.text(1500, 1.05, "통상 최저의 4배", ha="center", fontsize=15, color=AMBER, fontweight="bold")
ax.axis("off")
save(fig, "chart_perwork.png")

# C. Claims rate (Final Approval Order p. 4)
claimed, total = 440_490, 482_460
fig, ax = plt.subplots(figsize=(5, 5))
ax.pie([claimed, total - claimed], colors=[GREEN, "#E5E7EB"], startangle=90, counterclock=False,
       wedgeprops=dict(width=0.28, edgecolor="white", linewidth=2))
ax.text(0, 0.1, f"{claimed/total*100:.1f}%", ha="center", va="center", fontsize=40, fontweight="bold", color=INK)
ax.text(0, -0.22, f"{claimed:,} / {total:,}건", ha="center", va="center", fontsize=15, color=INK)
ax.set(aspect="equal")
save(fig, "chart_claims.png")

# D. Attorney fees: request -> reduced request -> award (Final Approval Order pp. 14-15, 22)
fig, ax = plt.subplots(figsize=(9, 4.6))
steps = [("최초 요청\n(20%)", 300_000_000, "#9CA3AF"), ("수정 요청\n(12.5%)", 187_500_000, "#6B7280"),
         ("법원 인정\n(약 6.8%)", 101_561_111, GREEN)]
x = range(len(steps))
bars = ax.bar(x, [s[1] for s in steps], color=[s[2] for s in steps], width=0.56)
for b, s in zip(bars, steps):
    ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 6e6, f"${s[1]/1e6:,.1f}M",
            ha="center", fontsize=18, fontweight="bold", color=INK)
ax.axhline(27_082_963, color=BLUE, lw=1.5, ls="--")
ax.text(2.45, 315_000_000, "- - -  실제 투입 시간 환산(lodestar) $27.1M", ha="right", fontsize=12.5, color=BLUE)
ax.set_xticks(list(x), [s[0] for s in steps], fontsize=14)
ax.set_ylim(0, 340_000_000)
ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"${v/1e6:.0f}M"))
ax.tick_params(axis="y", colors=MUTED, labelsize=12)
ax.grid(axis="y", color=GRID, lw=1)
ax.set_axisbelow(True)
clean(ax)
ax.tick_params(axis="x", length=0)
save(fig, "chart_fees.png")
print("ok")
