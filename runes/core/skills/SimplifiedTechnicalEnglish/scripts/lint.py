import argparse
import glob
import hashlib
import json
import os
import re
import sys
from pathlib import Path

# Score v6 skips verb-only banned words in noun position. It lints prose
# inside Markdown fences, keeps other fenced content masked, protects
# uncertainty, and reports short-text density as advisory.
SCORE_VERSION = 6
DENSITY_RELIABLE_WORDS = 40
DEFAULT_CONFIG = Path(__file__).resolve().parent.parent / "config" / "rules.json"
CONFIG_KEYS = {
    "marketing",
    "bannedWords",
    "bannedPhrases",
    "strictBannedWords",
    "phrasalVerbs",
    "fillerPhrases",
    "verbOnlyWords",
}
BE = r"(?:am|is|are|was|were|be|been|being)"
PP_IRREG = r"(?:done|made|sent|read|built|kept|held|set|put|run|written|shown|given|taken|found|got|gotten|seen|known|thrown|drawn)"
# Rule 3.3: a past participle used as an adjective is not passive. These
# stative participles only count as passive when a by-agent follows.
STATIVE = r"(?:closed|opened?|damaged|completed?|installed|connected|required|expected|configured|enabled|disabled|deprecated|supported)"
FUNC_WORDS = set(
    """a an the this that these those of for to in on at by with from as and or but if
when then than not no is are was were be been being am do does did has have had will would can could
may might must should shall it its their your our his her they we you i""".split()  # noqa: SIM905
)
ABBREVIATIONS = ("e.g.", "i.e.", "etc.", "Mr.", "Mrs.", "Ms.", "Dr.", "vs.")
SEVERITIES = {
    "long_sentence(>20w)": "hard",
    "semicolon": "hard",
    "contraction": "hard",
    "passive_voice": "soft",
    "complex_tense": "hard",
    "ing_main_verb": "hard",
    "nominalization": "soft",
    "phrasal_verb": "hard",
    "banned_word": "soft",
    "marketing_adjective": "soft",
    "filler_phrase": "soft",
    "long_paragraph(>6s)": "hard",
    "strict_banned_word": "hard",
}


def load_config(path=DEFAULT_CONFIG):
    path = Path(path).expanduser()
    try:
        raw = path.read_bytes()
    except OSError as error:
        raise ValueError(f"cannot read config {path}: {error.strerror}") from error
    try:
        data = json.loads(raw)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError(f"invalid JSON in config {path}: {error}") from error
    if not isinstance(data, dict):
        raise TypeError(f"config {path} must contain a JSON object")
    keys = set(data)
    unknown = sorted(keys - CONFIG_KEYS)
    missing = sorted(CONFIG_KEYS - keys)
    if unknown:
        raise ValueError(f"config {path} has unknown keys: {', '.join(unknown)}")
    if missing:
        raise ValueError(f"config {path} is missing keys: {', '.join(missing)}")
    normalized = {}
    for key in sorted(CONFIG_KEYS):
        values = data[key]
        if not isinstance(values, list):
            raise TypeError(f"config {path} key {key} must be a list")
        clean = []
        seen = set()
        for value in values:
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"config {path} key {key} must contain non-empty strings")
            value = value.strip().lower()
            if value not in seen:
                seen.add(value)
                clean.append(value)
        normalized[key] = clean
    return normalized, str(path.resolve()), hashlib.sha256(raw).hexdigest()


def strip_code(text):
    """Mask Markdown regions that do not contain prose."""
    lines = text.splitlines()
    masked = list(lines)
    structure_reliable = True
    if lines and lines[0].strip() == "---":
        frontmatter_end = next(
            (index for index in range(1, len(lines)) if lines[index].strip() == "---"),
            None,
        )
        if frontmatter_end is None:
            structure_reliable = False
            frontmatter_end = len(lines) - 1
        for index in range(frontmatter_end + 1):
            masked[index] = ""
    in_fence = False
    fenced_prose = False
    table = False
    for index, line in enumerate(lines):
        stripped = line.lstrip()
        if stripped.startswith(("```", "~~~")):
            if in_fence:
                in_fence = False
                fenced_prose = False
            else:
                in_fence = True
                language = stripped[3:].strip().casefold()
                fenced_prose = language in {"markdown", "md"}
            masked[index] = ""
            continue
        if in_fence and not fenced_prose:
            masked[index] = ""
            continue
        next_line = lines[index + 1] if index + 1 < len(lines) else ""
        if "|" in line and re.fullmatch(r"\s*\|?\s*:?-+:?\s*(?:\|\s*:?-+:?\s*)+\|?\s*", next_line):
            table = True
            masked[index] = ""
            continue
        if table:
            if "|" in line:
                masked[index] = ""
                continue
            table = False
        masked[index] = re.sub(r"`[^`]*`", " ", masked[index])
    if in_fence:
        structure_reliable = False
    return "\n".join(masked), structure_reliable


def sentences(text):
    blocks = []
    current = []
    for line in text.split("\n"):
        sentence = line.strip()
        if not sentence:
            if current:
                blocks.append(" ".join(current))
                current = []
            continue
        structural = bool(re.match(r"^\s*(?:#{1,6}\s+|[-*+]\s+|\d+[.)]\s+)", line))
        sentence = re.sub(r"^\s*#{1,6}\s*", "", sentence)
        sentence = re.sub(r"^\s*(?:[-*+]|\d+[.)])\s+", "", sentence)
        if not sentence:
            continue
        if structural and current:
            blocks.append(" ".join(current))
            current = []
        current.append(sentence)
        if structural:
            blocks.append(" ".join(current))
            current = []
    if current:
        blocks.append(" ".join(current))
    out = []
    for block in blocks:
        protected = block
        for index, abbreviation in enumerate(ABBREVIATIONS):
            protected = re.sub(
                re.escape(abbreviation),
                abbreviation.replace(".", f"\x00{index}"),
                protected,
                flags=re.IGNORECASE,
            )
        parts = re.split(r"(?<=[.!?:])\s+(?=[A-Z0-9\"'\-])", protected)
        for part in parts:
            for index in range(len(ABBREVIATIONS)):
                part = part.replace(f"\x00{index}", ".")
            if part.strip():
                out.append(part.strip())
    return out


def wc(sentence):
    return len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'\-/]*", sentence))


# Noun-position guard for verb-only banned words. A determiner, possessive,
# or preposition before the word marks a noun use ("the API surface", "by
# ship"), unless an auxiliary or infinitive marker follows it ("the team
# will ship"). Ambiguous positions still count as soft findings.
NOUN_MARKERS = set(
    """the a an this that these those its their our your his her my each every
any some no of on in at by from into onto over under across through near""".split()  # noqa: SIM905
)
VERB_MARKERS = set(
    "will would can could may might must shall should do does did to not".split()  # noqa: SIM905
)


def is_noun_position(prefix):
    segment = re.split(r"[.,;:!?()\n]", prefix)[-1]
    tokens = re.findall(r"[a-z'\-]+", segment)[-3:]
    for index, token in enumerate(tokens):
        if token in NOUN_MARKERS and not set(tokens[index + 1 :]) & VERB_MARKERS:
            return True
    return False


def count_verb_only(text, words):
    count = 0
    hits = []
    lower = text.lower()
    for word in words:
        for match in re.finditer(r"(?<![a-z])" + re.escape(word) + r"(?![a-z])", lower):
            if is_noun_position(lower[: match.start()]):
                continue
            count += 1
            hits.append(word)
    return count, hits


def count_ci(text, phrases):
    count = 0
    hits = []
    lower = text.lower()
    for phrase in phrases:
        for _ in re.finditer(r"(?<![a-z])" + re.escape(phrase) + r"(?![a-z])", lower):
            count += 1
            hits.append(phrase)
    return count, hits


def noun_trains(text):
    """Return 4-word non-function runs as a heuristic Rule 2.1 marker."""
    hits = []
    for sentence in sentences(text):
        words = re.findall(r"[A-Za-z][A-Za-z'\-]*", sentence)[1:]
        run = []
        for word in [*words, ""]:
            if word and word.lower() not in FUNC_WORDS and not word[0].isupper():
                run.append(word)
            else:
                if len(run) >= 4:
                    hits.append(" ".join(run))
                run = []
    return hits


def lint(text, strict=False, config=None, config_path=None, config_digest=None):
    if config is None:
        config, config_path, config_digest = load_config()
    text, structure_reliable = strip_code(text)
    sents = sentences(text)
    words = sum(wc(sentence) for sentence in sents) or 1
    violations = {}
    long_sentences = [(wc(sentence), sentence) for sentence in sents if wc(sentence) > 20]
    violations["long_sentence(>20w)"] = len(long_sentences)
    violations["semicolon"] = text.count(";")
    # 's counts as a contraction only on known heads (it's, there's, ...);
    # a possessive noun ("the standard's list") is correct STE and stays clean.
    violations["contraction"] = len(
        re.findall(r"\b\w+['’](?:t|re|ve|ll|d|m)\b", text)
    ) + len(
        re.findall(
            r"\b(?:it|that|this|there|here|what|who|she|he|let)['’]s\b",
            text,
            re.IGNORECASE,
        )
    )
    passive_parts = re.findall(
        rf"\b{BE}\s+(\w+ed|{PP_IRREG})\b", text, re.IGNORECASE
    )
    violations["passive_voice"] = sum(
        1 for part in passive_parts if not re.fullmatch(STATIVE, part, re.IGNORECASE)
    ) + len(re.findall(rf"\b{BE}\s+{STATIVE}\s+by\b", text, re.IGNORECASE))
    tense_text = re.sub(
        rf"\b(?:may|might|could|would|should|must)\s+have\s+(?:been\s+)?(?:\w+ed|{PP_IRREG})\b",
        " ",
        text,
        flags=re.IGNORECASE,
    )
    violations["complex_tense"] = len(
        re.findall(
            rf"\b(?:have|has|had)\s+(?:been\s+)?(?:\w+ed|{PP_IRREG})\b",
            tense_text,
            re.IGNORECASE,
        )
    )
    violations["ing_main_verb"] = len(
        re.findall(rf"\b{BE}\s+\w+ing\b", text, re.IGNORECASE)
    )
    violations["nominalization"] = len(
        re.findall(
            r"\b(?:perform(?:s|ed)?|conduct(?:s|ed)?|carry out|carries out|make use of|makes use of)\b",
            text,
            re.IGNORECASE,
        )
    ) + len(
        re.findall(
            r"\b\w{4,}(?:tion|ment|ance|ence)\s+of\b", text, re.IGNORECASE
        )
    )
    violations["phrasal_verb"], _ = count_ci(text, config["phrasalVerbs"])
    banned = [*config["bannedWords"], *config["bannedPhrases"]]
    violations["banned_word"], banned_hits = count_ci(text, banned)
    verb_only_count, verb_only_hits = count_verb_only(text, config["verbOnlyWords"])
    violations["banned_word"] += verb_only_count
    banned_hits.extend(verb_only_hits)
    violations["marketing_adjective"], marketing_hits = count_ci(
        text, config["marketing"]
    )
    violations["filler_phrase"], _ = count_ci(text, config["fillerPhrases"])
    paragraphs = [part for part in re.split(r"\n\s*\n", text) if part.strip()]
    violations["long_paragraph(>6s)"] = sum(
        1 for paragraph in paragraphs if len(sentences(paragraph)) > 6
    )
    em_dash = text.count("—") + text.count("–")
    trains = noun_trains(text)
    if strict:
        strict_count, _ = count_ci(text, config["strictBannedWords"])
        violations["strict_banned_word"] = strict_count
    total = sum(violations.values())
    severity_totals = {
        severity: sum(
            count for name, count in violations.items()
            if SEVERITIES.get(name) == severity
        )
        for severity in ("hard", "soft")
    }
    density_reliable = structure_reliable and words >= DENSITY_RELIABLE_WORDS
    if not structure_reliable:
        density_note = "Advisory: unterminated Markdown structure."
    elif not density_reliable:
        density_note = "Advisory: fewer than 40 words."
    else:
        density_note = None
    return {
        "score_version": SCORE_VERSION,
        "mode": "strict" if strict else "flavored",
        "config_path": config_path,
        "config_sha256": config_digest,
        "words": words,
        "sentences": len(sents),
        "violations": violations,
        "total": total,
        "severity_totals": severity_totals,
        "total_per100w": round(total * 100.0 / words, 2),
        "density_reliable": density_reliable,
        "density_note": density_note,
        "em_dash(slop-marker)": em_dash,
        "noun_train(>=4w,marker)": len(trains),
        "longest_sentence_words": (
            max(long_sentences)[0]
            if long_sentences
            else max((wc(sentence) for sentence in sents), default=0)
        ),
        "sample_marketing": list(dict.fromkeys(marketing_hits))[:6],
        "sample_banned": list(dict.fromkeys(banned_hits))[:6],
        "sample_noun_train": trains[:3],
    }


def parse_args(argv):
    parser = argparse.ArgumentParser(description="Score prose with heuristic STE checks.")
    parser.add_argument("--strict", action="store_true", help="enable strict checks")
    parser.add_argument("--json", action="store_true", help="print JSON for files")
    parser.add_argument("--config", default=DEFAULT_CONFIG, help="complete JSON rule set")
    parser.add_argument("--fail-over", type=float, help="fail above this score")
    parser.add_argument(
        "--context",
        metavar="ARGUMENTS",
        help="lint a readable draft path supplied as skill arguments",
    )
    parser.add_argument("files", nargs="*", help="files or glob patterns; stdin if empty")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    try:
        config, config_path, config_digest = load_config(args.config)
    except (TypeError, ValueError) as error:
        raise SystemExit(str(error)) from error
    if args.context is not None:
        candidate = Path(args.context).expanduser()
        if candidate.is_file():
            args.files.insert(0, str(candidate))
        else:
            message = "No readable draft path was supplied for automatic linting."
            if args.fail_over is not None:
                raise SystemExit(message)
            print(message)
            return 0
    worst = 0.0
    if not args.files:
        sys.stdin.reconfigure(encoding="utf-8")
        result = lint(
            sys.stdin.read(),
            strict=args.strict,
            config=config,
            config_path=config_path,
            config_digest=config_digest,
        )
        print(json.dumps(result, indent=2))
        worst = result["total_per100w"]
    else:
        expanded = []
        for filename in args.files:
            matches = (
                sorted(glob.glob(filename, recursive=True))
                if any(character in filename for character in "*?[")
                else [filename]
            )
            if not matches:
                raise SystemExit(f"no files matched {filename!r}")
            expanded.extend(matches)
        for filename in expanded:
            with open(filename, encoding="utf-8") as file:
                result = lint(
                    file.read(),
                    strict=args.strict,
                    config=config,
                    config_path=config_path,
                    config_digest=config_digest,
                )
            worst = max(worst, result["total_per100w"])
            if args.json:
                print(json.dumps({"file": filename, **result}, indent=2))
            else:
                print(
                    f"{os.path.basename(filename):32} "
                    f"words={result['words']:4d} total={result['total']:3d} "
                    f"per100w={result['total_per100w']:6.2f} "
                    f"em_dash={result['em_dash(slop-marker)']:2d}"
                )
    return int(args.fail_over is not None and worst > args.fail_over)


if __name__ == "__main__":
    sys.exit(main())
