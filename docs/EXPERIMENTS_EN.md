# Experiment map and reported results

[한국어](EXPERIMENTS.md)

## Main comparison

All values below are reproduced from the paper. Lower is better.

### Clothing, Shoes and Jewelry

| Model | MAE | MSE | RMSE | MAPE |
|---|---:|---:|---:|---:|
| NeuMF | 0.588 | 0.539 | 0.734 | 0.168 |
| ANR | 0.527 | 0.509 | 0.713 | 0.152 |
| AFRAM | 0.500 | 0.461 | 0.679 | 0.145 |
| MFNR | 0.483 | 0.450 | 0.670 | 0.141 |
| CAMRec | 0.397 | 0.299 | 0.547 | 0.110 |
| MMCN | 0.386 | 0.302 | 0.549 | 0.108 |
| **MAS-Rec** | **0.316** | **0.257** | **0.507** | **0.089** |

### Cell Phones and Accessories

| Model | MAE | MSE | RMSE | MAPE |
|---|---:|---:|---:|---:|
| NeuMF | 0.595 | 0.585 | 0.765 | 0.182 |
| ANR | 0.544 | 0.575 | 0.758 | 0.168 |
| AFRAM | 0.505 | 0.529 | 0.727 | 0.160 |
| MFNR | 0.500 | 0.500 | 0.707 | 0.156 |
| CAMRec | 0.451 | 0.403 | 0.635 | 0.136 |
| MMCN | 0.444 | 0.386 | 0.621 | 0.126 |
| **MAS-Rec** | **0.299** | **0.278** | **0.527** | **0.090** |

## RQ1: fusion strategy

| Dataset | Fusion | MAE | MSE | RMSE | MAPE |
|---|---|---:|---:|---:|---:|
| Clothing | Dot product | 0.539 | 0.505 | 0.711 | 0.138 |
| Clothing | Element-wise | 0.355 | 0.287 | 0.536 | 0.098 |
| Clothing | Concatenation | 0.318 | 0.264 | 0.514 | 0.089 |
| Clothing | Co-attention | **0.316** | **0.257** | **0.507** | **0.089** |
| Cell Phones | Dot product | 0.535 | 0.517 | 0.719 | 0.141 |
| Cell Phones | Element-wise | 0.376 | 0.326 | 0.571 | 0.107 |
| Cell Phones | Concatenation | 0.310 | 0.289 | 0.538 | 0.095 |
| Cell Phones | Co-attention | **0.299** | **0.278** | **0.527** | **0.090** |

Notebook: `notebooks/04_experiments/rq1_fusion_strategy.ipynb`

## RQ2: prompt strategy

| Dataset | Prompt strategy | MAE | MSE | RMSE | MAPE |
|---|---|---:|---:|---:|---:|
| Clothing | Segment | 0.342 | 0.309 | 0.556 | 0.098 |
| Clothing | Reasoning | **0.290** | **0.229** | **0.478** | **0.082** |
| Clothing | Aspect-based summary | 0.316 | 0.257 | 0.507 | 0.089 |
| Cell Phones | Segment | 0.381 | 0.392 | 0.626 | 0.118 |
| Cell Phones | Reasoning | 0.307 | 0.287 | 0.535 | 0.093 |
| Cell Phones | Aspect-based summary | **0.299** | **0.278** | **0.527** | **0.090** |

Notebooks: `notebooks/04_experiments/rq2_prompt_comparison/`

## Conventional encoders vs. LLM summaries

| Dataset | Representation | MAE | MSE | RMSE | MAPE |
|---|---|---:|---:|---:|---:|
| Clothing | BERT + ViT | 0.398 | 0.315 | 0.561 | 0.112 |
| Clothing | LLM summaries | **0.316** | **0.257** | **0.507** | **0.089** |
| Cell Phones | BERT + ViT | 0.447 | 0.393 | 0.627 | 0.133 |
| Cell Phones | LLM summaries | **0.299** | **0.278** | **0.527** | **0.090** |

## Interpretability analysis

`notebooks/04_experiments/rq3_attention_rollout.ipynb` applies Attention Rollout to inspect which expressions receive relatively high attention after recommendation-oriented fine-tuning. This is an interpretability aid, not a causal explanation of the prediction.

