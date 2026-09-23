# Stale queue fixtures

Each file carries `age_days` in its frontmatter. The test in
`tests/test_check_scripts.py` copies a fixture tree into a scratch git
repository and commits each file with an author and committer date that
many days in the past, because `scripts/check-stale-queue` reads an item's
age from the commit that added it at its queue path and never from the
file system. The check skips `tests/fixtures/` by anchored prefix, so the
copy of this tree in the repository never ages, and a test proves it.
