# Thing

## Requirements

### Requirement: Thing Is Checked

An *[analysis tool][ANALYSISTOOL]* reads the files. Two [analysis tools][ANALYSISTOOL] may share a rule. By *[Occam's razor][OCCAMSRAZOR]*, the shorter instruction wins. A record names its *[change][CHANGE-KEY]*, and a *[change][CHANGE]* holds specifications. Plain *emphasis* carries no meaning, and a code span such as `*[fake][FAKE]*` is not read. The format is JSON ([RFC 8259][RFC8259]).

```markdown
*[inside a fence][FENCE]*
```

#### Scenario: Tool reads a file

- **WHEN** the [analysis tool][ANALYSISTOOL] reads a file
- **THEN** it reports each finding

[ANALYSISTOOL]: ../../../../specs/glossary/analysis-tool.md
[OCCAMSRAZOR]: ../../../../specs/glossary/occams-razor.md
[CHANGE]: ../../../../specs/glossary/change.md
[CHANGE-KEY]: ../../../../specs/glossary/change-key.md
[RFC8259]: https://www.rfc-editor.org/rfc/rfc8259.html
