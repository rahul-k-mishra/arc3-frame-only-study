"""
manuscript_figures.py -- the four figures of the JOTE manuscript, drawn from committed files only.

    fig1.png  V1 agreement per assumption, per suite and condition, with the registered thresholds
              0.75 and 0.90 and the verdict above each bar           (docs/tables/v1.json; registered)
    fig2.png  V2 AUROC with its bootstrap interval per agent and line, the nuisance baseline's AUROC
              beside it, and the thresholds 0.65 and 0.80           (docs/tables/v2.json; registered)
    fig3.png  truth (holds, fails) against census (holds, fails, undetermined), as stacked bars
                                                            (runs/exploratory/v1_diagnosis.json; exploratory)
    fig4.png  seed dissent: games by the number of their 10 seeds that disagree with the majority
                                                            (runs/exploratory/v1_diagnosis.json; exploratory)

matplotlib only.  One worker process per figure.  300 dpi, 170 mm wide, grayscale-safe (gray levels and
hatching, no hue), no title inside the image; the caption in the manuscript carries it.  Each worker
returns the list of numbers it drew, and the parent prints them in figure order, with the source file,
so that the console can be matched against docs/manuscript/numbers.json.  The thresholds drawn are
read from docs/manuscript/numbers.json (keys thr.*), which reads them from docs/PREREG.md.

Run (working directory D:\\Research\\arc3\\repo), after scripts\\manuscript_numbers.py:
    D:\\Research\\arc3\\brutus\\.venv\\Scripts\\python.exe scripts\\manuscript_figures.py

Expected console output: four blocks "fig<k>.png from <source>" with one line per drawn number,
then "4 figures written to docs/manuscript".
"""
from __future__ import annotations

import json
import os
from multiprocessing import Pool

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs", "manuscript")
MM = 1 / 25.4
WIDTH = 170 * MM

LINES_V1 = [("minigrid", "macro", "all", "MiniGrid/BabyAI, absolute moves\n(161 games)"),
            ("minigrid", "raw", "all", "MiniGrid/BabyAI, primitive actions\n(161 games)"),
            ("procgen", "center_off", "all", "Procgen, camera off,\nall games (14)"),
            ("procgen", "center_off", "in_range", "Procgen, camera off,\nin range (9)"),
            ("procgen", "center_on", "camera_distinct", "Procgen, camera on,\ncamera-distinct (5)")]
A = ("A1", "A2", "A3", "A4", "A5")


def _load(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return json.load(f)


def _thr(key):
    return float(_load("docs/manuscript/numbers.json")[key]["value"])


def _setup():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    global MaxNLocator
    from matplotlib.ticker import MaxNLocator
    plt.rcParams.update({"font.size": 7.5, "axes.labelsize": 7.5, "xtick.labelsize": 7, "ytick.labelsize": 7,
                         "legend.fontsize": 7, "font.family": "DejaVu Sans", "axes.linewidth": 0.6,
                         "hatch.linewidth": 0.5})
    return plt


def fig1():
    plt = _setup()
    src = "docs/tables/v1.json"
    v1 = _load(src)
    rows = {(r[0], r[1], r[2], r[3]): dict(zip(v1["header"], r)) for r in v1["rows"]}
    lo, hi = _thr("thr.v1_fail_agreement"), _thr("thr.v1_pass_agreement")
    drawn = [f"threshold FAIL below {lo:.2f}", f"threshold PASS needs at least {hi:.2f}"]
    fig, axes = plt.subplots(2, 3, figsize=(WIDTH, 120 * MM), sharey=True)
    for ax, (s, c, sub, title) in zip(axes.flat, LINES_V1):
        vals = [rows[(s, c, sub, a)]["agreement"] for a in A]
        verd = [rows[(s, c, sub, a)]["verdict"] for a in A]
        ax.bar(range(5), vals, color="0.75", edgecolor="black", linewidth=0.6, width=0.65)
        ax.axhline(lo, color="black", linestyle="--", linewidth=0.8)
        ax.axhline(hi, color="black", linestyle=":", linewidth=1.0)
        for i, (v, w) in enumerate(zip(vals, verd)):
            ax.text(i, v + 0.03, w, rotation=90, ha="center", va="bottom", fontsize=6.5,
                    bbox=dict(facecolor="white", edgecolor="none", pad=0.6))
            drawn.append(f"{s} {c} {sub} {A[i]}: agreement {v:.4f}, verdict {w}")
        ax.set_xticks(range(5), A)
        ax.set_ylim(0, 1.75)
        ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
        ax.set_xlabel(title, fontsize=7)
        ax.spines[["top", "right"]].set_visible(False)
    for ax in axes[:, 0]:
        ax.set_ylabel("Agreement with the truth table")
    leg = axes.flat[5]
    leg.axis("off")
    leg.plot([0.05, 0.25], [0.7, 0.7], "k:", linewidth=1.0)
    leg.text(0.3, 0.7, f"{hi:.2f}: PASS needs agreement\nat or above this line\n(and κ ≥ {_thr('thr.v1_pass_kappa'):.2f} where κ applies)",
             va="center", fontsize=6.8)
    leg.plot([0.05, 0.25], [0.4, 0.4], "k--", linewidth=0.8)
    leg.text(0.3, 0.4, f"{lo:.2f}: FAIL below this line", va="center", fontsize=6.8)
    leg.text(0.05, 0.15, "Word above each bar: the verdict\nprinted by the frozen analysis code", fontsize=6.8,
             va="center")
    leg.set_xlim(0, 1)
    leg.set_ylim(0, 1)
    fig.tight_layout(h_pad=1.2, w_pad=0.6)
    fig.savefig(os.path.join(OUT, "fig1.png"), dpi=300)
    plt.close(fig)
    return "fig1.png", src, drawn


def fig2():
    plt = _setup()
    src = "docs/tables/v2.json"
    v2 = _load(src)
    rows = [dict(zip(v2["header"], r)) for r in v2["rows"]]
    lo, hi = _thr("thr.v2_fail_auroc"), _thr("thr.v2_pass_auroc")
    drawn = [f"threshold FAIL at or below {lo:.2f}", f"threshold PASS needs at least {hi:.2f}"]
    suite_name = {"arc": "ARC-AGI-3", "minigrid": "MiniGrid/BabyAI", "procgen": "Procgen"}
    cond_name = {"native": "", "macro": "abs. moves", "raw": "primitive", "center_off": "camera off",
                 "center_on": "camera on"}
    fig, ax = plt.subplots(figsize=(WIDTH, 175 * MM))
    labels = []
    n = len(rows)
    for i, r in enumerate(rows):
        y = n - 1 - i
        if r["ci_low"] is not None:
            ax.plot([r["ci_low"], r["ci_high"]], [y, y], color="black", linewidth=0.9)
        ax.plot(r["auroc"], y, "o", color="black", markersize=4)
        ax.plot(r["auroc_B"], y + 0.0, "s", markerfacecolor="white", markeredgecolor="0.35", markersize=4.2)
        ax.text(1.06, y, r["verdict"], va="center", fontsize=6.5, transform=ax.get_yaxis_transform())
        labels.append((f"{suite_name[r['suite']]} {cond_name[r['condition']]}".strip() + f", {r['subset']}: {r['agent']}"))
        ci = "no interval (VOID)" if r["ci_low"] is None else f"[{r['ci_low']:.4f}, {r['ci_high']:.4f}]"
        drawn.append(f"{r['suite']} {r['condition']} {r['subset']} {r['agent']}: AUROC {r['auroc']:.4f}, CI {ci}, "
                     f"AUROC_B {r['auroc_B']:.4f}, verdict {r['verdict']}")
    ax.axvline(lo, color="black", linestyle="--", linewidth=0.8)
    ax.axvline(hi, color="black", linestyle=":", linewidth=1.0)
    ax.set_yticks(range(n), labels[::-1], fontsize=6.3)
    ax.set_ylim(-0.7, n - 0.3)
    ax.set_xlim(0, 1.04)
    ax.set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_xlabel("AUROC of the census score for level-1 completion")
    ax.spines[["top", "right"]].set_visible(False)
    from matplotlib.lines import Line2D
    handles = [Line2D([], [], color="black", marker="o", linestyle="-", markersize=4, linewidth=0.9,
                      label="census AUROC with 95% bootstrap interval"),
               Line2D([], [], color="0.35", marker="s", markerfacecolor="white", linestyle="none", markersize=4.2,
                      label="nuisance baseline AUROC"),
               Line2D([], [], color="black", linestyle="--", linewidth=0.8, label=f"{lo:.2f}: FAIL at or below"),
               Line2D([], [], color="black", linestyle=":", linewidth=1.0, label=f"{hi:.2f}: PASS needs at least")]
    ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.35, -0.06), ncol=2, frameon=False)
    fig.tight_layout()
    fig.subplots_adjust(right=0.80)
    fig.savefig(os.path.join(OUT, "fig2.png"), dpi=300)
    plt.close(fig)
    return "fig2.png", src, drawn


def fig3():
    plt = _setup()
    src = "runs/exploratory/v1_diagnosis.json"
    d = _load(src)["part1"]
    drawn = []
    styles = {"holds": dict(color="white", edgecolor="black", hatch=""),
              "fails": dict(color="0.35", edgecolor="black", hatch=""),
              "undetermined": dict(color="0.82", edgecolor="black", hatch="////")}
    fig, axes = plt.subplots(2, 3, figsize=(WIDTH, 125 * MM))
    for ax, (s, c, sub, title) in zip(axes.flat, LINES_V1):
        xt, xl = [], []
        for i, a in enumerate(A):
            conf = d[f"{s} | {c} | {sub} | {a}"]["confusion"]
            for j, t in enumerate(("holds", "fails")):
                x = i * 2.6 + j * 1.0
                bottom = 0
                for p in ("holds", "fails", "undetermined"):
                    v = conf[f"{t} / {p}"]
                    if v:
                        ax.bar(x, v, bottom=bottom, width=0.9, linewidth=0.5, **styles[p])
                    bottom += v
                    drawn.append(f"{s} {c} {sub} {a}: truth {t}, census {p}: {v}")
                xt.append(x)
                xl.append("h" if t == "holds" else "f")
            ax.text(i * 2.6 + 0.5, -0.16, a, transform=ax.get_xaxis_transform(), ha="center", fontsize=7)
        ax.set_xticks(xt, xl, fontsize=6.5)
        ax.set_xlabel("\n" + title, fontsize=7)
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        ax.spines[["top", "right"]].set_visible(False)
    for ax in axes[:, 0]:
        ax.set_ylabel("Games")
    leg = axes.flat[5]
    leg.axis("off")
    from matplotlib.patches import Patch
    leg.legend(handles=[Patch(facecolor="white", edgecolor="black", label="census holds"),
                        Patch(facecolor="0.35", edgecolor="black", label="census fails"),
                        Patch(facecolor="0.82", edgecolor="black", hatch="////", label="census undetermined")],
               loc="upper left", frameon=False, title="Bar segments", title_fontsize=7)
    leg.text(0.0, 0.25, "Bar label h: games where the truth\ntable says the assumption holds;\n"
                        "f: games where it says it fails", fontsize=6.8, va="center", transform=leg.transAxes)
    fig.tight_layout(h_pad=1.0, w_pad=0.8)
    fig.savefig(os.path.join(OUT, "fig3.png"), dpi=300)
    plt.close(fig)
    return "fig3.png", src, drawn


def fig4():
    plt = _setup()
    src = "runs/exploratory/v1_diagnosis.json"
    d = _load(src)["part1"]
    drawn = []
    kmax = max(max(p["seeds_against_majority"].values()) for p in d.values())
    grays = [str(1 - k / kmax * 0.95) for k in range(kmax + 1)]
    fig, axes = plt.subplots(2, 3, figsize=(WIDTH, 110 * MM))
    for ax, (s, c, sub, title) in zip(axes.flat, LINES_V1):
        for i, a in enumerate(A):
            vals = list(d[f"{s} | {c} | {sub} | {a}"]["seeds_against_majority"].values())
            left = 0
            y = 4 - i
            for k in range(kmax + 1):
                cnt = sum(v == k for v in vals)
                if cnt:
                    ax.barh(y, cnt, left=left, color=grays[k], edgecolor="black", linewidth=0.4, height=0.7)
                    drawn.append(f"{s} {c} {sub} {a}: {cnt} games with {k} dissenting seeds")
                left += cnt
        ax.set_yticks(range(5), A[::-1])
        ax.set_xlabel("Games\n" + title, fontsize=7)
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax.spines[["top", "right"]].set_visible(False)
    leg = axes.flat[5]
    leg.axis("off")
    from matplotlib.patches import Patch
    leg.legend(handles=[Patch(facecolor=grays[k], edgecolor="black", label=f"{k}") for k in range(kmax + 1)],
               loc="center left", frameon=False, ncol=2,
               title="Seeds of 10 that disagree\nwith the game's majority", title_fontsize=7)
    fig.tight_layout(h_pad=1.0, w_pad=0.8)
    fig.savefig(os.path.join(OUT, "fig4.png"), dpi=300)
    plt.close(fig)
    return "fig4.png", src, drawn


def _run(name):
    return {"fig1": fig1, "fig2": fig2, "fig3": fig3, "fig4": fig4}[name]()


def main():
    os.makedirs(OUT, exist_ok=True)
    with Pool(4) as pool:
        results = pool.map(_run, ["fig1", "fig2", "fig3", "fig4"])
    for name, src, drawn in results:
        print(f"{name} from {src}")
        for line in drawn:
            print("  " + line)
    print(f"{len(results)} figures written to docs/manuscript")


if __name__ == "__main__":
    main()
