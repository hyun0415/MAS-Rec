# Limitations

[한국어](LIMITATIONS.md)

- LLM-generated summaries may omit preference-relevant details or introduce
  expressions that are not supported by the original review or image.
- The experiments cover two Amazon product categories. Additional domains are
  required to verify generalizability.
- The study converts each review and image into an attribute-oriented summary.
  Future work may construct user- and item-level summaries from sets of UGC to
  represent longer-term preferences more directly.
- The effect of interaction sparsity on each model component was not isolated
  quantitatively.
- Textual attribute matching can support systematic error analysis, but visual
  evidence cannot be validated with the same procedure. The image-modality
  analysis is therefore more limited.
- Attention Rollout indicates relative attention allocation and does not
  establish a causal explanation for an individual prediction.
- Full reproduction requires access to the original data, large language
  models, processed features, trained weights, and substantial compute.
