#!/usr/bin/env python3
"""Generate JCDL paper figures and LaTeX tables from the final result CSVs."""

from __future__ import annotations

import textwrap
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.lines import Line2D
from matplotlib.patches import FancyBboxPatch, Rectangle


ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper"
DATA = ROOT / "data/derived/database/19_jcdl_revision"
WWWDATA = ROOT / "data/derived/database/16_www_revision"
VALID18 = ROOT / "data/derived/database/18_www_reviewer_requested_validations"
FIG = PAPER / "figures"
TAB = PAPER / "tables"

DUKE_NAVY = "#012169"
DUKE_ROYAL = "#00539B"
BLUE = "#0072CE"
LIGHT_BLUE = "#72A0C1"
CYAN = "#41B6E6"
TEAL = "#76B7B2"
GREY = "#7A869A"
LIGHT_GREY = "#E7ECF2"
DARK = "#1F2937"
ORANGE = "#D67C2C"
RED = "#B64A4A"

F4P = {
    "blue_main": "#0F4D92",
    "blue_secondary": "#3775BA",
    "green_1": "#DDF3DE",
    "green_2": "#AADCA9",
    "green_3": "#8BCF8B",
    "red_1": "#F6CFCB",
    "red_2": "#E9A6A1",
    "red_strong": "#B64342",
    "neutral": "#CFCECE",
    "neutral_dark": "#4D4D4D",
    "teal": "#42949E",
    "violet": "#9A4D8E",
    "highlight": "#FFD700",
}


def apply_f4p_style(font_size: int = 14, axes_linewidth: float = 1.9) -> None:
    """Apply a figures4papers-inspired publication style."""
    plt.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["DejaVu Sans", "Arial", "Helvetica", "sans-serif"],
            "font.size": font_size,
            "axes.labelsize": font_size,
            "axes.titlesize": font_size,
            "xtick.labelsize": font_size - 2,
            "ytick.labelsize": font_size - 2,
            "legend.fontsize": font_size - 2,
            "axes.linewidth": axes_linewidth,
            "axes.spines.right": False,
            "axes.spines.top": False,
            "legend.frameon": False,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
        }
    )


def polish_axis(ax, grid_axis: str = "x") -> None:
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    ax.spines["left"].set_linewidth(1.4)
    ax.spines["bottom"].set_linewidth(1.4)
    ax.spines["left"].set_color("#272727")
    ax.spines["bottom"].set_color("#272727")
    ax.tick_params(axis="both", length=3, width=1.2, colors="#272727")
    if grid_axis:
        ax.grid(axis=grid_axis, linestyle="-", color="#E2E6EA", linewidth=0.9, zorder=0)


def draw_percent_heatmap(ax, matrix, row_labels, col_labels, title, vmax=100, fontsize=9):
    cmap = LinearSegmentedColormap.from_list(
        "f4p_blue_green",
        ["#F7FAFC", "#DCEAF7", "#92BDE6", "#3775BA", "#0F4D92"],
    )
    im = ax.imshow(matrix, cmap=cmap, vmin=0, vmax=vmax, aspect="auto", zorder=1)
    ax.set_xticks(np.arange(len(col_labels)))
    ax.set_xticklabels(col_labels, rotation=32, ha="right", rotation_mode="anchor")
    ax.set_yticks(np.arange(len(row_labels)))
    ax.set_yticklabels(row_labels)
    ax.set_title(title, loc="left", fontweight="bold", color=F4P["blue_main"], pad=8)
    ax.set_xticks(np.arange(-0.5, len(col_labels), 1), minor=True)
    ax.set_yticks(np.arange(-0.5, len(row_labels), 1), minor=True)
    ax.grid(which="minor", color="white", linewidth=1.2)
    ax.tick_params(which="minor", bottom=False, left=False)
    for spine in ax.spines.values():
        spine.set_visible(False)
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            value = float(matrix[i, j])
            if value < 0.05:
                label = "0"
            elif value < 1:
                label = "<1"
            else:
                label = f"{value:.0f}"
            color = "white" if value >= 55 else DARK
            ax.text(j, i, label, ha="center", va="center", fontsize=fontsize, fontweight="bold", color=color)
    return im


def label_hbars(ax, values, y_positions, xpad=1.0, fontsize=11, color=DARK) -> None:
    for value, y in zip(values, y_positions):
        text = "<0.2%" if 0 < float(value) < 0.2 else f"{float(value):.1f}%"
        ax.text(float(value) + xpad, y, text, va="center", ha="left", fontsize=fontsize, color=color)


def ensure_dirs() -> None:
    FIG.mkdir(parents=True, exist_ok=True)
    TAB.mkdir(parents=True, exist_ok=True)


def clean_label(text: str) -> str:
    text = str(text).replace("_", " ")
    text = text.replace("paper hf exact edge::", "")
    text = text.replace("paper text ", "")
    text = text.replace("jcdl ", "")
    text = text.replace("release package ", "")
    return text.title()


def latex_escape(value) -> str:
    text = str(value)
    text = text.replace("rows.;", "rows;")
    replacements = {
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def display_curation_function(value: str) -> str:
    mapping = {
        "Bibliographic control": "Bibliographic and linkage control",
        "Reuse and preservation triage": "Release-package readiness",
        "Reuse and preservation readiness": "Release-package readiness",
    }
    return mapping.get(str(value), str(value))


def display_metadata_field(value: str) -> str:
    mapping = {
        "Artifact role": "Artifact role label (assigned)",
        "Variant type": "Variant/package label (assigned)",
    }
    return mapping.get(str(value), str(value))


def clean_key_result(value: str) -> str:
    text = str(value)
    text = text.replace("paper exact HF edge", "matched paper-HF evidence")
    text = text.replace("concrete release, and link criteria", "asset-level release, and link criteria")
    text = text.replace("high curatability 6.1%", "high-curatability threshold 6.1%")
    text = text.replace(
        "high or operational curatability 18.1% under the operational rubric",
        "operational P+R threshold 18.1% combines usable provenance with concrete release evidence",
    )
    return text.replace("rows.;", "rows;")


def display_alignment_signal(value: str) -> str:
    mapping = {
        "paper_text_huggingface_link": "HF link in paper text",
        "paper_text_github_link": "GitHub or code-hosting link in paper text",
        "paper_hf_exact_edge::exact_model_mention": "Matched exact model mention",
        "paper_hf_exact_edge::family_size_fuzzy_match": "Low-confidence fuzzy family/size match",
        "paper_hf_exact_edge::model_card_arxiv_ref": "Model-card arXiv backlink",
        "paper_hf_exact_edge::all_methods": "All matched paper-HF evidence combined",
    }
    return mapping.get(str(value), clean_label(value))


def display_sensitivity_test(value: str) -> str:
    mapping = {
        "strict_joint_high": "Strict joint high",
        "operational_current": "Operational rubric",
        "operational_requires_link": "Operational plus direct link",
        "full_recipe_with_link": "Full recipe plus direct link",
        "any_useful_signal": "Any useful signal",
    }
    return mapping.get(str(value), clean_label(value))


def display_curatability_rule(value: str) -> str:
    mapping = {
        "provenance>=2 AND release>=3 AND link>=1": "provenance >= 2; release >= 3; link >= 1",
        "provenance>=2 AND release>=2": "provenance >= 2; release >= 2",
        "provenance>=2 AND release>=2 AND link>=1": "provenance >= 2; release >= 2; link >= 1",
        "provenance>=2 AND release>=4 AND link>=1": "provenance >= 2; release >= 4; link >= 1",
        "category != low_curatability": "category is not low curatability",
    }
    return mapping.get(str(value), str(value))


def display_query_subset(value: str) -> str:
    mapping = {
        "all_query_buckets": "All query buckets",
        "exclude_deployment_format_bucket": "Exclude deployment-format bucket",
        "exclude_derivation_or_tuning_bucket": "Exclude derivation/tuning bucket",
        "exclude_deployment_and_derivation_buckets": "Exclude deployment and derivation buckets",
        "exclude_family_name_bucket": "Exclude family-name bucket",
        "size_domain_family_only": "Size/domain/family only",
    }
    return mapping.get(str(value), clean_label(value))


def display_query_bucket_list(value: str) -> str:
    text = str(value)
    mapping = {
        "none": "None",
        "deployment_format": "Deployment format",
        "derivation_or_tuning": "Derivation/tuning",
        "family_name": "Family name",
        "deployment_format, derivation_or_tuning": "Deployment format; derivation/tuning",
        "deployment_format, derivation_or_tuning, other_or_unmapped": "Deployment format; derivation/tuning; other/unmapped",
    }
    return mapping.get(text, clean_label(text))


def savefig(name: str) -> None:
    for ext in ["pdf", "png"]:
        plt.savefig(FIG / f"{name}.{ext}", bbox_inches="tight", dpi=300)
    plt.close()


def style_axis(ax) -> None:
    ax.grid(axis="x", linestyle="-", color="#C8D0DA", alpha=0.7, zorder=0)
    ax.grid(axis="y", visible=False)
    for spine in ["top", "right", "left"]:
        ax.spines[spine].set_visible(False)
    ax.spines["bottom"].set_color("#4B5563")
    ax.tick_params(axis="both", labelsize=9, colors=DARK)


def style_ygrid_axis(ax) -> None:
    ax.grid(axis="y", linestyle="-", color="#C8D0DA", alpha=0.7, zorder=0)
    ax.grid(axis="x", visible=False)
    for spine in ["top", "right", "left"]:
        ax.spines[spine].set_visible(False)
    ax.spines["bottom"].set_color("#4B5563")
    ax.tick_params(axis="both", labelsize=8.6, colors=DARK)


def draw_centered_funnel(ax, labels, values, colors, max_percent, title, counts=None) -> None:
    """Draw a compact evidence ladder where width encodes share and vertical order encodes strength."""
    max_width = 6.6
    n = len(labels)
    ax.axis("off")
    for i, (label, value, color) in enumerate(zip(labels, values, colors)):
        y = n - 1 - i
        width = max(max_width * (float(value) / max_percent), 0.08)
        patch = FancyBboxPatch(
            (-width / 2, y - 0.29),
            width,
            0.58,
            boxstyle="round,pad=0.01,rounding_size=0.08",
            facecolor=color,
            edgecolor="white",
            linewidth=1.35,
            zorder=2,
        )
        ax.add_patch(patch)
        ax.plot([-max_width / 2, max_width / 2], [y - 0.42, y - 0.42], color="#E4E9F0", lw=0.7, zorder=0)
        ax.text(
            -max_width / 2 - 0.28,
            y,
            textwrap.fill(label, 18),
            ha="right",
            va="center",
            fontsize=8.1,
            color=DARK,
        )
        value_text = "<0.2%" if 0 < value < 0.2 else f"{value:.1f}%"
        if counts is not None:
            value_text = f"{value_text}\n({int(counts[i]):,})"
        ax.text(
            width / 2 + 0.20,
            y,
            value_text,
            ha="left",
            va="center",
            fontsize=8.1,
            fontweight="bold" if i in {0, n - 1} else "normal",
            color=DARK,
        )
    ax.set_xlim(-max_width / 2 - 2.8, max_width / 2 + 2.2)
    ax.set_ylim(-0.75, n - 0.1)
    ax.set_title(title, fontsize=10.5, fontweight="bold", loc="left", color=DUKE_NAVY)


def draw_pipeline() -> None:
    fig, ax = plt.subplots(figsize=(15.8, 5.4))
    ax.set_xlim(0, 16.2)
    ax.set_ylim(0, 5.7)
    ax.axis("off")

    def box(x, y, w, h, title, body, color, edge=DUKE_NAVY, fontsize=8.2, title_size=9.6):
        patch = FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle="round,pad=0.02,rounding_size=0.08",
            facecolor=color,
            edgecolor=edge,
            linewidth=1.4,
        )
        ax.add_patch(patch)
        ax.text(x + 0.14, y + h - 0.18, title, fontsize=title_size, fontweight="bold", color=DARK, va="top")
        ax.text(
            x + 0.14,
            y + h - 0.62,
            "\n".join(textwrap.wrap(body, max(16, int(w * 12)))),
            fontsize=fontsize,
            color=DARK,
            va="top",
        )

    headers = [
        (0.25, "Public record sources"),
        (3.3, "Evidence extracted"),
        (6.45, "Curation questions"),
        (13.05, "Checks"),
    ]
    for x, label in headers:
        ax.text(x, 5.35, label, fontsize=11, fontweight="bold", color=DUKE_NAVY)

    box(0.25, 3.55, 2.35, 1.1, "Model-hub records", "191,375 HF repository records", "#DDEBFA")
    box(0.25, 1.55, 2.35, 1.1, "Scholarly records", "2,729 paper records; 2,214 main-analysis records", "#E5F3F2")

    evidence = [
        (3.25, 4.00, "Artifact fields", "role, variant, owner, tags"),
        (3.25, 2.85, "Paper links", "HF/GitHub links; paper backlinks"),
        (3.25, 1.70, "Provenance signals", "upstream fields; family evidence"),
        (3.25, 0.55, "Release signals", "code, weights, adapters, data"),
    ]
    for x, y, title, body in evidence:
        box(x, y, 2.4, 0.92, title, body, "#F2F6FC", fontsize=7.1, title_size=8.8)

    questions = [
        ("RQ1", "Artifact identity"),
        ("RQ2", "Bibliographic linkage"),
        ("RQ3", "Provenance sufficiency"),
        ("RQ4", "Release package"),
        ("RQ5", "Curation readiness"),
    ]
    q_colors = ["#DDEBFA", "#D8EEF3", "#D9EFEA", "#F4E3CD", "#EEF0F5"]
    for i, ((rq, label), color) in enumerate(zip(questions, q_colors)):
        x = 6.15 + i * 1.25
        box(x, 2.05, 1.12, 1.62, rq, label, color, fontsize=6.8, title_size=8.8)

    box(13.0, 3.55, 2.45, 1.1, "Expert audits", "300 repository-role rows; 200 lineage rows; 50 release rows", "#F7F2E8")
    box(13.0, 1.55, 2.45, 1.1, "Sensitivity checks", "query buckets, alignment methods, rubric thresholds", "#EEF0F5")

    for y in [4.1, 2.1]:
        ax.annotate("", xy=(3.1, y), xytext=(2.62, y), arrowprops=dict(arrowstyle="->", lw=1.35, color=DARK))
    for y in [4.46, 3.31, 2.16, 1.01]:
        ax.annotate("", xy=(6.18, 2.85), xytext=(5.63, y), arrowprops=dict(arrowstyle="->", lw=1.05, color="#4B5563"))
    ax.annotate("", xy=(12.9, 4.1), xytext=(12.45, 3.1), arrowprops=dict(arrowstyle="->", lw=1.2, color=DARK))
    ax.annotate("", xy=(12.9, 2.1), xytext=(12.45, 3.1), arrowprops=dict(arrowstyle="->", lw=1.2, color=DARK))
    savefig("fig1_pipeline")


def draw_metadata_completeness() -> None:
    apply_f4p_style(font_size=12, axes_linewidth=1.8)
    meta = pd.read_csv(DATA / "metadata_completeness_matrix.csv").copy()
    field_order = [
        "Task descriptors",
        "Model family label",
        "Explicit upstream model",
        "Typed upstream relation",
        "License tag signal",
        "Scholarly reference",
        "Domain descriptors",
    ]
    field_labels = {
        "Task descriptors": "Task",
        "Model family label": "Family",
        "Explicit upstream model": "Upstream",
        "Typed upstream relation": "Typed\nupstream",
        "License tag signal": "License",
        "Scholarly reference": "Paper\nref.",
        "Domain descriptors": "Domain",
    }
    meta = meta[meta["curation_field"].isin(field_order)].copy()
    meta["curation_field"] = pd.Categorical(meta["curation_field"], field_order, ordered=True)
    meta = meta.sort_values("curation_field", ascending=True)
    meta["label"] = meta["curation_field"].map(field_labels)

    fig, axes = plt.subplots(
        ncols=2,
        figsize=(13.6, 4.35),
        gridspec_kw={"width_ratios": [1.02, 1.18]},
    )

    ax = axes[0]
    y = np.arange(len(meta))
    values = meta["share_percent"].to_numpy(dtype=float)
    colors = [
        F4P["blue_secondary"],
        F4P["green_3"],
        F4P["green_2"],
        F4P["green_2"],
        F4P["teal"],
        F4P["neutral_dark"],
        F4P["red_2"],
    ]
    bars = ax.barh(
        y,
        values,
        color=colors,
        edgecolor="black",
        linewidth=1.15,
        height=0.70,
        zorder=3,
    )
    ax.bar_label(bars, labels=[f"{v:.1f}%" for v in values], padding=4, fontsize=10.5, fontweight="bold")
    ax.set_yticks(y)
    ax.set_yticklabels(meta["label"])
    ax.invert_yaxis()
    ax.set_xlim(0, 72)
    ax.set_xlabel("Repository records (%)")
    ax.set_title("(a) Curation metadata fields", loc="left", fontweight="bold", color=F4P["blue_main"], pad=8)
    polish_axis(ax, "x")

    ax = axes[1]
    audit = pd.read_csv(VALID18 / "hf_repo_artifact_typing_precision.csv").copy()
    role_order = ["finetune", "adapter_lora", "quantized_or_deployment", "base", "merge_mixed"]
    role_labels = ["Fine-tune", "Adapter/\nLoRA", "Quantized/\ndeploy", "Base\ncheckpoint", "Merge/\nmixed"]
    audit["repo_type"] = pd.Categorical(audit["repo_type"], role_order, ordered=True)
    audit = audit.sort_values("repo_type")
    x = np.arange(len(audit))
    strict = audit["strict_precision"].to_numpy(dtype=float) * 100
    usable = audit["usable_precision"].to_numpy(dtype=float) * 100
    width = 0.36
    strict_bars = ax.bar(
        x - width / 2,
        strict,
        width,
        color=F4P["blue_main"],
        edgecolor="black",
        linewidth=1.25,
        label="Strict",
        zorder=3,
    )
    usable_bars = ax.bar(
        x + width / 2,
        usable,
        width,
        color=F4P["green_3"],
        edgecolor="black",
        linewidth=1.25,
        hatch="/",
        label="Usable",
        zorder=3,
    )
    for xi, s, u in zip(x, strict, usable):
        if abs(s - u) < 0.5:
            ax.text(xi, max(s, u) + 2.5, f"{s:.0f}%", ha="center", va="bottom", fontsize=10.2, fontweight="bold")
        else:
            ax.text(xi - width / 2, s + 2.2, f"{s:.0f}%", ha="center", va="bottom", fontsize=9.6, fontweight="bold")
            ax.text(xi + width / 2, u + 2.2, f"{u:.0f}%", ha="center", va="bottom", fontsize=9.6, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(role_labels, fontsize=10.2)
    ax.set_ylim(45, 111)
    ax.set_ylabel("Audit support (%)")
    ax.set_title("(b) Role-label audit", loc="left", fontweight="bold", color=F4P["blue_main"], pad=8)
    ax.legend(loc="lower center", bbox_to_anchor=(0.50, -0.22), ncol=2, handlelength=1.1, columnspacing=1.0)
    polish_axis(ax, "y")

    fig.tight_layout(pad=1.35, w_pad=1.8)
    savefig("fig2_metadata_completeness")


def draw_provenance_alignment() -> None:
    apply_f4p_style(font_size=12, axes_linewidth=1.6)
    prov = pd.read_csv(DATA / "jcdl_provenance_sufficiency_by_mechanism.csv")
    prov_order = [
        "1_exact_paper_hf_repo_edge",
        "3_inventory_backed_family_signal",
        "4_weak_or_context_family_signal",
        "5_no_usable_family_or_provenance_signal",
    ]
    prov_labels = {
        "1_exact_paper_hf_repo_edge": "Matched\nHF",
        "3_inventory_backed_family_signal": "Inventory\nfamily",
        "4_weak_or_context_family_signal": "Weak\nfamily",
        "5_no_usable_family_or_provenance_signal": "No usable\nsignal",
    }
    mech_order = [
        "distillation_compression",
        "peft_adapter",
        "evaluation_analysis",
        "training_method",
        "deployment_system",
        "architecture",
        "domain_specialization",
    ]
    mech_labels = ["Distill/\ncompress", "PEFT/\nadapter", "Eval/\nanalysis", "Training\nmethod", "Deploy\nsystem", "Architecture", "Domain\nspecial."]
    prov_heat = (
        prov.pivot(index="mechanism", columns="provenance_sufficiency_tier", values="share_percent")
        .reindex(index=mech_order, columns=prov_order)
        .fillna(0)
    )

    align = pd.read_csv(DATA / "jcdl_paper_repo_alignment_decomposition.csv")
    align_order = [
        "paper_text_github_link",
        "paper_text_huggingface_link",
        "paper_hf_exact_edge::all_methods",
        "paper_hf_exact_edge::exact_model_mention",
        "paper_hf_exact_edge::model_card_arxiv_ref",
    ]
    align_labels = {
        "paper_text_github_link": "GitHub/code link",
        "paper_text_huggingface_link": "HF link in paper",
        "paper_hf_exact_edge::all_methods": "Matched paper-HF",
        "paper_hf_exact_edge::exact_model_mention": "Exact model mention",
        "paper_hf_exact_edge::model_card_arxiv_ref": "Model-card backlink",
    }
    align = align[align["alignment_signal"].isin(align_order)].copy()
    align["alignment_signal"] = pd.Categorical(align["alignment_signal"], align_order, ordered=True)
    align = align.sort_values("alignment_signal", ascending=False)
    align["label"] = align["alignment_signal"].map(align_labels)

    fig, axes = plt.subplots(ncols=2, figsize=(12.8, 4.75), gridspec_kw={"width_ratios": [1.12, 1.0]})

    ax = axes[0]
    stack_colors = ["#0F4D92", "#8BCF8B", "#F6CFCB", "#CFCECE"]
    left = np.zeros(len(prov_heat))
    y_stack = np.arange(len(prov_heat))
    for idx, col in enumerate(prov_order):
        values = prov_heat[col].to_numpy(dtype=float)
        bars = ax.barh(
            y_stack,
            values,
            left=left,
            color=stack_colors[idx],
            edgecolor="black",
            linewidth=0.9,
            height=0.72,
            zorder=3,
            label=prov_labels[col].replace("\n", " "),
        )
        for bar, value in zip(bars, values):
            if value >= 12:
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_y() + bar.get_height() / 2,
                    f"{value:.0f}",
                    ha="center",
                    va="center",
                    fontsize=8.6,
                    fontweight="bold",
                    color="white" if idx == 0 else DARK,
                    zorder=4,
                )
            elif idx == 0 and value >= 2:
                ax.text(
                    bar.get_x() + bar.get_width() + 1.2,
                    bar.get_y() + bar.get_height() / 2,
                    f"{value:.0f}",
                    ha="left",
                    va="center",
                    fontsize=8.2,
                    fontweight="bold",
                    color=DARK,
                    zorder=4,
                )
        left += values
    ax.set_yticks(y_stack)
    ax.set_yticklabels(mech_labels)
    ax.invert_yaxis()
    ax.set_xlim(0, 100)
    ax.set_xlabel("Mechanism-specific paper records (%)")
    ax.set_ylabel("Mechanism")
    ax.set_title("(a) Upstream evidence by mechanism", loc="left", fontweight="bold", color=F4P["blue_main"], pad=8)
    ax.legend(loc="upper center", bbox_to_anchor=(0.50, -0.18), ncol=2, fontsize=8.6, handlelength=1.3, columnspacing=1.2)
    polish_axis(ax, "x")

    ax = axes[1]
    y = np.arange(len(align))
    values = align["main_record_share_percent"].to_numpy(dtype=float)
    colors = [F4P["teal"], F4P["blue_secondary"], F4P["blue_main"], F4P["green_3"], F4P["neutral_dark"]]
    bar_x = np.arange(len(align))
    bars = ax.bar(
        bar_x,
        values,
        color=colors,
        edgecolor="black",
        linewidth=1.35,
        width=0.68,
        zorder=3,
    )
    ax.bar_label(bars, labels=[f"{v:.1f}%" for v in values], padding=4, fontsize=11.5, fontweight="bold")
    label_map = {
        "GitHub/code link": "GitHub/\ncode",
        "HF link in paper": "HF link\nin paper",
        "Matched paper-HF": "Matched\npaper-HF",
        "Exact model mention": "Exact\nmention",
        "Model-card backlink": "Card\nbacklink",
    }
    ax.set_xticks(bar_x)
    ax.set_xticklabels([label_map.get(v, v) for v in align["label"]], fontsize=9.7)
    ax.set_ylim(0, 34)
    ax.set_ylabel("Main-analysis paper records (%)")
    ax.set_title("(b) Alignment signals", loc="left", fontweight="bold", color=F4P["blue_main"], pad=8)
    polish_axis(ax, "y")

    fig.tight_layout(pad=1.5, w_pad=2.0)
    savefig("fig3_provenance_alignment")


def draw_release_curatability() -> None:
    apply_f4p_style(font_size=12, axes_linewidth=1.6)
    rel = pd.read_csv(DATA / "release_package_completeness_distribution.csv")
    rel_order = [
        "no_explicit_release_signal",
        "stated_or_incomplete_release_signal",
        "code_or_scripts_or_recipe",
        "model_checkpoint_or_adapter",
        "data_or_evaluation_assets",
        "multiple_assets_or_complete_recipe",
    ]
    rel_label_map = {
        "no_explicit_release_signal": "No signal",
        "stated_or_incomplete_release_signal": "Stated",
        "code_or_scripts_or_recipe": "Code/\nrecipe",
        "model_checkpoint_or_adapter": "Checkpoint/\nadapter",
        "data_or_evaluation_assets": "Data/\neval",
        "multiple_assets_or_complete_recipe": "Multi-\nasset",
    }
    rel["release_package_tier"] = pd.Categorical(rel["release_package_tier"], rel_order, ordered=True)
    rel = rel.sort_values("release_package_tier", ascending=True)
    rel["label"] = rel["release_package_tier"].map(rel_label_map)

    paper = pd.read_csv(DATA / "jcdl_paper_curatability_paper_level.csv")
    p_order = [3, 2, 1, 0]
    r_order = [0, 1, 2, 3, 4]
    count_grid = (
        pd.crosstab(paper["provenance_points_0_to_3"], paper["release_package_points_0_to_4"])
        .reindex(index=p_order, columns=r_order)
        .fillna(0)
        .astype(int)
    )
    share_grid = count_grid / len(paper) * 100

    fig, axes = plt.subplots(ncols=2, figsize=(12.8, 4.6), gridspec_kw={"width_ratios": [1.02, 1.1]})

    ax = axes[0]
    x = np.arange(len(rel))
    values = rel["share_percent"].to_numpy(dtype=float)
    colors = [
        F4P["neutral"],
        F4P["red_2"],
        F4P["blue_secondary"],
        F4P["green_3"],
        F4P["teal"],
        F4P["blue_main"],
    ]
    bars = ax.bar(
        x,
        values,
        color=colors,
        edgecolor="black",
        linewidth=1.05,
        width=0.72,
        zorder=3,
    )
    ax.bar_label(
        bars,
        labels=["<0.2%" if 0 < v < 0.2 else f"{v:.1f}%" for v in values],
        padding=3,
        fontsize=9.5,
        fontweight="bold",
    )
    ax.set_xticks(x)
    ax.set_xticklabels(rel["label"], fontsize=9.0)
    ax.set_ylim(0, 37)
    ax.set_ylabel("Paper records (%)")
    ax.set_title("(a) Release evidence", loc="left", fontweight="bold", color=F4P["blue_main"], pad=8)
    polish_axis(ax, "y")

    ax = axes[1]
    cmap = LinearSegmentedColormap.from_list(
        "f4p_pr_grid",
        ["#F7FAFC", "#DCEAF7", "#A9CBEA", "#5B95CF", "#0F4D92"],
    )
    ax.imshow(share_grid.to_numpy(dtype=float), cmap=cmap, vmin=0, vmax=16, aspect="auto", zorder=1)
    ax.set_xticks(np.arange(len(r_order)))
    ax.set_xticklabels(["R0\nnone", "R1\nstated", "R2\ncode", "R3\nasset", "R4\nmulti"], fontsize=9.2)
    ax.set_yticks(np.arange(len(p_order)))
    ax.set_yticklabels(["P3\nmatched", "P2\nfamily", "P1\nweak", "P0\nnone"], fontsize=9.2)
    ax.set_xlabel("Release-package score")
    ax.set_ylabel("Provenance score")
    ax.set_title("(b) P/R co-occurrence", loc="left", fontweight="bold", color=F4P["blue_main"], pad=8)
    ax.set_xticks(np.arange(-0.5, len(r_order), 1), minor=True)
    ax.set_yticks(np.arange(-0.5, len(p_order), 1), minor=True)
    ax.grid(which="minor", color="white", linewidth=1.3)
    ax.tick_params(which="minor", bottom=False, left=False)
    for spine in ax.spines.values():
        spine.set_visible(False)
    for i in range(len(p_order)):
        for j in range(len(r_order)):
            count = int(count_grid.iloc[i, j])
            share = float(share_grid.iloc[i, j])
            label = "<0.2%" if 0 < share < 0.2 else f"{share:.1f}%"
            color = "white" if share >= 8.0 else DARK
            ax.text(j, i, label, ha="center", va="center", fontsize=8.2, fontweight="bold", color=color, zorder=4)
    ax.add_patch(Rectangle((1.5, -0.5), 3.0, 2.0, fill=False, edgecolor="#4B5563", linewidth=2.0, linestyle="--", zorder=5))
    ax.add_patch(Rectangle((2.5, -0.5), 2.0, 2.0, fill=False, edgecolor=F4P["blue_main"], linewidth=2.4, zorder=6))

    fig.tight_layout(pad=1.45, w_pad=1.9)
    savefig("fig4_release_curatability")


def make_table_curation_functions() -> None:
    df = pd.read_csv(DATA / "jcdl_record_function_coverage_summary.csv")
    df = df.replace(
        {
            "Public records are useful for family-level discovery but much weaker for exact genealogy.": (
                "Public records are useful for family-level discovery but much weaker for exact upstream claims."
            ),
        }
    )
    rows = []
    for _, r in df.iterrows():
        rows.append(
            [
                latex_escape(display_curation_function(r["curation_function"])),
                latex_escape(r["operational_question"]),
                latex_escape(clean_key_result(r["key_result"])),
                latex_escape(r["curation_implication"]),
            ]
        )
    tex = [
        r"\begin{table*}[!tbp]",
        r"\centering",
        r"\caption{Curation functions measured in the linked open LLM artifact record set.}",
        r"\label{tab:curation-functions}",
        r"\small",
        r"\begin{tabular}{p{0.16\linewidth}p{0.25\linewidth}p{0.27\linewidth}p{0.24\linewidth}}",
        r"\toprule",
        r"Function & Operational question & Key result & Curation implication \\",
        r"\midrule",
    ]
    for row in rows:
        tex.append(" & ".join(row) + r" \\")
    tex += [r"\bottomrule", r"\end{tabular}", r"\end{table*}", ""]
    (TAB / "table_curation_functions.tex").write_text("\n".join(tex), encoding="utf-8")


def make_table_study_design() -> None:
    rows = [
        ("Artifact identity", "191,375 repos", "Role + package form", "300-role audit", "Typed identity"),
        ("Scholarly linkage", "Repos + 2,214 papers", "HF/GitHub links; backlinks", "Alignment split", "Typed relation"),
        ("Provenance", "2,214 papers", "Upstream tier $P$", "200-row audit", "Upstream claim"),
        ("Release package", "2,214 papers", "Release tier $R$", "50-URL audit", "Visible assets"),
        (r"\textbf{Integrated}", "2,214 papers", r"\textbf{P/R/L rule}", "Sensitivity", r"\textbf{Readiness status}"),
    ]
    tex = [
        r"\begin{table*}[!tbp]",
        r"\centering",
        r"\caption{Measurement constructs and checks. Each row maps one curation construct to its denominator, signal, calibration check, and supported claim.}",
        r"\label{tab:measurement-constructs}",
        r"\small",
        r"\setlength{\tabcolsep}{3.6pt}",
        r"\renewcommand{\arraystretch}{1.08}",
        r"\begin{tabular}{@{}p{0.17\linewidth}p{0.18\linewidth}p{0.22\linewidth}p{0.17\linewidth}p{0.18\linewidth}@{}}",
        r"\toprule",
        r"\textbf{Construct} & \textbf{Unit} & \textbf{Signal} & \textbf{Check} & \textbf{Output claim} \\",
        r"\midrule",
    ]
    for row in rows:
        tex.append(" & ".join(v if "\\" in v or "$" in v else latex_escape(v) for v in row) + r" \\")
    tex += [r"\bottomrule", r"\end{tabular}", r"\renewcommand{\arraystretch}{1.0}", r"\end{table*}", ""]
    (TAB / "table_study_design.tex").write_text("\n".join(tex), encoding="utf-8")


def make_table_key_results() -> None:
    component_rows = [
        ("Linkage", "Matched paper--HF repo", "124 / 2,214", "5.6%", "Direct relation rare"),
        ("Provenance", "Inventory-backed family", "1,009 / 2,214", "45.6%", "Grouping, not lineage"),
        ("Release", r"Code/asset evidence ($R\geq2$)", "793 / 2,214", "35.8%", "Concrete release uneven"),
    ]
    threshold_rows = [
        ("Discovery-ready", "Any useful signal", "2,008 / 2,214", r"\textbf{90.7\%}", "Broad visibility"),
        ("Operational P+R", r"$P\geq2, R\geq2$", "401 / 2,214", r"\textbf{18.1\%}", "Usable P + release"),
        ("High-curatability", r"$P\geq2, R\geq3, L\geq1$", "136 / 2,214", r"\textbf{6.1\%}", "Joint evidence bottleneck"),
        ("Preservation-review", r"$P\geq2, R\geq4, L\geq1$", "50 / 2,214", "2.3%", "Multi-asset subset"),
    ]
    tex = [
        r"\begin{table*}[!tbp]",
        r"\centering",
        r"\caption{Headline evidence components and curation thresholds. Counts use 2,214 analysis-set paper records. $P$, $R$, and $L$ denote provenance, release-package, and direct-linkage scores.}",
        r"\label{tab:key-results}",
        r"\normalsize",
        r"\setlength{\tabcolsep}{6pt}",
        r"\renewcommand{\arraystretch}{1.08}",
        r"\begin{tabular*}{\textwidth}{@{\extracolsep{\fill}}llrrl@{}}",
        r"\toprule",
        r"\textbf{Group} & \textbf{Evidence or threshold} & \textbf{Count} & \textbf{Share} & \textbf{Takeaway} \\",
        r"\midrule",
        r"\multicolumn{5}{@{}l}{\textit{Evidence components}} \\",
        r"\cmidrule(lr){1-5}",
    ]
    for row in component_rows:
        tex.append(" & ".join(v if "\\" in v else latex_escape(v) for v in row) + r" \\")
    tex.append(r"\midrule")
    tex.append(r"\multicolumn{5}{@{}l}{\textit{Curation-readiness thresholds}} \\")
    tex.append(r"\cmidrule(lr){1-5}")
    for row in threshold_rows:
        tex.append(" & ".join(v if "\\" in v else latex_escape(v) for v in row) + r" \\")
    tex += [r"\bottomrule", r"\end{tabular*}", r"\renewcommand{\arraystretch}{1.0}", r"\end{table*}", ""]
    (TAB / "table_key_results.tex").write_text("\n".join(tex), encoding="utf-8")


def make_table_reproducibility_workflow() -> None:
    def latex_file_cell(value: str) -> str:
        escaped = latex_escape(value)
        escaped = escaped.replace(r"\_", r"\_\allowbreak{}")
        escaped = escaped.replace(";", r";\allowbreak{}")
        return escaped

    query_terms = {
        "Size/compactness": "0.5b, 1b, 1.5b, 1.8b, 2b, 3b, 4b, 7b, small, mini, tiny, compact, lite, slim, nano, micro, sub-billion",
        "Deployment format": "quantized, gguf, gptq, awq, exl2, 4bit, 8bit, mobile, edge, on-device, efficient, low-memory, fast",
        "Derivation/tuning": "distilled, distill, merge, merged, lora, qlora, sft, dpo, instruction, instruct, chat",
        "Domain/language/task": "medical, biomedical, clinical, legal, law, finance, financial, code, coding, math, reasoning, multilingual, Chinese, English, Japanese, Korean, Arabic",
        "Family": "Llama, Qwen, Mistral, Gemma, Phi, DeepSeek, MiniCPM, OpenELM, Falcon, OLMo",
    }
    rows = [
        ("HF snapshot", "May 2026 Hugging Face API query run", "68 matched queries grouped into five buckets", "hf_models_pool_raw.csv; model_repo_master_HF.csv"),
        ("Paper corpus", "OpenAlex/arXiv/top-conference paper records", "2,729 records; 2,722 works after source-level deduplication", "www_data_funnel.csv"),
        ("Main-analysis filter", "Paper records with extracted model/release evidence", "Include papers centrally studying compact or derived open LLM artifacts", "paper_codebook_v3_full_enriched.csv; www_data_funnel.csv"),
        ("Link extraction", "Paper text links and model-card references", "Separate paper-side HF links, GitHub links, model-card backlinks, and matched paper-HF evidence", "jcdl_paper_repo_alignment_decomposition.csv"),
        ("Provenance coding", "Paper-family signals and repository evidence", "Assign strongest public-record sufficiency tier; do not infer full upstream genealogy", "jcdl_provenance_sufficiency_paper_level.csv"),
        ("Release coding", "Paper-side release statements and links", "Assign five-level release package score from no signal to full recipe", "jcdl_release_package_completeness_paper_level.csv"),
    ]
    tex = [
        r"\begin{table*}[t]",
        r"\centering",
        r"\caption{Data construction and reproducibility workflow. Query terms are grouped into buckets for scope and sensitivity analysis.}",
        r"\label{tab:reproducibility-workflow}",
        r"\small",
        r"\begin{tabular}{p{0.16\linewidth}p{0.24\linewidth}p{0.31\linewidth}p{0.20\linewidth}}",
        r"\toprule",
        r"Stage & Input / source & Rule or output & Main reproducibility file \\",
        r"\midrule",
    ]
    for row in rows:
        cells = [latex_escape(row[0]), latex_escape(row[1]), latex_escape(row[2]), latex_file_cell(row[3])]
        tex.append(" & ".join(cells) + r" \\")
    tex += [r"\midrule", r"\multicolumn{4}{l}{\textit{HF query buckets used for the fixed snapshot}} \\"]
    for bucket, terms in query_terms.items():
        tex.append(rf"\multicolumn{{1}}{{p{{0.16\linewidth}}}}{{{latex_escape(bucket)}}} & \multicolumn{{3}}{{p{{0.78\linewidth}}}}{{{latex_escape(terms)}}} \\")
    tex += [r"\bottomrule", r"\end{tabular}", r"\end{table*}", ""]
    (TAB / "table_reproducibility_workflow.tex").write_text("\n".join(tex), encoding="utf-8")


def make_table_validation_layers() -> None:
    rows = [
        ("Repository role", "300 repositories; 60 per predicted role", "Balanced expert metadata audit", "85.3% strict agreement; 24 packaging-overlay cases"),
        ("Upstream/provenance evidence", "200 paper-level provenance rows", "Expert review of strict vs usable support", "28.0% strict unique-primary support; 79.0% usable family-signal support"),
        ("Release evidence", "50 release-evidence rows", "Expert URL/asset-level plausibility check", "No required aggregate category changes in reviewed rows"),
        ("Query sensitivity", "191,375 repository records", "Leave-one-query-bucket-out robustness", "Downstream share remains 69.1% after excluding deployment and derivation buckets"),
        ("Corpus construction", "2,729 paper records; 2,722 works", "Record/work denominator check", "2,214 main-analysis records; 2,208 main-analysis works"),
    ]
    tex = [
        r"\begin{table*}[t]",
        r"\centering",
        r"\caption{Validation and sensitivity layers used to calibrate the main constructs.}",
        r"\label{tab:validation-layers}",
        r"\small",
        r"\begin{tabular}{p{0.18\linewidth}p{0.22\linewidth}p{0.27\linewidth}p{0.25\linewidth}}",
        r"\toprule",
        r"Layer & Sample / denominator & Check & Outcome used in the paper \\",
        r"\midrule",
    ]
    for row in rows:
        tex.append(" & ".join(latex_escape(v) for v in row) + r" \\")
    tex += [r"\bottomrule", r"\end{tabular}", r"\end{table*}", ""]
    (TAB / "table_validation_layers.tex").write_text("\n".join(tex), encoding="utf-8")


def make_table_curatability_components() -> None:
    df = pd.read_csv(DATA / "jcdl_paper_curatability_paper_level.csv").copy()
    total = len(df)
    df["usable_provenance"] = df["provenance_points_0_to_3"] >= 2
    df["concrete_release"] = df["release_package_points_0_to_4"] >= 2
    df["direct_link"] = df["paper_repo_link_points_0_to_2"] >= 1
    grouped = (
        df.groupby(["usable_provenance", "concrete_release", "direct_link"], dropna=False)
        .size()
        .reset_index(name="paper_count")
        .sort_values(["usable_provenance", "concrete_release", "direct_link"], ascending=[False, False, False])
    )
    tex = [
        r"\begin{table*}[t]",
        r"\centering",
        r"\caption{Component cross-tab for integrated curatability.}",
        r"\label{tab:curatability-components}",
        r"\small",
        r"\begin{tabular}{lllrr}",
        r"\toprule",
        r"Prov. & Release & Link & Count & Share \\",
        r"\midrule",
    ]
    for _, r in grouped.iterrows():
        count = int(r["paper_count"])
        share = count / total * 100
        tex.append(
            " & ".join(
                [
                    "yes" if r["usable_provenance"] else "no",
                    "yes" if r["concrete_release"] else "no",
                    "yes" if r["direct_link"] else "no",
                    f"{count:,}",
                    f"{share:.1f}\\%",
                ]
            )
            + r" \\"
        )
    tex += [r"\bottomrule", r"\end{tabular}", r"\end{table*}", ""]
    (TAB / "table_curatability_components.tex").write_text("\n".join(tex), encoding="utf-8")


def make_table_metadata_schema() -> None:
    rows = [
        ("Artifact role", "primary_artifact_role", "base; fine-tune; adapter; merge; distilled student; evaluation package; deployment artifact", "Model-card identity field"),
        ("Packaging overlay", "artifact_package_form", "quantized; converted; adapter-only; merged; checkpoint-complete; deployment format", "Model-card technical metadata"),
        ("Upstream relation", "upstream_relation_type", "base; teacher; adapter target; merge input; quantization source; evaluator; baseline", "PROV-style relation type"),
        ("Provenance evidence", "provenance_evidence_tier", "explicit upstream field; matched repository with visible upstream relation; inventory-backed family; contextual mention", "PROV evidence confidence"),
        ("Paper link", "paper_repository_relation", "introduced-by; supports-paper; evaluated-in; baseline-in; cited-by-card", "Bidirectional paper/repository relation"),
        ("Release package", "release_asset_types", "code; scripts; weights; adapter; data; evaluation assets; recipe; environment", "Model card / openness component"),
        ("Governance", "license_and_access_signal", "license tag; gated flag; missing/unknown", "Trust and reuse metadata"),
    ]
    tex = [
        r"\begin{table*}[t]",
        r"\centering",
        r"\caption{Concrete metadata schema implied by the curation findings. The fields can be implemented in model-card, repository, or scholarly-index records.}",
        r"\label{tab:metadata-schema}",
        r"\small",
        r"\begin{tabular}{p{0.16\linewidth}p{0.20\linewidth}p{0.39\linewidth}p{0.17\linewidth}}",
        r"\toprule",
        r"Record need & Field & Controlled values or type & Design anchor \\",
        r"\midrule",
    ]
    for row in rows:
        tex.append(" & ".join(latex_escape(v) for v in row) + r" \\")
    tex += [r"\bottomrule", r"\end{tabular}", r"\end{table*}", ""]
    (TAB / "table_metadata_schema.tex").write_text("\n".join(tex), encoding="utf-8")


def make_table_metadata_completeness() -> None:
    df = pd.read_csv(DATA / "metadata_completeness_matrix.csv").copy()
    order = [
        "Stable repository id",
        "Publisher or owner",
        "Creation timestamp",
        "Artifact role",
        "Variant type",
        "General tag record",
        "Task descriptors",
        "Model family label",
        "Explicit upstream model",
        "Typed upstream relation",
        "License tag signal",
        "Scholarly reference",
        "Domain descriptors",
    ]
    df["curation_field"] = pd.Categorical(df["curation_field"], order, ordered=True)
    df = df.sort_values("curation_field")
    df["display_field"] = df["curation_field"].astype(str).map(display_metadata_field)
    tex = [
        r"\begin{table*}[t]",
        r"\centering",
        r"\caption{Repository metadata completeness in the fixed query-based Hugging Face snapshot.}",
        r"\label{tab:metadata-completeness}",
        r"\small",
        r"\begin{tabular}{p{0.23\linewidth}p{0.22\linewidth}r r p{0.24\linewidth}}",
        r"\toprule",
        r"Field & Curation function & Records & Share & Interpretation \\",
        r"\midrule",
    ]
    for _, r in df.iterrows():
        tex.append(
            " & ".join(
                [
                    latex_escape(r["display_field"]),
                    latex_escape(r["curation_function"]),
                    f"{int(r['records_with_signal']):,}",
                    f"{float(r['share_percent']):.1f}\\%",
                    latex_escape(r["interpretation"]),
                ]
            )
            + r" \\"
        )
    tex += [r"\bottomrule", r"\end{tabular}", r"\end{table*}", ""]
    (TAB / "table_metadata_completeness.tex").write_text("\n".join(tex), encoding="utf-8")


def make_table_role_audit() -> None:
    rows = [
        ("Base", "60", "43", "71.7%", "Boundary cases often contain adaptation or task-tuning evidence."),
        ("Fine-tune", "60", "60", "100.0%", "Highly consistent in the balanced audit sample."),
        ("Adapter/LoRA", "60", "60", "100.0%", "Highly consistent in the balanced audit sample."),
        ("Merge/mixed", "60", "33", "55.0%", "Often overlaps with quantization or deployment packaging."),
        ("Quantized/deployment", "60", "60", "100.0%", "Highly consistent in the balanced audit sample."),
        ("Overall", "300", "256", "85.3%", "Strict agreement across the balanced artifact-role audit."),
    ]
    tex = [
        r"\begin{table*}[t]",
        r"\centering",
        r"\caption{Balanced artifact-role audit summary.}",
        r"\label{tab:role-audit}",
        r"\small",
        r"\begin{tabular}{p{0.20\linewidth}r r r p{0.34\linewidth}}",
        r"\toprule",
        r"Predicted role & Audit rows & Strict support & Precision & Note \\",
        r"\midrule",
    ]
    for row in rows:
        tex.append(" & ".join(latex_escape(v) for v in row) + r" \\")
    tex += [r"\bottomrule", r"\end{tabular}", r"\end{table*}", ""]
    (TAB / "table_role_audit.tex").write_text("\n".join(tex), encoding="utf-8")


def make_table_query_sensitivity() -> None:
    df = pd.read_csv(WWWDATA / "hf_query_bucket_leave_one_out.csv").copy()
    tex = [
        r"\begin{table*}[t]",
        r"\centering",
        r"\caption{Query-bucket sensitivity for the fixed repository snapshot. Shares are scope checks for the query-based collection, not a full-platform census.}",
        r"\label{tab:query-sensitivity}",
        r"\small",
        r"\begin{tabular}{p{0.30\linewidth}p{0.24\linewidth}r r r}",
        r"\toprule",
        r"Subset & Excluded bucket(s) & Repos & Base share & Downstream share \\",
        r"\midrule",
    ]
    for _, r in df.iterrows():
        excluded = display_query_bucket_list(r["excluded_query_buckets"])
        tex.append(
            " & ".join(
                [
                    latex_escape(display_query_subset(r["sensitivity_subset"])),
                    latex_escape(excluded),
                    f"{int(r['repo_count']):,}",
                    f"{float(r['base_repo_share']) * 100:.1f}\\%",
                    f"{float(r['downstream_repo_share']) * 100:.1f}\\%",
                ]
            )
            + r" \\"
        )
    tex += [r"\bottomrule", r"\end{tabular}", r"\end{table*}", ""]
    (TAB / "table_query_sensitivity.tex").write_text("\n".join(tex), encoding="utf-8")


def make_table_construct_validity() -> None:
    df = pd.read_csv(DATA / "jcdl_evidence_source_construct_validity.csv")
    df = df[df["construct"].isin(["Artifact role", "Bibliographic linkage", "Provenance sufficiency", "Release package completeness", "Integrated curatability"])]
    df = df.copy()
    df["construct"] = df["construct"].replace({"Release package completeness": "Release-package evidence"})
    df["validation_status"] = df["validation_status"].str.replace("expert/coauthor URL-level audit", "expert URL-level audit", regex=False)
    df["construct_risk"] = df["construct_risk"].str.replace(
        "not an objective quality, preservation, adoption, or reproducibility score",
        "measures record completeness rather than model quality, adoption, preservation success, or executable reproducibility",
        regex=False,
    )
    tex = [
        r"\begin{table*}[t]",
        r"\centering",
        r"\caption{Construct validity notes for the main measures. The table separates platform metadata, project-inferred fields, audited evidence, and operational composites.}",
        r"\label{tab:construct-validity}",
        r"\small",
        r"\begin{tabular}{p{0.17\linewidth}p{0.22\linewidth}p{0.25\linewidth}p{0.27\linewidth}}",
        r"\toprule",
        r"Construct & Record source type & Validation status & Construct risk controlled in wording \\",
        r"\midrule",
    ]
    for _, r in df.iterrows():
        tex.append(
            " & ".join(
                [
                    latex_escape(r["construct"]),
                    latex_escape(r["record_source_type"]),
                    latex_escape(r["validation_status"]),
                    latex_escape(r["construct_risk"]),
                ]
            )
            + r" \\"
        )
    tex += [r"\bottomrule", r"\end{tabular}", r"\end{table*}", ""]
    (TAB / "table_construct_validity.tex").write_text("\n".join(tex), encoding="utf-8")


def make_table_crosswalk() -> None:
    df = pd.read_csv(DATA / "jcdl_metadata_recommendation_crosswalk.csv")
    for col in df.columns:
        df[col] = df[col].astype(str)
        df[col] = df[col].str.replace("Release package completeness hierarchy.", "Release-package evidence hierarchy.", regex=False)
        df[col] = df[col].str.replace("exact genealogy", "exact upstream claims", regex=False)
        df[col] = df[col].str.replace(
            "Weak and ambiguous provenance signals can be mistaken for exact lineage.",
            "Weak and ambiguous provenance signals can be mistaken for exact upstream evidence.",
            regex=False,
        )
    tex = [
        r"\begin{table*}[t]",
        r"\centering",
        r"\caption{Evidence-to-design crosswalk. Each recommendation follows from an observed curation gap.}",
        r"\label{tab:crosswalk}",
        r"\small",
        r"\begin{tabular}{p{0.31\linewidth}p{0.24\linewidth}p{0.36\linewidth}}",
        r"\toprule",
        r"Curation problem & Empirical basis & Metadata or interface intervention \\",
        r"\midrule",
    ]
    for _, r in df.iterrows():
        tex.append(
            " & ".join(
                [
                    latex_escape(r["curation_problem"]),
                    latex_escape(r["empirical_basis"]),
                    latex_escape(r["recommended_metadata_or_interface"]),
                ]
            )
            + r" \\"
        )
    tex += [r"\bottomrule", r"\end{tabular}", r"\end{table*}", ""]
    (TAB / "table_crosswalk.tex").write_text("\n".join(tex), encoding="utf-8")


def make_appendix_tables() -> None:
    alignment_df = pd.read_csv(DATA / "jcdl_paper_repo_alignment_decomposition.csv")[
        [
            "alignment_signal",
            "main_unique_paper_record_count",
            "main_record_share_percent",
            "link_confidence_or_status",
            "interpretation",
        ]
    ].copy()
    alignment_df["alignment_signal"] = alignment_df["alignment_signal"].map(display_alignment_signal)
    alignment_df["link_confidence_or_status"] = alignment_df["link_confidence_or_status"].map(clean_label)
    alignment_df["main_record_share_percent"] = alignment_df["main_record_share_percent"].map(lambda x: f"{float(x):.1f}%")
    alignment_df["interpretation"] = alignment_df["interpretation"].replace(
        {
            "all exact paper-HF edge methods combined; report separately from explicit paper text links": (
                "all matched paper-HF evidence methods combined; report separately from explicit paper text links "
                "and avoid treating low-confidence fuzzy matches as direct links"
            )
        }
    )

    sensitivity_df = pd.read_csv(DATA / "jcdl_curatability_threshold_sensitivity.csv")[
        ["sensitivity_test", "rule", "paper_count", "share_percent", "interpretation"]
    ].copy()
    sensitivity_df["sensitivity_test"] = sensitivity_df["sensitivity_test"].map(display_sensitivity_test)
    sensitivity_df["rule"] = sensitivity_df["rule"].map(display_curatability_rule)
    sensitivity_df["share_percent"] = sensitivity_df["share_percent"].map(lambda x: f"{float(x):.1f}%")
    sensitivity_df["interpretation"] = sensitivity_df["interpretation"].str.replace(
        "matches high+operational curatability: usable provenance plus code/recipe-or-stronger release evidence",
        "operational P+R threshold: usable provenance plus code/recipe-or-stronger release evidence",
        regex=False,
    )

    failure_df = pd.read_csv(DATA / "jcdl_curation_failure_examples.csv")[
        ["failure_mode", "curation_problem", "metadata_fix"]
    ]
    for col in failure_df.columns:
        failure_df[col] = failure_df[col].astype(str)
        failure_df[col] = failure_df[col].str.replace("exact genealogy", "exact upstream claims", regex=False)
        failure_df[col] = failure_df[col].str.replace(
            "Binary open/not-open metadata hides large differences in reuse and preservation readiness.",
            "Binary open/not-open metadata hides large differences in release evidence and preservation triage.",
            regex=False,
        )

    tables = {
        "table_alignment_decomposition.tex": (
            "Paper-repository alignment signal decomposition.",
            "tab:alignment-decomposition",
            alignment_df,
            ["Signal", "Main records", "Share", "Status", "Interpretation"],
        ),
        "table_curatability_sensitivity.tex": (
            "Curatability threshold sensitivity.",
            "tab:curatability-sensitivity",
            sensitivity_df,
            ["Test", "Rule", "Count", "Share", "Interpretation"],
        ),
        "table_failure_examples.tex": (
            "Curation failure modes and metadata fixes.",
            "tab:failure-examples",
            failure_df,
            ["Failure mode", "Curation problem", "Metadata fix"],
        ),
    }
    for filename, (caption, label, df, headers) in tables.items():
        tex = [
            r"\begin{table*}[t]",
            r"\centering",
            rf"\caption{{{latex_escape(caption)}}}",
            rf"\label{{{label}}}",
            r"\small",
            r"\begin{tabular}{p{0.20\linewidth}p{0.18\linewidth}p{0.13\linewidth}p{0.17\linewidth}p{0.22\linewidth}}" if len(headers) == 5 else r"\begin{tabular}{p{0.22\linewidth}p{0.34\linewidth}p{0.34\linewidth}}",
            r"\toprule",
            " & ".join(headers) + r" \\",
            r"\midrule",
        ]
        for _, r in df.iterrows():
            tex.append(" & ".join(latex_escape(v) for v in r.tolist()) + r" \\")
        tex += [r"\bottomrule", r"\end{tabular}", r"\end{table*}", ""]
        (TAB / filename).write_text("\n".join(tex), encoding="utf-8")


def main() -> None:
    ensure_dirs()
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "axes.titlesize": 11,
            "axes.labelsize": 10,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )
    draw_pipeline()
    draw_metadata_completeness()
    draw_provenance_alignment()
    draw_release_curatability()
    make_table_study_design()
    make_table_key_results()
    make_table_reproducibility_workflow()
    make_table_validation_layers()
    make_table_curatability_components()
    make_table_metadata_schema()
    make_table_curation_functions()
    make_table_metadata_completeness()
    make_table_role_audit()
    make_table_query_sensitivity()
    make_table_construct_validity()
    make_table_crosswalk()
    make_appendix_tables()
    print(f"Wrote figures to {FIG}")
    print(f"Wrote tables to {TAB}")


if __name__ == "__main__":
    main()
