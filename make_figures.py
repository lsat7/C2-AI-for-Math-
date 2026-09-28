#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Generate the two figures referenced by paper.tex as vector PDFs.

fig1_architecture.pdf -- the three-layer decomposition diagram
fig2_defects.pdf      -- where the seven defect classes originate

Output is vector PDF so it stays crisp at any zoom and does not
require an external image converter at LaTeX compile time.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import os

OUT = os.path.dirname(os.path.abspath(__file__))

# Light-theme palette (paper is printed on white)
INK      = "#1a1a1a"
MUTED    = "#5a5a5a"
L_GEN    = "#dce9f7"
E_GEN    = "#2f6db5"
L_RED    = "#fbe2e2"
E_RED    = "#b53a3a"
L_VER    = "#dff0e2"
E_VER    = "#2f7d4f"
L_NOTE   = "#f4f0d8"
E_NOTE   = "#8a7a20"
NOTE_EDGE = "#8a7a20"


def box(ax, x, y, w, h, text, face, edge, fs=10, weight="normal", radius=0.02):
    p = FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0.004,rounding_size={radius}",
        linewidth=1.3, facecolor=face, edgecolor=edge, zorder=2,
    )
    ax.add_patch(p)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
            fontsize=fs, color=INK, weight=weight, zorder=3,
            linespacing=1.45)


def arrow(ax, p1, p2, color=INK, style="-|>", lw=1.4, dashed=False, rad=0.0):
    a = FancyArrowPatch(
        p1, p2, arrowstyle=style, mutation_scale=13,
        linewidth=lw, color=color, zorder=4,
        linestyle="--" if dashed else "-",
        connectionstyle=f"arc3,rad={rad}",
        shrinkA=1, shrinkB=1,
    )
    ax.add_patch(a)


# ===========================================================================
# Figure 1: three-layer architecture
# ===========================================================================
def figure1():
    fig, ax = plt.subplots(figsize=(9.0, 4.6))
    ax.set_xlim(0, 10); ax.set_ylim(0, 5.2); ax.axis("off")

    bw, bh, by = 2.55, 1.25, 2.55

    # outer system boundary
    ax.add_patch(FancyBboxPatch(
        (0.30, 2.10), 9.40, 2.20,
        boxstyle="round,pad=0.01,rounding_size=0.06",
        linewidth=1.0, facecolor="none", edgecolor="#bbbbbb",
        linestyle=":", zorder=1))
    ax.text(0.52, 4.40, "AI4Math system", fontsize=9.5, color=MUTED,
            style="italic", ha="left", va="center", zorder=3)

    # the three layers
    box(ax, 0.55, by, bw, bh,
        "Layer 1 — Generation\n$(G: \\mathcal{N} \\to \\mathcal{N})$\n\n"
        "informal derivation, CoT",
        L_GEN, E_GEN, fs=9.5, weight="normal")
    box(ax, 3.72, by, bw, bh,
        "Layer 2 — Semantic Reduction\n$(R: \\mathcal{N} \\to \\mathcal{I})$\n\n"
        "informal $\\rightarrow$ typed formal",
        L_RED, E_RED, fs=9.5, weight="bold")
    box(ax, 6.90, by, bw, bh,
        "Layer 3 — Verification\n$(C: \\mathcal{I} \\to \\{\\top,\\bot\\})$\n\n"
        "kernel check (Lean / Coq)",
        L_VER, E_VER, fs=9.5, weight="normal")

    # data path
    arrow(ax, (3.10, by + bh / 2), (3.72, by + bh / 2), color=INK, lw=1.6)
    arrow(ax, (6.27, by + bh / 2), (6.90, by + bh / 2), color=INK, lw=1.6)

    # endpoint labels
    ax.text(0.55, by + bh + 0.30, "informal problem", fontsize=8.5,
            color=MUTED, ha="left")
    ax.text(9.45, by + bh + 0.30, "formal verdict", fontsize=8.5,
            color=MUTED, ha="right")

    # the anchoring gap annotation
    ax.annotate("", xy=(3.55, by - 0.42), xytext=(3.55, by + bh + 0.10),
                arrowprops=dict(arrowstyle="-", color=E_RED, lw=1.0,
                                linestyle=":"))
    ax.annotate("", xy=(6.42, by - 0.42), xytext=(6.42, by + bh + 0.10),
                arrowprops=dict(arrowstyle="-", color=E_RED, lw=1.0,
                                linestyle=":"))
    arrow(ax, (3.55, by - 0.42), (6.42, by - 0.42), color=E_RED, lw=1.3,
          style="<|-|>")
    ax.text(5.00, by - 0.68, "the anchoring gap", fontsize=9, color=E_RED,
            ha="center", weight="bold")
    ax.text(5.00, by - 0.98,
            "the informal claim a user asked about\n"
            "$\\neq$ the formal claim the kernel certifies",
            fontsize=8, color=MUTED, ha="center", linespacing=1.4)

    # feedback path (omitted by current systems)
    arrow(ax, (8.18, by), (1.83, by), color=NOTE_EDGE, lw=1.3, dashed=True,
          rad=0.16)
    ax.text(5.00, 1.12,
            "audit / re-reduction feedback path\n"
            "(largely absent in current systems)",
            fontsize=8.5, color=NOTE_EDGE, ha="center",
            style="italic", linespacing=1.4)

    # blindness annotation
    ax.text(5.20, 3.18,
            "Layer 3 can see only the formal object.\n"
            "Layer 2 failures are invisible to it.",
            fontsize=8.5, color=E_RED, ha="center", va="center",
            style="italic", linespacing=1.4,
            bbox=dict(boxstyle="round,pad=0.34", facecolor="white",
                      edgecolor=E_RED, linewidth=0.9, alpha=0.96))

    fig.subplots_adjust(left=0.005, right=0.995, top=0.995, bottom=0.005)
    fig.savefig(os.path.join(OUT, "fig1_architecture.pdf"),
                format="pdf", transparent=False, facecolor="white")
    plt.close(fig)
    print("wrote fig1_architecture.pdf")


# ===========================================================================
# Figure 2: defect origination
# ===========================================================================
def figure2():
    fig, ax = plt.subplots(figsize=(8.2, 4.4))
    ax.set_xlim(0, 10); ax.set_ylim(0, 5.4); ax.axis("off")

    # pipeline spine
    box(ax, 0.45, 4.15, 2.4, 0.85, "Layer 1\nGeneration", L_GEN, E_GEN, fs=9.5)
    box(ax, 3.70, 4.15, 2.4, 0.85, "Layer 2\nSemantic Reduction",
        L_RED, E_RED, fs=9.5, weight="bold")
    box(ax, 6.95, 4.15, 2.4, 0.85, "Layer 3\nVerification",
        L_VER, E_VER, fs=9.5)
    arrow(ax, (2.85, 4.575), (3.70, 4.575), color=INK, lw=1.5)
    arrow(ax, (6.10, 4.575), (6.95, 4.575), color=INK, lw=1.5)

    ax.text(9.72, 4.575, "verdict", fontsize=8, color=MUTED,
            ha="right", va="center")

    # the six invisible defects, fanning out from Layer 2
    defects_invisible = [
        ("D1", "Type coercion"),
        ("D2", "Quantifier drift"),
        ("D3", "Hidden hypothesis"),
        ("D4", "Lemma mismatch"),
        ("D5", "Boundary loss"),
        ("D6", "Notational collision"),
    ]
    y0 = 3.25
    for i, (tag, name) in enumerate(defects_invisible):
        y = y0 - i * 0.47
        # connector from layer2 down to defect row
        arrow(ax, (4.90, 4.15), (2.60, y + 0.16), color=E_RED, lw=0.85,
              style="-", rad=0.05)
        ax.text(1.55, y + 0.16, f"{tag}", fontsize=9.5, color=E_RED,
                ha="right", va="center", weight="bold")
        ax.text(1.75, y + 0.16, name, fontsize=9, color=INK,
                ha="left", va="center")
        # defect propagates to the boundary undetected
        arrow(ax, (3.55, y + 0.16), (9.55, y + 0.16), color=E_RED, lw=0.8,
              style="-|>", dashed=True)
        ax.text(9.62, y + 0.16, "✗", fontsize=11, color=E_RED,
                ha="left", va="center", weight="bold")

    # D7 partially visible
    yd7 = y0 - 6 * 0.47 - 0.10
    ax.text(1.55, yd7 + 0.16, "D7", fontsize=9.5, color=NOTE_EDGE,
            ha="right", va="center", weight="bold")
    ax.text(1.75, yd7 + 0.16, "Unanchored assertion", fontsize=9,
            color=INK, ha="left", va="center")
    arrow(ax, (3.55, yd7 + 0.16), (9.55, yd7 + 0.16), color=NOTE_EDGE,
          lw=0.9, style="-|>", dashed=True)
    ax.text(9.62, yd7 + 0.16, "~", fontsize=12, color=NOTE_EDGE,
            ha="left", va="center", weight="bold")

    # legend / reading aid
    ax.text(1.55, yd7 - 0.42,
            "✗  invisible to Layer 3        "
            "~  visible only if the assumption is made explicit (SRIR)",
            fontsize=8, color=MUTED, ha="left", va="center")

    ax.text(1.55, 0.28,
            "Six of seven defect classes originate in Layer 2 and survive "
            "to the interface undetected.",
            fontsize=9, color=E_RED, ha="left", va="center", style="italic")

    fig.subplots_adjust(left=0.005, right=0.995, top=0.995, bottom=0.005)
    fig.savefig(os.path.join(OUT, "fig2_defects.pdf"),
                format="pdf", transparent=False, facecolor="white")
    plt.close(fig)
    print("wrote fig2_defects.pdf")


if __name__ == "__main__":
    figure1()
    figure2()
    print("done")
