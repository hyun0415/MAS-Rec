# 실험 구성 및 결과

[English](EXPERIMENTS_EN.md)

아래 결과는 논문에 보고된 값을 정리한 것이며, 모든 오차 지표는 낮을수록 우수하다.

## 주요 비교 결과

### Clothing, Shoes and Jewelry

| 모델 | MAE | MSE | RMSE | MAPE |
|---|---:|---:|---:|---:|
| NeuMF | 0.588 | 0.539 | 0.734 | 0.168 |
| ANR | 0.527 | 0.509 | 0.713 | 0.152 |
| AFRAM | 0.500 | 0.461 | 0.679 | 0.145 |
| MFNR | 0.483 | 0.450 | 0.670 | 0.141 |
| CAMRec | 0.397 | 0.299 | 0.547 | 0.110 |
| MMCN | 0.386 | 0.302 | 0.549 | 0.108 |
| **MAS-Rec** | **0.316** | **0.257** | **0.507** | **0.089** |

### Cell Phones and Accessories

| 모델 | MAE | MSE | RMSE | MAPE |
|---|---:|---:|---:|---:|
| NeuMF | 0.595 | 0.585 | 0.765 | 0.182 |
| ANR | 0.544 | 0.575 | 0.758 | 0.168 |
| AFRAM | 0.505 | 0.529 | 0.727 | 0.160 |
| MFNR | 0.500 | 0.500 | 0.707 | 0.156 |
| CAMRec | 0.451 | 0.403 | 0.635 | 0.136 |
| MMCN | 0.444 | 0.386 | 0.621 | 0.126 |
| **MAS-Rec** | **0.299** | **0.278** | **0.527** | **0.090** |

MAS-Rec은 두 카테고리에서 비교 모델보다 낮은 MAE와 RMSE를 기록하였다. 이는
텍스트와 이미지 UGC를 속성 중심의 문장으로 변환하고, 추천 목적에 맞게 표현을
학습하는 방식이 사용자 선호와 상품 특성을 나타내는 데 효과적임을 보여준다.

## RQ1: 특징 결합 방식

| 데이터셋 | 결합 방식 | MAE | MSE | RMSE | MAPE |
|---|---|---:|---:|---:|---:|
| Clothing | Dot product | 0.539 | 0.505 | 0.711 | 0.138 |
| Clothing | Element-wise product | 0.355 | 0.287 | 0.536 | 0.098 |
| Clothing | Concatenation | 0.318 | 0.264 | 0.514 | 0.089 |
| Clothing | Co-Attention | **0.316** | **0.257** | **0.507** | **0.089** |
| Cell Phones | Dot product | 0.535 | 0.517 | 0.719 | 0.141 |
| Cell Phones | Element-wise product | 0.376 | 0.326 | 0.571 | 0.107 |
| Cell Phones | Concatenation | 0.310 | 0.289 | 0.538 | 0.095 |
| Cell Phones | Co-Attention | **0.299** | **0.278** | **0.527** | **0.090** |

Co-Attention은 두 데이터셋에서 가장 낮은 오차를 기록하였다. Concatenation도 유사한
성능을 보였으나, Co-Attention은 사용자 표현과 상품 표현 사이의 상호작용을 명시적으로
반영한다는 점에서 차이가 있다.

분석 노트북:
[`notebooks/04_experiments/rq1_fusion_strategy.ipynb`](../notebooks/04_experiments/rq1_fusion_strategy.ipynb)

## RQ2: 프롬프트 전략

| 데이터셋 | 프롬프트 전략 | MAE | MSE | RMSE | MAPE |
|---|---|---:|---:|---:|---:|
| Clothing | Segment | 0.342 | 0.309 | 0.556 | 0.098 |
| Clothing | Reasoning | **0.290** | **0.229** | **0.478** | **0.082** |
| Clothing | Aspect-based summary | 0.316 | 0.257 | 0.507 | 0.089 |
| Cell Phones | Segment | 0.381 | 0.392 | 0.626 | 0.118 |
| Cell Phones | Reasoning | 0.307 | 0.287 | 0.535 | 0.093 |
| Cell Phones | Aspect-based summary | **0.299** | **0.278** | **0.527** | **0.090** |

Clothing에서는 Reasoning 방식이 가장 높은 성능을 보였으며, Cell Phones에서는 속성
요약 방식이 가장 높은 성능을 보였다. 따라서 하나의 프롬프트가 모든 도메인에서 항상
우수하다고 보기 어렵고, 도메인의 리뷰 특성과 주요 속성을 고려하여 프롬프트를 선택할
필요가 있다.

분석 노트북:
[`notebooks/04_experiments/rq2_prompt_comparison/`](../notebooks/04_experiments/rq2_prompt_comparison/)

## 기존 인코더와 LLM 요약 비교

| 데이터셋 | 표현 방식 | MAE | MSE | RMSE | MAPE |
|---|---|---:|---:|---:|---:|
| Clothing | BERT + ViT | 0.398 | 0.315 | 0.561 | 0.112 |
| Clothing | LLM summary | **0.316** | **0.257** | **0.507** | **0.089** |
| Cell Phones | BERT + ViT | 0.447 | 0.393 | 0.627 | 0.133 |
| Cell Phones | LLM summary | **0.299** | **0.278** | **0.527** | **0.090** |

LLM 요약 표현은 BERT와 ViT의 직접적인 임베딩 결합보다 낮은 오차를 기록하였다. 이는
UGC의 전체 정보를 그대로 결합하기보다 추천과 관련된 속성 정보를 선별하여 공통된
텍스트 표현으로 변환하는 과정이 추천 성능 향상에 기여할 수 있음을 보여준다.

## 모델 해석

[`notebooks/04_experiments/rq3_attention_rollout.ipynb`](../notebooks/04_experiments/rq3_attention_rollout.ipynb)는
Attention Rollout을 이용하여 추천 목적의 미세조정 이후 상대적으로 높은 주의를 받은
표현을 확인한다. 해당 결과는 모델 내부 표현을 점검하기 위한 보조 자료이며, 개별
예측의 직접적인 인과관계를 설명하는 결과로 해석하지 않는다.

텍스트 요약 오류와 예측 오차의 관계는
[`TEXT_ERROR_ANALYSIS.md`](TEXT_ERROR_ANALYSIS.md)에 별도로 정리하였다.
