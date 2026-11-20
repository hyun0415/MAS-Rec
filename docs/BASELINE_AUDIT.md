# Baseline protocol audit

This audit separates the archived paper notebooks from the new portfolio
protocol. It does not change the published results.

## What the archived notebooks do

All rating models use a 70% training, 10% validation, and 20% test split with
random seed 42. However, each notebook creates its own split. This is safe only
when every notebook receives rows in exactly the same order.

| Model | Archived batch size | Archived validation setup | Best weights restored |
|---|---:|---|---|
| MAS-Rec | 64 | Explicit validation rows | Yes, through Trainer |
| AFRAM | 64 | Explicit validation rows | Yes |
| ANR | 128 | Explicit validation rows | Yes |
| NeuMF | 128 | Explicit validation rows | Yes |
| MFNR | 128 | Explicit validation rows | Yes |
| CAMRec | 256 | Explicit validation rows | Yes |
| MMCN | 128 | Explicit validation rows | Yes |

User and item encoders are fitted before the split in the archived notebooks.
ANR and AFRAM also fit their text vocabulary before the split. This exposes the
set of validation and test IDs or words during preparation, even though ratings
are not used directly.

## Refactored portfolio protocol

The new protocol uses one saved split file for every model. ID mappings and text
vocabularies are fitted on training rows only. Unknown validation or test IDs
map to a reserved index instead of changing the training vocabulary.

The shared settings are:

- random seed 42;
- 70% training, 10% validation, and 20% test;
- batch size 32;
- early stopping after five validation epochs without improvement;
- best validation weights restored before final evaluation;
- MAE, MSE, RMSE, and MAPE from `src/evaluation.py`;
- test rows used once, after model selection.

No full experiment has been rerun with this protocol because the processed
datasets and trained checkpoints are not included. New values must be labeled
`refactored_protocol` and must not replace the paper values.

