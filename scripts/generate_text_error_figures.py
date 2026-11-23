"""Generate SVG figures reported in the text error analysis note.

The values are copied from the executed outputs of
``notebooks/05_text_error_analysis.ipynb``. The script uses only the Python
standard library so that the figures can be regenerated without Matplotlib.
"""

from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "results" / "figures"

NAVY = "#243B5A"
GREEN = "#008000"
ORANGE = "#FFA000"
PALE_BLUE = "#5B8DB8"
GRID = "#D9DEE5"
TEXT = "#25313C"


def _multiline_text(x, y, label, *, size=13, anchor="middle", weight=400):
    tspans = []
    for index, line in enumerate(label.split("\n")):
        dy = "0" if index == 0 else "1.15em"
        tspans.append(
            f'<tspan x="{x:.1f}" dy="{dy}">{escape(line)}</tspan>'
        )
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" '
        f'font-size="{size}" font-weight="{weight}" fill="{TEXT}">'
        + "".join(tspans)
        + "</text>"
    )


def grouped_bar_svg(
    path,
    *,
    title,
    categories,
    series,
    y_label,
    value_format,
    y_max=None,
):
    width, height = 760, 470
    left, right, top, bottom = 82, 28, 62, 105
    plot_width = width - left - right
    plot_height = height - top - bottom
    all_values = [value for item in series for value in item[1]]
    maximum = y_max or max(all_values) * 1.18
    tick_count = 5

    elements = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" '
        f'height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        _multiline_text(width / 2, 31, title, size=18, weight=600),
    ]

    for tick in range(tick_count + 1):
        value = maximum * tick / tick_count
        y = top + plot_height - plot_height * tick / tick_count
        elements.append(
            f'<line x1="{left}" y1="{y:.1f}" x2="{width-right}" '
            f'y2="{y:.1f}" stroke="{GRID}" stroke-width="1"/>'
        )
        elements.append(
            f'<text x="{left-10}" y="{y+4:.1f}" text-anchor="end" '
            f'font-size="11" fill="{TEXT}">{escape(value_format(value))}</text>'
        )

    category_width = plot_width / len(categories)
    group_width = category_width * 0.72
    gap = 5
    bar_width = (group_width - gap * (len(series) - 1)) / len(series)

    for category_index, category in enumerate(categories):
        center = left + category_width * (category_index + 0.5)
        start = center - group_width / 2
        for series_index, (_, values, color) in enumerate(series):
            value = values[category_index]
            bar_height = plot_height * value / maximum
            x = start + series_index * (bar_width + gap)
            y = top + plot_height - bar_height
            elements.append(
                f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_width:.1f}" '
                f'height="{bar_height:.1f}" rx="2" fill="{color}"/>'
            )
            elements.append(
                f'<text x="{x+bar_width/2:.1f}" y="{max(y-7, top+12):.1f}" '
                f'text-anchor="middle" font-size="10.5" fill="{TEXT}">'
                f'{escape(value_format(value))}</text>'
            )
        elements.append(
            _multiline_text(center, top + plot_height + 24, category, size=12)
        )

    elements.append(
        f'<line x1="{left}" y1="{top+plot_height}" x2="{width-right}" '
        f'y2="{top+plot_height}" stroke="{TEXT}" stroke-width="1.2"/>'
    )
    elements.append(
        f'<text transform="translate(20 {top+plot_height/2}) rotate(-90)" '
        f'text-anchor="middle" font-size="12" fill="{TEXT}">{escape(y_label)}</text>'
    )

    legend_x = width - right - 105 * len(series)
    for index, (name, _, color) in enumerate(series):
        x = legend_x + index * 105
        elements.append(
            f'<rect x="{x}" y="{height-26}" width="12" height="12" '
            f'rx="2" fill="{color}"/>'
        )
        elements.append(
            f'<text x="{x+18}" y="{height-16}" font-size="11" '
            f'fill="{TEXT}">{escape(name)}</text>'
        )

    elements.append("</svg>")
    path.write_text("\n".join(elements), encoding="utf-8")


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    grouped_bar_svg(
        OUTPUT_DIR / "text_error_aspect_status.svg",
        title="Aspect Preservation Status",
        categories=["Paper\naspect", "Derived\naspect", "Additional\naspect"],
        series=[
            ("Omitted", [932, 1677, 15392], ORANGE),
            ("Preserved", [5366, 4304, 5661], GREEN),
            ("Summary only", [14510, 6284, 16906], NAVY),
        ],
        y_label="Comparison pairs",
        value_format=lambda value: f"{value:,.0f}",
        y_max=20000,
    )

    grouped_bar_svg(
        OUTPUT_DIR / "text_error_issue_mae.svg",
        title="MAE by Text Summary Issue",
        categories=["Sentiment\nflip", "Negative\nomission", "Summary-only\naspect"],
        series=[
            ("Without issue", [0.3143, 0.2983, 0.3436], PALE_BLUE),
            ("With issue", [0.5337, 0.5831, 0.3270], ORANGE),
        ],
        y_label="MAE",
        value_format=lambda value: f"{value:.3f}",
        y_max=0.70,
    )

    grouped_bar_svg(
        OUTPUT_DIR / "text_error_large_error_rate.svg",
        title="Large-error Rate by Text Summary Issue",
        categories=["Sentiment\nflip", "Negative\nomission", "Summary-only\naspect"],
        series=[
            ("Without issue", [0.0728, 0.0659, 0.0784], PALE_BLUE),
            ("With issue", [0.1514, 0.1793, 0.0776], GREEN),
        ],
        y_label="Large-error rate",
        value_format=lambda value: f"{value*100:.1f}%",
        y_max=0.22,
    )

    grouped_bar_svg(
        OUTPUT_DIR / "text_error_gpt_review.svg",
        title="GPT-5.6-Sol Medium Review of 96 Cases",
        categories=["Unsupported\nclaim", "Sentiment\ndistortion", "Complaint\nomission"],
        series=[
            ("Small error", [0.2391, 0.0217, 0.0217], PALE_BLUE),
            ("Large error", [0.4800, 0.2200, 0.4200], NAVY),
        ],
        y_label="Case rate",
        value_format=lambda value: f"{value*100:.1f}%",
        y_max=0.60,
    )

    print(f"Saved four SVG figures to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
