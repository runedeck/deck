"""Print the case cards of a rendered benchmark report as plain text.

usage: report-cards.py <rendered.html> [--details <card number>]

The input is the page after its script ran, as a browser serializes it. For
each card the script prints the title, the quoted prompt, the explanation,
and the grid: one line for each row, one cell for each model, each label
with the color of its cell. With `--details` it prints the check details of
one card instead.
"""
import sys
from html.parser import HTMLParser
from pathlib import Path

COLORS = {"b-ok": "green", "b-fail": "red", "b-neutral": "grey"}
VOID = {"br", "img", "input", "meta", "link", "hr"}


class Cards(HTMLParser):
    def __init__(self):
        super().__init__()
        self.cards = []
        self.stack = []

    def handle_starttag(self, tag, attrs):
        if tag in VOID:
            return
        classes = (dict(attrs).get("class") or "").split()
        self.stack.append((tag, classes))
        if tag == "article" and "case-card" in classes:
            self.cards.append({"title": "", "prompt": "", "why": "", "head": [], "rows": [], "details": []})
            return
        if not self.inside():
            return
        card = self.cards[-1]
        if tag == "tr" and not self.under("thead"):
            card["rows"].append([])
        elif tag == "td" and card["rows"]:
            card["rows"][-1].append([])
        elif tag == "th":
            card["head"].append("")
        elif tag in ("li",) or (tag == "div" and "run-head" in classes):
            card["details"].append("  " if tag == "li" else "")

    def handle_endtag(self, tag):
        while self.stack:
            if self.stack.pop()[0] == tag:
                break

    def inside(self):
        return any(tag == "article" and "case-card" in classes for tag, classes in self.stack)

    def under(self, name):
        return any(tag == name for tag, _ in self.stack)

    def handle_data(self, data):
        if not self.inside() or not data.strip():
            return
        card = self.cards[-1]
        tag, classes = self.stack[-1]
        if self.under("details"):
            if card["details"] and not self.under("summary"):
                card["details"][-1] += data
        elif tag == "h3":
            card["title"] += data
        elif tag == "blockquote":
            card["prompt"] += data
        elif tag == "p" and "case-why" in classes:
            card["why"] += data
        elif tag == "th":
            card["head"][-1] += data
        elif tag == "td" and "case-arm" in classes:
            card["rows"][-1][-1].append(data)
        elif tag == "span" and self.under("td"):
            color = next((COLORS[name] for name in classes if name in COLORS), "no color")
            card["rows"][-1][-1].append(f"{data} ({color})")


def main(argv: list[str]) -> int:
    parser = Cards()
    parser.feed(Path(argv[1]).read_text(encoding="utf-8"))
    if len(argv) > 2 and argv[2] == "--details":
        card = parser.cards[int(argv[3]) - 1]
        print(f"check details of card {argv[3]}: {card['title']}")
        print("\n".join(card["details"]))
        return 0
    print(f"cards: {len(parser.cards)}")
    for number, card in enumerate(parser.cards, start=1):
        print(f"card {number}: {card['title']}")
        print(f"  prompt: {card['prompt'] or '(none)'}")
        print(f"  why: {card['why'] or '(none)'}")
        print("  models: " + " | ".join(name for name in card["head"] if name))
        for row in card["rows"]:
            cells = [", ".join(cell) for cell in row]
            print("  " + " | ".join(cells))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
