"""Reject inherited Git repository state before the bookmark gate writes."""

import importlib.util
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "bookmark_gate", ROOT / ".githooks" / "jj-push-bookmark.py"
)
GATE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GATE)
DISCOVERY = ("git", "rev-parse", "--local-env-vars")


class GitEnvironmentTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="jj-push-env-")
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)
        self.names = GATE.run(*DISCOVERY).splitlines()
        self.environment = {
            name: value for name, value in os.environ.items() if name not in self.names
        }

    def assert_rejected(self, variables):
        calls = []
        original_run = GATE.run

        def read_only(*arguments, **keywords):
            calls.append(arguments)
            self.assertEqual(arguments, DISCOVERY, "The gate reached a stateful command")
            return original_run(*arguments, **keywords)

        environment = {**self.environment, **variables}
        with (
            mock.patch.dict(os.environ, environment, clear=True),
            mock.patch.object(GATE, "run", side_effect=read_only),
            self.assertRaises(ValueError) as raised,
        ):
            GATE.main(["--bookmark", "codex/fixture"])
        self.assertEqual(calls, [DISCOVERY])
        self.assertEqual(
            str(raised.exception),
            "Unset repository-local Git variables before pushing: "
            + ", ".join(sorted(variables)),
        )
        self.assertEqual(list(self.directory.iterdir()), [])

    def test_all_git_repository_variables_stop_before_stateful_commands(self):
        self.assertTrue({"GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"} <= set(self.names))
        for name in self.names:
            for value in ("", str(self.directory / "private-fixture-value")):
                with self.subTest(name=name, empty=value == ""):
                    self.assert_rejected({name: value})

    def test_combined_repository_redirection_reports_only_names(self):
        self.assert_rejected(
            {
                "GIT_DIR": str(self.directory / "outside.git"),
                "GIT_WORK_TREE": str(self.directory / "outside-worktree"),
                "GIT_INDEX_FILE": str(self.directory / "outside-index"),
                "GIT_COMMON_DIR": str(self.directory / "outside-common"),
            }
        )

    def test_malformed_runtime_configuration_stops_before_parsing(self):
        self.assert_rejected(
            {"GIT_CONFIG_PARAMETERS": "malformed fixture", "GIT_CONFIG_COUNT": "invalid"}
        )

    def test_cli_preserves_external_repository_and_index(self):
        outside = self.directory / "outside"
        environment = {
            **self.environment,
            "GIT_CONFIG_GLOBAL": os.devnull,
            "GIT_CONFIG_SYSTEM": os.devnull,
            "GIT_CONFIG_NOSYSTEM": "1",
        }
        subprocess.run(
            ["git", "init", "--quiet", str(outside)],
            env=environment,
            check=True,
            capture_output=True,
        )
        (outside / "payload.txt").write_text("Preserve the outside fixture.\n")
        subprocess.run(
            ["git", "add", "payload.txt"],
            cwd=outside,
            env=environment,
            check=True,
            capture_output=True,
        )

        def contents():
            return {
                str(path.relative_to(outside)): path.read_bytes()
                for path in outside.rglob("*")
                if path.is_file()
            }

        before = contents()
        variables = {
            "GIT_DIR": str(outside / ".git"),
            "GIT_WORK_TREE": str(outside),
            "GIT_INDEX_FILE": str(outside / ".git" / "index"),
        }
        for selected in [*({name: value} for name, value in variables.items()), variables]:
            with self.subTest(variables=sorted(selected)):
                result = subprocess.run(
                    [
                        sys.executable,
                        str(ROOT / ".githooks" / "jj-push-bookmark.py"),
                        "--bookmark",
                        "codex/fixture",
                    ],
                    cwd=outside,
                    env={**environment, **selected},
                    text=True,
                    capture_output=True,
                    timeout=15,
                    check=False,
                )
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertEqual(
                    result.stderr.strip(),
                    "jj push: Unset repository-local Git variables before pushing: "
                    + ", ".join(sorted(selected)),
                )
                self.assertEqual(contents(), before)

    def test_future_git_repository_variable_is_rejected(self):
        with (
            mock.patch.object(GATE, "run", return_value="GIT_FUTURE_REPOSITORY_STATE"),
            mock.patch.dict(os.environ, {"GIT_FUTURE_REPOSITORY_STATE": "fixture"}),
            self.assertRaisesRegex(ValueError, "GIT_FUTURE_REPOSITORY_STATE"),
        ):
            GATE.main(["--bookmark", "codex/fixture"])

    def test_discovery_failure_stops_before_stateful_commands(self):
        error = subprocess.CalledProcessError(1, DISCOVERY)
        with (
            mock.patch.object(GATE, "run", side_effect=error) as run,
            self.assertRaises(subprocess.CalledProcessError),
        ):
            GATE.main(["--bookmark", "codex/fixture"])
        run.assert_called_once_with(*DISCOVERY)

    def test_authentication_and_signing_environment_is_preserved(self):
        preserved = {
            "GIT_SSH_COMMAND": "fixture-ssh",
            "GIT_ASKPASS": "/fixture/askpass",
            "GIT_CONFIG_GLOBAL": "/fixture/global",
            "GIT_CONFIG_SYSTEM": "/fixture/system",
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_TERMINAL_PROMPT": "0",
            "JJ_CONFIG": "/fixture/jj.toml",
            "GPG_TTY": "/fixture/tty",
        }
        environment = {**self.environment, **preserved}
        original_run = GATE.run

        def stop_at_ref_check(*arguments, **keywords):
            if arguments == DISCOVERY:
                return original_run(*arguments, **keywords)
            self.assertEqual(arguments[0:2], ("git", "check-ref-format"))
            self.assertEqual(dict(os.environ), environment)
            raise StopIteration

        with mock.patch.dict(os.environ, environment, clear=True):
            with (
                mock.patch.object(GATE, "run", side_effect=stop_at_ref_check),
                self.assertRaises(StopIteration),
            ):
                GATE.main(["--bookmark", "codex/fixture"])
            output = GATE.run(
                sys.executable,
                "-c",
                "import os; print(os.environ['GIT_SSH_COMMAND'], os.environ['GPG_TTY'])",
            )
            self.assertEqual(output, "fixture-ssh /fixture/tty")


if __name__ == "__main__":
    unittest.main()
