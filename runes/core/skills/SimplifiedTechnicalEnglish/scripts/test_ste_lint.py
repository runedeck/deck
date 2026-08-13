import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("ste-lint.py")
SPEC = importlib.util.spec_from_file_location("ste_lint", SCRIPT)
STE_LINT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(STE_LINT)


class ConfigTests(unittest.TestCase):
    def setUp(self):
        self.config, self.path, self.digest = STE_LINT.load_config()

    def write_config(self, data):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", encoding="utf-8", delete=False
        ) as temporary:
            json.dump(data, temporary)
        self.addCleanup(Path(temporary.name).unlink, missing_ok=True)
        return temporary.name

    def test_default_config_preserves_policy_checks(self):
        result = STE_LINT.lint("Use a seamless system prior to launch.")

        self.assertEqual(result["violations"]["marketing_adjective"], 1)
        self.assertEqual(result["violations"]["banned_word"], 1)
        self.assertEqual(result["config_path"], self.path)
        self.assertEqual(result["config_sha256"], self.digest)

    def test_complete_custom_config_replaces_defaults(self):
        custom = {key: [] for key in STE_LINT.CONFIG_KEYS}
        custom["marketing"] = ["frictionless", "FRICTIONLESS"]
        path = self.write_config(custom)
        config, config_path, digest = STE_LINT.load_config(path)

        result = STE_LINT.lint(
            "A seamless system is frictionless.",
            config=config,
            config_path=config_path,
            config_digest=digest,
        )

        self.assertEqual(config["marketing"], ["frictionless"])
        self.assertEqual(result["violations"]["marketing_adjective"], 1)
        self.assertEqual(result["sample_marketing"], ["frictionless"])
        self.assertNotEqual(result["config_sha256"], self.digest)

    def test_strict_mode_uses_configured_strict_words(self):
        custom = {key: [] for key in STE_LINT.CONFIG_KEYS}
        custom["strictBannedWords"] = ["customword"]
        path = self.write_config(custom)
        config, config_path, digest = STE_LINT.load_config(path)

        result = STE_LINT.lint(
            "Use customword now.",
            strict=True,
            config=config,
            config_path=config_path,
            config_digest=digest,
        )

        self.assertEqual(result["violations"]["strict_banned_word"], 1)

    def test_config_rejects_unknown_and_missing_keys(self):
        with self.subTest("unknown"):
            custom = {key: [] for key in STE_LINT.CONFIG_KEYS}
            custom["unknown"] = []
            with self.assertRaisesRegex(ValueError, "unknown keys: unknown"):
                STE_LINT.load_config(self.write_config(custom))
        with self.subTest("missing"):
            custom = {key: [] for key in STE_LINT.CONFIG_KEYS if key != "marketing"}
            with self.assertRaisesRegex(ValueError, "missing keys: marketing"):
                STE_LINT.load_config(self.write_config(custom))

    def test_config_rejects_invalid_json_and_values(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", encoding="utf-8", delete=False
        ) as invalid:
            invalid.write("{")
        self.addCleanup(Path(invalid.name).unlink, missing_ok=True)
        with self.assertRaisesRegex(ValueError, "invalid JSON"):
            STE_LINT.load_config(invalid.name)

        custom = {key: [] for key in STE_LINT.CONFIG_KEYS}
        custom["marketing"] = [""]
        with self.assertRaisesRegex(ValueError, "non-empty strings"):
            STE_LINT.load_config(self.write_config(custom))

    def test_missing_config_exits_without_traceback(self):
        process = subprocess.run(
            [sys.executable, str(SCRIPT), "--config", "/does/not/exist"],
            input="Use this text.",
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertNotEqual(process.returncode, 0)
        self.assertIn("cannot read config", process.stderr)
        self.assertNotIn("Traceback", process.stderr)

    def test_json_output_carries_config_identity(self):
        process = subprocess.run(
            [sys.executable, str(SCRIPT)],
            input="Use this text.",
            text=True,
            capture_output=True,
            check=True,
        )
        result = json.loads(process.stdout)

        self.assertEqual(result["config_path"], self.path)
        self.assertEqual(result["config_sha256"], self.digest)

    def test_fail_over_uses_configured_score(self):
        custom = {key: [] for key in STE_LINT.CONFIG_KEYS}
        custom["marketing"] = ["customword"]
        path = self.write_config(custom)
        process = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--config",
                path,
                "--fail-over",
                "0",
            ],
            input="Use customword.",
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(process.returncode, 1)


if __name__ == "__main__":
    unittest.main()
