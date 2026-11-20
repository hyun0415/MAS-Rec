# Data guide

The paper uses Amazon review interactions that contain the information needed
for the text and image experiments. After filtering, the two datasets contain:

| Category | Reviews | Users | Items |
|---|---:|---:|---:|
| Clothing, Shoes and Jewelry | 66,718 | 7,449 | 16,099 |
| Cell Phones and Accessories | 23,491 | 4,149 | 4,975 |

The original source URL and exact source version must be confirmed before this
repository is made public. This repository therefore does not provide an
unverified download link.

## Expected columns after preparation

| Column | Meaning |
|---|---|
| `user_id` | Original user identifier |
| `item_id` | Original product identifier |
| `rating` | 1-to-5 star rating |
| `review_text` | Review content |
| `title` | Product title |
| `image_url` or local image reference | Product image input |
| `user_summary` | Attribute summary built from user reviews |
| `item_summary` | Attribute summary built from image and title |

Place private full data under `data/clothing/` or `data/cell_phones/`. These
folders are ignored by Git. The committed `data/sample/interactions.csv` is
synthetic and exists only for a small code check.

## Preparation rules

1. Apply the documented filters before splitting.
2. Create one split file and reuse it for every model.
3. Fit encoders and vocabularies using training rows only.
4. Keep test rows out of model selection and preprocessing decisions.
5. Record the source version, filtering counts, and dataset fingerprint.

Do not commit customer identifiers, raw reviews, signed image URLs, model
weights, or access tokens.

