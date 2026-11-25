#!/usr/bin/env python3
"""Tahmures 2D/3D character workflow utility scoring. Standard library only."""

import argparse
import json
import math
from pathlib import Path

DEFAULT_CONFIG = Path(__file__).resolve().parents[1] / "config" / "utility_weights.json"


def load_config(path=DEFAULT_CONFIG):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def evaluate(stage, scores, gates=None, config=None):
    config = config or load_config()
    if stage not in config["profiles"]:
        raise ValueError("stage must be one of: " + ", ".join(config["profiles"]))

    profile = config["profiles"][stage]
    weights = profile["weights"]
    required = profile["required_gates"]
    gates = gates or {}

    missing_scores = sorted(set(weights) - set(scores))
    extra_scores = sorted(set(scores) - set(weights))
    if missing_scores:
        raise ValueError(f"Missing score fields: {missing_scores}")
    if extra_scores:
        raise ValueError(f"Unknown score fields: {extra_scores}")

    normalized = {}
    for key, raw in scores.items():
        value = float(raw)
        if not math.isfinite(value) or value < 0 or value > 5:
            raise ValueError(f"{key} must be a finite number from 0 to 5")
        normalized[key] = value

    total_weight = sum(weights.values())
    if total_weight != 100:
        raise ValueError(f"Profile weights must total 100; got {total_weight}")

    score = round(sum(weights[k] * normalized[k] / 5 for k in weights), 1)
    failed = [g for g in required if gates.get(g) is False]
    unverified = [g for g in required if gates.get(g) is not True
                  and gates.get(g) is not False]

    if failed:
        status = "excluded"
        score_for_decision = 0.0
    elif unverified:
        status = "provisional"
        score_for_decision = score
    else:
        status = "eligible"
        score_for_decision = score

    return {
        "stage": stage,
        "score": score,
        "decision_score": score_for_decision,
        "status": status,
        "failed_gates": failed,
        "unverified_gates": unverified,
        "criterion_scores": normalized,
        "weights": weights,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Evaluate a Tahmures 2D or 3D character-design workflow."
    )
    parser.add_argument("--stage", choices=["2d", "3d"], required=True)
    parser.add_argument("--scores", required=True,
                        help="Path to JSON file containing criterion scores.")
    parser.add_argument("--gates", default=None,
                        help="Optional JSON file containing true/false gate values.")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    args = parser.parse_args()

    with open(args.scores, "r", encoding="utf-8") as f:
        scores = json.load(f)
    gates = {}
    if args.gates:
        with open(args.gates, "r", encoding="utf-8") as f:
            gates = json.load(f)

    result = evaluate(args.stage, scores, gates, load_config(args.config))
    print(json.dumps(result, indent=2))
    return 0 if result["status"] != "excluded" else 2


if __name__ == "__main__":
    raise SystemExit(main())
