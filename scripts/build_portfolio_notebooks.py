"""Build small, output-preserving portfolio notebooks from committed files."""

from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.data import make_split_indices
from src.evaluation import rating_metrics


NOTEBOOKS = ROOT / "notebooks"
SAMPLE = ROOT / "data" / "sample" / "interactions.csv"
METRICS = ROOT / "results" / "metrics.csv"


def markdown(text: str) -> dict:
    return {"cell_type": "markdown", "metadata": {}, "source": text.splitlines(True)}


def code(source: str, output: str, count: int) -> dict:
    return {
        "cell_type": "code",
        "execution_count": count,
        "metadata": {},
        "outputs": [{"name": "stdout", "output_type": "stream", "text": output.splitlines(True)}],
        "source": source.splitlines(True),
    }


def notebook(cells: list[dict]) -> dict:
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def write(name: str, cells: list[dict]) -> None:
    destination = NOTEBOOKS / name
    destination.write_text(json.dumps(notebook(cells), ensure_ascii=False, indent=1), encoding="utf-8")


def main() -> None:
    sample = pd.read_csv(SAMPLE)
    ratings = sample["rating"].value_counts().sort_index()
    missing = sample.isna().sum()
    eda_output = (
        f"rows: {len(sample)}\nusers: {sample.user_id.nunique()}\nitems: {sample.item_id.nunique()}\n"
        f"missing cells: {int(missing.sum())}\nrating counts:\n{ratings.to_string()}\n"
    )
    write(
        "01_eda.ipynb",
        [
            markdown("# 01. Data check\n\nThis notebook uses the committed synthetic sample. It does not reproduce the paper dataset."),
            code(
                "from pathlib import Path\nimport pandas as pd\n\nROOT = Path.cwd().parent if Path.cwd().name == 'notebooks' else Path.cwd()\ndf = pd.read_csv(ROOT / 'data/sample/interactions.csv')\nprint(f'rows: {len(df)}')\nprint(f'users: {df.user_id.nunique()}')\nprint(f'items: {df.item_id.nunique()}')\nprint(f'missing cells: {int(df.isna().sum().sum())}')\nprint('rating counts:')\nprint(df.rating.value_counts().sort_index())\n",
                eda_output,
                1,
            ),
            markdown("The sample is intentionally tiny. The useful checks are column names, missing values, and whether the rating scale is read correctly."),
        ],
    )

    examples = sample[["user_summary", "item_summary", "rating"]].head(3)
    write(
        "02_summarization_demo.ipynb",
        [
            markdown("# 02. Attribute-summary examples\n\nThe full study used LLaMA and LLaVA. This lightweight notebook only shows the expected input and output shape; it does not call an LLM."),
            code(
                "from pathlib import Path\nimport pandas as pd\n\nROOT = Path.cwd().parent if Path.cwd().name == 'notebooks' else Path.cwd()\ndf = pd.read_csv(ROOT / 'data/sample/interactions.csv')\nprint(df[['user_summary', 'item_summary', 'rating']].head(3).to_string(index=False))\n",
                examples.to_string(index=False) + "\n",
                1,
            ),
            markdown("A useful summary keeps preference-bearing details, avoids unsupported claims, and uses similar attribute language for the user and the product."),
        ],
    )

    split = make_split_indices(sample)
    train_mean = float(sample.iloc[split.train].rating.mean())
    smoke = sample.iloc[split.validation]
    smoke_metrics = rating_metrics(smoke.rating, np.full(len(smoke), train_mean))
    smoke_output = (
        f"split sizes: train={len(split.train)}, validation={len(split.validation)}, test={len(split.test)}\n"
        f"training-mean baseline on validation: {smoke_metrics}\n"
        "status: SMOKE TEST - not comparable to paper results\n"
    )
    paper = pd.read_csv(METRICS)
    main_results = paper[(paper.protocol == "reported_paper") & (paper.study == "main")]
    main_table = main_results.pivot(index="model", columns="dataset", values="rmse").round(3)
    write(
        "03_mas_rec_experiment.ipynb",
        [
            markdown("# 03. Experiment protocol and reported results\n\nThe first cell checks the shared split on synthetic data. The second cell reads published values from the committed result file."),
            code(
                "from pathlib import Path\nimport sys\nimport numpy as np\nimport pandas as pd\n\nROOT = Path.cwd().parent if Path.cwd().name == 'notebooks' else Path.cwd()\nsys.path.insert(0, str(ROOT))\nfrom src.data import make_split_indices\nfrom src.evaluation import rating_metrics\n\ndf = pd.read_csv(ROOT / 'data/sample/interactions.csv')\nsplit = make_split_indices(df)\ntrain_mean = df.iloc[split.train].rating.mean()\nvalid = df.iloc[split.validation]\nmetrics = rating_metrics(valid.rating, np.full(len(valid), train_mean))\nprint(f'split sizes: train={len(split.train)}, validation={len(split.validation)}, test={len(split.test)}')\nprint(f'training-mean baseline on validation: {metrics}')\nprint('status: SMOKE TEST - not comparable to paper results')\n",
                smoke_output,
                1,
            ),
            code(
                "results = pd.read_csv(ROOT / 'results/metrics.csv')\nmain = results[(results.protocol == 'reported_paper') & (results.study == 'main')]\nprint(main.pivot(index='model', columns='dataset', values='rmse').round(3).to_string())\nprint('status: REPORTED PAPER VALUES - full training not rerun')\n",
                main_table.to_string() + "\nstatus: REPORTED PAPER VALUES - full training not rerun\n",
                2,
            ),
        ],
    )

    error_frame = sample.iloc[split.validation].copy()
    error_frame["prediction"] = train_mean
    error_frame["absolute_error"] = (error_frame.rating - train_mean).abs()
    error_view = error_frame[["user_id", "item_id", "rating", "prediction", "absolute_error", "user_summary", "item_summary"]].sort_values("absolute_error", ascending=False)
    write(
        "04_error_analysis.ipynb",
        [
            markdown("# 04. Error-analysis pattern\n\nThis notebook demonstrates the questions to ask with a synthetic mean-prediction baseline. It is not an analysis of the trained MAS-Rec model."),
            code(
                "valid_errors = valid.copy()\nvalid_errors['prediction'] = train_mean\nvalid_errors['absolute_error'] = (valid_errors.rating - train_mean).abs()\ncolumns = ['user_id', 'item_id', 'rating', 'prediction', 'absolute_error', 'user_summary', 'item_summary']\nprint(valid_errors[columns].sort_values('absolute_error', ascending=False).to_string(index=False))\n",
                error_view.to_string(index=False) + "\n",
                1,
            ),
            markdown("For full-model errors, inspect summary omissions, unsupported image descriptions, rare users/items, and domain-specific attributes. Do not treat attention as a causal explanation."),
        ],
    )


if __name__ == "__main__":
    main()

