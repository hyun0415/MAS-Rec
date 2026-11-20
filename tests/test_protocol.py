import tempfile
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

from src.data import (
    apply_id_mapping,
    fit_id_mapping,
    load_split_indices,
    make_split_indices,
    save_split_indices,
)
from src.evaluation import rating_metrics


class ProtocolTests(unittest.TestCase):
    def setUp(self):
        self.frame = pd.DataFrame(
            {
                "user_id": [f"u{i % 5}" for i in range(20)],
                "item_id": [f"i{i % 4}" for i in range(20)],
                "rating": [(i % 5) + 1 for i in range(20)],
            }
        )

    def test_split_is_deterministic_and_disjoint(self):
        first = make_split_indices(self.frame, seed=42)
        second = make_split_indices(self.frame, seed=42)
        self.assertEqual(first, second)
        sets = [set(first.train), set(first.validation), set(first.test)]
        self.assertFalse(sets[0] & sets[1])
        self.assertFalse(sets[0] & sets[2])
        self.assertFalse(sets[1] & sets[2])
        self.assertEqual(set.union(*sets), set(range(len(self.frame))))

    def test_split_round_trip(self):
        split = make_split_indices(self.frame)
        with tempfile.TemporaryDirectory(dir=Path.cwd() / "tests") as directory:
            path = Path(directory) / "split.json"
            save_split_indices(split, path)
            self.assertEqual(split, load_split_indices(path))

    def test_unknown_ids_use_reserved_zero(self):
        mapping = fit_id_mapping(pd.Series(["known-a", "known-b"]))
        encoded = apply_id_mapping(pd.Series(["known-a", "new"]), mapping)
        np.testing.assert_array_equal(encoded, np.array([1, 0]))

    def test_metrics(self):
        result = rating_metrics([1, 2, 4], [1, 3, 2])
        self.assertAlmostEqual(result["mae"], 1.0)
        self.assertAlmostEqual(result["mse"], 5 / 3)
        self.assertAlmostEqual(result["rmse"], np.sqrt(5 / 3))
        self.assertAlmostEqual(result["mape"], (0 + 0.5 + 0.5) / 3)


if __name__ == "__main__":
    unittest.main()
