# Limitations

- The LLM summaries can omit details or introduce unsupported wording. They are
  useful representations, not verified facts about a product.
- The reported results cover two Amazon categories. Performance may change in
  domains with different language, images, or interaction patterns.
- Attention Rollout shows where the encoder placed relatively high attention.
  It does not prove why a rating was predicted.
- The archived notebooks fit some encoders before splitting the data. The new
  protocol fixes this, but the large experiments have not yet been rerun.
- The co-attention layer receives one pooled vector per side. Its attention map
  should therefore not be interpreted as token-level interaction evidence.
- Large language models, processed data, and trained weights are not included,
  so full reproduction requires separate access and substantial compute.

