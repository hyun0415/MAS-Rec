# Data preparation

## Published experiment data

The paper reports two Amazon review domains after retaining interactions with both textual and visual information and applying the study's filtering procedure.

| Domain | Reviews | Users | Items | Sparsity |
|---|---:|---:|---:|---:|
| Clothing, Shoes and Jewelry | 66,718 | 7,449 | 16,099 | 99.944% |
| Cell Phones and Accessories | 23,491 | 4,149 | 4,975 | 99.886% |

The experiments use a random 70%/10%/20% train/validation/test split.

## Local processed files

The research archive supplied with this repository contains the following processed artifacts, which are intentionally excluded from Git because of size and redistribution concerns:

| Domain | Artifact | Approx. size |
|---|---|---:|
| Clothing | `Clothing_Shoes_aspect_final.pkl` | 154 MB |
| Clothing | `Clothing_Shoes_baseline_emb.pkl` | 2.98 GB |
| Clothing | `Clothing_Shoes_reasoning_final.pkl` | 204 MB |
| Clothing | `Clothing_Shoes_segment_final.pkl` | 170 MB |
| Clothing | `Clothing_Shoes_추가실험_1.pkl` | 441 MB |
| Cell Phones | `Cell_Phones_aspect_final.pkl` | 63 MB |
| Cell Phones | `Cell_Phones_baseline_emb.pkl` | 1.06 GB |
| Cell Phones | `Cell_Phones_reasoning_final.pkl` | 77 MB |
| Cell Phones | `Cell_Phones_segment_final.pkl` | 67 MB |
| Cell Phones | `Cell_Phones_추가실험_1.pkl` | 160 MB |

Keep these files outside version control. For local use, place them under category-specific folders inside `data/` and update the notebook path cells accordingly.

```text
data/
├── clothing/
└── cell_phones/
```

## Data governance

- Do not commit raw or processed customer/review data without confirming the source license and redistribution terms.
- Do not commit user identifiers, credentials, or signed download URLs.
- If the repository is later made public, document the official source and provide preprocessing instructions instead of uploading restricted artifacts.

