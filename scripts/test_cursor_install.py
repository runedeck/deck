"""Test release installation with local assets and an isolated binary directory."""

import hashlib
import os
import shlex
import shutil
import subprocess
import tarfile
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = (ROOT / ".cursor/install.sh").read_text(encoding="utf-8")
FETCH_START = SCRIPT.index("fetch() {")
FETCH = SCRIPT[FETCH_START : SCRIPT.index("\n}\n", FETCH_START) + 3]


class CursorInstallTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.bin = self.root / "bin"
        self.bin.mkdir()
        self.asset = self.root / "release-binary"
        self.asset.write_bytes(b"verified release\n")

    def fetch(self, asset=None, digest=None, name="example"):
        asset = asset or self.asset
        digest = digest or hashlib.sha256(asset.read_bytes()).hexdigest()
        checksum = shutil.which("gsha256sum") or shutil.which("sha256sum")
        self.assertIsNotNone(checksum, "The test needs GNU sha256sum.")
        # These stubs keep all writes inside the test directory.
        source = (
            "set -euo pipefail\n"
            'BIN="$TEST_ROOT/bin"\n'
            'export PATH="$BIN:$PATH"\n'
            'log() { printf "%s\\n" "$*"; }\n'
            'sudo() { "$@"; }\n'
            'mktemp() { command mktemp -d "$TEST_ROOT/scratch.XXXXXX"; }\n'
            f'sha256sum() {{ {shlex.quote(checksum)} "$@"; }}\n'
            + FETCH
            + '\nfetch "$1" "$2" "$3"\n'
        )
        return subprocess.run(
            ["bash", "-s", "--", asset.as_uri(), digest, name],
            input=source,
            text=True,
            capture_output=True,
            env={**os.environ, "TEST_ROOT": str(self.root)},
            check=False,
        )

    def test_installs_verified_binary(self):
        result = self.fetch()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.bin / "example").read_bytes(), self.asset.read_bytes())
        self.assertTrue(os.access(self.bin / "example", os.X_OK))

    def test_replaces_existing_binary_without_executing_it(self):
        existing = self.bin / "example"
        existing.write_text(
            '#!/bin/sh\nprintf invoked > "$TEST_ROOT/existing-invoked"\nexit 99\n',
            encoding="utf-8",
        )
        existing.chmod(0o755)
        result = self.fetch()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(existing.read_bytes(), self.asset.read_bytes())
        self.assertIn("installing example", result.stdout)
        self.assertFalse((self.root / "existing-invoked").exists())

    def test_rejects_bad_digest_before_replacing_existing_binary(self):
        existing = self.bin / "example"
        existing.write_bytes(b"existing release\n")
        existing.chmod(0o755)
        result = self.fetch(digest="0" * 64)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(existing.read_bytes(), b"existing release\n")

    def test_rejects_bad_digest_before_new_install(self):
        result = self.fetch(digest="0" * 64)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.bin / "example").exists())

    def test_installs_mdschema_from_verified_archive(self):
        archive = self.root / "mdschema.tar.gz"
        with tarfile.open(archive, "w:gz") as stream:
            stream.add(self.asset, arcname="mdschema")
        result = self.fetch(asset=archive, name="mdschema")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.bin / "mdschema").read_bytes(), self.asset.read_bytes())

    def test_installer_prefers_its_verified_binary_directory(self):
        path_line = next(
            line for line in SCRIPT.splitlines() if line.startswith("export PATH=")
        )
        self.assertTrue(path_line.startswith('export PATH="$BIN:'))

    def test_mdschema_release_has_a_fixed_url_and_digest(self):
        calls = [
            shlex.split(line)
            for line in SCRIPT.replace("\\\n", " ").splitlines()
            if line.startswith("fetch ")
        ]
        mdschema = [call for call in calls if call[-1] == "mdschema"]
        self.assertEqual(
            mdschema,
            [
                [
                    "fetch",
                    (
                        "https://github.com/jackchuka/mdschema/releases/download/"
                        "v0.15.3/mdschema_0.15.3_linux_amd64.tar.gz"
                    ),
                    "ab6ada2b546cd177c9c067a2199b528a8e119c5492a87692acf6e8b4e1ca15a7",
                    "mdschema",
                ]
            ],
        )


if __name__ == "__main__":
    unittest.main()
