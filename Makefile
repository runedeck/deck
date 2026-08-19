.PHONY: help install validate worktree

help:
	@echo "  make install    activate hooks (git + jj)"
	@echo "  make validate   run commit-stage checks"
	@echo "  make worktree   create an agent worktree: make worktree BRANCH=change/x IDENTITY=<model-id>"

install:
	git config core.hooksPath .githooks
	chmod +x .githooks/* scripts/* 2>/dev/null || true
	@if [ -d .jj ] && command -v jj >/dev/null 2>&1; then \
	    jj config set --repo aliases.push "[\"util\",\"exec\",\"--\",\"bash\",\"$$(git rev-parse --show-toplevel)/.githooks/jj-push\"]"; \
	    echo "jj detected: 'jj push' runs the pre-push checks, then 'jj git push'"; \
	elif [ -d .jj ]; then \
	    echo "warn: .jj/ present but jj not on PATH — 'jj push' checks NOT wired"; \
	fi

validate:
	@bash .githooks/pre-commit --all-files

# Create a worktree whose commits carry a listed model identity, with no
# per-command env exports. The identity must exist in authors.yaml.
worktree:
	@[ -n "$(BRANCH)" ] && [ -n "$(IDENTITY)" ] \
	    || { echo "usage: make worktree BRANCH=change/x IDENTITY=<model-id>"; exit 2; }
	@identity=$$(grep -E '^    - .+ \($(IDENTITY)\) <.+>$$' authors.yaml | sed 's/^    - //'); \
	[ -n "$$identity" ] || { echo "identity '$(IDENTITY)' is not in authors.yaml"; exit 1; }; \
	name=$$(printf '%s' "$(BRANCH)" | tr '/' '-'); \
	git worktree add ".worktrees/$$name" -b "$(BRANCH)"; \
	author=$${identity% <*}; \
	address=$${identity##*<}; address=$${address%>}; \
	git -C ".worktrees/$$name" config user.name "$$author"; \
	git -C ".worktrees/$$name" config user.email "$$address"; \
	echo "worktree .worktrees/$$name on $(BRANCH) authors as $$identity"
