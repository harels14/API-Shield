import json
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec

RESULTS_FILE = "results/metrics.json"
CHARTS_DIR = "results/charts"
os.makedirs(CHARTS_DIR, exist_ok=True)

BG    = "#0d1117"
PANEL = "#161b22"
BORDER= "#30363d"
WHITE = "#e6edf3"
MUTED = "#8b949e"

BLUE   = "#58a6ff"   # Layer 1 entities
PURPLE = "#bc8cff"   # Layer 2 entities
GREEN  = "#3fb950"   # combined / positive
YELLOW = "#e3b341"

LAYER1_TYPES = {"ISRAELI_ID", "CREDIT_CARD", "PHONE_NUMBER", "EMAIL"}
LAYER2_TYPES = {"PERSON", "LOCATION", "DATE"}


def style(ax, title=None):
    ax.set_facecolor(PANEL)
    ax.tick_params(colors=WHITE, labelsize=9)
    ax.xaxis.label.set_color(WHITE)
    ax.yaxis.label.set_color(WHITE)
    for spine in ax.spines.values():
        spine.set_color(BORDER)
    if title:
        ax.set_title(title, color=WHITE, fontsize=12, pad=10)


def load():
    with open(RESULTS_FILE) as f:
        return json.load(f)


# ── Chart 1: Coverage by Layer ────────────────────────────────────────────────
def chart_coverage(metrics):
    """
    Shows clearly what each layer detects.
    Layer 1 entities: 100% — shown in blue.
    Layer 2 entities: only detected with Both layers — shown in purple.
    """
    all_types = [k for k in metrics if not k.startswith("_")]
    l1_types  = [t for t in all_types if t in LAYER1_TYPES]
    l2_types  = [t for t in all_types if t in LAYER2_TYPES]

    fig, axes = plt.subplots(1, 2, figsize=(14, 5), facecolor=BG)
    fig.suptitle("What Each Layer Detects", color=WHITE, fontsize=15, y=1.02)

    for ax, types, color, subtitle, layer_key in [
        (axes[0], l1_types, BLUE,   "Layer 1 — Regex (Fast & Deterministic)", "layer1"),
        (axes[1], l2_types, PURPLE, "Layer 2 — NLP / Presidio (Adds Coverage)", "both"),
    ]:
        style(ax, subtitle)
        f1_vals = [metrics[t][layer_key]["f1"] for t in types]
        bars = ax.barh(types, f1_vals, color=color, alpha=0.9, height=0.5)

        for bar, val in zip(bars, f1_vals):
            ax.text(min(val + 0.01, 0.97), bar.get_y() + bar.get_height() / 2,
                    f"{val:.0%}", va="center", color=WHITE, fontsize=11, fontweight="bold")

        ax.set_xlim(0, 1.15)
        ax.set_xlabel("F1 Score")
        ax.axvline(1.0, color=BORDER, linewidth=1, linestyle="--")
        ax.tick_params(axis="y", colors=WHITE, labelsize=10)

    plt.tight_layout()
    plt.savefig(f"{CHARTS_DIR}/coverage_by_layer.png", dpi=150, bbox_inches="tight", facecolor=BG)
    plt.close()
    print("  Saved coverage_by_layer.png")


# ── Chart 2: Combined F1 — all types ─────────────────────────────────────────
def chart_combined_f1(metrics):
    """
    Full picture: F1 for all entity types using both layers.
    Color-coded by which layer is responsible for detection.
    """
    all_types = sorted([k for k in metrics if not k.startswith("_")])
    f1_vals   = [metrics[t]["both"]["f1"] for t in all_types]
    colors    = [BLUE if t in LAYER1_TYPES else PURPLE for t in all_types]

    fig, ax = plt.subplots(figsize=(12, 5), facecolor=BG)
    style(ax, "Combined F1 Score per Entity Type (Both Layers)")

    bars = ax.bar(all_types, f1_vals, color=colors, alpha=0.9, width=0.55)

    for bar, val in zip(bars, f1_vals):
        ax.text(bar.get_x() + bar.get_width() / 2, val + 0.01,
                f"{val:.0%}", ha="center", va="bottom", color=WHITE, fontsize=10)

    ax.set_ylim(0, 1.18)
    ax.set_ylabel("F1 Score")
    ax.axhline(1.0, color=BORDER, linewidth=0.8, linestyle="--")
    ax.tick_params(axis="x", colors=WHITE, labelsize=10, rotation=10)

    l1_patch = mpatches.Patch(color=BLUE,   label="Detected by Layer 1 (Regex)")
    l2_patch = mpatches.Patch(color=PURPLE, label="Added by Layer 2 (NLP)")
    ax.legend(handles=[l1_patch, l2_patch], facecolor=PANEL, labelcolor=WHITE, fontsize=10)

    plt.tight_layout()
    plt.savefig(f"{CHARTS_DIR}/combined_f1.png", dpi=150, bbox_inches="tight", facecolor=BG)
    plt.close()
    print("  Saved combined_f1.png")


# ── Chart 3: Latency trade-off ────────────────────────────────────────────────
def chart_latency(metrics):
    """
    Latency: Layer 1 alone vs Both layers.
    Annotated with what the extra latency buys you.
    """
    meta = metrics.get("_meta", {}).get("latency", {})
    l1_ms   = meta.get("layer1_avg_ms", 0)
    both_ms = meta.get("both_avg_ms", 0)
    added   = round(both_ms - l1_ms, 1)

    fig, ax = plt.subplots(figsize=(7, 5), facecolor=BG)
    style(ax, "Average Response Latency")

    bars = ax.bar(["Layer 1\n(Regex only)", "Both Layers\n(Regex + NLP)"],
                  [l1_ms, both_ms], color=[BLUE, PURPLE], width=0.4, alpha=0.9)

    for bar, val in zip(bars, [l1_ms, both_ms]):
        ax.text(bar.get_x() + bar.get_width() / 2, val + 1,
                f"{val:.0f} ms", ha="center", va="bottom", color=WHITE, fontsize=13, fontweight="bold")

    if added > 0:
        ax.annotate(
            f"+{added} ms for\nPERSON, LOCATION, DATE",
            xy=(1, both_ms), xytext=(1.15, both_ms * 0.6),
            color=YELLOW, fontsize=9,
            arrowprops=dict(arrowstyle="->", color=YELLOW, lw=1.2),
        )

    ax.set_ylabel("Avg Latency (ms)")
    ax.set_ylim(0, max(both_ms * 1.5, 50))
    ax.tick_params(axis="x", colors=WHITE)

    plt.tight_layout()
    plt.savefig(f"{CHARTS_DIR}/latency.png", dpi=150, bbox_inches="tight", facecolor=BG)
    plt.close()
    print("  Saved latency.png")


# ── Chart 4: Summary dashboard ────────────────────────────────────────────────
def chart_summary(metrics):
    """
    One-glance summary: overall F1, entity types covered, latency.
    """
    meta       = metrics.get("_meta", {})
    overall    = meta.get("overall_macro_f1", {}).get("both", 0)
    latency    = meta.get("latency", {}).get("both_avg_ms", 0)
    n_types    = len([k for k in metrics if not k.startswith("_")])
    dataset_sz = meta.get("dataset_size", 0)

    fig = plt.figure(figsize=(12, 4), facecolor=BG)
    gs  = GridSpec(1, 3, figure=fig, wspace=0.05)

    cards = [
        (f"{overall:.0%}", "Overall F1\n(Both Layers)", GREEN),
        (f"{n_types}",     "Entity Types\nCovered",     BLUE),
        (f"{latency:.0f}ms", "Avg Latency\n(Both Layers)", PURPLE),
    ]

    for i, (value, label, color) in enumerate(cards):
        ax = fig.add_subplot(gs[i])
        ax.set_facecolor(PANEL)
        for spine in ax.spines.values():
            spine.set_color(color)
            spine.set_linewidth(2)
        ax.set_xticks([])
        ax.set_yticks([])

        ax.text(0.5, 0.58, value, ha="center", va="center",
                transform=ax.transAxes, color=color,
                fontsize=38, fontweight="bold")
        ax.text(0.5, 0.22, label, ha="center", va="center",
                transform=ax.transAxes, color=MUTED,
                fontsize=11, linespacing=1.6)

    fig.suptitle(f"API Shield — Accuracy Report  ·  {dataset_sz} test examples",
                 color=WHITE, fontsize=13, y=1.03)

    plt.savefig(f"{CHARTS_DIR}/summary.png", dpi=150, bbox_inches="tight", facecolor=BG)
    plt.close()
    print("  Saved summary.png")


if __name__ == "__main__":
    metrics = load()
    print("Generating charts...")
    chart_coverage(metrics)
    chart_combined_f1(metrics)
    chart_latency(metrics)
    chart_summary(metrics)
    print(f"\nAll charts saved to {CHARTS_DIR}/")
