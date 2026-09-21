"""Write the proof page: one self-contained HTML file that plays each cast
through the html-tools cast player, with a scene list read from the driver's
`# Scenario:` lines. The page is the handover to the owner.

Usage:
  python3 proof-page.py --title "Pinned Signers" --lede "..." \
      --player vendor/html-tools/runtime/cast-player.js \
      --cast trusted-key-anchor=docs/proofs/trusted-key-anchor/proof.cast \
      --caption trusted-key-anchor="what the proof shows" \
      --meta trusted-key-anchor="skeleton 079fa98c" \
      --out docs/proofs/index.html

--cast, --caption, and --meta repeat, keyed by the proof name. --meta may
repeat for one name. The player file is inlined, so the page needs no network.
"""
import argparse
import html
import json
import pathlib
import re

STYLE = """
:root{--ground:#F3F5F7;--panel:#FFFFFF;--ink:#1B2430;--muted:#5C6B7A;--line:#D5DCE3;--accent:#0F7B8A;--code:#EAF0F3}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--ground:#0F151B;--panel:#161E26;--ink:#E6ECF1;--muted:#98A6B3;--line:#2A3641;--accent:#4FC1CF;--code:#1C2630}}
:root[data-theme="dark"]{--ground:#0F151B;--panel:#161E26;--ink:#E6ECF1;--muted:#98A6B3;--line:#2A3641;--accent:#4FC1CF;--code:#1C2630}
body{background:var(--ground);color:var(--ink);font-family:system-ui,sans-serif;font-size:15px;line-height:1.5;margin:0;padding-block:32px 64px;padding-inline:16px}
main{max-width:880px;margin:0 auto;display:grid;gap:40px}
h1,h2{font-weight:600;text-wrap:balance;margin:0}
h1{font-size:2.2rem;line-height:1.1}
h2{font-size:1.45rem}
.lede{color:var(--muted);max-width:62ch;margin:8px 0 0}
.eyebrow{font-family:ui-monospace,monospace;font-size:.75rem;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
code,.mono{font-family:ui-monospace,monospace;font-size:.86em}
code{background:var(--code);padding:1px 5px;border-radius:3px}
figure{margin:0;background:var(--panel);border:1px solid var(--line);border-radius:6px;overflow:hidden}
.cast pre{max-height:60vh}
figcaption{padding:14px 16px 16px;display:grid;gap:8px}
figcaption p{margin:0}
.scenes{margin:0;padding-left:18px;color:var(--muted);font-size:.9rem;columns:2;column-gap:24px}
@media (max-width:560px){.scenes{columns:1}}
.meta{display:flex;flex-wrap:wrap;gap:8px 18px;color:var(--muted);font-size:.85rem}
"""

SCENE = re.compile(r"# Scenario: (.*?)(?:\x1b|\r|$)")


def scenes(cast_text):
    """Scene titles in playback order, from the driver's comment lines."""
    titles = []
    for line in cast_text.splitlines()[1:]:
        _, kind, data = json.loads(line)
        found = SCENE.search(data) if kind == "o" else None
        if found:
            titles.append(found.group(1))
    return titles


def keyed(pairs):
    out = {}
    for pair in pairs or []:
        name, _, value = pair.partition("=")
        out.setdefault(name, []).append(value)
    return out


def section(name, cast_text, caption, meta):
    items = "".join(f"<li>{html.escape(t)}</li>" for t in scenes(cast_text))
    spans = "".join(f'<span class="mono">{html.escape(m)}</span>' for m in meta)
    safe = cast_text.replace("</script", "<\\/script")
    return (
        f"<section>\n<h2>{html.escape(name)}</h2>\n<figure>\n"
        f'<div id="cast-{name}"></div>\n'
        f'<script type="text/plain" id="text-{name}">{safe}</script>\n'
        f"<figcaption>\n<p>{html.escape(caption)}</p>\n"
        f'<div class="meta">{spans}</div>\n<ol class="scenes">{items}</ol>\n'
        f"</figcaption>\n</figure>\n</section>\n"
    )


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--title", required=True)
    ap.add_argument("--lede", default="")
    ap.add_argument("--eyebrow", default="")
    ap.add_argument("--player", required=True, type=pathlib.Path, help="html-tools runtime/cast-player.js")
    ap.add_argument("--cast", action="append", required=True, help="name=path/to/proof.cast")
    ap.add_argument("--caption", action="append", help="name=one sentence on what the proof shows")
    ap.add_argument("--meta", action="append", help="name=short fact (repeatable)")
    ap.add_argument("--out", required=True, type=pathlib.Path)
    args = ap.parse_args()

    casts = keyed(args.cast)
    captions = keyed(args.caption)
    metas = keyed(args.meta)
    body = "".join(
        section(name, pathlib.Path(paths[0]).read_text(), captions.get(name, [""])[0], metas.get(name, []))
        for name, paths in casts.items()
    )
    names = json.dumps(list(casts))
    page = (
        f"<title>{html.escape(args.title)}</title>\n<style>{STYLE}</style>\n<main>\n<header>\n"
        f'<div class="eyebrow">{html.escape(args.eyebrow)}</div>\n<h1>{html.escape(args.title)}</h1>\n'
        f'<p class="lede">{html.escape(args.lede)}</p>\n</header>\n{body}</main>\n'
        f"<script>{args.player.read_text()}</script>\n"
        f"<script>for (const name of {names}) CastPlayer.attach(document.getElementById('cast-' + name), "
        f"document.getElementById('text-' + name).textContent);</script>\n"
    )
    args.out.write_text(page)
    print(f"{args.out} ({len(casts)} casts)")


if __name__ == "__main__":
    main()
