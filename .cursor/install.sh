#!/usr/bin/env bash
# Provision the Rune Deck validation toolchain for a Cloud Agent VM.
#
# Mirrors .github/workflows/quality.yaml so a local commit sees the same
# gates as CI: pinned single binaries verified against their release
# digests, the Python-based hooks, the openspec CLI behind a docs/ shadow
# root, and rune itself. Idempotent: every install guards on presence, so
# re-runs converge cheaply without rewriting existing state. Targets an
# x86_64 Debian/Ubuntu base image with passwordless sudo.
set -euo pipefail

BIN=/usr/local/bin
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Pinned upstream releases, matching quality.yaml. Each digest is the
# sha256 of the linked asset, so verification attests provenance.
GITLEAKS_VERSION=8.30.1
GITLEAKS_SHA256=551f6fc83ea457d62a0d98237cbad105af8d557003051f41f3e7ca7b3f2470eb
OPENSPEC_VERSION=1.10.0

log() { printf '==> %s\n' "$*"; }

export PATH="$HOME/.local/bin:/usr/local/cargo/bin:$BIN:$PATH"

if [ "$(uname -m)" != "x86_64" ]; then
    log "warning: this script pins x86_64 release assets; detected $(uname -m)"
fi

# Download, digest-verify, and install one release binary into $BIN. The
# archive is unpacked in a scratch directory so it can never write into the
# checkout. Mirrors the fetch() helper in quality.yaml.
fetch() { # url  sha256  binary_name
    local url=$1 sha=$2 name=$3 file scratch bin
    command -v "$name" >/dev/null 2>&1 && return 0
    log "installing $name"
    file=${url##*/}
    scratch=$(mktemp -d)
    curl -fsSL -o "$scratch/$file" "$url"
    (cd "$scratch" && echo "$sha  $file" | sha256sum --check)
    case "$file" in
        *.tar.gz)
            tar -xzf "$scratch/$file" -C "$scratch"
            bin=$(find "$scratch" -maxdepth 3 -name "$name" -type f | head -1)
            ;;
        *) bin="$scratch/$file" ;;
    esac
    sudo install -m 755 "$bin" "$BIN/$name"
    rm -rf "$scratch"
}

# ---------------------------------------------------------------------------
# System package: shellcheck powers the pre-commit shell gate.
# ---------------------------------------------------------------------------
if ! command -v shellcheck >/dev/null 2>&1; then
    log "installing shellcheck via apt"
    sudo apt-get update -qq
    sudo apt-get install -y -qq shellcheck
fi

# ---------------------------------------------------------------------------
# uv drives the Python-based tools. quality.yaml uses `pipx install prek
# ruff semgrep`; copier is added for template updates (see INSTALL.md).
# Each shim is symlinked onto the global PATH so git-invoked hooks resolve
# it in non-login shells.
# ---------------------------------------------------------------------------
if ! command -v uv >/dev/null 2>&1; then
    log "installing uv"
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi

for tool in prek ruff semgrep copier; do
    log "uv tool install $tool"
    uv tool install "$tool"
done

for shim in uv uvx prek ruff semgrep pysemgrep copier; do
    [ -e "$HOME/.local/bin/$shim" ] && sudo ln -sf "$HOME/.local/bin/$shim" "$BIN/$shim"
done

# ---------------------------------------------------------------------------
# Pinned single-binary gates, digest-verified before install.
# ---------------------------------------------------------------------------
fetch "https://github.com/gitleaks/gitleaks/releases/download/v${GITLEAKS_VERSION}/gitleaks_${GITLEAKS_VERSION}_linux_x64.tar.gz" \
    "$GITLEAKS_SHA256" gitleaks
fetch https://github.com/rvben/rumdl/releases/download/v0.2.60/rumdl-v0.2.60-x86_64-unknown-linux-gnu.tar.gz \
    84fc96856d21203b6482b7284aff5b539b7329a5cc078d7a94c55ae40d88752f rumdl
fetch https://github.com/crate-ci/typos/releases/download/v1.49.0/typos-v1.49.0-x86_64-unknown-linux-musl.tar.gz \
    48bd2d58e02ce713b8c0f1aa239e68ee4f7d8c551013135806e6aed3938d9e10 typos
fetch https://github.com/errata-ai/vale/releases/download/v3.18.0/vale_3.18.0_Linux_64-bit.tar.gz \
    a6f71a75a12fe689345b754f2412b90367fe33648abb7d200fa19eaadc2dbf6d vale
fetch https://github.com/lycheeverse/lychee/releases/download/lychee-v0.24.2/lychee-x86_64-unknown-linux-gnu.tar.gz \
    1f4e0ef7f6554a6ed33dd7ac144fb2e1bbed98598e7af973042fc5cd43951c9a lychee
fetch https://github.com/zizmorcore/zizmor/releases/download/v1.29.0/zizmor-x86_64-unknown-linux-gnu.tar.gz \
    dd96df044a6e8538d5f423790f453bdd03d49e5b2bcc38214acc41a2f1297839 zizmor
fetch https://github.com/rhysd/actionlint/releases/download/v1.7.12/actionlint_1.7.12_linux_amd64.tar.gz \
    8aca8db96f1b94770f1b0d72b6dddcb1ebb8123cb3712530b08cc387b349a3d8 actionlint
fetch https://github.com/rudof-project/rudof/releases/download/0.3.12/rudof_0.3.12_x86_64_linux_gnu \
    a9d6d8dc101b6896a43150d18e2b2c070f34ffbf747f376977e1eb6c892f9a92 rudof

# ---------------------------------------------------------------------------
# openspec validates docs/changes and docs/specs. The CLI expects an
# openspec/ root, so — as in quality.yaml — install it globally and front
# it with a wrapper that runs from a directory whose openspec/ symlink
# points at this repository's docs/.
# ---------------------------------------------------------------------------
if ! command -v openspec >/dev/null 2>&1; then
    log "installing openspec $OPENSPEC_VERSION"
    sudo env "PATH=$PATH" npm install -g --prefix /usr/local "@fission-ai/openspec@${OPENSPEC_VERSION}"
    sudo unlink "$BIN/openspec" 2>/dev/null || true
    mkdir -p "$HOME/.openspec-root"
    ln -sfn "$REPO_ROOT/docs" "$HOME/.openspec-root/openspec"
    printf '#!/bin/sh\ncd "%s" && exec /usr/local/lib/node_modules/@fission-ai/openspec/bin/openspec.js "$@"\n' \
        "$HOME/.openspec-root" | sudo tee "$BIN/openspec" >/dev/null
    sudo chmod +x "$BIN/openspec"
fi

# ---------------------------------------------------------------------------
# rune is the deck's own tool (`rune validate`). It is a Rust edition-2024
# crate, so ensure a recent stable toolchain, then build from source.
# ---------------------------------------------------------------------------
if ! command -v rune >/dev/null 2>&1; then
    log "installing rune from source"
    rustup toolchain install stable --profile minimal >/dev/null 2>&1 || true
    rustup default stable
    rm -rf /tmp/rune-cli-src
    git clone --depth 1 https://github.com/runedeck/cli /tmp/rune-cli-src
    cargo install --path /tmp/rune-cli-src --locked
fi

log "toolchain ready"

# ---------------------------------------------------------------------------
# Wire the repository's git hooks (git core.hooksPath + optional jj alias).
# ---------------------------------------------------------------------------
make -C "$REPO_ROOT" install
