"""The term model the fallback scripts share: check-terms, generate-glossary,
and fix-terms import it, so the three never disagree about a page name, a
tag, or a byte of a rendered page.

The ontology (ontology/rune.ttl) is the one definition of every term. A
labeled class, property, or concept gets one generated page under
docs/specs/glossary/, and a Markdown file marks a term by a reference link
to that page: `*[analysis tool][ANALYSISTOOL]*` at first use, then
`[analysis tool][ANALYSISTOOL]`, with `[ANALYSISTOOL]: <relative path>` at
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
DEFINITION = re.compile(r"^\[(" + TAG + r")\]:[ \t]*(\S+)[ \t]*$", re.MULTILINE)
# The link form: an optional emphasis star on each side of `[text][TAG]`.
REF_LINK = re.compile(r"(\*?)\[([^\]\n]+)\]\[(" + TAG + r")\](\*?)")
# The legacy form: an italic term followed by a bare tag. The italic text
# never starts with `[`, so a converted link is never matched again.
LEGACY = re.compile(r"(?<![*\w])\*([^*\[\n][^*\n]*?)\*[ \t]*\[(" + TAG + r")\]")
CODE_FENCE = re.compile(r"^(`{3,}|~{3,}).*?^\1[ \t]*$", re.MULTILINE | re.DOTALL)
CODE_SPAN = re.compile(r"`[^`\n]*`")
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


def blank_code(text):
    """Code fences and spans replaced by spaces, so offsets and lines hold."""
    def blank(match):
        return re.sub(r"[^\n]", " ", match.group(0))
    return CODE_SPAN.sub(blank, CODE_FENCE.sub(blank, text))


def line_of(text, offset):
    return text.count("\n", 0, offset) + 1


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
    """What a reference definition stands for, from its target and its tag."""
    if target.startswith(NS):
        name = target[len(NS):]
        return Resolution("legacy", name if name in index.by_name else None, None)
    page = page_path(root, path, target)
    if page is None:
        return Resolution(None, None, None)
    if page.is_file():
        name = iri_of(page)
        return Resolution("link", name if name in index.by_name else None, page)
    return Resolution("link", index.by_tag.get(tag), page)
