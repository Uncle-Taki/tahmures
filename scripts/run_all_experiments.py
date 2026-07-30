#!/usr/bin/env python3
"""Run every committed pilot manifest with the fixture client."""

from pathlib import Path

from tahmures.manifest import load_manifest
from tahmures.runner import fixture_runner


def main() -> int:
    manifests = sorted(Path("experiments/manifests").glob("ch*.json"))
    if not manifests:
        raise SystemExit("no completed-chapter manifests found")
    for path in manifests:
        manifest = load_manifest(path)
        report = fixture_runner(manifest, path).run()
        variants = ", ".join(
            f"{name}: pass={metrics['pass_rate']:.3f}"
            for name, metrics in report.variant_summaries.items()
        )
        print(f"{manifest.experiment_id}: {variants}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
