The *[repository][REPOSITORY]* has an ontology, `ontology/rune.ttl`. It defines every word with a special meaning once, and a generator renders one glossary page per term under `docs/specs/glossary/`. You read the pages. People edit the ontology. Nobody edits a page.

Before you use or introduce a word that has a special meaning, look it up. Open its glossary page, or search `ontology/rune.ttl` for its label. Use the word the way its definition says. A *[projection][PROJECTION]* is a form that drops information. A *[canon][CANON]* is a rune's entrypoint file. A *[deck][DECK]* is a set of runes deployed together, and the [repository][REPOSITORY] is the container that holds [decks][DECK].

A word that seems to have a meaning but has no entry is a question. Do not guess. Ask the user what it means. When the user asks for it, run the *[fixer][FIXER]*, which adds a draft entry to the ontology and writes the term's page. A draft term warns while a change is active, and the *[archiver][ARCHIVER]* refuses a change that still links to one.

Mark a term by a link to its glossary page. Italics do not mark a term. The first use in a file is an emphasized link. A reader then notices a new term:

```markdown
The *[analysis tool][ANALYSISTOOL]* reads the file. A second [analysis tool][ANALYSISTOOL] reads the record.

[ANALYSISTOOL]: ../../../docs/specs/glossary/analysis-tool.md
```

Every later use in the same file is a plain link, so a copied paragraph keeps its links. The [fixer][FIXER] links a plain occurrence of a term the file links, and it cannot tell the verb `changes` from the term, the everyday `rule` from the artifact, or the `target` of a link from a harness *[target][TARGET]*. So a file that links a term uses that word in the term's sense only. For the everyday sense, choose another word: `alters`, `principle`, `destination`. A cited record title or file name is an inline link to the file, never bare text, so its words stay its own. Define each tag once at the end of the file as a reference definition that points at the page by a relative path. A skill is deployed as a bundle, and a relative path out of the bundle breaks after deployment, so a skill file points at the page by its repository URL, `https://github.com/runedeck/deck/blob/main/docs/specs/glossary/<term>.md`. The tag is the label in upper case with every non-letter removed. Plain italics are emphasis and mean nothing more.

Why: a model given a bare word takes its everyday meaning, and the guess reads as fact. A link puts the definition one step away and keeps one home for it. The validator reports a term that points at no entry.

[REPOSITORY]: ../../../docs/specs/glossary/repository.md
[PROJECTION]: ../../../docs/specs/glossary/projection.md
[CANON]: ../../../docs/specs/glossary/canon.md
[DECK]: ../../../docs/specs/glossary/deck.md
[FIXER]: ../../../docs/specs/glossary/fixer.md
[ARCHIVER]: ../../../docs/specs/glossary/archiver.md
[TARGET]: ../../../docs/specs/glossary/target.md
