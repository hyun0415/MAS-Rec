"""Leakage-aware data preparation shared by MAS-Rec and its baselines."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd


UNKNOWN_ID = 0


@dataclass(frozen=True)
class SplitIndices:
    """Row positions used by every model in one experiment."""

    seed: int
    train: list[int]
    validation: list[int]
    test: list[int]
    source_fingerprint: str


def dataframe_fingerprint(frame: pd.DataFrame, columns: Iterable[str]) -> str:
    """Return a stable fingerprint without storing private row contents."""

    selected = frame.loc[:, list(columns)].astype(str)
    hashed_rows = pd.util.hash_pandas_object(selected, index=False).to_numpy()
    return hashlib.sha256(hashed_rows.tobytes()).hexdigest()


def make_split_indices(
    frame: pd.DataFrame,
    *,
    seed: int = 42,
    train_ratio: float = 0.70,
    validation_ratio: float = 0.10,
    test_ratio: float = 0.20,
    fingerprint_columns: tuple[str, ...] = ("user_id", "item_id", "rating"),
) -> SplitIndices:
    """Create one deterministic random split for all compared models."""

    ratios = np.array([train_ratio, validation_ratio, test_ratio], dtype=float)
    if not np.isclose(ratios.sum(), 1.0):
        raise ValueError("train, validation, and test ratios must sum to 1")
    if len(frame) < 3:
        raise ValueError("at least three interactions are required")

    rng = np.random.default_rng(seed)
    shuffled = rng.permutation(len(frame))
    train_end = int(len(frame) * train_ratio)
    validation_end = train_end + int(len(frame) * validation_ratio)
    if train_end == 0 or validation_end == train_end or validation_end == len(frame):
        raise ValueError("the dataset is too small for the requested split")

    return SplitIndices(
        seed=seed,
        train=shuffled[:train_end].tolist(),
        validation=shuffled[train_end:validation_end].tolist(),
        test=shuffled[validation_end:].tolist(),
        source_fingerprint=dataframe_fingerprint(frame, fingerprint_columns),
    )


def save_split_indices(split: SplitIndices, path: str | Path) -> None:
    """Save the shared split as a small JSON file."""

    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(asdict(split), indent=2, sort_keys=True), encoding="utf-8"
    )


def load_split_indices(path: str | Path) -> SplitIndices:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    return SplitIndices(**payload)


def select_split(frame: pd.DataFrame, split: SplitIndices, name: str) -> pd.DataFrame:
    """Select a split by row position and return an independent copy."""

    if name not in {"train", "validation", "test"}:
        raise ValueError("name must be train, validation, or test")
    return frame.iloc[getattr(split, name)].copy().reset_index(drop=True)


def fit_id_mapping(values: pd.Series) -> dict[str, int]:
    """Build a deterministic ID map; zero is reserved for unknown IDs."""

    unique_values = sorted(values.dropna().astype(str).unique())
    return {value: position + 1 for position, value in enumerate(unique_values)}


def apply_id_mapping(values: pd.Series, mapping: dict[str, int]) -> np.ndarray:
    """Encode IDs with an existing mapping and map unseen values to zero."""

    return values.astype(str).map(mapping).fillna(UNKNOWN_ID).astype("int64").to_numpy()

