#!/usr/bin/env python3
"""Render a run_loop result, partial or final, as one self-contained HTML page.

Usage, from the skill directory:

    python3 -m scripts.generate_report results.json -o report.html
    cat results.json | python3 -m scripts.generate_report - --skill-name my-skill
"""

import argparse
import html
import json
import sys
from pathlib import Path

GOOD_PERCENT = 80
FAIR_PERCENT = 50
QUERY_HEADER_WIDTH = 48


def esc(value: object) -> str:
    """Escape any data value for safe placement in markup."""
    return html.escape("" if value is None else str(value), quote=True)


def normalize_entry(entry: dict) -> dict:
    """Return a history entry with the ``train_``/``test_`` keys filled in.

    Older entries carry ``passed``, ``total`` and ``results`` instead of the
    ``train_`` keys; those are accepted too.
    """
    train_results = entry.get("train_results")
    if train_results is None:
        train_results = entry.get("results") or []
    train_passed = entry.get("train_passed", entry.get("passed"))
    train_total = entry.get("train_total", entry.get("total"))
    if train_passed is None:
        train_passed = sum(1 for item in train_results if item.get("pass"))
    if train_total is None:
        train_total = len(train_results)

    test_results = entry.get("test_results")
    test_passed = entry.get("test_passed")
    test_total = entry.get("test_total")
    if test_results is not None:
        if test_passed is None:
            test_passed = sum(1 for item in test_results if item.get("pass"))
        if test_total is None:
            test_total = len(test_results)

    return {
        "iteration": entry.get("iteration"),
        "description": entry.get("description", ""),
        "train_passed": train_passed,
        "train_total": train_total,
        "train_results": list(train_results),
        "test_passed": test_passed,
        "test_total": test_total,
        "test_results": None if test_results is None else list(test_results),
    }


def best_iteration_index(history: list[dict]) -> int | None:
    """Index of the best entry: most passed test queries when a test set
    exists, otherwise most passed train queries; ties go to the earliest."""
    entries = [normalize_entry(entry) for entry in history]
    if not entries:
        return None
    use_test = any(entry["test_total"] is not None for entry in entries)
    best_index: int | None = None
    best_score = -1
    for index, entry in enumerate(entries):
        score = entry["test_passed"] if use_test else entry["train_passed"]
        if score is None:
            score = -1
        if score > best_score:
            best_index, best_score = index, score
    return best_index


def run_score(results: list[dict]) -> tuple[int, int]:
    """Correct runs over total runs for a list of per-query results."""
    correct = 0
    total = 0
    for item in results:
        runs = int(item.get("runs") or 0)
        triggers = int(item.get("triggers") or 0)
        correct += triggers if item.get("should_trigger") else runs - triggers
        total += runs
    return correct, total


def grade(correct: int, total: int) -> str:
    if total <= 0:
        return "none"
    percent = 100 * correct / total
    if percent >= GOOD_PERCENT:
        return "good"
    if percent >= FAIR_PERCENT:
        return "fair"
    return "poor"


def _score_cell(results: list[dict] | None) -> str:
    if not results:
        return '<td class="score none">n/a</td>'
    correct, total = run_score(results)
    label = f"{correct}/{total}"
    if total:
        label += f" <small>({100 * correct / total:.0f}%)</small>"
    return f'<td class="score {grade(correct, total)}">{label}</td>'


def _query_columns(entries: list[dict]) -> list[dict]:
    """Query columns in a stable order: train queries first, then test."""
    columns: list[dict] = []
    seen: set[tuple[str, str]] = set()
    for split in ("train", "test"):
        for entry in entries:
            for item in entry[f"{split}_results"] or []:
                key = (split, str(item.get("query")))
                if key in seen:
                    continue
                seen.add(key)
                columns.append(
                    {
                        "split": split,
                        "query": str(item.get("query")),
                        "should_trigger": bool(item.get("should_trigger")),
                    }
                )
    return columns


def _query_header(column: dict) -> str:
    query = column["query"]
    short = query if len(query) <= QUERY_HEADER_WIDTH else query[: QUERY_HEADER_WIDTH - 1] + "…"
    kind = "should trigger" if column["should_trigger"] else "should NOT trigger"
    kind_class = "want-yes" if column["should_trigger"] else "want-no"
    return (
        f'<th class="query {esc(column["split"])} {kind_class}" title="{esc(query)}">'
        f'<span class="tag">{esc(column["split"])}</span> '
        f'<span class="tag">{esc(kind)}</span>'
        f'<div class="qtext">{esc(short)}</div></th>'
    )


def _query_cell(entry: dict, column: dict) -> str:
    lookup = {
        str(item.get("query")): item for item in entry[f"{column['split']}_results"] or []
    }
    item = lookup.get(column["query"])
    if item is None:
        return '<td class="cell none">–</td>'
    status = "pass" if item.get("pass") else "fail"
    mark = "✓" if item.get("pass") else "✗"
    return (
        f'<td class="cell {status}">{mark} '
        f'{esc(item.get("triggers"))}/{esc(item.get("runs"))}</td>'
    )


_STYLE = """
:root { --ink: #1f2430; --muted: #6b7280; --line: #e3e6ec; --bg: #f7f8fa;
        --good: #d9f2e3; --good-ink: #146c43; --fair: #fff1cc; --fair-ink: #8a6100;
        --poor: #fbe0e0; --poor-ink: #a32d2d; --best: #eef3ff; --accent: #2f55d4; }
* { box-sizing: border-box; }
body { margin: 0; padding: 2rem; background: var(--bg); color: var(--ink);
       font: 15px/1.5 -apple-system, "Segoe UI", Helvetica, Arial, sans-serif; }
h1 { margin: 0 0 .25rem; font-size: 1.6rem; }
h2 { margin: 2rem 0 .75rem; font-size: 1.15rem; }
.note { color: var(--muted); max-width: 70rem; }
.card { background: #fff; border: 1px solid var(--line); border-radius: 10px;
        padding: 1.25rem 1.5rem; margin-top: 1.25rem; }
dl { display: grid; grid-template-columns: max-content 1fr; gap: .5rem 1.5rem; margin: 0; }
dt { color: var(--muted); font-weight: 600; }
dd { margin: 0; overflow-wrap: anywhere; }
.scorechip { display: inline-block; padding: .1rem .55rem; border-radius: 999px; font-weight: 600; }
.good { background: var(--good); color: var(--good-ink); }
.fair { background: var(--fair); color: var(--fair-ink); }
.poor { background: var(--poor); color: var(--poor-ink); }
.none { color: var(--muted); }
.tablewrap { overflow-x: auto; }
table { border-collapse: collapse; background: #fff; min-width: 100%; }
th, td { border: 1px solid var(--line); padding: .45rem .6rem; vertical-align: top; text-align: left; }
thead th { background: #f0f2f6; position: sticky; top: 0; }
th.query { min-width: 11rem; font-weight: 500; }
th.test { background: #e8edf8; }
.tag { display: inline-block; font-size: .7rem; text-transform: uppercase; letter-spacing: .04em;
       color: var(--muted); border: 1px solid var(--line); border-radius: 4px; padding: 0 .3rem; }
th.want-no .tag:last-of-type { color: var(--poor-ink); }
th.want-yes .tag:last-of-type { color: var(--good-ink); }
.qtext { margin-top: .25rem; font-size: .85rem; }
td.cell { white-space: nowrap; text-align: center; }
td.pass { background: var(--good); color: var(--good-ink); }
td.fail { background: var(--poor); color: var(--poor-ink); }
td.score { white-space: nowrap; font-weight: 600; }
td.desc { min-width: 24rem; max-width: 40rem; font-size: .9rem; }
tr.best td { box-shadow: inset 0 0 0 1px var(--accent); }
tr.best td.iter { background: var(--best); font-weight: 700; }
.best-mark { color: var(--accent); font-size: .8rem; margin-left: .3rem; }
"""


def generate_html(data: dict, auto_refresh: bool = False, skill_name: str = "") -> str:
    """Build the report page from a run_loop result."""
    entries = [normalize_entry(entry) for entry in data.get("history") or []]
    best_index = best_iteration_index(data.get("history") or [])
    columns = _query_columns(entries)
    has_test = any(entry["test_total"] is not None for entry in entries)
    test_size = data.get("test_size")
    deciding_split = "test" if has_test or (test_size or 0) > 0 else "train"

    title = "Trigger optimization report"
    if skill_name:
        title += f": {skill_name}"
    refresh = '<meta http-equiv="refresh" content="5">\n' if auto_refresh else ""

    best_score = data.get("best_score")
    best_score_text = esc(best_score) if best_score is not None else "n/a"

    summary_rows = [
        ("Original description", esc(data.get("original_description"))),
        ("Best description", esc(data.get("best_description"))),
        (f"Best score ({deciding_split})", best_score_text),
        ("Iterations run", esc(data.get("iterations_run"))),
        ("Train / test queries", f"{esc(data.get('train_size'))} / {esc(test_size)}"),
    ]
    exit_reason = data.get("exit_reason")
    if exit_reason is not None:
        summary_rows.append(("Exit reason", esc(exit_reason)))
    holdout = data.get("holdout")
    if holdout is not None:
        summary_rows.append(("Holdout fraction", esc(holdout)))
    summary_html = "".join(f"<dt>{label}</dt><dd>{value}</dd>" for label, value in summary_rows)

    header_cells = [
        "<th>Iteration</th>",
        "<th>Train score<br><small>correct runs / runs</small></th>",
        "<th>Test score<br><small>correct runs / runs</small></th>",
        "<th>Description</th>",
    ] + [_query_header(column) for column in columns]

    body_rows = []
    for index, entry in enumerate(entries):
        is_best = index == best_index
        row_class = "iteration best" if is_best else "iteration"
        iteration_label = esc(entry["iteration"] if entry["iteration"] is not None else index + 1)
        if is_best:
            iteration_label += '<span class="best-mark">best</span>'
        cells = [
            f'<td class="iter">{iteration_label}</td>',
            _score_cell(entry["train_results"]),
            _score_cell(entry["test_results"]),
            f'<td class="desc">{esc(entry["description"])}</td>',
        ] + [_query_cell(entry, column) for column in columns]
        body_rows.append(f'<tr class="{row_class}">{"".join(cells)}</tr>')

    if body_rows:
        table_html = (
            '<div class="tablewrap"><table>'
            f"<thead><tr>{''.join(header_cells)}</tr></thead>"
            f"<tbody>{''.join(body_rows)}</tbody></table></div>"
        )
    else:
        table_html = '<p class="note">No iteration has finished yet.</p>'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
{refresh}<title>{esc(title)}</title>
<style>{_STYLE}</style>
</head>
<body>
<h1>{esc(title)}</h1>
<p class="note">Each row is one iteration of the optimization loop. Scores count
correct runs over all runs: a should-trigger query is correct when the skill was
picked, a should-not-trigger query when it was not. Query cells show pass or fail
and picks over runs. Column tags mark train versus test queries and whether the
query should trigger. Green is {GOOD_PERCENT}% or better, amber is {FAIR_PERCENT}%
or better, red is below that. The outlined row is the best iteration, chosen by
test score when a test set exists and by train score otherwise.</p>
<div class="card"><dl>{summary_html}</dl></div>
<h2>Iterations</h2>
{table_html}
</body>
</html>
"""


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Render a run_loop result as HTML")
    parser.add_argument("input", help="result JSON path, or '-' for standard input")
    parser.add_argument("-o", "--output", type=Path, default=None, help="output file")
    parser.add_argument("--skill-name", default="")
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    if args.input == "-":
        data = json.load(sys.stdin)
    else:
        data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    page = generate_html(data, skill_name=args.skill_name)
    if args.output is None:
        sys.stdout.write(page)
    else:
        args.output.write_text(page, encoding="utf-8")


if __name__ == "__main__":
    main()
