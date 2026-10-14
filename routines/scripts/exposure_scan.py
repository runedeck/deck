"""Deterministic exposure detector for a Git repository checkout.

The detector reads Git objects only: every commit and every blob reachable
from one ref, through ``git cat-file --batch`` in a hardened environment. It
never opens the working tree and never runs repository content. It applies
versioned rules for secrets, private hosts, and personal data, groups the
matches into findings by rule and matched value, and prints one JSON
document on standard output. A matched value never appears in the output:
a finding carries its rule name and the SHA-256 of the value, its id is the
rule name plus the first ten hex digits of that digest, a path segment that
matches a rule is redacted, and the context of a location is the line with
every match replaced.

A finding is acknowledged per commit. The detector reads
``.auditignore.yaml`` from the root tree of the scanned commit, through Git
objects like every other blob. The file has one key, ``acknowledged``, with
a list of items::

    acknowledged:
      - rule: personal-email-address
        sha256: <64 hex digits of the value>
        commit: <the scanned commit of the report that listed it>
        expires: 2027-01-01   # optional, the item acknowledges nothing after
        reason: old address   # optional

The detector parses that shape with its own code, since the standard
library has no YAML parser: a ``#`` starts a comment, a value may be
quoted, and nothing else of YAML is accepted. A file outside the shape is a
configuration failure, and an item that cannot be used is listed as
malformed. An occurrence is known only when its object is reachable from
the item's commit, and the same value in any other object is a new
occurrence. An item whose date has passed no longer acknowledges and is
listed under ``expired_known``. An absent file is an empty list. The report
ends with ``acknowledgement_yaml``, the items for every finding with a new
location, ready to paste.

Finding status is separate from scan health. Status is ALERT when a new
occurrence of a secret or of a sensitive-domain host exists, REVIEW when the
only new occurrences are personal data or private-TLD hosts, and
NO_NEW_FINDINGS otherwise. Health reports what the walk covered and what it
could not read, and is INCOMPLETE when an object was unreadable, an
acknowledged commit is absent from the clone, or the history of the ref
stops at a shallow boundary.

Run it as ``python3 -I - <args>`` from a directory that is not a checkout,
so no tracked module shadows the standard library. Usage:

    python3 -I exposure_scan.py --repo <checkout> [--ref FETCH_HEAD]
        [--sensitive-domains-file F | --sensitive-domains a.example,b.example]
        [--known-findings-file F] [--acknowledgement-path .auditignore.yaml]

``SENSITIVE_DOMAINS_FILE``, ``KNOWN_FINDINGS_FILE``, and
``SENSITIVE_DOMAINS`` are read from the environment when the flags are
absent. The known-findings file has the same shape as the in-repository
file, and its items join that file's items. An empty
``--acknowledgement-path`` skips the in-repository file. Exit code 0 means
the scan ran, 2 means it could not (health CONFIGURATION_FAILURE).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import UTC, date, datetime

RULES_VERSION = "3"
SCHEMA = 4
ACKNOWLEDGEMENT_PATH = ".auditignore.yaml"
ACKNOWLEDGEMENT_KEY = "acknowledged"
ACKNOWLEDGEMENT_FIELDS = ("rule", "sha256", "commit", "expires", "reason")
MAX_BLOB_BYTES = 4 * 1024 * 1024
BINARY_PROBE_BYTES = 8192
MAX_LOCATIONS = 100
CONTEXT_CHARS = 100
MIN_KEY_BODY = 40

ALERT_RULES = frozenset({"host-sensitive-domain"})
ALERT_CATEGORIES = frozenset({"secret"})
PRIVATE_TLDS = frozenset({"internal", "local", "lan", "corp", "intranet", "localdomain"})

GIT_ENVIRONMENT = {
    "GIT_CONFIG_NOSYSTEM": "1",
    "GIT_CONFIG_GLOBAL": "/dev/null",
    "GIT_ATTR_NOSYSTEM": "1",
    "GIT_NO_LAZY_FETCH": "1",
    "GIT_OPTIONAL_LOCKS": "0",
    "GIT_TERMINAL_PROMPT": "0",
    "GIT_PAGER": "cat",
    "PAGER": "cat",
    "GIT_EXTERNAL_DIFF": "",
    "LANG": "C",
    "LC_ALL": "C",
}
GIT_OPTIONS = [
    "--no-replace-objects",
    "--no-pager",
    "-c",
    "core.hooksPath=/dev/null",
    "-c",
    "core.fsmonitor=false",
    "-c",
    "core.attributesFile=/dev/null",
    "-c",
    "protocol.allow=never",
    "-c",
    "maintenance.auto=false",
    "-c",
    "gc.auto=0",
]

PLACEHOLDER_VALUES = re.compile(
    r"^(?:x+|\*+|\.+|_+|-+|changeme|change_me|example|placeholder|redacted|"
    r"secret|password|passwd|your[_-]?\w*|my[_-]?\w*|none|null|nil|true|false|"
    r"todo|tbd|dummy|sample|test|insert[_-]?\w*|replace[_-]?\w*)$",
    re.IGNORECASE,
)
REFERENCE_PREFIXES = ("$", "{", "<", "%", "!", "/", "~", "op://", "pass:", "env:", "file:", "from_env")
# An unquoted value that reads as a variable, an attribute chain, or an
# upper-case constant is a reference. A lower-case word is a literal.
REFERENCE_SHAPES = re.compile(r"^(?:[A-Z][A-Z0-9_]*|[A-Za-z_][\w-]*(?:[.:][\w-]+)+|\w+_(?:var|env|ref|key_name|secret_name))$")
PLACEHOLDER_EMAIL_LOCAL = frozenset(
    {
        "user",
        "you",
        "name",
        "email",
        "someone",
        "foo",
        "bar",
        "john.doe",
        "jane.doe",
        "git",
        "root",
        "admin",
        "example",
        "test",
        "me",
        "username",
        "first.last",
    }
)
PLACEHOLDER_EMAIL_DOMAINS = (
    "example.com",
    "example.org",
    "example.net",
    "example",
    "test",
    "localhost",
    "domain.com",
    "email.com",
    "your-domain.com",
    "invalid",
)


@dataclass(frozen=True)
class Rule:
    code: str
    category: str
    pattern: re.Pattern | None = None
    normalize: bool = False  # lowercase the value before hashing


# Secret rules precede host rules, which precede personal rules. The order
# decides which rule reports a value that two rules match (see suppressed).
SEC_TOKEN = Rule(
    "secret-api-token",
    "secret",
    re.compile(
        r"(?<![A-Za-z0-9_])(?:"
        r"gh[pousr]_[A-Za-z0-9]{36,}"
        r"|github_pat_[A-Za-z0-9_]{22,}"
        r"|glpat-[A-Za-z0-9_-]{20,}"
        r"|(?:AKIA|ASIA)[0-9A-Z]{16}"
        r"|xox[baprs]-[A-Za-z0-9-]{10,}"
        r"|(?:sk|rk)_live_[0-9a-zA-Z]{24,}"
        r"|AIza[0-9A-Za-z_-]{35}"
        r"|sk-ant-[A-Za-z0-9_-]{20,}"
        r"|sk-proj-[A-Za-z0-9_-]{20,}"
        r"|sk-[A-Za-z0-9]{20}T3BlbkFJ[A-Za-z0-9]{20}"
        r"|npm_[A-Za-z0-9]{36}"
        r"|pypi-AgEIcHlwaS5vcmc[A-Za-z0-9_-]{20,}"
        r"|hf_[A-Za-z0-9]{30,}"
        r"|SG\.[A-Za-z0-9_-]{22}\.[A-Za-z0-9_-]{43}"
        r"|AGE-SECRET-KEY-1[0-9A-Z]{58}"
        r"|eyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}"
        r")(?![A-Za-z0-9_])"
    ),
)
SEC_URL_AUTH = Rule(
    "secret-url-credential",
    "secret",
    re.compile(r"\b[a-z][a-z0-9+.-]*+://(?P<credential>(?P<user>[^\s/:@'\"]++):(?P<password>[^\s/@'\"]++))@[^\s'\"]++"),
)
SEC_ASSIGNMENT = Rule(
    "secret-assigned-value",
    "secret",
    re.compile(
        r"(?i)(?<![.:/-])\b(?:password|passwd|pwd|secret|token|api[_-]?key|access[_-]?token|"
        r"auth[_-]?token|client[_-]?secret|private[_-]?key|secret[_-]?key)"
        r"[A-Za-z0-9_]*+\s*+[:=]\s*+(?P<quote>[\"']?)(?P<credential>[^\s\"',;]{8,}+)"
    ),
)
SEC_PRIVATE_KEY = Rule("secret-private-key", "secret")
HOST_SENSITIVE_DOMAIN = Rule("host-sensitive-domain", "host", normalize=True)
HOST_PRIVATE_TLD = Rule("host-private-tld", "host", normalize=True)
PII_EMAIL = Rule(
    "personal-email-address",
    "personal",
    re.compile(r"(?<![A-Za-z0-9._%+/-])([A-Za-z0-9._%+-]++@[A-Za-z0-9.-]+\.[A-Za-z]{2,})(?![A-Za-z0-9-])"),
    normalize=True,
)
PII_PHONE = Rule(
    "personal-phone-number",
    "personal",
    re.compile(r"(?<![\w.+-])(\+\d{1,3}(?:[ .-]?\(?\d{1,4}\)?)(?:[ .-]?\d{2,4}){2,4}|\(\d{3}\) ?\d{3}-\d{4})(?![\w-])"),
)
LINE_RULES = [SEC_TOKEN, SEC_URL_AUTH, SEC_ASSIGNMENT, PII_EMAIL, PII_PHONE]
RULES_BY_CODE = {
    rule.code: rule
    for rule in (SEC_TOKEN, SEC_URL_AUTH, SEC_ASSIGNMENT, SEC_PRIVATE_KEY, HOST_SENSITIVE_DOMAIN, HOST_PRIVATE_TLD, PII_EMAIL, PII_PHONE)
}
CATEGORY_ORDER = {"secret": 0, "host": 1, "personal": 2}

# Hostnames are found by one linear tokenizer and classified in code, so no
# suffix alternation backtracks over a long run of labels.
HOST_TOKEN = re.compile(r"(?<![\w.-])([a-z0-9][a-z0-9-]*+(?:\.[a-z0-9][a-z0-9-]*+)++)(?![\w-])(?!\.[a-z0-9])", re.IGNORECASE)
KEY_BEGIN = "-----BEGIN "
KEY_END = "-----END "
KEY_HEADER = re.compile(r"-----BEGIN (?:[A-Z0-9 ]+ )?PRIVATE KEY(?: BLOCK)?-----")


class GitError(RuntimeError):
    pass


class Repository:
    """Read-only access to one Git object store through a batch reader."""

    def __init__(self, path: str):
        self.path = path
        self.environment = {"PATH": os.environ.get("PATH", "/usr/bin:/bin")}
        self.environment.update(GIT_ENVIRONMENT)
        self._batch = None

    def run(self, *arguments: str) -> str:
        command = ["git", *GIT_OPTIONS, "-C", self.path, *arguments]
        try:
            completed = subprocess.run(
                command, env=self.environment, capture_output=True, check=False, text=True, errors="replace"
            )
        except OSError as error:
            raise GitError(f"git could not start: {error}") from error
        if completed.returncode != 0:
            raise GitError(f"git {arguments[0]} failed: {completed.stderr.strip()[:200]}")
        return completed.stdout

    def batch(self):
        if self._batch is None:
            self._batch = subprocess.Popen(
                ["git", *GIT_OPTIONS, "-C", self.path, "cat-file", "--batch"],
                env=self.environment,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
            )
        return self._batch

    def read_object(self, oid: str) -> tuple[str, bytes] | None:
        """Return (type, bytes) for one object id, or None when unreadable."""
        process = self.batch()
        process.stdin.write(oid.encode("ascii") + b"\n")
        process.stdin.flush()
        header = process.stdout.readline()
        if not header:
            raise GitError("cat-file --batch ended early")
        parts = header.decode("ascii", "replace").split()
        if len(parts) != 3:
            return None
        _, kind, size = parts
        body = process.stdout.read(int(size))
        process.stdout.read(1)  # trailing newline
        return kind, body

    def close(self):
        if self._batch is not None:
            self._batch.stdin.close()
            self._batch.wait()
            self._batch = None


def parse_tree(body: bytes):
    """Yield (mode, name, oid) for one raw tree object."""
    position = 0
    while position < len(body):
        space = body.index(b" ", position)
        nul = body.index(b"\x00", space)
        mode = body[position:space].decode("ascii")
        name = body[space + 1 : nul].decode("utf-8", "replace")
        oid = body[nul + 1 : nul + 21].hex()
        position = nul + 21
        yield mode, name, oid


@dataclass
class Match:
    rule: Rule
    value: str
    line: int
    start: int  # span of the credential or value within the line
    end: int


@dataclass
class Location:
    path: str
    line: int
    commit: str
    blob: str
    context: str
    state: str = "new"

    def as_dict(self):
        return {
            "path": self.path,
            "line": self.line,
            "commit": self.commit,
            "blob": self.blob,
            "state": self.state,
            "context": self.context,
        }


@dataclass
class Finding:
    id: str
    rule: str
    category: str
    sha256: str
    locations: list[Location] = field(default_factory=list)
    location_count: int = 0


def value_digest(rule: Rule, value: str) -> str:
    """The SHA-256 of the matched value, lowercased first for a rule that normalizes."""
    normalized = value.lower() if rule.normalize else value
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def finding_id(rule: Rule, value: str) -> str:
    """The display id: the rule name plus the first ten hex digits of the digest."""
    return f"{rule.code}-{value_digest(rule, value)[:10]}"


def placeholder_assignment(value: str, quoted: bool) -> bool:
    """A reference or a placeholder is not a literal secret.

    A quoted value is a literal: only the placeholder words exempt it. An
    unquoted value is a reference when it starts like one, calls or indexes
    something, or has the shape of a variable or an attribute chain.
    """
    if PLACEHOLDER_VALUES.match(value):
        return True
    if quoted:
        return False  # a quoted value is a literal, whatever it starts with
    if value.startswith(REFERENCE_PREFIXES):
        return True
    if any(character in value for character in "()[]"):
        return True
    return REFERENCE_SHAPES.match(value) is not None


def placeholder_email(value: str) -> bool:
    lowered = value.lower()
    local, _, domain = lowered.rpartition("@")
    if "noreply" in lowered or "no-reply" in lowered:
        return True
    if local in PLACEHOLDER_EMAIL_LOCAL:
        return True
    return any(domain == suffix or domain.endswith("." + suffix) for suffix in PLACEHOLDER_EMAIL_DOMAINS)


def placeholder_url_auth(password: str) -> bool:
    return password.startswith(REFERENCE_PREFIXES) or PLACEHOLDER_VALUES.match(password) is not None


def phone_digits_ok(value: str) -> bool:
    digits = sum(character.isdigit() for character in value)
    return 9 <= digits <= 15


def classify_host(value: str, sensitive_domains: list[str]) -> Rule | None:
    lowered = value.lower()
    labels = "." + lowered + "."
    for domain in sensitive_domains:
        if "." + domain + "." in labels:  # the domain as whole labels, anywhere in the name
            return HOST_SENSITIVE_DOMAIN
    if lowered.rsplit(".", 1)[-1] in PRIVATE_TLDS and "noreply" not in lowered:
        return HOST_PRIVATE_TLD
    return None


def suppressed(start: int, end: int, rule: Rule, spans: list[tuple[int, int, Rule]]) -> bool:
    """A match that overlaps the credential span of an earlier rule is the
    same credential and is reported once, under the earlier rule.

    A token inside an assignment value, or an email that is the user and
    password of an authenticated URL, is one finding. A credential outside
    the earlier credential span is its own finding. A host and a personal
    value may share a span: an email at a sensitive domain is both.
    """
    for other_start, other_end, other in spans:
        if end <= other_start or start >= other_end:
            continue
        if {rule.category, other.category} == {"host", "personal"}:
            continue
        return True
    return False


def private_key_blocks(text: str):
    """Yield (line, body) for each terminated private-key block, linearly."""
    position = 0
    while True:
        begin = text.find(KEY_BEGIN, position)
        if begin < 0:
            return
        header_end = text.find("-----", begin + len(KEY_BEGIN))
        if header_end < 0:
            return
        header = text[begin : header_end + 5]
        position = header_end + 5
        if not KEY_HEADER.fullmatch(header):
            continue
        end = text.find(KEY_END, position)
        next_begin = text.find(KEY_BEGIN, position)
        if end < 0 or (0 <= next_begin < end):
            continue  # an unterminated header; a later block is still searched
        body = text[position:end]
        position = end + len(KEY_END)
        yield text.count("\n", 0, begin) + 1, body


def scan_text(text: str, sensitive_domains: list[str]) -> list[Match]:
    matches: list[Match] = []
    for line, body in private_key_blocks(text):
        if len(re.sub(r"\s", "", body)) < MIN_KEY_BODY or "..." in body:
            continue
        matches.append(Match(SEC_PRIVATE_KEY, body, line, 0, 0))
    for number, line in enumerate(text.splitlines(), start=1):
        spans: list[tuple[int, int, Rule]] = []
        for rule in LINE_RULES:
            for found in rule.pattern.finditer(line):
                value = found.group(1) if found.groups() else found.group(0)
                start, end = found.span()
                if rule is SEC_ASSIGNMENT:
                    value = found.group("credential")
                    if placeholder_assignment(value, bool(found.group("quote"))):
                        continue
                    start, end = found.span("credential")
                elif rule is SEC_URL_AUTH:
                    if placeholder_url_auth(found.group("password")):
                        continue
                    value = found.group(0)
                    start, end = found.span("credential")
                elif (rule is PII_EMAIL and placeholder_email(value)) or (rule is PII_PHONE and not phone_digits_ok(value)):
                    continue
                if suppressed(start, end, rule, spans):
                    continue
                spans.append((start, end, rule))
                matches.append(Match(rule, value, number, start, end))
            if rule is SEC_ASSIGNMENT:
                # Hosts come after the secret rules and before the personal rules.
                for found in HOST_TOKEN.finditer(line):
                    host_rule = classify_host(found.group(1), sensitive_domains)
                    if host_rule is None or suppressed(*found.span(1), host_rule, spans):
                        continue
                    spans.append((*found.span(1), host_rule))
                    matches.append(Match(host_rule, found.group(1), number, *found.span(1)))
    return matches


def redact(text: str, sensitive_domains: list[str]) -> tuple[str, bool]:
    """Replace every rule match in one line of text with [REDACTED]."""
    spans = sorted(
        {(match.start, match.end) for match in scan_text(text, sensitive_domains) if match.end > match.start},
        reverse=True,
    )
    for start, end in spans:
        text = text[:start] + "[REDACTED]" + text[end:]
    return text, bool(spans)


def is_binary(body: bytes) -> bool:
    return b"\x00" in body[:BINARY_PROBE_BYTES]


@dataclass
class Acknowledgement:
    rule: str
    sha256: str
    commit: str
    expires: date | None = None
    reason: str = ""

    @property
    def key(self) -> tuple[str, str]:
        return self.rule, self.sha256


@dataclass
class Acknowledgements:
    valid: list[Acknowledgement] = field(default_factory=list)
    malformed: list[str] = field(default_factory=list)
    expired: list[Acknowledgement] = field(default_factory=list)

    def extend(self, other: Acknowledgements):
        self.valid.extend(other.valid)
        self.malformed.extend(other.malformed)
        self.expired.extend(other.expired)


def strip_comment(line: str) -> str:
    """Drop a `#` comment that starts the line or follows a space, outside quotes."""
    quote = None
    for index, character in enumerate(line):
        if quote:
            if character == quote:
                quote = None
        elif character in "\"'":
            quote = character
        elif character == "#" and (index == 0 or line[index - 1] in " \t"):
            return line[:index]
    return line


def split_pair(text: str, number: int) -> tuple[str, str]:
    """Split `key: value`; the value may be empty."""
    key, separator, value = text.partition(":")
    if not separator or not re.fullmatch(r"[a-z][a-z0-9_]*", key) or (value and not value[0] in " \t"):
        raise ValueError(f"{ACKNOWLEDGEMENT_PATH} line {number}: expected `key: value`")
    return key, value.strip()


def parse_acknowledgement_yaml(text: str, today: date | None = None) -> Acknowledgements:
    """Parse the one YAML shape of `.auditignore.yaml` without a YAML library.

    The document is a mapping with one key, `acknowledged`, whose value is a
    list of mappings with plain or quoted scalar values. A document outside
    that shape raises ValueError, which is a configuration failure. An item
    that cannot be used is malformed and listed with its line number.
    """
    today = today or datetime.now(UTC).date()
    items: list[tuple[int, dict[str, str], list[str]]] = []
    item_indent = None
    key_column = None
    seen_key = False
    for number, raw in enumerate(text.splitlines(), start=1):
        line = strip_comment(raw).rstrip()
        content = line.strip()
        if not content or content == "---":
            continue
        indent = len(line) - len(line.lstrip(" "))
        if "\t" in line[:indent]:
            raise ValueError(f"{ACKNOWLEDGEMENT_PATH} line {number}: a tab indents the line")
        if indent == 0:
            if content not in (f"{ACKNOWLEDGEMENT_KEY}:", f"{ACKNOWLEDGEMENT_KEY}: []"):
                raise ValueError(f"{ACKNOWLEDGEMENT_PATH} line {number}: only the `{ACKNOWLEDGEMENT_KEY}` key is allowed at the top level")
            if seen_key:
                raise ValueError(f"{ACKNOWLEDGEMENT_PATH} line {number}: the `{ACKNOWLEDGEMENT_KEY}` key appears twice")
            seen_key = True
            continue
        if not seen_key:
            raise ValueError(f"{ACKNOWLEDGEMENT_PATH} line {number}: an indented line before the `{ACKNOWLEDGEMENT_KEY}` key")
        if content.startswith("-") and (len(content) == 1 or content[1] in " \t"):
            if item_indent is None:
                item_indent = indent
            if indent != item_indent:
                raise ValueError(f"{ACKNOWLEDGEMENT_PATH} line {number}: a list item at another indentation")
            rest = content[1:]
            key_column = indent + 1 + (len(rest) - len(rest.lstrip(" \t")))
            items.append((number, {}, []))
            pair = rest.strip()
            if not pair:
                raise ValueError(f"{ACKNOWLEDGEMENT_PATH} line {number}: an empty list item")
        else:
            if not items or indent != key_column:
                raise ValueError(f"{ACKNOWLEDGEMENT_PATH} line {number}: a line that is neither a list item nor one of its keys")
            pair = content
        key, value = split_pair(pair, number)
        _, mapping, errors = items[-1]
        if key in mapping:
            errors.append(f"line {number}: the key `{key}` appears twice")
        elif key not in ACKNOWLEDGEMENT_FIELDS:
            errors.append(f"line {number}: unknown key `{key}`")
        elif value[:1] in ("[", "{", "|", ">", "&", "*", "!"):
            errors.append(f"line {number}: `{key}` is not a plain value")
        else:
            if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
                value = value[1:-1]
            mapping[key] = value
    parsed = Acknowledgements()
    for number, mapping, errors in items:
        errors.extend(acknowledgement_errors(mapping, number))
        if errors:
            parsed.malformed.extend(errors)
            continue
        expires = date.fromisoformat(mapping["expires"]) if mapping.get("expires") else None
        acknowledgement = Acknowledgement(mapping["rule"], mapping["sha256"].lower(), mapping["commit"].lower(), expires, mapping.get("reason", ""))
        if expires is not None and expires < today:
            parsed.expired.append(acknowledgement)
        else:
            parsed.valid.append(acknowledgement)
    return parsed


def acknowledgement_errors(mapping: dict[str, str], number: int) -> list[str]:
    errors = []
    for name in ("rule", "sha256", "commit"):
        if not mapping.get(name):
            errors.append(f"line {number}: `{name}` is missing")
    if mapping.get("rule") and mapping["rule"] not in RULES_BY_CODE:
        errors.append(f"line {number}: unknown rule `{mapping['rule']}`")
    if mapping.get("sha256") and not re.fullmatch(r"[0-9a-fA-F]{64}", mapping["sha256"]):
        errors.append(f"line {number}: `sha256` is not 64 hex digits")
    if mapping.get("commit") and not re.fullmatch(r"[0-9a-fA-F]{7,40}", mapping["commit"]):
        errors.append(f"line {number}: `commit` is not a commit id")
    if mapping.get("expires"):
        try:
            date.fromisoformat(mapping["expires"])
        except ValueError:
            errors.append(f"line {number}: `expires` is not a YYYY-MM-DD date")
    return errors


def acknowledgement_yaml(findings: list[dict], commit: str) -> str:
    """The items that acknowledge every finding with a new location at this commit."""
    lines = []
    for finding in findings:
        if finding["new_locations"]:
            lines += [f"  - rule: {finding['rule']}", f"    sha256: {finding['sha256']}", f"    commit: {commit}"]
    if not lines:
        return f"{ACKNOWLEDGEMENT_KEY}: []\n"
    return "\n".join([f"{ACKNOWLEDGEMENT_KEY}:", *lines]) + "\n"


class Scan:
    def __init__(self, repository: Repository, ref: str, sensitive_domains: list[str], known: Acknowledgements, acknowledgement_path: str = ACKNOWLEDGEMENT_PATH):
        self.repository = repository
        self.ref = ref
        self.sensitive_domains = sorted({domain.strip().lower().lstrip(".") for domain in sensitive_domains if domain.strip()})
        self.acknowledgements = known
        self.acknowledgement_path = acknowledgement_path
        self.findings: dict[tuple[str, str], Finding] = {}  # (rule, sha256) -> finding
        self.blob_matches: dict[str, list[Match] | None] = {}
        self.blob_lines: dict[str, list[str]] = {}
        self.tree_entries: dict[str, list[tuple[str, str, str]] | None] = {}
        self.seen_tree_paths: set[tuple[str, str]] = set()
        self.seen_blob_paths: set[tuple[str, str]] = set()
        self.seen_submodules: set[str] = set()
        self.acknowledged: dict[tuple[str, str], set[str]] = {}  # (rule, sha256) -> reachable objects of its commits
        self.health = {
            "commits": 0,
            "blobs": 0,
            "scanned_blobs": 0,
            "binary_blobs": 0,
            "oversize_blobs": 0,
            "symlinks": 0,
            "submodules": 0,
            "unreadable_objects": 0,
            "shallow": False,
            "shallow_boundary": [],
            "locations_capped": 0,
            "missing_acknowledged_commits": [],
            "malformed_known_entries": known.malformed,
            "acknowledgement_file": None,
        }

    # -- findings -----------------------------------------------------------

    def record(self, matches: list[Match], lines: list[str], path: str, commit: str, oid: str):
        safe_path, _ = redact(path, self.sensitive_domains)
        for match in matches:
            digest = value_digest(match.rule, match.value)
            key = (match.rule.code, digest)
            finding = self.findings.get(key)
            if finding is None:
                finding = Finding(f"{match.rule.code}-{digest[:10]}", match.rule.code, match.rule.category, digest)
                self.findings[key] = finding
            finding.location_count += 1
            if len(finding.locations) >= MAX_LOCATIONS:
                self.health["locations_capped"] += 1
                continue
            line = lines[match.line - 1] if 0 < match.line <= len(lines) else ""
            context, _ = redact(line, self.sensitive_domains)
            if match.rule is SEC_PRIVATE_KEY:
                context = "[REDACTED PRIVATE KEY BLOCK]"
            finding.locations.append(Location(safe_path, match.line, commit, oid, context[:CONTEXT_CHARS]))

    def scan_blob(self, oid: str, path: str, commit: str):
        if (oid, path) in self.seen_blob_paths:
            return
        self.seen_blob_paths.add((oid, path))
        if oid not in self.blob_matches:
            self.health["blobs"] += 1
            self.blob_matches[oid] = None
            read = self.repository.read_object(oid)
            if read is None or read[0] != "blob":
                self.health["unreadable_objects"] += 1
                return
            body = read[1]
            if len(body) > MAX_BLOB_BYTES:
                self.health["oversize_blobs"] += 1
                return
            if is_binary(body):
                self.health["binary_blobs"] += 1
                return
            self.health["scanned_blobs"] += 1
            text = body.decode("utf-8", "replace")
            matches = scan_text(text, self.sensitive_domains)
            self.blob_matches[oid] = matches
            if matches:
                self.blob_lines[oid] = text.splitlines()
        matches = self.blob_matches[oid]
        if matches:
            self.record(matches, self.blob_lines[oid], path, commit, oid)

    # -- walk ---------------------------------------------------------------

    def tree(self, oid: str) -> list[tuple[str, str, str]] | None:
        if oid not in self.tree_entries:
            read = self.repository.read_object(oid)
            if read is None or read[0] != "tree":
                self.health["unreadable_objects"] += 1
                self.tree_entries[oid] = None
            else:
                self.tree_entries[oid] = list(parse_tree(read[1]))
        return self.tree_entries[oid]

    def scan_tree(self, root: str, commit: str):
        stack = [(root, "")]
        while stack:
            oid, prefix = stack.pop()
            if (oid, prefix) in self.seen_tree_paths:
                continue
            self.seen_tree_paths.add((oid, prefix))
            entries = self.tree(oid)
            if entries is None:
                continue
            for mode, name, child in reversed(entries):
                path = f"{prefix}{name}"
                if mode == "40000":
                    stack.append((child, path + "/"))
                elif mode == "120000":
                    if child not in self.blob_matches:
                        self.health["symlinks"] += 1
                    self.scan_blob(child, path, commit)  # the link target text is data
                elif mode == "160000":
                    if child not in self.seen_submodules:
                        self.seen_submodules.add(child)
                        self.health["submodules"] += 1
                else:
                    self.scan_blob(child, path, commit)

    def scan_commit(self, oid: str):
        read = self.repository.read_object(oid)
        if read is None or read[0] != "commit":
            self.health["unreadable_objects"] += 1
            return
        text = read[1].decode("utf-8", "replace")
        self.record(scan_text(text, self.sensitive_domains), text.splitlines(), "(commit)", oid, oid)
        tree = next((line[5:].strip() for line in text.split("\n\n", 1)[0].splitlines() if line.startswith("tree ")), None)
        if tree:
            self.scan_tree(tree, oid)

    def run(self) -> str:
        repository = self.repository
        commit = repository.run("rev-parse", "--verify", f"{self.ref}^{{commit}}").strip()
        commits = repository.run("rev-list", commit).split()
        self.health["commits"] = len(commits)
        # A root of the walk whose object names a parent is a shallow graft: the
        # history of this ref stops there. A shallow side branch does not count.
        roots = repository.run("rev-list", "--max-parents=0", commit).split()
        boundary = [oid for oid in roots if self.names_parent(oid)]
        self.health["shallow"] = bool(boundary)
        self.health["shallow_boundary"] = boundary
        self.load_acknowledgement_file(commit)
        for oid in commits:
            self.scan_commit(oid)
        self.resolve_acknowledgements()
        return commit

    def load_acknowledgement_file(self, commit: str):
        """Read the acknowledgement file from the root tree of the scanned commit."""
        path = self.acknowledgement_path
        if not path:
            return
        entry = self.repository.run("ls-tree", commit, "--", path).strip()
        if not entry:
            return
        mode, kind, oid = entry.split("\t", 1)[0].split()
        if mode not in ("100644", "100755") or kind != "blob":
            raise GitError(f"{path} at the scanned commit is not a regular file (mode {mode}, type {kind})")
        read = self.repository.read_object(oid)
        if read is None or read[0] != "blob":
            raise GitError(f"{path} at the scanned commit could not be read")
        self.health["acknowledgement_file"] = path
        self.acknowledgements.extend(parse_acknowledgement_yaml(read[1].decode("utf-8", "replace")))

    def names_parent(self, oid: str) -> bool:
        read = self.repository.read_object(oid)
        if read is None or read[0] != "commit":
            return False
        header = read[1].decode("utf-8", "replace").split("\n\n", 1)[0]
        return any(line.startswith("parent ") for line in header.splitlines())

    def resolve_acknowledgements(self):
        reachable: dict[str, set[str] | None] = {}
        for entry in self.acknowledgements.valid:
            if entry.commit not in reachable:
                try:
                    full = self.repository.run("rev-parse", "--verify", f"{entry.commit}^{{commit}}").strip()
                    objects = self.repository.run("rev-list", "--objects", full).split("\n")
                    reachable[entry.commit] = {line.split(" ", 1)[0] for line in objects if line}
                except GitError:
                    reachable[entry.commit] = None
                    self.health["missing_acknowledged_commits"].append(entry.commit)
            objects = reachable[entry.commit]
            if objects is not None:
                self.acknowledged.setdefault(entry.key, set()).update(objects)
        for key, finding in self.findings.items():
            objects = self.acknowledged.get(key, set())
            for location in finding.locations:
                location.state = "known" if location.blob in objects else "new"

    # -- report -------------------------------------------------------------

    def report(self, commit: str) -> dict:
        findings = []
        new_counts = {"secret": 0, "host": 0, "personal": 0}
        known_count = 0
        alert = False
        for finding in self.findings.values():
            finding.locations.sort(key=lambda location: (location.path, location.line, location.commit))
            new_locations = sum(location.state == "new" for location in finding.locations)
            state = "new" if new_locations else "known"
            if state == "known":
                known_count += 1
            else:
                new_counts[finding.category] += 1
                if finding.category in ALERT_CATEGORIES or finding.rule in ALERT_RULES:
                    alert = True
            findings.append(
                {
                    "id": finding.id,
                    "state": state,
                    "rule": finding.rule,
                    "category": finding.category,
                    "sha256": finding.sha256,
                    "location_count": finding.location_count,
                    "new_locations": new_locations,
                    "known_locations": len(finding.locations) - new_locations,
                    "locations": [location.as_dict() for location in finding.locations],
                }
            )
        findings.sort(key=lambda item: (item["state"] != "new", CATEGORY_ORDER[item["category"]], item["rule"], item["id"]))
        new_total = sum(new_counts.values())
        status = "ALERT" if alert else "REVIEW" if new_total else "NO_NEW_FINDINGS"
        health = dict(self.health)
        incomplete = (
            health["unreadable_objects"]
            or health["missing_acknowledged_commits"]
            or health["malformed_known_entries"]
            or health["shallow"]
        )
        health["status"] = "INCOMPLETE" if incomplete else "COMPLETE"
        acknowledged_keys = {entry.key for entry in self.acknowledgements.valid}
        expired_keys = {entry.key for entry in self.acknowledgements.expired} - acknowledged_keys
        return {
            "schema": SCHEMA,
            "rules_version": RULES_VERSION,
            "ref": self.ref,
            "commit": commit,
            "status": status,
            "health": health,
            "counts": {"new": new_total, "known": known_count, "new_by_category": new_counts},
            "stale_known": [{"rule": rule, "sha256": digest} for rule, digest in sorted(acknowledged_keys - set(self.findings))],
            "expired_known": [{"rule": rule, "sha256": digest} for rule, digest in sorted(expired_keys)],
            "findings": findings,
            "acknowledgement_yaml": acknowledgement_yaml(findings, commit),
        }


def split_list(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in re.split(r"[,\n]+", value) if item.strip()]


def read_list(path: str | None, inline: str | None) -> list[str]:
    if path:
        with open(path, encoding="utf-8") as handle:
            return split_list(handle.read())
    return split_list(inline)


def parse_arguments(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--repo", required=True, help="path of the Git checkout or bare repository")
    parser.add_argument("--ref", default="FETCH_HEAD", help="ref to scan (default FETCH_HEAD)")
    parser.add_argument("--sensitive-domains-file", default=os.environ.get("SENSITIVE_DOMAINS_FILE"))
    parser.add_argument(
        "--known-findings-file",
        default=os.environ.get("KNOWN_FINDINGS_FILE"),
        help=f"a file in the shape of {ACKNOWLEDGEMENT_PATH} whose items join the in-repository file",
    )
    parser.add_argument("--sensitive-domains", default=os.environ.get("SENSITIVE_DOMAINS", ""))
    parser.add_argument(
        "--acknowledgement-path",
        default=ACKNOWLEDGEMENT_PATH,
        help=f"path of the acknowledgement file in the scanned tree (default {ACKNOWLEDGEMENT_PATH}; empty skips it)",
    )
    return parser.parse_args(argv)


def failure(ref: str, error: str) -> dict:
    return {
        "schema": SCHEMA,
        "rules_version": RULES_VERSION,
        "ref": ref,
        "status": None,
        "health": {"status": "CONFIGURATION_FAILURE", "error": error},
    }


def main(argv: list[str] | None = None) -> int:
    arguments = parse_arguments(sys.argv[1:] if argv is None else argv)
    repository = Repository(arguments.repo)
    try:
        # Domain lists do not support "domain,domain" spelling in the stub,
        # but the inline form accepts commas for the command line.
        domains = [item for value in read_list(arguments.sensitive_domains_file, arguments.sensitive_domains) for item in value.split()]
        known = Acknowledgements()
        if arguments.known_findings_file:
            with open(arguments.known_findings_file, encoding="utf-8") as handle:
                known = parse_acknowledgement_yaml(handle.read())
        scan = Scan(repository, arguments.ref, domains, known, arguments.acknowledgement_path)
        commit = scan.run()
        report = scan.report(commit)
    except Exception as error:  # noqa: BLE001 - any failure is a configuration failure, never a traceback
        json.dump(failure(arguments.ref, f"{type(error).__name__}: {error}"[:300]), sys.stdout, indent=2)
        sys.stdout.write("\n")
        return 2
    finally:
        repository.close()
    json.dump(report, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
