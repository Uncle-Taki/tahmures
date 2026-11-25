import importlib.util
import json
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "tahmures_character_utility.py"
spec = importlib.util.spec_from_file_location("tahmures_character_utility", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class UtilityTests(unittest.TestCase):
    def test_2d_perfect_score_is_provisional_without_gates(self):
        config = module.load_config()
        scores = {k: 5 for k in config["profiles"]["2d"]["weights"]}
        result = module.evaluate("2d", scores, {})
        self.assertEqual(result["score"], 100.0)
        self.assertEqual(result["status"], "provisional")

    def test_3d_failed_gate_excludes(self):
        config = module.load_config()
        scores = {k: 5 for k in config["profiles"]["3d"]["weights"]}
        gates = {k: True for k in config["profiles"]["3d"]["required_gates"]}
        gates["visual_identity_preserved"] = False
        result = module.evaluate("3d", scores, gates)
        self.assertEqual(result["status"], "excluded")
        self.assertEqual(result["decision_score"], 0.0)

    def test_2d_all_gates_true_is_eligible(self):
        config = module.load_config()
        scores = {k: 4 for k in config["profiles"]["2d"]["weights"]}
        gates = {k: True for k in config["profiles"]["2d"]["required_gates"]}
        result = module.evaluate("2d", scores, gates)
        self.assertEqual(result["status"], "eligible")
        self.assertEqual(result["score"], 80.0)

    def test_rejects_out_of_range_score(self):
        config = module.load_config()
        scores = {k: 3 for k in config["profiles"]["2d"]["weights"]}
        scores["approved_reference_fidelity"] = 6
        with self.assertRaises(ValueError):
            module.evaluate("2d", scores, {})


if __name__ == "__main__":
    unittest.main()
