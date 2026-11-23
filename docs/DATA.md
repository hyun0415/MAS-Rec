# 데이터 구성

[English](DATA_EN.md)

## 연구 데이터

본 연구는 텍스트와 이미지 정보가 모두 존재하는 Amazon 리뷰를 대상으로 필터링을
수행하였다. 최종 실험에는 Clothing, Shoes and Jewelry와 Cell Phones and
Accessories의 두 카테고리를 사용하였다.

| 카테고리 | 리뷰 수 | 사용자 수 | 상품 수 | 희소성 |
|---|---:|---:|---:|---:|
| Clothing, Shoes and Jewelry | 66,718 | 7,449 | 16,099 | 99.944% |
| Cell Phones and Accessories | 23,491 | 4,149 | 4,975 | 99.886% |

각 데이터셋은 학습 70%, 검증 10%, 테스트 20%의 비율로 무작위 분할하였다. 예측
대상은 리뷰에 포함된 1~5점 평점이며, 검증 성능을 기준으로 최적 모델을 선택한 뒤
테스트 데이터에서 최종 성능을 평가하였다.

## 주요 분석 파일

대용량 전처리 파일은 크기와 재배포 조건을 고려하여 GitHub 저장소에 포함하지
않았다. 연구 과정에서 사용한 주요 파일은 다음과 같다.

| 카테고리 | 파일 | 용도 | 대략적인 크기 |
|---|---|---|---:|
| Clothing | `Clothing_Shoes_aspect_final.pkl` | 속성 요약 최종 데이터 | 154 MB |
| Clothing | `Clothing_Shoes_baseline_emb.pkl` | Baseline 임베딩 | 2.98 GB |
| Clothing | `Clothing_Shoes_reasoning_final.pkl` | Reasoning 프롬프트 결과 | 204 MB |
| Clothing | `Clothing_Shoes_segment_final.pkl` | Segment 프롬프트 결과 | 170 MB |
| Clothing | `Clothing_Shoes_추가실험_1.pkl` | 추가 실험 데이터 | 441 MB |
| Cell Phones | `Cell_Phones_aspect_final.pkl` | 속성 요약 최종 데이터 | 63 MB |
| Cell Phones | `Cell_Phones_baseline_emb.pkl` | Baseline 임베딩 | 1.06 GB |
| Cell Phones | `Cell_Phones_reasoning_final.pkl` | Reasoning 프롬프트 결과 | 77 MB |
| Cell Phones | `Cell_Phones_segment_final.pkl` | Segment 프롬프트 결과 | 67 MB |
| Cell Phones | `Cell_Phones_추가실험_1.pkl` | 추가 실험 데이터 | 160 MB |

## 주요 컬럼

| 컬럼 | 의미 |
|---|---|
| `user_id` | 사용자 식별값 |
| `asin` | Amazon 상품 식별값 |
| `rating` | 1~5점 평점 |
| `text` | 리뷰 원문 |
| `title_y` | 상품명 |
| `medium_image_url` | 리뷰 또는 상품 이미지 주소 |
| `LLaMA_Output` | 리뷰에서 생성한 속성 중심 요약문 |
| `LLaVA_Output` | 이미지와 상품명에서 생성한 속성 설명 |

파일별 임베딩 컬럼은 실험 목적에 따라 BERT, RoBERTa, ViT, VGG16 표현을 포함한다.
EDA와 오류 분석에서는 원문, 요약문, 평점 및 원본 행 번호를 중심으로 사용하였다.

## 데이터 경로

노트북은 Google Colab과 Google Drive를 기준으로 작성되어 있다. 대용량 파일은
카테고리별 폴더에 보관하고 각 노트북의 경로 셀을 실제 Drive 구성에 맞게 확인해야
한다.

```text
MAS-Rec/
├── Clothing and Shoes/
│   ├── 01_Base_Data/
│   ├── 02_Feature_Data/
│   ├── 03_LLM_Outputs/
│   ├── 04_Chunks/
│   └── 05_Experiment_Results/
└── Cell Phone/
    ├── 01_Base_Data/
    ├── 02_Feature_Data/
    ├── 03_LLM_Outputs/
    ├── 04_Chunks/
    └── 05_Experiment_Results/
```

`data/sample/`의 CSV는 실제 데이터의 컬럼 구성을 확인하기 위한 합성 예시이며, 논문
결과 산출에는 사용하지 않았다.

## 공개 시 주의사항

- 원본 및 전처리 리뷰 데이터는 출처의 라이선스와 재배포 조건을 확인하지 않은 상태로
  저장소에 포함하지 않는다.
- 사용자 식별값, 인증정보 및 서명된 다운로드 주소는 공개하지 않는다.
- 대용량 임베딩, 모델 가중치, 캐시 및 실험 로그는 저장소 외부에서 관리한다.
- 공개 저장소에서는 데이터 원본 대신 공식 출처와 전처리 절차를 안내한다.
