"""Normal, boundary, malformed and missing-input regressions for local recovery."""

import copy
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import build_character_library as builder
import validate_character_library as validator
from library_contract import read_json, verify_inputs

PKG = Path(__file__).resolve().parents[2]
REPO = PKG.parent.parent


class LibraryContracts(unittest.TestCase):
    def test_bad_channel_shape_and_negative_tolerance_fail(self):
        for array, tolerance in [(np.zeros((3, 3)), 22), (np.zeros((3, 3, 3)), -1)]:
            with self.assertRaises(ValueError):
                builder.remove_bg_border_flood(array, tolerance)

    def test_border_connected_background_preserves_enclosed_pale_pixels(self):
        arr = np.full((7, 7, 3), 230, dtype=np.uint8)
        arr[1:6, 1:6] = 10
        arr[2:5, 2:5] = 230
        rgba, fg = builder.remove_bg_border_flood(arr)
        self.assertEqual(int(fg.sum()), 25)
        self.assertEqual(rgba[3, 3, 3], 255)
        self.assertEqual(rgba[0, 0].tolist(), [0, 0, 0, 0])

    def test_partial_source_alpha_is_preserved(self):
        arr = np.full((3, 3, 4), 255, dtype=np.uint8)
        arr[1, 1] = [20, 30, 40, 127]
        rgba, _ = builder.remove_bg_border_flood(arr)
        self.assertEqual(rgba[1, 1].tolist(), [20, 30, 40, 127])

    def test_missing_repo_fails(self):
        with self.assertRaises(FileNotFoundError):
            verify_inputs(
                Path("/definitely-missing-tahmures"),
                read_json(PKG / "character-library-manifest.json"),
            )

    def test_tampered_source_hash_fails(self):
        manifest = copy.deepcopy(read_json(PKG / "character-library-manifest.json"))
        manifest["characters"][0]["sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "hash mismatch"):
            verify_inputs(REPO, manifest)

    def test_missing_component_output_is_not_skipped(self):
        original = validator.read_json

        def missing(path):
            if Path(path).name == "component-map.json":
                raise FileNotFoundError("missing output")
            return original(path)

        with (
            patch.object(validator, "read_json", side_effect=missing),
            self.assertRaises(FileNotFoundError),
        ):
            validator.validate(REPO)

    def test_malformed_component_map_fails(self):
        original = validator.read_json

        def malformed(path):
            if Path(path).name == "component-map.json":
                return {}
            return original(path)

        with (
            patch.object(validator, "read_json", side_effect=malformed),
            self.assertRaises(KeyError),
        ):
            validator.validate(REPO)


if __name__ == "__main__":
    unittest.main()
