"""Adversarial tests of the supervisor gate; synthetic images live in /tmp."""

import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from PIL import Image

spec = importlib.util.spec_from_file_location(
    "layout01_validator", Path(__file__).with_name("validate_submission.py")
)
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class StructuralGateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="layout01-gate-test-")
        self.addCleanup(self.tmp.cleanup)
        self.canvas = patch.object(validator, "CANVAS", (8, 8))
        self.canvas.start()
        self.addCleanup(self.canvas.stop)
        self.base = Path(self.tmp.name) / "baseline"
        self.root = Path(self.tmp.name) / "candidate"
        for folder in ("source", "masks", "previews", "face"):
            (self.base / folder).mkdir(parents=True)
        for folder in ("parts", "masks", "provenance", "previews"):
            (self.root / folder).mkdir(parents=True)
        Image.new("RGBA", (8, 8), (90, 80, 70, 255)).save(
            self.base / "source/approved_master.png"
        )
        Image.new("L", (8, 8), 255).save(self.base / "masks/visible_head_domain.png")
        Image.new("L", (8, 8), 255).save(self.root / "masks/domain.png")
        for n in validator.PREVIEW_FILES:
            Image.new("RGBA", (8, 8), (1, 2, 3, 255)).save(self.base / n)
        baseline_sprites = []
        records = []
        for sid in sorted(validator.REQUIRED_IDS):
            im = Image.new("RGBA", (8, 8))
            if sid == "head_base":
                im = Image.new("RGBA", (8, 8), (91, 80, 70, 255))
            elif sid.startswith("lower_face"):
                im.putpixel(
                    (4, 6), (20 if sid.endswith("neutral") else 40, 10, 10, 255)
                )
            else:
                im.putpixel((1, 1), (90, 80, 70, 255))
            im.save(self.root / ("parts/" + sid + ".png"))
            record = {
                "id": sid,
                "role": "rig_component",
                "path": "parts/" + sid + ".png",
                "mask_path": "masks/" + sid + ".png",
                "pivot": {"x": 4, "y": 4},
                "parent": None,
                "provenance": {
                    "source_pixel_mask": "provenance/" + sid + "-src.png",
                    "reconstructed_pixel_mask": "provenance/" + sid + "-new.png",
                    "reconstruction_method": "synthetic test surface",
                },
            }
            records.append(record)
            baseline_sprites.append({"id": sid, "pivot": {"x": 4, "y": 4}})
        (self.base / "manifest.json").write_text(
            json.dumps({"sprites": baseline_sprites})
        )
        order = [
            "head_base",
            "hair_back",
            "ear_left",
            "ear_right",
            "beard",
            "nose",
            "eye_left",
            "eye_right",
            "eyebrow_left",
            "eyebrow_right",
            "moustache",
            "diadem_gold",
        ]

        def with_patch(sid):
            out = order.copy()
            out.insert(out.index("moustache"), sid)
            return out

        self.manifest = {
            "source_image_sha256": sha(self.base / "source/approved_master.png"),
            "source_master_repo_path": (
                "Characters/tahmures/versions/layout01-v2/source/approved_master.png"
            ),
            "canvas": [8, 8],
            "mouth_anchor": {"x": 540, "y": 241},
            "mouth_architecture": "B_LOCAL_LOWER_FACE_PATCH",
            "status": "CANDIDATE",
            "human_approved": False,
            "sprites": records,
            "coverage_domain_path": "masks/domain.png",
            "render_groups": {
                "puppet_core": {"type": "rig_composition", "layer_order": order},
                "puppet_core_neutral": {
                    "type": "rig_composition",
                    "layer_order": with_patch("lower_face_neutral"),
                },
                "puppet_core_open_test": {
                    "type": "rig_composition",
                    "layer_order": with_patch("lower_face_open_test"),
                },
            },
            "previews": {
                "mouthless": "previews/mouthless.png",
                "neutral": "previews/neutral.png",
                "open_test": "previews/open.png",
            },
        }
        self.refresh()

    def refresh(self):
        images = {}
        for record in self.manifest["sprites"]:
            im = Image.open(self.root / record["path"]).convert("RGBA")
            im.getchannel("A").save(self.root / record["mask_path"])
            support = im.getchannel("A").point(lambda a: 255 if a else 0)
            support.save(self.root / record["provenance"]["reconstructed_pixel_mask"])
            Image.new("L", (8, 8)).save(
                self.root / record["provenance"]["source_pixel_mask"]
            )
            record.update(
                {
                    "sha256": sha(self.root / record["path"]),
                    "mask_sha256": sha(self.root / record["mask_path"]),
                    "alpha_bounding_rect": list(im.getchannel("A").getbbox()),
                }
            )
            images[record["id"]] = im
        for group, key in [
            ("puppet_core", "mouthless"),
            ("puppet_core_neutral", "neutral"),
            ("puppet_core_open_test", "open_test"),
        ]:
            out = Image.new("RGBA", (8, 8))
            for sid in self.manifest["render_groups"][group]["layer_order"]:
                out.alpha_composite(images[sid])
            out.save(self.root / self.manifest["previews"][key])
        (self.root / "manifest.json").write_text(json.dumps(self.manifest))
        self.index_files()

    def index_files(self):
        index = {
            str(p.relative_to(self.root)): sha(p)
            for p in self.root.rglob("*")
            if p.is_file() and p.name != "files-sha256.json"
        }
        (self.root / "files-sha256.json").write_text(json.dumps(index))

    def result(self):
        return validator.validate(self.root, self.base)

    def assert_fails(self, check_name):
        result = self.result()
        self.assertFalse(result["pass"])
        self.assertTrue(
            any(c["check"] == check_name and not c["pass"] for c in result["checks"])
        )

    def test_structural_pass_does_not_grant_art_approval(self):
        result = self.result()
        self.assertTrue(result["pass"], result)
        self.assertFalse(result["artistic_approval"])

    def test_renamed_source_underlay_is_rejected(self):
        Image.open(self.base / validator.PREVIEW_FILES[0]).save(
            self.root / "parts/head_base.png"
        )
        self.refresh()
        self.assert_fails("head_base:not_preview_underlay")

    def test_master_image_cannot_be_rig_backing(self):
        Image.open(self.base / "source/approved_master.png").save(
            self.root / "parts/head_base.png"
        )
        self.refresh()
        self.assert_fails("head_base:not_preview_underlay")

    def test_reconstruction_cannot_be_claimed_as_original_pixels(self):
        record = next(r for r in self.manifest["sprites"] if r["id"] == "head_base")
        src = Image.open(self.root / record["provenance"]["source_pixel_mask"])
        rebuilt = Image.open(
            self.root / record["provenance"]["reconstructed_pixel_mask"]
        )
        src.putpixel((2, 2), 255)
        rebuilt.putpixel((2, 2), 0)
        src.save(self.root / record["provenance"]["source_pixel_mask"])
        rebuilt.save(self.root / record["provenance"]["reconstructed_pixel_mask"])
        self.index_files()
        self.assert_fails("head_base:source_pixel_claim")

    def test_binary_support_is_not_exact_alpha(self):
        im = Image.open(self.root / "parts/head_base.png")
        im.putpixel((5, 5), (90, 80, 70, 253))
        im.save(self.root / "parts/head_base.png")
        self.refresh()
        Image.new("L", (8, 8), 255).save(self.root / "masks/head_base.png")
        record = next(r for r in self.manifest["sprites"] if r["id"] == "head_base")
        record["mask_sha256"] = sha(self.root / "masks/head_base.png")
        (self.root / "manifest.json").write_text(json.dumps(self.manifest))
        self.index_files()
        self.assert_fails("head_base:mask_exact_alpha")

    def test_shrinking_domain_cannot_hide_gaps(self):
        Image.new("L", (8, 8)).save(self.root / "masks/domain.png")
        self.index_files()
        self.assert_fails("domain_not_shrunk")

    def test_real_interior_gap_fails(self):
        im = Image.open(self.root / "parts/head_base.png")
        im.putpixel((5, 5), (0, 0, 0, 0))
        im.save(self.root / "parts/head_base.png")
        self.refresh()
        self.assert_fails("puppet_core:interior_coverage")

    def test_intrinsic_source_antialiasing_is_allowed(self):
        source = self.base / "source/approved_master.png"
        im = Image.open(source)
        im.putpixel((5, 5), (90, 80, 70, 10))
        im.save(source)
        head = Image.open(self.root / "parts/head_base.png")
        head.putpixel((5, 5), (91, 80, 70, 10))
        head.save(self.root / "parts/head_base.png")
        self.manifest["source_image_sha256"] = sha(source)
        self.refresh()
        result = self.result()
        self.assertTrue(result["pass"], result)

    def test_two_mouth_patches_are_rejected(self):
        order = self.manifest["render_groups"]["puppet_core_neutral"]["layer_order"]
        order.insert(order.index("moustache"), "lower_face_open_test")
        self.refresh()
        self.assert_fails("puppet_core_neutral:single_patch")

    def test_machine_human_promotion_is_rejected(self):
        self.manifest["human_approved"] = True
        self.refresh()
        self.assert_fails("unapproved_candidate")

    def test_parent_cycle_is_rejected(self):
        for r in self.manifest["sprites"]:
            if r["id"] == "head_base":
                r["parent"] = "head_base"
        self.refresh()
        self.assert_fails("parents_resolve_without_cycles")

    def test_path_escape_is_rejected(self):
        with self.assertRaises(ValueError):
            validator.local_path(self.root, "../baseline/source/approved_master.png")


if __name__ == "__main__":
    unittest.main()
