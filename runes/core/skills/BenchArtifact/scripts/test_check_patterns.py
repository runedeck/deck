import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("check_patterns.py")
SPEC = importlib.util.spec_from_file_location("check_patterns", SCRIPT)
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)


class PatternCheckerTests(unittest.TestCase):
    def config(self, data):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", encoding="utf-8", delete=False
        ) as temporary:
            json.dump(data, temporary)
        self.addCleanup(Path(temporary.name).unlink, missing_ok=True)
        return Path(temporary.name)

    def test_counts_plain_and_regex_patterns(self):
        path = self.config({"rules": [
            {"id": "em_dash", "patterns": ["—"]},
            {"id": "hedge", "patterns": [r"may\s+possibly"], "regex": True},
        ]})
        config, config_path, digest = CHECKER.load_config(path)

        result = CHECKER.check(
            "This — line may possibly break.", config, config_path, digest
        )

        self.assertEqual(result["violations"], {"em_dash": 1, "hedge": 1})
        self.assertEqual(result["total"], 2)
        self.assertFalse(result["density_reliable"])

    def test_masks_code_and_matches_whole_words(self):
        path = self.config({"rules": [{"id": "jargon", "patterns": ["gate"]}]})
        config, config_path, digest = CHECKER.load_config(path)

        result = CHECKER.check(
            "The gate opens. The delegate waits. Run `gate --help` now.",
            config, config_path, digest,
        )

        self.assertEqual(result["violations"], {"jargon": 1})

    def test_rejects_config_without_rules(self):
        path = self.config({"rules": []})
        with self.assertRaises(ValueError):
            CHECKER.load_config(path)


if __name__ == "__main__":
    unittest.main()
