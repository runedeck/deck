#!/bin/sh
# Render the report of the stored run into the current directory.
# usage: sh render-stored-run.sh [--labels]
# It copies the stored iteration to ./iteration, removes the old aggregate and
# report from the copy, aggregates the copy, builds the report, and writes the
# page as a browser renders it to ./rendered.html. With --labels it first adds
# the card fields to the frozen manifest of the copy. It never writes to the
# stored run. It prints each command before it runs.
set -eu

here=$(cd "$(dirname "$0")" && pwd)
skill=$(cd "$here/../../../runes/core/skills/BenchArtifact" && pwd)
store="${ROOT_BENCHMARK:-$HOME/Data/Benchmarks}/runedeck/BrowserbaseToolkit-deck/iteration-2"
browser="${BROWSER_BINARY:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"

echo '+ cp -R <stored run> iteration'
cp -R "$store" iteration
rm -f iteration/benchmark.json iteration/benchmark.md iteration/report.html
if [ "${1:-}" = --labels ]; then
    echo '+ python3 label-manifest.py iteration/manifest.json card-labels.json'
    python3 "$here/label-manifest.py" iteration/manifest.json "$here/card-labels.json"
fi
echo '+ python3 -m scripts.aggregate_benchmark iteration'
PYTHONPATH="$skill" python3 -m scripts.aggregate_benchmark iteration
echo '+ python3 -m scripts.build_report iteration/benchmark.json'
PYTHONPATH="$skill" python3 -m scripts.build_report iteration/benchmark.json
echo '+ <browser> --headless --dump-dom iteration/report.html > rendered.html'
"$browser" --headless --disable-gpu --no-first-run --user-data-dir="$PWD/browser-profile" \
    --dump-dom "file://$PWD/iteration/report.html" > rendered.html 2> browser.log
