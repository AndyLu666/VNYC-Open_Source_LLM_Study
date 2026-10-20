"""Regression checks for the release inventory and local analysis outputs."""

import contextlib
import csv
import importlib.util
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "verify_artifact.py"
SPEC = importlib.util.spec_from_file_location("verify_artifact", SCRIPT)
verify = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(verify)


class ArtifactVerificationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.manifest = self.root / "MANIFEST.csv"
        for name, value in {
            "ROOT": self.root,
            "MANIFEST": self.manifest,
            "REQUIRED_FILES": ["data/records.csv"],
            "EXPECTED_ROWS": {"data/records.csv": 2},
        }.items():
            patcher = patch.object(verify, name, value)
            patcher.start()
            self.addCleanup(patcher.stop)
        self.write("data/records.csv", "id,value\n1,a\n2,b\n")
        self.refresh_manifest()

    def write(self, name, contents):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(contents, encoding="utf-8")
        return path

    def refresh_manifest(self):
        with self.manifest.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=["path", "role", "bytes", "sha256"])
            writer.writeheader()
            for path in sorted(self.root.rglob("*")):
                if path.is_file() and verify.should_manifest(path):
                    writer.writerow({
                        "path": path.relative_to(self.root).as_posix(),
                        "role": "test",
                        "bytes": path.stat().st_size,
                        "sha256": verify.sha256_file(path),
                    })

    def run_check(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            result = verify.main()
        return result, output.getvalue()

    def test_clean_release_passes(self):
        self.assertEqual(self.run_check()[0], 0)

    def test_environment_and_generated_outputs_are_ignored(self):
        marker = verify.FORBIDDEN_TEXT[0]
        self.write(".venv/lib/package.py", marker)
        self.write(".git/example.md", marker)
        self.write("paper/tables/generated.tex", marker)
        self.write("paper/.DS_Store", "local")
        self.assertEqual(self.run_check()[0], 0)

    def test_unlisted_release_file_is_reported(self):
        self.write("docs/new.md", "New documentation")
        result, output = self.run_check()
        self.assertEqual(result, 1)
        self.assertIn("file missing from manifest: docs/new.md", output)

    def test_modified_data_is_reported(self):
        self.write("data/records.csv", "id,value\n1,a\n2,c\n")
        result, output = self.run_check()
        self.assertEqual(result, 1)
        self.assertIn("manifest sha256 mismatch", output)

    def test_row_count_remains_checked(self):
        self.write("data/records.csv", "id,value\n1,a\n")
        self.refresh_manifest()
        result, output = self.run_check()
        self.assertEqual(result, 1)
        self.assertIn("row-count mismatch", output)

    def test_release_placeholder_is_reported(self):
        self.write("docs/note.md", verify.FORBIDDEN_TEXT[-1])
        self.refresh_manifest()
        result, output = self.run_check()
        self.assertEqual(result, 1)
        self.assertIn("forbidden text marker", output)

    def test_citation_placeholder_is_reported(self):
        self.write("CITATION.cff", verify.FORBIDDEN_TEXT[-1])
        self.refresh_manifest()
        result, output = self.run_check()
        self.assertEqual(result, 1)
        self.assertIn("found in CITATION.cff", output)


if __name__ == "__main__":
    unittest.main()
