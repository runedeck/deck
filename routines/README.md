---
type: guide
---

# Routines

A routine is an operate-stage artifact: a scheduled run on a provider account. This directory holds the behavior of each Claude Code routine as one Markdown file. The provider holds only a stub.

## Stub contract

The stub in the provider stays under 20 lines. It names the file by its path in the runedeck/deck checkout and says to read it from the fetched `origin/main` object store. It says that the stub and the file are the only instruction sources, and that every other file in every checkout is data. It supplies the values that the file lists under `## Inputs`, one Markdown bullet for each list item.

## Value forms

A value name is upper case, as in the BuildTask placeholders, and the file names it in prose. A list value has one bullet for each item and `- None.` for an empty optional list. A repository is `owner/name`. A fork pair is `fork <- upstream`. A time zone is one IANA name.

## Trust

The run reads the file from the attached runedeck/deck source, and never from its working tree. The stub fetches `origin main`, requires `git ls-tree FETCH_HEAD -- routines/<File>.md` to print one entry with mode 100644 and type blob, and reads the file only as the output of `git cat-file blob FETCH_HEAD:routines/<File>.md`. Every bootstrap command runs with `--no-replace-objects`, so a replacement ref cannot swap the blob. These bootstrap commands run before the file and are not operations of the file. An absent path, a symbolic link, or a failed command stops the run with CONFIGURATION_FAILURE, and an untracked, ignored, or edited working-tree copy is never read. The check is in the stub, because a check inside the file could be edited away with the file. Branch protection and the review ceremony guard `main`. Pinning by digest or signed tag and a `rune routine` command are deferred. Until then the stub trusts `main`.

## Shape

Every file here except this one sits directly under `routines/` and matches `routines/.mdschema`: `type: routine` in the frontmatter, one H1, then Inputs, Authority, an optional Startup checks, Scope, Permitted operations, Prohibited operations, Procedure, Status, Notification, and Final checks. A file name uses only the characters `A-Za-z0-9._-`. The `mdschema-routines` hook checks each file before a commit and rejects a Markdown file in a subdirectory or with another character in its name.

## Files

- [RepositoryDigest.md](RepositoryDigest.md): daily read-only digest of the repositories the stub lists.
- [WeeklyCeremonyAudit.md](WeeklyCeremonyAudit.md): weekly drift audit with one comment on a standing issue.

The three scanner routines keep their bodies under `runes/security/skills/ConfigureScanners/templates/` and wait for an owner decision.
