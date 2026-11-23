# 재현 안내

[English](REPRODUCIBILITY_EN.md)

## 결과의 출처

- `results/metrics.csv`의 `reported_paper`는 출판 논문에 보고된 값을 의미한다.
- `data/sample/`은 실제 데이터의 컬럼 구성을 확인하기 위한 합성 예시이며, 논문 결과와
  비교할 수 없다.
- 노트북에 저장된 출력은 연구 당시 실행 결과를 보존한 것으로, 새로운 환경에서 다시
  실행하면 라이브러리 버전과 하드웨어에 따라 일부 값이 달라질 수 있다.

## 노트북 실행 환경

```bash
pip install -r requirements.txt
```

노트북은 Google Colab과 Google Drive를 기준으로 작성되어 있다. 실행 전 다음 항목을
확인해야 한다.

1. Google Drive가 `/content/drive`에 연결되어 있는가?
2. 데이터 파일과 모델 가중치의 경로가 현재 Drive 구성과 일치하는가?
3. GPU가 필요한 노트북에서 CUDA 런타임이 활성화되어 있는가?
4. Hugging Face 등 외부 모델 접근에 필요한 인증정보가 안전하게 설정되어 있는가?
5. 설치 셀 실행 후 런타임 재시작이 필요한 라이브러리가 있는가?

## 전체 실험 순서

1. Amazon 리뷰 데이터를 원본 배포 조건에 따라 준비한다.
2. 논문에 기술된 리뷰, 이미지 및 상호작용 필터링을 적용한다.
3. Seed 42를 사용하여 학습 70%, 검증 10%, 테스트 20%로 분할한다.
4. 각 모델에 필요한 사용자, 상품, 텍스트 및 이미지 표현을 준비한다.
5. LLaMA 리뷰 요약과 LLaVA 이미지 설명을 생성한다.
6. 노트북에 기록된 하이퍼파라미터를 사용하여 모델을 학습한다.
7. 검증 MSE가 가장 낮은 체크포인트를 선택한다.
8. 선택한 모델을 테스트 데이터에서 MAE, MSE, RMSE, MAPE로 평가한다.
9. 데이터셋, 모델, Seed, 하이퍼파라미터 및 평가 결과를 함께 기록한다.

NeuMF, CAMRec, MMCN은 대표 비교 모델 노트북으로 제공한다. 전체 논문 결과에는 다른
비교 모델도 포함되지만, 저장소에는 직접 공유 가능한 대표 구현만 남겼다.

## 주요 노트북 흐름

| 단계 | 경로 | 역할 |
|---|---|---|
| 전처리 | `notebooks/00_preprocessing/` | 텍스트·이미지 특징 준비 |
| 요약 | `notebooks/01_summarization/` | LLaMA·LLaVA 출력 생성 |
| EDA | `notebooks/01_eda.ipynb` | 데이터 분포와 주요 컬럼 확인 |
| 비교 모델 | `notebooks/03_baselines/` | NeuMF·CAMRec·MMCN 실험 |
| 제안 모델 | `notebooks/03_mas_rec_experiment.ipynb` | MAS-Rec 학습 및 평가 |
| 추가 실험 | `notebooks/04_experiments/` | 결합 방식·프롬프트·Attention 분석 |
| 오류 분석 | `notebooks/05_text_error_analysis.ipynb` | 텍스트 요약 오류와 예측 오차 분석 |

## 인증정보와 대용량 파일

Hugging Face 토큰은 `HF_TOKEN`이나 숨겨진 입력 방식을 사용한다. 인증정보를 노트북에
직접 기록하지 않는다. 원본 리뷰, 전처리 pickle, 이미지, 모델 가중치, 캐시 및 실험
로그는 Git 저장소 외부에서 관리한다.
