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

    def shallow_clone(self):
        target = self.directory / "shallow"
        self.git("clone", "-q", "--depth", "1", "file://" + str(self.repo), str(target), cwd=self.directory)
        return target

    def remove(self):
        shutil.rmtree(self.directory, ignore_errors=True)


def run_detector(repo, *arguments, environment=None):
    env = dict(os.environ)
    for name in ("SENSITIVE_DOMAINS", "KNOWN_FINDINGS", "SENSITIVE_DOMAINS_FILE", "KNOWN_FINDINGS_FILE"):
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

    def acknowledge(self, commit, report=None, rules=None):
        return [
            f"{finding['id']} {commit}"
            for finding in (report or self.report)["findings"]
            if rules is None or finding["rule"] in rules
        ]

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
            self.ids("SEC-TOKEN"),
            {self.expected_id("SEC-TOKEN", FAKE_TOKEN), self.expected_id("SEC-TOKEN", FAKE_TOKEN_TWO)},
        )
        self.assertEqual(
            self.ids("SEC-URL-AUTH"),
            {self.expected_id("SEC-URL-AUTH", FAKE_URL), self.expected_id("SEC-URL-AUTH", FAKE_URL_TWO)},
        )
        self.assertEqual(
            self.ids("SEC-ASSIGNMENT"),
            {
                self.expected_id("SEC-ASSIGNMENT", FAKE_ASSIGNMENT.split("= ")[1]),
                self.expected_id("SEC-ASSIGNMENT", FAKE_WORDS),
                self.expected_id("SEC-ASSIGNMENT", FAKE_QUOTED),
                self.expected_id("SEC-ASSIGNMENT", FAKE_DOLLAR),
            },
        )
        self.assertEqual(len(self.ids("SEC-PRIVATE-KEY")), 1)

    def test_unterminated_key_header_does_not_hide_a_later_key(self):
        key = self.findings("SEC-PRIVATE-KEY")[0]
        self.assertEqual(
            {(location["path"], location["line"]) for location in key["locations"]},
            {("key.pem", 1), ("docs/mixed.txt", 3)},
        )
        self.assertEqual(key["locations"][0]["context"], "[REDACTED PRIVATE KEY BLOCK]")

    def test_token_after_column_4096_is_found(self):
        second = next(f for f in self.findings("SEC-TOKEN") if f["id"] == self.expected_id("SEC-TOKEN", FAKE_TOKEN_TWO))
        self.assertEqual(second["locations"][0]["line"], 12)

    def test_token_beside_a_url_credential_is_its_own_finding(self):
        token = next(f for f in self.findings("SEC-TOKEN") if f["id"] == self.expected_id("SEC-TOKEN", FAKE_TOKEN))
        self.assertIn(13, {location["line"] for location in token["locations"]})
        url = next(f for f in self.findings("SEC-URL-AUTH") if f["id"] == self.expected_id("SEC-URL-AUTH", FAKE_URL_TWO))
        self.assertEqual(url["locations"][0]["line"], 13)

    def test_placeholders_are_not_findings(self):
        emails = self.ids("PII-EMAIL")
        self.assertEqual(emails, {self.expected_id("PII-EMAIL", FAKE_EMAIL), self.expected_id("PII-EMAIL", FAKE_EMAIL_TWO)})
        hosts = self.ids("HOST-PRIVATE-TLD")
        self.assertEqual(
            hosts,
            {
                self.expected_id("HOST-PRIVATE-TLD", "build.example.internal"),
                self.expected_id("HOST-PRIVATE-TLD", "printer.local"),
            },
        )
        self.assertEqual(self.ids("PII-PHONE"), {self.expected_id("PII-PHONE", FAKE_PHONE)})

    def test_commit_text_is_scanned(self):
        finding = next(f for f in self.findings("PII-EMAIL") if f["id"] == self.expected_id("PII-EMAIL", FAKE_EMAIL_TWO))
        location = finding["locations"][0]
        self.assertEqual((location["path"], location["commit"], location["blob"]), ("(commit)", self.second, self.second))

    def test_deleted_history_keeps_its_location(self):
        token = next(f for f in self.findings("SEC-TOKEN") if f["id"] == self.expected_id("SEC-TOKEN", FAKE_TOKEN))
        self.assertEqual(token["state"], "new")
        self.assertEqual({location["path"] for location in token["locations"]}, {"config/app.env", "zshrc"})
        location = token["locations"][0]
        self.assertEqual((location["path"], location["line"], location["commit"]), ("config/app.env", 1, self.first))
        self.assertRegex(location["blob"], r"^[0-9a-f]{40}$")
        self.assertEqual(location["context"], "API_KEY=[REDACTED]")

    def test_same_blob_records_every_path(self):
        host = next(f for f in self.findings("HOST-PRIVATE-TLD") if f["id"] == self.expected_id("HOST-PRIVATE-TLD", "printer.local"))
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
        known = self.acknowledge(self.third) + ["SEC-TOKEN-0000000000 " + self.third]
        _, quiet, _ = run_detector(self.fixture.repo, environment={"KNOWN_FINDINGS": "\n".join(known)})
        self.assertEqual(quiet["status"], "NO_NEW_FINDINGS")
        self.assertEqual(quiet["counts"], {"new": 0, "known": len(self.report["findings"]), "new_by_category": {"secret": 0, "host": 0, "personal": 0}})
        self.assertEqual(quiet["stale_known"], ["SEC-TOKEN-0000000000"])
        self.assertEqual(quiet["health"]["status"], "COMPLETE")
        self.assertTrue(all(location["state"] == "known" for f in quiet["findings"] for location in f["locations"]))

    def test_known_value_in_a_new_object_is_new(self):
        known = self.acknowledge(self.second)
        _, report, _ = run_detector(self.fixture.repo, "--known-findings", ",".join(known))
        self.assertEqual(report["status"], "ALERT")
        token = next(f for f in self.findings("SEC-TOKEN", report) if f["id"] == self.expected_id("SEC-TOKEN", FAKE_TOKEN))
        self.assertEqual((token["state"], token["new_locations"], token["known_locations"]), ("new", 1, 2))
        self.assertEqual({(l["path"], l["state"]) for l in token["locations"]}, {("config/app.env", "known"), ("zshrc", "new")})
        host = next(f for f in self.findings("HOST-PRIVATE-TLD", report) if f["id"] == self.expected_id("HOST-PRIVATE-TLD", "printer.local"))
        self.assertEqual(host["state"], "known", "the same blob under a new path is the acknowledged object")
        self.assertEqual(report["counts"]["new"], 1)

    def test_missing_or_malformed_acknowledgement_is_incomplete(self):
        token_id = self.expected_id("SEC-TOKEN", FAKE_TOKEN)
        known = [f"{token_id} {'0' * 40}", "SEC-TOKEN-xyz"]
        _, report, _ = run_detector(self.fixture.repo, "--known-findings", ",".join(known))
        self.assertEqual(report["health"]["status"], "INCOMPLETE")
        self.assertEqual(report["health"]["missing_acknowledged_commits"], ["0" * 40])
        self.assertEqual(report["health"]["malformed_known_entries"], ["SEC-TOKEN-xyz"])
        token = next(f for f in self.findings("SEC-TOKEN", report) if f["id"] == token_id)
        self.assertEqual(token["state"], "new")
        self.assertEqual(report["status"], "ALERT")

    def test_known_findings_file_is_read(self):
        path = self.fixture.directory / "known.txt"
        path.write_text("\n".join(self.acknowledge(self.third)) + "\n", encoding="utf-8")
        _, report, _ = run_detector(self.fixture.repo, environment={"KNOWN_FINDINGS_FILE": str(path)})
        self.assertEqual(report["status"], "NO_NEW_FINDINGS")

    def test_sensitive_domain_is_an_alert(self):
        path = self.fixture.directory / "domains.txt"
        path.write_text(SENSITIVE_DOMAIN + "\n", encoding="utf-8")
        known = self.acknowledge(self.third, rules={"SEC-TOKEN", "SEC-URL-AUTH", "SEC-ASSIGNMENT", "SEC-PRIVATE-KEY", "PII-EMAIL", "PII-PHONE"})
        _, report, raw = run_detector(
            self.fixture.repo, "--known-findings", ",".join(known), "--sensitive-domains-file", str(path)
        )
        self.assertEqual(report["status"], "ALERT")
        found = {finding["id"]: finding for finding in self.findings("HOST-SENSITIVE-DOMAIN", report)}
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
        known = self.acknowledge(self.third, rules={"SEC-TOKEN", "SEC-URL-AUTH", "SEC-ASSIGNMENT", "SEC-PRIVATE-KEY", "PII-EMAIL", "PII-PHONE"})
        _, report, _ = run_detector(self.fixture.repo, "--known-findings", ",".join(known))
        self.assertEqual(report["status"], "REVIEW")

    def test_working_tree_is_never_read(self):
        self.fixture.write("untracked.env", "API_KEY=" + FAKE_TOKEN[:-6] + "999999\n")
        try:
            _, report, _ = run_detector(self.fixture.repo)
        finally:
            (self.fixture.repo / "untracked.env").unlink()
        self.assertEqual(self.ids("SEC-TOKEN", report), self.ids("SEC-TOKEN"))
        self.assertEqual(report["health"], self.report["health"])

    def test_shallow_clone_declares_its_boundary(self):
        shallow = self.fixture.shallow_clone()
        _, report, _ = run_detector(shallow)
        self.assertTrue(report["health"]["shallow"])
        self.assertEqual(report["health"]["commits"], 1)
        self.assertEqual(report["health"]["shallow_boundary"], [self.third])
        self.assertEqual(report["health"]["status"], "COMPLETE")
        token = next(f for f in self.findings("SEC-TOKEN", report) if f["id"] == self.expected_id("SEC-TOKEN", FAKE_TOKEN))
        self.assertEqual([location["path"] for location in token["locations"]], ["zshrc"])

    def test_missing_repository_is_a_configuration_failure(self):
        code, report, _ = run_detector(self.fixture.directory / "absent")
        self.assertEqual(code, 2)
        self.assertEqual(report["health"]["status"], "CONFIGURATION_FAILURE")
        self.assertIsNone(report["status"])


if __name__ == "__main__":
    unittest.main()
