import json

from tahmures.cli import main
from tahmures.manifest import load_manifest
from tahmures.runner import fixture_runner


def test_runner_builds_variant_summaries() -> None:
    path = "experiments/manifests/ch01-prompt-roles.json"
    report = fixture_runner(load_manifest(path), path).run()
    assert report.experiment_id == "ch01-prompt-roles"
    assert set(report.variant_summaries) == {"baseline", "explicit"}
    assert report.variant_summaries["explicit"]["accuracy"] == 1.0


def test_cli_writes_report(tmp_path) -> None:
    output = tmp_path / "report.json"
    exit_code = main(
        [
            "run",
            "--manifest",
            "experiments/manifests/ch01-prompt-roles.json",
            "--output",
            str(output),
        ]
    )
    assert exit_code == 0
    report = json.loads(output.read_text(encoding="utf-8"))
    assert report["schema_version"] == 1


def test_cli_reports_bad_manifest(capsys) -> None:
    assert main(["run", "--manifest", "missing.json"]) == 2
    assert "error:" in capsys.readouterr().out
