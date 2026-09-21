# Reproducibility guide

## Published setup

- Split: random 70% training / 10% validation / 20% test
- Optimizer: AdamW
- Learning rate: `1e-5`
- Batch size: `32`
- User/item ID embedding dimension: `64`
- Attention heads: `8`
- Maximum epochs: `100`
- Early stopping patience: `5`
- Runs reported: `5`
- Hardware reported: Google Colab with NVIDIA A100 GPU
- Metrics: MAE, MSE, RMSE, MAPE

## Recommended execution order

1. Run the category filtering notebook in `notebooks/00_preprocessing/`.
2. Generate conventional text/image representations where required by the baselines.
3. Generate review and image aspect summaries in `notebooks/01_summarization/`.
4. Train `notebooks/02_model/mas_rec.ipynb`.
5. Run baseline and additional experiment notebooks.

## Path configuration

The archived notebooks preserve some legacy Google Colab paths such as `/content/drive/MyDrive/...`. Before execution, replace them with paths for your runtime. A practical local convention is:

```text
MAS-Rec/
├── data/
│   ├── clothing/
│   └── cell_phones/
└── checkpoints/
```

Do not commit generated datasets, model weights, or local virtual environments.

## Credentials

The summarization notebooks accept a Hugging Face access token from the `HF_TOKEN` environment variable or a hidden interactive prompt. Never paste a token into a notebook cell. If a credential was ever embedded in a notebook, revoke it before sharing the repository—even if the notebook was later cleaned.

## Scope of this archive

Notebook outputs were removed to keep the repository reviewable and to avoid exposing runtime metadata. The paper's numerical results are preserved in `docs/EXPERIMENTS.md`. Exact reruns may vary with package versions, model revisions, random seeds, and hosted-model access; freeze a tested environment before claiming byte-for-byte reproducibility.

