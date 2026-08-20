.PHONY: help install validate validate-schemas worktree

help:
	@echo "  make install    activate hooks (git + jj)"
	@echo "  make validate   run commit-stage checks"
	@echo "  make validate-schemas   compare Stable shell schemas"
	@echo "  make worktree   create an agent worktree: make worktree BRANCH=change/x IDENTITY=<model-id> [HARNESS=<harness>]"

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

validate-schemas:
	@cmp runes/core/skills/.mdschema runes/meta/skills/.mdschema
	@if [ -f ../cli/templates/init/skills/.mdschema ]; then \
	    cmp runes/core/skills/.mdschema ../cli/templates/init/skills/.mdschema; \
	fi

# Create a worktree whose commits carry a listed model identity.
# HARNESS selects one identity when a model ID has multiple harness entries.
worktree:
	@[ -n "$(BRANCH)" ] && [ -n "$(IDENTITY)" ] \
	    || { echo "usage: make worktree BRANCH=change/x IDENTITY=<model-id> [HARNESS=<harness>]"; exit 2; }
	@set -e; \
	identities=$$(awk -v model='$(IDENTITY)' -v harness='$(HARNESS)' '\
	    /^[^ #]/ { in_authors = ($$0 == "authors:") } \
	    in_authors && /^    - / { \
	        identity = $$0; sub(/^    - /, "", identity); \
	        suffix = "@" harness ".noreply.nexus.local>"; \
	        if (index(identity, "(" model ") <") \
	            && (harness == "" || substr(identity, length(identity) - length(suffix) + 1) == suffix)) \
	            print identity; \
	    }' authors.yaml); \
	count=$$(printf '%s\n' "$$identities" | awk 'NF { count++ } END { print count + 0 }'); \
	[ "$$count" -gt 0 ] \
	    || { echo "identity '$(IDENTITY)' with harness '$(HARNESS)' is not in authors.yaml"; exit 1; }; \
	[ "$$count" -eq 1 ] \
	    || { echo "identity '$(IDENTITY)' is ambiguous. Set HARNESS=<harness>."; exit 1; }; \
	identity=$$identities; \
	name=$$(printf '%s' "$(BRANCH)" | tr '/' '-'); \
	git config extensions.worktreeConfig true; \
	git worktree add ".worktrees/$$name" -b "$(BRANCH)"; \
	author=$${identity% <*}; \
	address=$${identity##*<}; address=$${address%>}; \
	git -C ".worktrees/$$name" config --worktree user.name "$$author"; \
	git -C ".worktrees/$$name" config --worktree user.email "$$address"; \
	echo "worktree .worktrees/$$name on $(BRANCH) authors as $$identity"
