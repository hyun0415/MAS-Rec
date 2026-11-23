# Reproducibility guide

## Result provenance

- `reported_paper` identifies values reported in the published article and
  stored in `results/metrics.csv`.
- `data/sample/` is a synthetic schema example and is not comparable with the
  paper results.

## Notebook environment

```bash
pip install -r requirements.txt
```

The notebooks are designed for Google Colab and Google Drive. Confirm the
runtime, mounted Drive path, and required data files before running each
notebook.

## Full experiment order

1. Obtain the Amazon review data under its original terms.
2. Apply the review, image, and interaction filters described in the paper.
3. Generate the 70:10:20 training, validation, and test split with seed 42.
4. Prepare the user, item, text, and image representations required by each
   model.
5. Generate the LLaMA review summaries and LLaVA image descriptions.
6. Train each model using its documented hyperparameters.
7. Select the checkpoint with the lowest validation MSE.
8. Evaluate the selected checkpoint on the test set using MAE, MSE, RMSE, and
   MAPE.
9. Record the dataset, model, seed, hyperparameters, and metric values together.

The notebooks retain their Colab-oriented paths and research-stage outputs.
NeuMF, CAMRec, and MMCN are provided as representative baseline notebooks.

## Credentials and large files

Provide a Hugging Face token through `HF_TOKEN` or a hidden prompt. Never store
credentials in a notebook. Raw reviews, processed pickle files, images,
checkpoints, caches, and experiment-tracking logs should not be committed to the
repository.
