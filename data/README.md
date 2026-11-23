# 데이터 안내

이 프로젝트는 Amazon 리뷰 데이터의 두 카테고리를 사용한다.

| 카테고리 | 리뷰 수 | 사용자 수 | 상품 수 |
|---|---:|---:|---:|
| Clothing, Shoes and Jewelry | 66,718 | 7,449 | 16,099 |
| Cell Phones and Accessories | 23,491 | 4,149 | 4,975 |

## EDA에 사용한 파일

`notebooks/01_eda.ipynb`는 `우수현_논문_Dataset.zip`에 포함된 다음 두 파일을 읽는다.

- `Clothing_Shoes_aspect_final.pkl`
- `Cell_Phones_aspect_final.pkl`

ZIP 전체를 풀 필요는 없다. 파일을 기본 다운로드 폴더에 두면 바로 읽을 수 있으며,
다른 위치에 저장한 경우 실행 전에 경로를 지정한다.

```powershell
$env:MAS_REC_DATA_ZIP = "D:\data\우수현_논문_Dataset.zip"
```

## 주요 컬럼

| 컬럼 | 의미 |
|---|---|
| `user_id` | 사용자 식별값 |
| `asin` | 상품 식별값 |
| `rating` | 1~5점 평점 |
| `text` | 리뷰 원문 |
| `title_y` | 상품명 |
| `LLaMA_Output` | 리뷰에서 생성한 속성 요약 |
| `LLaVA_Output` | 이미지에서 생성한 속성 설명 |

## 실험 데이터 관리 기준

1. 모든 모델은 동일한 필터링 결과와 70:10:20 분할 비율을 사용한다.
2. 사용자와 상품 식별값에는 동일한 인덱싱 기준을 적용한다.
3. 모델별로 필요한 리뷰 텍스트, 이미지, 요약문 표현을 동일한 원본 행에 연결한다.
4. 검증 데이터로 최적 모델을 선택하고 테스트 데이터로 최종 성능을 평가한다.
5. 사용 파일명과 SHA-256 값을 함께 기록한다.

## 공개 시 주의사항

전체 데이터, 사용자 ID, 리뷰 원문, 이미지 URL은 GitHub에 올리지 않는다. EDA
노트북에는 데이터 규모와 분포처럼 여러 행을 집계한 결과만 남긴다. `data/sample/`은
코드 확인용 합성 데이터이며 논문 결과 산출에는 사용하지 않았다.

최종 분석 파일의 SHA-256 값은 다음과 같다.

- Clothing: `f3b09fd9d860ef9370454f4195dc65aa84f765e615c7b5565f4415fd9d16a8ff`
- Cell Phones: `c32ad3de384500c7eff6990affd68cf37363601c9f14d4a0881015af7d5b04f0`
