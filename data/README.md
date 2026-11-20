# 데이터 안내

이 프로젝트는 Amazon 리뷰 데이터의 두 카테고리를 사용합니다.

| 카테고리 | 리뷰 수 | 사용자 수 | 상품 수 |
|---|---:|---:|---:|
| Clothing, Shoes and Jewelry | 66,718 | 7,449 | 16,099 |
| Cell Phones and Accessories | 23,491 | 4,149 | 4,975 |

## EDA에 사용한 파일

`notebooks/01_eda.ipynb`는 사용자가 보관한 `우수현_논문_Dataset.zip` 안에서 다음 두
파일만 읽습니다.

- `Clothing_Shoes_aspect_final.pkl`
- `Cell_Phones_aspect_final.pkl`

ZIP 전체를 풀 필요는 없습니다. ZIP을 기본 다운로드 폴더에 두면 바로 읽을 수 있습니다.
다른 위치에 두었다면 실행 전에 경로를 지정합니다.

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
| `LLaMA_Output` | 리뷰에서 만든 속성 요약 |
| `LLaVA_Output` | 이미지에서 만든 속성 설명 |

## 모델 실험에서 지킬 기준

1. 모든 모델이 같은 필터링 결과를 사용합니다.
2. 한 번 만든 Train, Validation, Test 인덱스를 모든 모델이 공유합니다.
3. 사용자·상품 인코더와 텍스트 처리 기준은 Train 데이터에서만 만듭니다.
4. Test 데이터는 마지막 성능 평가에서만 사용합니다.
5. 사용한 파일의 이름과 SHA-256 값을 함께 기록합니다.

## 공개 시 주의사항

전체 데이터, 사용자 ID, 리뷰 원문, 이미지 URL은 GitHub에 올리지 않습니다. EDA
노트북에는 데이터 규모와 분포처럼 여러 행을 합친 결과만 남깁니다. 저장소의
`data/sample/`은 코드 확인용 합성 데이터이며 논문 결과를 재현한 데이터가 아닙니다.

두 최종 파일의 SHA-256 값은 다음과 같습니다.

- Clothing: `f3b09fd9d860ef9370454f4195dc65aa84f765e615c7b5565f4415fd9d16a8ff`
- Cell Phones: `c32ad3de384500c7eff6990affd68cf37363601c9f14d4a0881015af7d5b04f0`
