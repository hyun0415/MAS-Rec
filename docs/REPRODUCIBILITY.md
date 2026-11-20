# Reproducibility guide

## Two kinds of results

- `reported_paper`: values copied from the published paper. They are stored in
  `results/metrics.csv` and must not be overwritten.
- `refactored_protocol`: values produced later with the shared split and metric
  code. No full result of this type is included yet.

A result from the synthetic sample is only a Smoke Test. It is not comparable
to the paper result.

## Lightweight code check

```bash
python -m venv .venv
pip install -r requirements.txt
python -m unittest discover -s tests -v
```

## Full experiment order

1. Obtain the Amazon review data under its original terms.
2. Apply the paper's review, image, and interaction filters.
3. Generate one shared split file with `src/data.py`.
4. Fit user IDs, item IDs, and text vocabularies on training rows only.
5. Generate the review and image summaries.
6. Train every model with `configs/refactored_protocol.toml`.
7. Choose the best checkpoint using validation MSE.
8. Evaluate the chosen checkpoint once on the test rows.
9. Save new rows as `refactored_protocol`; keep paper rows unchanged.

The archived notebooks under `notebooks/00_preprocessing` through
`notebooks/04_experiments` retain their original Colab paths and model-specific
settings. They are evidence of the research workflow, not the recommended local
entry point.

## Credentials and large files

Provide a Hugging Face token through `HF_TOKEN` or a hidden prompt. Never store
it in a notebook. Do not commit raw reviews, processed pickle files, images,
checkpoints, caches, or experiment-tracking logs.

