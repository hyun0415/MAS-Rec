# Shared split files

Generate one split file with `src.data.make_split_indices` and reuse it for
MAS-Rec and every baseline. A split file is tied to a dataset fingerprint so a
file created for one processed dataset is not silently reused for another.

The full research split is not included because the processed interaction data
is not distributed in this repository.

