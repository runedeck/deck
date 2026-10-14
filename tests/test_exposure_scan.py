"""Prove the exposure detector against fixtures in a temporary Git repository.

Every fixture value is built at run time from fragments, so no fake secret
sits in this file as a literal and the deck's own secret scan stays quiet.
The fixtures never leave the temporary directory.
"""

import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DETECTOR = ROOT / "routines" / "scripts" / "exposure_scan.py"

FAKE_TOKEN = "ghp_" + "A" * 30 + "123456"
FAKE_TOKEN_TWO = "ghp_" + "B" * 30 + "654321"
FAKE_URL = "postgres://alice:" + "s3cret-" + "pass9" + "@db.fixture.example-corp.net/app"
FAKE_URL_TWO = "postgres://alice:" + "p4ss" + "word!" + "@db.fixture.example-corp.net/"
FAKE_ASSIGNMENT = "password = " + "hunter2" + "x9!q"
FAKE_WORDS = "correct" + "horse" + "battery" + "staple"
FAKE_QUOTED = "tulip" + "violet" + "copper" + "orbit"
FAKE_DOLLAR = "$up3r" + "S3cr3t!"
FAKE_EMAIL = "alice@fixture-mail.example-corp.net"
FAKE_EMAIL_TWO = "bob@fixture-mail.example-corp.net"
FAKE_PHONE = "+420 601 234 567"
FAKE_KEY = "-----BEGIN " + "RSA PRIVATE KEY-----\n" + "QUJD" * 20 + "\n" + "-----END " + "RSA PRIVATE KEY-----\n"
SENSITIVE_DOMAIN = "corp.example"


def load_module():
    spec = importlib.util.spec_from_file_location("exposure_scan", DETECTOR)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class Fixture:
    def __init__(self):
        self.directory = Path(tempfile.mkdtemp(prefix="exposure-"))
        self.repo = self.directory / "repo"
        self.repo.mkdir()
        self.environment = dict(os.environ)
        self.environment.update(
            {
                "GIT_CONFIG_GLOBAL": "/dev/null",
                "GIT_CONFIG_NOSYSTEM": "1",
                "GIT_AUTHOR_NAME": "Fixture",
                "GIT_AUTHOR_EMAIL": "fixture@users.noreply.github.com",
                "GIT_COMMITTER_NAME": "Fixture",
                "GIT_COMMITTER_EMAIL": "fixture@users.noreply.github.com",
            }
        )
        self.git("init", "-q", "-b", "main")
        self.commits = []

    def git(self, *arguments, cwd=None):
        return subprocess.check_output(
            ["git", "-c", "commit.gpgsign=false", *arguments],
            cwd=cwd or self.repo,
            env=self.environment,
            text=True,
        ).strip()

    def write(self, relative, content):
        path = self.repo / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(content, bytes):
            path.write_bytes(content)
        else:
            path.write_text(content, encoding="utf-8")

    def commit(self, message):
        self.git("add", "-A")
        self.git("commit", "-q", "-m", message)
        self.commits.append(self.git("rev-parse", "HEAD"))
        return self.commits[-1]

    def populate(self):
        self.write(
            "config/app.env",
            "API_KEY=" + FAKE_TOKEN + "\n"
            "DB_URL=" + FAKE_URL + "\n"
            "PASSWORD=${PASSWORD}\n"
            "password_file = /etc/app/secret\n"
            "secret_key = settings.SECRET_KEY\n"
            "API_TOKEN = TOKEN_NAME\n"
            "token = os.environ.get(TOKEN)\n"
            "password = " + FAKE_WORDS + "\n"
            'token="' + FAKE_QUOTED + '"\n'
            'password = "' + FAKE_DOLLAR + '"\n'
            + FAKE_ASSIGNMENT
            + "\n"
            + " " * 5000
            + FAKE_TOKEN_TWO
            + "\n"
            + FAKE_URL_TWO
            + " "
            + FAKE_TOKEN
            + "\n",
        )
        self.write(
            "hosts.txt",
            "build.example.internal\n"
            "printer.local\n"
            "settings.local.json\n"
            ".env.local\n"
            "model@claude.noreply.nexus.local\n"
            "robot@claude.noreply." + SENSITIVE_DOMAIN + "\n"
            "vpn." + SENSITIVE_DOMAIN + "\n"
            "mail." + SENSITIVE_DOMAIN + " again mail." + SENSITIVE_DOMAIN.upper() + "\n",
        )
        self.write(
            "contacts.md",
            "Contact " + FAKE_EMAIL + " or user@example.com.\n"
            "Bot: 123456+bot@users.noreply.github.com\n"
            "Phone: " + FAKE_PHONE + "\n"
            "Version +1.2.3 and date 2026-10-02 +0100\n",
        )
        self.write("key.pem", FAKE_KEY)
        self.write("docs/placeholder.md", "-----BEGIN " + "PRIVATE KEY-----\n...\n-----END " + "PRIVATE KEY-----\n")
        self.write("docs/unterminated.txt", "-----BEGIN " + "PRIVATE KEY-----\n" + " " * 50000 + "\nno end here\n")
        self.write("docs/mixed.txt", "-----BEGIN " + "PRIVATE KEY-----\nexample without an end\n" + FAKE_KEY)
        self.write("bin.dat", b"\x00\x01" + FAKE_TOKEN.encode() + b"\x00")
        os.symlink("hosts.txt", self.repo / "link")
        first = self.commit("Add config, contact root@example.com")
        (self.repo / "config" / "app.env").unlink()
        self.write("README.md", "Plain text.\n")
        second = self.commit("Remove the environment file, ask " + FAKE_EMAIL_TWO)
        self.write("backup/hosts.txt", (self.repo / "hosts.txt").read_text(encoding="utf-8"))
        self.write("zshrc", "export GH=" + FAKE_TOKEN + "\n")
        self.write("vpn." + SENSITIVE_DOMAIN + ".conf", "HostName vpn." + SENSITIVE_DOMAIN + "\n")
        third = self.commit("Copy hosts, add the shell file")
        return first, second, third

    def clone(self, name, *options):
        target = self.directory / name
        self.git("clone", "-q", *options, "file://" + str(self.repo), str(target), cwd=self.directory)
        return target

    def shallow_clone(self, name="shallow"):
        return self.clone(name, "--depth", "1")

    def remove(self):
        shutil.rmtree(self.directory, ignore_errors=True)


def run_detector(repo, *arguments, environment=None):
    env = dict(os.environ)
    for name in ("SENSITIVE_DOMAINS", "SENSITIVE_DOMAINS_FILE", "KNOWN_FINDINGS_FILE"):
        env.pop(name, None)
    env.update(environment or {})
    completed = subprocess.run(
        [sys.executable, "-I", str(DETECTOR), "--repo", str(repo), "--ref", "HEAD", *arguments],
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )
    return completed.returncode, json.loads(completed.stdout), completed.stdout


class ExposureScanTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_module()
        cls.fixture = Fixture()
        cls.first, cls.second, cls.third = cls.fixture.populate()
        started = time.monotonic()
        cls.code, cls.report, cls.raw = run_detector(cls.fixture.repo)
        cls.seconds = time.monotonic() - started

    @classmethod
    def tearDownClass(cls):
        cls.fixture.remove()

    def findings(self, rule, report=None):
        return [finding for finding in (report or self.report)["findings"] if finding["rule"] == rule]

    def ids(self, rule, report=None):
        return {finding["id"] for finding in self.findings(rule, report)}

    def expected_id(self, rule_code, value):
        return self.module.finding_id(self.module.RULES_BY_CODE[rule_code], value)

    def acknowledgement(self, commit, report=None, rules=None, expires=None, reason=None):
        """The `.auditignore.yaml` text that acknowledges the findings of a report at one commit."""
        lines = ["acknowledged:"]
        for finding in (report or self.report)["findings"]:
            if rules is not None and finding["rule"] not in rules:
                continue
            lines += [f"  - rule: {finding['rule']}", f"    sha256: {finding['sha256']}", f"    commit: {commit}"]
            if expires:
                lines.append(f"    expires: {expires}")
            if reason:
                lines.append(f"    reason: {reason}")
        return "\n".join(lines) + "\n"

    def known_file(self, name, text):
        path = self.fixture.directory / name
        path.write_text(text, encoding="utf-8")
        return str(path)

    def test_scan_completes_with_alert(self):
        self.assertEqual(self.code, 0)
        self.assertEqual(self.report["status"], "ALERT")
        self.assertEqual(self.report["health"]["status"], "COMPLETE")
        self.assertEqual(self.report["commit"], self.third)
        self.assertEqual(self.report["rules_version"], self.module.RULES_VERSION)
        self.assertLess(self.seconds, 10, "an unterminated key block must not stall the scan")

    def test_values_never_appear_in_output(self):
        for value in (FAKE_TOKEN, FAKE_TOKEN_TWO, FAKE_EMAIL, FAKE_EMAIL_TWO, FAKE_PHONE, "hunter2", "s3cret", "p4ss", "QUJD", FAKE_WORDS, FAKE_QUOTED):
            self.assertNotIn(value, self.raw)

    def test_secret_rules_match_their_fixtures(self):
        self.assertEqual(
            self.ids("secret-api-token"),
            {self.expected_id("secret-api-token", FAKE_TOKEN), self.expected_id("secret-api-token", FAKE_TOKEN_TWO)},
        )
        self.assertEqual(
            self.ids("secret-url-credential"),
            {self.expected_id("secret-url-credential", FAKE_URL), self.expected_id("secret-url-credential", FAKE_URL_TWO)},
        )
        self.assertEqual(
            self.ids("secret-assigned-value"),
            {
                self.expected_id("secret-assigned-value", FAKE_ASSIGNMENT.split("= ")[1]),
                self.expected_id("secret-assigned-value", FAKE_WORDS),
                self.expected_id("secret-assigned-value", FAKE_QUOTED),
                self.expected_id("secret-assigned-value", FAKE_DOLLAR),
            },
        )
        self.assertEqual(len(self.ids("secret-private-key")), 1)

    def test_unterminated_key_header_does_not_hide_a_later_key(self):
        key = self.findings("secret-private-key")[0]
        self.assertEqual(
            {(location["path"], location["line"]) for location in key["locations"]},
            {("key.pem", 1), ("docs/mixed.txt", 3)},
        )
        self.assertEqual(key["locations"][0]["context"], "[REDACTED PRIVATE KEY BLOCK]")

    def test_token_after_column_4096_is_found(self):
        second = next(f for f in self.findings("secret-api-token") if f["id"] == self.expected_id("secret-api-token", FAKE_TOKEN_TWO))
        self.assertEqual(second["locations"][0]["line"], 12)

    def test_token_beside_a_url_credential_is_its_own_finding(self):
        token = next(f for f in self.findings("secret-api-token") if f["id"] == self.expected_id("secret-api-token", FAKE_TOKEN))
        self.assertIn(13, {location["line"] for location in token["locations"]})
        url = next(f for f in self.findings("secret-url-credential") if f["id"] == self.expected_id("secret-url-credential", FAKE_URL_TWO))
        self.assertEqual(url["locations"][0]["line"], 13)

    def test_placeholders_are_not_findings(self):
        emails = self.ids("personal-email-address")
        self.assertEqual(emails, {self.expected_id("personal-email-address", FAKE_EMAIL), self.expected_id("personal-email-address", FAKE_EMAIL_TWO)})
        hosts = self.ids("host-private-tld")
        self.assertEqual(
            hosts,
            {
                self.expected_id("host-private-tld", "build.example.internal"),
                self.expected_id("host-private-tld", "printer.local"),
            },
        )
        self.assertEqual(self.ids("personal-phone-number"), {self.expected_id("personal-phone-number", FAKE_PHONE)})

    def test_commit_text_is_scanned(self):
        finding = next(f for f in self.findings("personal-email-address") if f["id"] == self.expected_id("personal-email-address", FAKE_EMAIL_TWO))
        location = finding["locations"][0]
        self.assertEqual((location["path"], location["commit"], location["blob"]), ("(commit)", self.second, self.second))

    def test_deleted_history_keeps_its_location(self):
        token = next(f for f in self.findings("secret-api-token") if f["id"] == self.expected_id("secret-api-token", FAKE_TOKEN))
        self.assertEqual(token["state"], "new")
        self.assertEqual({location["path"] for location in token["locations"]}, {"config/app.env", "zshrc"})
        location = token["locations"][0]
        self.assertEqual((location["path"], location["line"], location["commit"]), ("config/app.env", 1, self.first))
        self.assertRegex(location["blob"], r"^[0-9a-f]{40}$")
        self.assertEqual(location["context"], "API_KEY=[REDACTED]")

    def test_same_blob_records_every_path(self):
        host = next(f for f in self.findings("host-private-tld") if f["id"] == self.expected_id("host-private-tld", "printer.local"))
        self.assertEqual({location["path"] for location in host["locations"]}, {"hosts.txt", "backup/hosts.txt"})
        self.assertEqual(host["location_count"], 2)

    def test_health_counts_the_walk(self):
        health = self.report["health"]
        self.assertEqual(health["commits"], 3)
        self.assertEqual(health["binary_blobs"], 1)
        self.assertEqual(health["symlinks"], 1)
        self.assertEqual(health["unreadable_objects"], 0)
        self.assertFalse(health["shallow"])
        self.assertEqual(health["shallow_boundary"], [])

    def test_output_is_deterministic(self):
        _, _, again = run_detector(self.fixture.repo)
        self.assertEqual(self.raw, again)

    def test_acknowledged_at_head_is_quiet(self):
        stale = "  - rule: secret-api-token\n    sha256: " + "0" * 64 + f"\n    commit: {self.third}\n"
        path = self.known_file("quiet.yaml", self.acknowledgement(self.third) + stale)
        _, quiet, _ = run_detector(self.fixture.repo, environment={"KNOWN_FINDINGS_FILE": path})
        self.assertEqual(quiet["status"], "NO_NEW_FINDINGS")
        self.assertEqual(quiet["counts"], {"new": 0, "known": len(self.report["findings"]), "new_by_category": {"secret": 0, "host": 0, "personal": 0}})
        self.assertEqual(quiet["stale_known"], [{"rule": "secret-api-token", "sha256": "0" * 64}])
        self.assertEqual(quiet["health"]["status"], "COMPLETE")
        self.assertTrue(all(location["state"] == "known" for f in quiet["findings"] for location in f["locations"]))
        self.assertEqual(quiet["acknowledgement_yaml"], "acknowledged: []\n")

    def test_known_value_in_a_new_object_is_new(self):
        path = self.known_file("second.yaml", self.acknowledgement(self.second))
        _, report, _ = run_detector(self.fixture.repo, "--known-findings-file", path)
        self.assertEqual(report["status"], "ALERT")
        token = next(f for f in self.findings("secret-api-token", report) if f["id"] == self.expected_id("secret-api-token", FAKE_TOKEN))
        self.assertEqual((token["state"], token["new_locations"], token["known_locations"]), ("new", 1, 2))
        self.assertEqual({(l["path"], l["state"]) for l in token["locations"]}, {("config/app.env", "known"), ("zshrc", "new")})
        host = next(f for f in self.findings("host-private-tld", report) if f["id"] == self.expected_id("host-private-tld", "printer.local"))
        self.assertEqual(host["state"], "known", "the same blob under a new path is the acknowledged object")
        self.assertEqual(report["counts"]["new"], 1)

    def test_missing_or_malformed_acknowledgement_is_incomplete(self):
        token = next(f for f in self.findings("secret-api-token") if f["id"] == self.expected_id("secret-api-token", FAKE_TOKEN))
        text = (
            "acknowledged:\n"
            f"  - rule: secret-api-token\n    sha256: {token['sha256']}\n    commit: {'0' * 40}\n"
            f"  - rule: secret-api-token\n    sha256: xyz\n    commit: {self.third}\n"
            f"  - rule: no-such-rule\n    sha256: {token['sha256']}\n    commit: {self.third}\n"
        )
        _, report, _ = run_detector(self.fixture.repo, "--known-findings-file", self.known_file("broken.yaml", text))
        self.assertEqual(report["health"]["status"], "INCOMPLETE")
        self.assertEqual(report["health"]["missing_acknowledged_commits"], ["0" * 40])
        self.assertEqual(
            report["health"]["malformed_known_entries"],
            ["line 5: `sha256` is not 64 hex digits", "line 8: unknown rule `no-such-rule`"],
        )
        found = next(f for f in self.findings("secret-api-token", report) if f["id"] == token["id"])
        self.assertEqual(found["state"], "new")
        self.assertEqual(report["status"], "ALERT")

    def test_known_findings_file_is_read(self):
        path = self.known_file("known.yaml", self.acknowledgement(self.third))
        _, report, _ = run_detector(self.fixture.repo, environment={"KNOWN_FINDINGS_FILE": path})
        self.assertEqual(report["status"], "NO_NEW_FINDINGS")

    def acknowledged_clone(self, name, text):
        clone = self.fixture.clone(name)
        (clone / ".auditignore.yaml").write_text(text, encoding="utf-8")
        self.fixture.git("add", ".auditignore.yaml", cwd=clone)
        self.fixture.git("commit", "-q", "-m", "Acknowledge the findings", cwd=clone)
        return clone

    def test_absent_auditignore_is_an_empty_list(self):
        self.assertIsNone(self.report["health"]["acknowledgement_file"])
        self.assertEqual(self.report["expired_known"], [])
        self.assertTrue(self.report["acknowledgement_yaml"].startswith("acknowledged:\n  - rule: "))

    def test_auditignore_at_the_scanned_commit_acknowledges(self):
        text = "# acknowledged after the first report\n---\n" + self.acknowledgement(self.third, reason="'still open'  # a comment")
        clone = self.acknowledged_clone("acknowledged", text)
        _, report, _ = run_detector(clone)
        self.assertEqual(report["status"], "NO_NEW_FINDINGS")
        self.assertEqual(report["health"]["status"], "COMPLETE")
        self.assertEqual(report["health"]["acknowledgement_file"], ".auditignore.yaml")
        self.assertEqual(report["health"]["commits"], 4)
        self.assertEqual(report["health"]["malformed_known_entries"], [])
        self.assertEqual(report["counts"]["known"], len(self.report["findings"]))

    def test_acknowledgement_block_round_trips(self):
        block = self.report["acknowledgement_yaml"]
        self.assertEqual(block.count("\n  - rule: "), len(self.report["findings"]))
        clone = self.acknowledged_clone("roundtrip", block)
        _, report, _ = run_detector(clone)
        self.assertEqual(report["status"], "NO_NEW_FINDINGS")
        self.assertEqual(report["counts"]["known"], len(self.report["findings"]))

    def test_expired_acknowledgement_is_new_again(self):
        token = next(f for f in self.findings("secret-api-token") if f["id"] == self.expected_id("secret-api-token", FAKE_TOKEN))
        text = f"acknowledged:\n  - rule: {token['rule']}\n    sha256: {token['sha256']}\n    commit: {self.third}\n    expires: 2000-01-01\n"
        for finding in self.report["findings"]:
            if finding["id"] != token["id"]:
                text += f"  - rule: {finding['rule']}\n    sha256: {finding['sha256']}\n    commit: {self.third}\n    expires: 2999-12-31\n"
        clone = self.acknowledged_clone("expired", text)
        _, report, _ = run_detector(clone)
        self.assertEqual(report["status"], "ALERT")
        self.assertEqual(report["counts"]["new"], 1)
        self.assertEqual(report["expired_known"], [{"rule": token["rule"], "sha256": token["sha256"]}])
        self.assertEqual(report["health"]["status"], "COMPLETE")

    def test_malformed_expiry_is_a_malformed_entry(self):
        text = self.acknowledgement(self.third, rules={"secret-api-token"}, expires="soon")
        _, report, _ = run_detector(self.fixture.repo, "--known-findings-file", self.known_file("soon.yaml", text))
        self.assertEqual(report["health"]["malformed_known_entries"], ["line 2: `expires` is not a YYYY-MM-DD date", "line 6: `expires` is not a YYYY-MM-DD date"])
        self.assertEqual(report["health"]["status"], "INCOMPLETE")

    def test_auditignore_that_is_not_a_file_is_a_configuration_failure(self):
        clone = self.fixture.clone("linked")
        os.symlink("hosts.txt", clone / ".auditignore.yaml")
        self.fixture.git("add", ".auditignore.yaml", cwd=clone)
        self.fixture.git("commit", "-q", "-m", "Link the acknowledgement file", cwd=clone)
        code, report, _ = run_detector(clone)
        self.assertEqual(code, 2)
        self.assertEqual(report["health"]["status"], "CONFIGURATION_FAILURE")
        self.assertIn(".auditignore.yaml", report["health"]["error"])

    def test_auditignore_outside_the_shape_is_a_configuration_failure(self):
        clone = self.acknowledged_clone("shape", "findings:\n  - rule: secret-api-token\n")
        code, report, _ = run_detector(clone)
        self.assertEqual(code, 2)
        self.assertEqual(report["health"]["status"], "CONFIGURATION_FAILURE")
        self.assertIn("line 1: only the `acknowledged` key", report["health"]["error"])

    def test_auditignore_is_skipped_on_request(self):
        clone = self.acknowledged_clone("skipped", self.acknowledgement(self.third))
        _, report, _ = run_detector(clone, "--acknowledgement-path", "")
        self.assertEqual(report["status"], "ALERT")
        self.assertIsNone(report["health"]["acknowledgement_file"])

    def test_sensitive_domain_is_an_alert(self):
        path = self.fixture.directory / "domains.txt"
        path.write_text(SENSITIVE_DOMAIN + "\n", encoding="utf-8")
        known = self.acknowledgement(self.third, rules={"secret-api-token", "secret-url-credential", "secret-assigned-value", "secret-private-key", "personal-email-address", "personal-phone-number"})
        _, report, raw = run_detector(
            self.fixture.repo, "--known-findings-file", self.known_file("no-hosts.yaml", known), "--sensitive-domains-file", str(path)
        )
        self.assertEqual(report["status"], "ALERT")
        found = {finding["id"]: finding for finding in self.findings("host-sensitive-domain", report)}
        rule = self.module.HOST_SENSITIVE_DOMAIN
        expected = {
            self.module.finding_id(rule, "vpn." + SENSITIVE_DOMAIN),
            self.module.finding_id(rule, "mail." + SENSITIVE_DOMAIN),
            self.module.finding_id(rule, "claude.noreply." + SENSITIVE_DOMAIN),
        }
        self.assertEqual(set(found), expected)
        self.assertEqual(found[self.module.finding_id(rule, "mail." + SENSITIVE_DOMAIN)]["location_count"], 4)
        self.assertNotIn(SENSITIVE_DOMAIN, raw)
        self.assertNotIn(SENSITIVE_DOMAIN.upper(), raw)
        vpn = found[self.module.finding_id(rule, "vpn." + SENSITIVE_DOMAIN)]
        self.assertIn("[REDACTED]", {location["path"] for location in vpn["locations"]})
        self.assertEqual({location["context"] for location in vpn["locations"]}, {"[REDACTED]", "HostName [REDACTED]"})

    def test_private_hosts_alone_are_review(self):
        known = self.acknowledgement(self.third, rules={"secret-api-token", "secret-url-credential", "secret-assigned-value", "secret-private-key", "personal-email-address", "personal-phone-number"})
        _, report, _ = run_detector(self.fixture.repo, "--known-findings-file", self.known_file("review.yaml", known))
        self.assertEqual(report["status"], "REVIEW")

    def test_working_tree_is_never_read(self):
        self.fixture.write("untracked.env", "API_KEY=" + FAKE_TOKEN[:-6] + "999999\n")
        try:
            _, report, _ = run_detector(self.fixture.repo)
        finally:
            (self.fixture.repo / "untracked.env").unlink()
        self.assertEqual(self.ids("secret-api-token", report), self.ids("secret-api-token"))
        self.assertEqual(report["health"], self.report["health"])

    def test_shallow_clone_is_incomplete(self):
        shallow = self.fixture.shallow_clone()
        _, report, _ = run_detector(shallow)
        self.assertTrue(report["health"]["shallow"])
        self.assertEqual(report["health"]["commits"], 1)
        self.assertEqual(report["health"]["shallow_boundary"], [self.third])
        self.assertEqual(report["health"]["status"], "INCOMPLETE")
        token = next(f for f in self.findings("secret-api-token", report) if f["id"] == self.expected_id("secret-api-token", FAKE_TOKEN))
        self.assertEqual([location["path"] for location in token["locations"]], ["zshrc"])

    def test_unshallowed_clone_is_complete(self):
        clone = self.fixture.shallow_clone("unshallowed")
        self.fixture.git("fetch", "-q", "--unshallow", "origin", "main", cwd=clone)
        _, report, _ = run_detector(clone)
        self.assertFalse(report["health"]["shallow"])
        self.assertEqual(report["health"]["commits"], 3)
        self.assertEqual(report["health"]["status"], "COMPLETE")

    def test_shallow_side_branch_leaves_the_scan_complete(self):
        clone = self.fixture.clone("side")
        side = self.fixture.git("commit-tree", self.third + "^{tree}", "-p", self.third, "-m", "side", cwd=clone)
        (clone / ".git" / "shallow").write_text(side + "\n", encoding="utf-8")
        self.assertEqual(self.fixture.git("rev-parse", "--is-shallow-repository", cwd=clone), "true")
        _, report, _ = run_detector(clone)
        self.assertFalse(report["health"]["shallow"])
        self.assertEqual(report["health"]["shallow_boundary"], [])
        self.assertEqual(report["health"]["status"], "COMPLETE")

    def test_missing_repository_is_a_configuration_failure(self):
        code, report, _ = run_detector(self.fixture.directory / "absent")
        self.assertEqual(code, 2)
        self.assertEqual(report["health"]["status"], "CONFIGURATION_FAILURE")
        self.assertIsNone(report["status"])


if __name__ == "__main__":
    unittest.main()
