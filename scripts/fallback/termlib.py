"""The term model the fallback scripts share: check-terms, generate-glossary,
and fix-terms import it, so the three never disagree about a page name, a
tag, or a byte of a rendered page.

The ontology (ontology/rune.ttl) is the one definition of every term. A
labeled class, property, or concept gets one generated page under
docs/specs/glossary/, and a Markdown file marks a term by a reference link
to that page: `*[analysis tool][ANALYSISTOOL]*` at first use, then
`[analysis tool][ANALYSISTOOL]` at every later use, with `[ANALYSISTOOL]: <relative path>` at
the end of the file. The rune CLI renders the same bytes; this module is the
fallback for a machine without it.
"""
import collections
import os
import pathlib
import re

NS = "https://runedeck.ai/ns#"
ONTOLOGY = pathlib.Path("ontology") / "rune.ttl"
GLOSSARY = pathlib.Path("docs") / "specs" / "glossary"
SINGLE_FILE = pathlib.Path("docs") / "specs" / "glossary.md"
DRAFT_TEXT = "Draft term. The fixer added it and nobody has defined it yet. Archive refuses a change that links to it."
PAGE_FOOTER = "Generated from `ontology/rune.ttl`. Edit the ontology, not this page."
INDEX_HEADER = "# Glossary\n\nGenerated from `ontology/rune.ttl`. Edit the ontology, not these pages.\n\n"
DRAFT_SECTION = "#################################################################\n# Draft terms\n#################################################################\n"

# Directories no term check or fixer enters: version control, duplicate
# trees, build output, fixtures with deliberate defects, and the pages.
SKIP_DIRS = {".git", ".jj", ".workspaces", ".worktrees", ".trash", "build", "node_modules", "target", ".provenance", ".vale", "__pycache__"}
SKIP_RELATIVE = {pathlib.Path("tests") / "fixtures", GLOSSARY}

BLOCK = re.compile(r"^rune:(\w+) a (rdfs:Class|rdf:Property|skos:Concept)\b(.*?)\s\.\s*$", re.MULTILINE | re.DOTALL)
LABEL = re.compile(r'rdfs:label "([^"]+)"')
COMMENT = re.compile(r'rdfs:comment "((?:[^"\\]|\\.)*)"')
STATUS = re.compile(r'rune:status "([^"]+)"')
IRI = re.compile(r"^iri:\s*(\S+)\s*$", re.MULTILINE)
KIND = {"rdfs:Class": "class", "rdf:Property": "property", "skos:Concept": "concept"}
PRECEDENCE = {"rdfs:Class": 0, "rdf:Property": 1, "skos:Concept": 2}

TAG = r"[A-Z][A-Z0-9-]*"
# A term definition: `[TAG]: target`, with an optional Markdown title in
# double quotes, single quotes, or parentheses. Two groups: tag and target.
DEFINITION = re.compile(r"^\[(" + TAG + r")\]:[ \t]*(\S+)(?:[ \t]+(?:\"[^\"\n]*\"|'[^'\n]*'|\([^()\n]*\)))?[ \t]*$", re.MULTILINE)
# Any definition line, titled or not, as rune's prose view skips it: any
# Markdown link label, so `[MORE INFO]: ./x.md` is a definition too.
DEFINITION_LINE = re.compile(r"^ {0,3}\[(?!\s*\])(?:\\.|[^\\\[\]])+\]:\s*\S")
# The link form: an optional emphasis star on each side of `[text][TAG]`.
REF_LINK = re.compile(r"(\*?)\[([^\]\n]+)\]\[(" + TAG + r")\](\*?)")
# The legacy form: an italic term followed by a bare tag. The italic text
# never starts with `[`, so a converted link is never matched again.
LEGACY = re.compile(r"(?<![*\w])\*([^*\[\n][^*\n]*?)\*[ \t]*\[(" + TAG + r")\]")
# A fence opens with three or more backticks or tildes indented at most
# three spaces, and a backtick fence's info string holds no backtick.
FENCE_OPEN = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
# A code span opens with a run of backticks and closes at the next run of
# the same length, so ``a `b` c`` is one span.
CODE_SPAN = re.compile(r"(?<!`)(`+)(?!`)[^\n]*?(?<!`)\1(?!`)")
# A Setext heading: a paragraph closed by a line of `=` or `-`.
SETEXT_UNDERLINE = re.compile(r"^ {0,3}(?:=+|-+)[ \t]*$")
# Lines that start another block, so they are never Setext heading text.
NOT_PARAGRAPH = re.compile(r"^ {0,3}(?:[-*+](?:[ \t]|$)|\d{1,9}[.)](?:[ \t]|$)|>|\||#)")
# A leading YAML block closed by `---` or `...`, as rune's prose view sees it.
FRONT_MATTER = re.compile(r"\A---[ \t]*\n.*?^(?:---|\.\.\.)[ \t]*$", re.MULTILINE | re.DOTALL)
SCHEME = re.compile(r"^[a-z][a-z0-9+.-]*:")

Term = collections.namedtuple("Term", "label precedence name kind comment status")
Finding = collections.namedtuple("Finding", "path line severity name message")


def kebab(label):
    """`Occam's razor` -> occams-razor, `analysis tool` -> analysis-tool."""
    return re.sub(r"[^a-z0-9]+", "-", label.lower().replace("'", "")).strip("-")


def tag_of(label):
    """The reference tag: the label in upper case with every non-letter removed."""
    return re.sub(r"[^A-Z]", "", label.upper())


def camel(text):
    """The local name of a draft term: the link text in UpperCamelCase."""
    return "".join(word[:1].upper() + word[1:] for word in re.findall(r"[A-Za-z0-9]+", text))


def read_terms(root):
    """Every labeled term in the ontology, sorted by label with Python's
    default string order, then the class before the property that shares it."""
    text = (pathlib.Path(root) / ONTOLOGY).read_text()
    found = []
    for match in BLOCK.finditer(text):
        name, kind, body = match.group(1), match.group(2), match.group(3)
        label = LABEL.search(body)
        if not label:
            continue
        comment, status = COMMENT.search(body), STATUS.search(body)
        found.append(Term(
            label.group(1), PRECEDENCE[kind], name, KIND[kind],
            comment.group(1).replace('\\"', '"') if comment else "",
            status.group(1) if status else "defined",
        ))
    return sorted(found)


class Index:
    """Lookups over the terms: by local name, by page file, and by tag.
    A property whose label collides with a class label gets -key on its
    file and -KEY on its tag, matching the single file's convention."""

    def __init__(self, terms):
        self.terms = terms
        self.by_name = {t.name: t for t in terms}
        self.file_of, self.tag_of = {}, {}
        taken_files, taken_tags = set(), set()
        for term in sorted(terms, key=lambda t: (t.precedence, t.label, t.name)):
            stem, tag = kebab(term.label), tag_of(term.label)
            while stem in taken_files:
                stem += "-key"
            while tag in taken_tags:
                tag += "-KEY"
            taken_files.add(stem)
            taken_tags.add(tag)
            self.file_of[term.name] = stem + ".md"
            self.tag_of[term.name] = tag
        self.by_file = {f: n for n, f in self.file_of.items()}
        # A tag resolves by the label rule or by the legacy rule (the local
        # name in upper case), so a migrated file keeps its tags.
        self.by_tag = {}
        for name, tag in self.tag_of.items():
            self.by_tag.setdefault(tag, name)
        for term in sorted(terms, key=lambda t: (t.precedence, t.label, t.name)):
            self.by_tag.setdefault(term.name.upper(), term.name)

    def body(self, term):
        return DRAFT_TEXT if term.status == "draft" else term.comment

    def page(self, term):
        return (
            f"---\ntitle: {term.label}\niri: {NS}{term.name}\nkind: {term.kind}\n"
            f"status: {'draft' if term.status == 'draft' else 'defined'}\n---\n\n"
            f"# {term.label}\n\n{self.body(term)}\n\n{PAGE_FOOTER}\n"
        )

    def index(self):
        lines = [f"- [{t.label}]({self.file_of[t.name]}): {self.body(t)}" for t in self.terms]
        return INDEX_HEADER + "\n".join(lines) + "\n"

    def render(self):
        """Every page and the index, by file name, exactly as written."""
        pages = {self.file_of[t.name]: self.page(t) for t in self.terms}
        pages["index.md"] = self.index()
        return pages


def load(root):
    return Index(read_terms(root))


def stale_files(root, pages):
    """Files the glossary should not hold: a page for a term the ontology no
    longer renders, and the single docs/specs/glossary.md. Reported, never
    removed: these tools write and do not delete."""
    root = pathlib.Path(root)
    found = [root / SINGLE_FILE] if (root / SINGLE_FILE).is_file() else []
    directory = root / GLOSSARY
    if directory.is_dir():
        found.extend(sorted(p for p in directory.glob("*.md") if p.name not in pages))
    return [p.relative_to(root) for p in found]


def write_pages(root, index=None):
    """Write every page and the index that differ from the render. Returns
    the number written, the number rendered, and the stale files."""
    root = pathlib.Path(root)
    index = index or load(root)
    pages = index.render()
    directory = root / GLOSSARY
    directory.mkdir(parents=True, exist_ok=True)
    written = 0
    for name, text in pages.items():
        path = directory / name
        if not path.is_file() or path.read_text() != text:
            path.write_text(text)
            written += 1
    return written, len(pages), stale_files(root, pages)


def markdown_files(root):
    """Every Markdown file under root the term tools read, sorted."""
    root = pathlib.Path(root)
    skip = {(root / rel).resolve() for rel in SKIP_RELATIVE}
    found = []
    for directory, subdirs, files in os.walk(root):
        here = pathlib.Path(directory)
        subdirs[:] = sorted(d for d in subdirs if d not in SKIP_DIRS and (here / d).resolve() not in skip)
        found.extend(here / f for f in files if f.endswith(".md"))
    return sorted(found)


def fenced_blocks(text):
    """(start, end) of every fenced code block: the opener, the body, and a
    closing line of the opener's character at least as long as the opener,
    indented at most three spaces. A fence with no closer runs to the end."""
    found, opener, offset = [], None, 0
    for line in text.split("\n"):
        body = line.rstrip("\r")
        if opener is None:
            match = FENCE_OPEN.match(body)
            if match and not (match.group(1)[0] == "`" and "`" in match.group(2)):
                opener = (match.group(1)[0], len(match.group(1)), offset)
        elif re.match(r" {0,3}" + re.escape(opener[0]) + "{" + str(opener[1]) + r",}[ \t]*$", body):
            found.append((opener[2], offset + len(body)))
            opener = None
        offset += len(line) + 1
    if opener is not None:
        found.append((opener[2], len(text)))
    return found


def blank_code(text):
    """Front matter, code fences, and code spans replaced by spaces, so
    offsets and lines hold. Rune's prose view skips the same three."""
    def blank(chunk):
        return re.sub(r"[^\n]", " ", chunk)
    text = FRONT_MATTER.sub(lambda match: blank(match.group(0)), text, count=1)
    out, last = [], 0
    for start, end in fenced_blocks(text):
        out += [text[last:start], blank(text[start:end])]
        last = end
    out.append(text[last:])
    return CODE_SPAN.sub(lambda match: blank(match.group(0)), "".join(out))


def line_of(text, offset):
    return text.count("\n", 0, offset) + 1


def heading_lines(lines):
    """Indexes of the heading lines: a `#` line, and every line of a
    paragraph that a Setext `===` or `---` underline closes. Text that
    continues a list item, a quote, or a table is not a heading."""
    found = {i for i, line in enumerate(lines) if line.lstrip().startswith("#")}
    for i, line in enumerate(lines):
        if i == 0 or not SETEXT_UNDERLINE.match(line):
            continue
        top = i - 1
        while top >= 0 and lines[top].strip() and not NOT_PARAGRAPH.match(lines[top]) and not DEFINITION_LINE.match(lines[top]):
            top -= 1
        if top == i - 1:
            continue
        if top >= 0 and lines[top].strip() and NOT_PARAGRAPH.match(lines[top]) and not lines[top].lstrip().startswith("#"):
            continue
        found.update(range(top + 1, i + 1))
    return found


def destination_end(line, start):
    """The offset after the `)` that closes the inline-link destination
    opening at start. Parentheses balance and a backslash escapes, as in
    `[record](path(foo)x)`. An unclosed destination runs to the line end."""
    depth, i = 0, start
    while i < len(line):
        if line[i] == "\\":
            i += 2
            continue
        if line[i] == "(":
            depth += 1
        elif line[i] == ")":
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    return len(line)


def prose_mask(line):
    """True for each character of a line that is not prose: a term link, a
    legacy citation, text in brackets, and an inline-link destination."""
    masked = [False] * len(line)
    for pattern in (REF_LINK, LEGACY):
        for match in pattern.finditer(line):
            masked[match.start():match.end()] = [True] * (match.end() - match.start())
    depth, i = 0, 0
    while i < len(line):
        if line[i] == "[":
            depth += 1
        elif line[i] == "]":
            depth = max(depth - 1, 0)
            if depth == 0 and line[i + 1:i + 2] == "(":
                end = destination_end(line, i + 1)
                masked[i:end] = [True] * (end - i)
                i = end
                continue
        if depth > 0:
            masked[i] = True
        i += 1
    return masked


def label_pattern(label):
    """A whole-word, case-insensitive pattern for a label and its plural:
    `s` or `es`, and `es` alone for a label that ends in s (`harnesses`).
    It matches the source text itself, so offsets hold for any letter."""
    plural = "(?:es)?" if label.lower().endswith("s") else "(?:es|s)?"
    return re.compile(r"(?<![\w-])" + re.escape(label) + plural + r"(?![\w-])", re.IGNORECASE)


def plain_occurrences(text, label):
    """(start, end) of every plain occurrence of a term label in blanked text:
    a whole word (or its plural), case-insensitive, outside a link, a legacy
    citation, brackets, and an inline-link destination, and not on a heading
    or a definition line, and not right after an emphasis star, where a
    run-in label sits.
    Every occurrence of a linked term is a link, so the validator reports
    these and the fixer links them."""
    if not label:
        return []
    pattern = label_pattern(label)
    lines = text.split("\n")
    headings = heading_lines(lines)
    found, base = [], 0
    for number, line in enumerate(lines):
        matches = list(pattern.finditer(line)) if number not in headings and not DEFINITION_LINE.match(line) else []
        if matches:
            masked = prose_mask(line)
            # A word right after an emphasis star is a run-in label such as
            # `**Change ceremony.**`, which rune's checker leaves alone too.
            found.extend(
                (base + m.start(), base + m.end())
                for m in matches
                if not any(masked[m.start():m.end()]) and not line[:m.start()].endswith("*")
            )
        base += len(line) + 1
    return found


def linked_terms(text, resolutions, index):
    """{name: tag} for every term the blanked text links by use: a
    `[text][TAG]` link whose definition resolves to a term. A definition
    alone links nothing. The tag is the term's own tag when the text uses
    it, else the tag of the first use."""
    uses = {}
    for match in REF_LINK.finditer(text):
        res = resolutions.get(match.group(3))
        if res is not None and res.name is not None:
            uses.setdefault(res.name, []).append(match.group(3))
    return {name: index.tag_of[name] if index.tag_of[name] in tags else tags[0] for name, tags in uses.items()}


def term_occurrences(text, linked, index):
    """(start, end, name, tag) of every plain occurrence of a linked term,
    sorted by position. Where two occurrences overlap, the longer one is the
    more specific term and wins, then the earlier one: `missed requirement`
    over `requirement`, `review lane` over `red review`."""
    candidates = [
        (start, end, name, tag)
        for name, tag in linked.items()
        for start, end in plain_occurrences(text, index.by_name[name].label)
    ]
    chosen = []
    for cand in sorted(candidates, key=lambda c: (c[0] - c[1], c[0])):
        if all(cand[1] <= kept[0] or cand[0] >= kept[1] for kept in chosen):
            chosen.append(cand)
    return sorted(chosen)


def page_path(root, path, target):
    """The glossary page a definition target names, or None when the target
    is not a relative path into docs/specs/glossary/."""
    if SCHEME.match(target) or target.startswith("#"):
        return None
    glossary = (pathlib.Path(root) / GLOSSARY).resolve()
    resolved = (pathlib.Path(path).parent / target).resolve()
    if resolved.parent != glossary or resolved.name == "index.md":
        return None
    return resolved


def iri_of(page):
    """The local name a page's `iri:` names, or None."""
    try:
        match = IRI.search(page.read_text())
    except OSError:
        return None
    if not match or not match.group(1).startswith(NS):
        return None
    return match.group(1)[len(NS):]


def relative_link(path, root, file_name):
    """The definition target for a page, relative to the file that holds it."""
    target = pathlib.Path(root) / GLOSSARY / file_name
    return os.path.relpath(target, pathlib.Path(path).parent)


Resolution = collections.namedtuple("Resolution", "form name page")
# form: "link" (a relative path into the glossary), "legacy" (an ontology
# IRI), or None (not a term link). name: the local name the link resolves
# to, or None when it resolves to no term. page: the page path for a link.


def resolve(root, path, tag, target, index):
    """What a reference definition stands for, from its target and its tag.
    A page that is not written yet resolves by its file name first, so a
    link that a migration pointed at a missing page keeps its term."""
    if target.startswith(NS):
        name = target[len(NS):]
        return Resolution("legacy", name if name in index.by_name else None, None)
    page = page_path(root, path, target)
    if page is None:
        return Resolution(None, None, None)
    if page.is_file():
        name = iri_of(page)
        return Resolution("link", name if name in index.by_name else None, page)
    return Resolution("link", index.by_file.get(page.name) or index.by_tag.get(tag), page)
