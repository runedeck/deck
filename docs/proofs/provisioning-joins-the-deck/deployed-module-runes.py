#!/usr/bin/env python3
"""Print, for each harness tree of a consumer, the provisioning rune names
that are present anywhere below it
(provisioning-joins-the-deck proof, Consumer takes the default selection).

    python3 deployed-module-runes.py <consumer>

The names come from runes/provisioning/ under RUNE_PROOF_ROOT: each
skills/<Name>/ directory and each rules/<Name>.md. A harness tree is a
top-level dot directory of the consumer, the shape the deployer writes.
A tree with no such name prints `none`. The script reads the trees and
changes nothing.
"""
import os
import pathlib
import sys


def module_names(root):
    module = root / "runes" / "provisioning"
    skills = sorted(path.name for path in (module / "skills").iterdir() if path.is_dir())
    rules = sorted(path.stem for path in (module / "rules").glob("*.md"))
    return set(skills + rules)


def main():
    root = pathlib.Path(os.environ["RUNE_PROOF_ROOT"])
    consumer = pathlib.Path(sys.argv[1])
    names = module_names(root)
    trees = sorted(path for path in consumer.iterdir() if path.is_dir() and path.name.startswith("."))
    for tree in trees:
        found = sorted({path.stem for path in tree.rglob("*") if path.stem in names})
        print(f"{tree.name}: {' '.join(found) if found else 'none'}")


if __name__ == "__main__":
    main()
