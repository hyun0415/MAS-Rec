"""Generate a dependency-free SVG from the published RMSE table."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "results" / "metrics.csv"
OUTPUT = ROOT / "results" / "figures" / "main_rmse_comparison.svg"


def main() -> None:
    with INPUT.open(encoding="utf-8", newline="") as stream:
        rows = [
            row for row in csv.DictReader(stream)
            if row["protocol"] == "reported_paper" and row["study"] == "main"
        ]
    datasets = list(dict.fromkeys(row["dataset"] for row in rows))
    models = list(dict.fromkeys(row["model"] for row in rows))
    values = {(row["dataset"], row["model"]): float(row["rmse"]) for row in rows}
    width, height = 960, 540
    left, top, chart_width = 210, 80, 680
    row_height = 27
    max_value = max(values.values()) * 1.08
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        '<style>text{font-family:Arial,sans-serif;fill:#17202a}.title{font-size:24px;font-weight:700}.small{font-size:12px}.label{font-size:13px}</style>',
        '<text x="40" y="38" class="title">Paper-reported RMSE comparison</text>',
        '<text x="40" y="60" class="small">Lower is better. These values were not rerun in the portfolio refactor.</text>',
    ]
    y = top
    colors = ["#5b8ff9", "#61d9a7"]
    for dataset_index, dataset in enumerate(datasets):
        short = "Clothing" if dataset.startswith("Clothing") else "Cell Phones"
        parts.append(f'<text x="40" y="{y + 15}" class="label" font-weight="700">{short}</text>')
        for model in models:
            value = values[(dataset, model)]
            bar_width = chart_width * value / max_value
            color = "#f28e2b" if model == "MAS-Rec" else colors[dataset_index]
            parts.append(f'<text x="125" y="{y + 15}" class="label">{model}</text>')
            parts.append(f'<rect x="{left}" y="{y}" width="{bar_width:.1f}" height="18" rx="3" fill="{color}"/>')
            parts.append(f'<text x="{left + bar_width + 8:.1f}" y="{y + 14}" class="label">{value:.3f}</text>')
            y += row_height
        y += 24
    parts.append('</svg>')
    OUTPUT.write_text("\n".join(parts), encoding="utf-8")


if __name__ == "__main__":
    main()

