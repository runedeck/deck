"""Add the card fields to the frozen manifest of a scratch copy of an iteration.

usage: label-manifest.py <manifest.json> <card-labels.json> [--pass-label <id>=<text>]

The labels file maps a case id to `question`, `why`, `pass_label`, and
`fail_labels`, which maps the text of an assertion to its fail label. The
script changes nothing else in the manifest, so the stored runs still match
their cases. `--pass-label` replaces the pass label of one case.
"""
import json
import sys
from pathlib import Path


def main(argv: list[str]) -> int:
    manifest_path, labels_path = Path(argv[1]), Path(argv[2])
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    labels = json.loads(labels_path.read_text(encoding="utf-8"))
    if len(argv) > 3 and argv[3] == "--pass-label":
        case_id, text = argv[4].split("=", 1)
        labels[case_id]["pass_label"] = text
    labelled = 0
    for case in manifest["evals"]:
        card = labels.get(str(case["id"]))
        if card is None:
            continue
        for field in ("question", "why", "pass_label"):
            case[field] = card[field]
        for assertion in case["assertions"]:
            fail_label = card["fail_labels"].get(assertion["text"])
            if fail_label:
                assertion["fail_label"] = fail_label
        labelled += 1
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"labelled {labelled} of {len(manifest['evals'])} cases")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
