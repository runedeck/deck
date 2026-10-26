---
name: HarnessSecurity
description: "How the coding harnesses on this machine are confined and who may change that: the Seatbelt sandbox policy and its first-token exclusions, the chezmoi-rendered Claude settings, dcg as the destructive-command net, Codex parity and its one gap, the metering proxy checks, mods, and Computer Use. USE WHEN changing a sandbox or permission setting, a write to ~/.claude/settings.json is blocked, installing or wiring dcg, seeding the Codex config, a gh or jj call fails TLS in the sandbox, verifying the proxy route, vetting a mod, or deciding what Computer Use may touch. NOT FOR VM-tier workloads (SandboxToolkit) or recovering from a live guard block (SafetyFirst)."
compatibility: "Claude Code, Codex, grok, and OpenCode on macOS. Scripts live in the provisioning codebase at $PROVISION_ROOT."
metadata:
    version: 0.3.0
---

# HarnessSecurity

The harness tier of ARCH-0031 is a process sandbox. VIRT-0001, both records in `$PROVISION_ROOT/docs/decisions/`, enables Claude Code's built-in Seatbelt sandbox in auto-allow mode: the OS confines every Bash subprocess, so the boundary holds whatever the model chose to run, and prompts stay at auto-mode levels. This skill holds the owner's policy, the scripts that install each layer, and the traps found here. SandboxToolkit covers the VM tier.

## Constraints

- Never weaken the sandbox, dcg, or commit signing to finish a task. Do not widen `excludedCommands`, and do not add `enableWeakerNetworkIsolation`, which the documentation reserves for man-in-the-middle proxies. Report the need to the owner.
- An agent never writes `~/.claude/settings.json`. The auto-mode classifier blocks the write as self-permission widening, even one that keeps every flag. Sandbox policy has one home, the user-level chezmoi template. A project-local settings file keeps permission allows only.
- Credentials stay provider-owned. Never copy an authentication state into tracked policy.
- Computer Use is a per-session grant for one GUI task. Keep it off every standing permission list and every autonomous path. It runs outside the command sandbox and dcg, so no config bounds what it clicks.
- A missing enforcement capability is a documented gap. Do not report it as a pass.

## Instructions

Resolve the codebase root once per shell before any script below:

```sh
PROVISION_ROOT="${PROVISION_ROOT:-$HOME/Developer/runedeck/provision}"
```

### Change a harness setting

Every policy file below is a chezmoi render. Find its source with `chezmoi source-path <target>`, edit the source, and hand the apply to the owner, because the agent sandbox cannot write the chezmoi state database. `chezmoi diff` on a `modify_` target shows hundreds of lines. Use the key-level `jq` check from the Chezmoi skill's Commands.md instead, which works inside the sandbox.

- `~/.claude/settings.json`: the permission rules (allow, ask, deny) come from `.chezmoidata/harness/claude.json`. Everything else, `sandbox.excludedCommands` included, comes from `dot_claude/modify_private_settings.json.tmpl`. That script prints the template and copies back only `hooks`, `model`, and `outputStyle` from the live file.
- `~/.codex/config.toml`: `dot_codex/modify_private_config.toml.tmpl` deep-merges the policy from `.chezmoidata/harness/codex.json` into the live file on every apply and passes the app-written keys through. A change to the Codex network allowlist or a filesystem grant goes into that data file. `$PROVISION_ROOT/scripts/configure/codex.sh` seeds the file from the codebase manifest only when absent and repairs `hooks.json`. It is not the place for a policy change, and the next apply re-renders the policy over a seeded file.
- `~/.config/dcg/config.toml` and the packs under `~/.config/dcg/packs/`: rendered from `dot_config/dcg/config.toml.tmpl` and `dot_config/dcg/packs/`. `$PROVISION_ROOT/scripts/configure/dcg.sh` skips every target that chezmoi manages and deploys only the `forge.yaml` pack, which chezmoi has no source for. Make a config or pack change in the chezmoi source. The dotfile is canonical, as the DotfilesScope rule says.

### Keep the layers in place

Four layers, outermost first, and every harness at every layer it supports:

1. Native sandbox. Claude: Seatbelt with writes confined to the working directory plus the `allowWrite` list in the settings template (the owner's workshop and clone trees, caches, and data directories), a credential `denyRead` list, a hostname allowlist, and `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB=1`. Codex: `default_permissions` names a permission set from `.chezmoidata/harness/codex.json`, with per-path filesystem grants, a limited network mode with a domain allowlist, and a shell environment policy that drops secret-shaped variables. OpenCode has permission rules and no kernel sandbox.
2. Hard structural deny. Claude `permissions.deny`, and dcg as a `PreToolUse` hook on Claude and Codex. dcg is a net for accidental commands. The sandbox is the boundary. `$PROVISION_ROOT/scripts/install/dcg.sh` installs the pinned release after a SHA-256 check. The config and the packs are chezmoi renders, see above. Nothing in the dotfiles or the codebase registers the hook: the settings template copies the live `hooks` block back as it is, and dcg's own `self_heal_hook`, on by default in its config, re-asserts its entry. When the entry is missing, the owner runs `dcg install` and checks with `dcg doctor`. The `user.dotguard` pack blocks shell edits of rune-managed harness trees: edit the deck and run `rune install`.
3. Soft, model-judged policy in prose: the `autoMode` block and CLAUDE.md on Claude, `approvals_reviewer` and AGENTS.md on Codex. Prose steers. The lower layers enforce.
4. Credential protection. Claude denies reads with the `denyRead` list in the settings template. Codex denies them in the permission set of `.chezmoidata/harness/codex.json`: each credential path (the ssh, gnupg, cloud, container, keychain, and package-registry credential directories and files) has a `deny` entry in the set's `filesystem` map, and every apply renders them into the live config. A new deny entry goes into that map beside the existing ones, and the owner applies. The one gap Codex keeps (PROV-0019) is a static command-exclusion list: a command that needs denied access escalates through `approval_policy` instead of running unsandboxed.

### Call an excluded tool

The list is `sandbox.excludedCommands` in the settings template, and it matches the first token of a command line only. Read it there before you rely on it. As of this writing it excludes `docker`, `gh`, `glab`, `git`, `brew`, `container`, `prlctl`, `orb`, `orbctl`, `jj`, and `zed`, each with an `rtk` twin, and only these rune forms: `rune run`, `rune launch`, `rune proof run`, `rune sign`, `rune install`, `rune deploy`, `rune clean`, and `rune repair`. Every other rune command runs sandboxed, and `autoAllowBashIfSandboxed` lets it through without a prompt. A pipe, a redirect, a loop, or `$( )` around an excluded tool runs it sandboxed, where a Go binary fails transport security (TLS) with `OSStatus -26276`, because Seatbelt blocks the port to `trustd`. Put the tool first on the line and pass the location as an argument, one call each: `gh -R owner/repo pr view 1`. A leading `cd dir &&` is tolerated, except for the guarded `jj push`, which reads the shell directory.

### Vet a mod

A mod runs with the user's permissions outside the Bash sandbox and can approve a tool call a deny rule refused. Read a candidate with `claude plugin validate <clone>` before adding it. `$PROVISION_ROOT/scripts/configure/claude-plugins.sh` installs the plugins named in the codebase manifest into `~/.claude/plugins`. The switch lives in the settings template, so a plugin missing there is disabled at the next apply.

## Verification

- `$PROVISION_ROOT/scripts/verify/harness-proxy.sh`: Claude Code and grok route through the local metering proxy on loopback, both through variables that the dotfiles' proxy shell file exports (`ANTHROPIC_BASE_URL` and the grok base URL). Codex does not: `.chezmoidata/harness/codex.json` pins the top-level `model_provider` to the direct vendor, so plain `codex` and the desktop app connect direct, and `codex-proxy` routes one command through the proxy with a `--config` override. Rune uses `codex-proxy` for every Codex call. The verify script passes on this state. It fails when the top-level provider points at the proxy, when `codex-proxy` is missing, or when `codex-proxy` routes elsewhere. `cliproxy off` is a deliberate state that the script skips. `cliproxy on|off|status` toggles Claude and grok and enables or disables `codex-proxy`, and `noproxy <cmd>` runs one command direct.
- `$PROVISION_ROOT/scripts/verify/ai-proxy-egress.sh`: the proxy's plugin loader is off, remote management is refused, and its connections reach model vendors only. The proxy stores OAuth tokens in plaintext under its own directory. Keep that directory at mode 700 and its files at 600.
- `$PROVISION_ROOT/scripts/verify/codex-skills.sh`: no divergent duplicate between the two Codex skill roots. PROV-0023 keeps the managed skills under `~/.codex/skills`.
- A Bash write to a new file directly under `$HOME` fails with `Operation not permitted`. A write under an `allowWrite` entry succeeds, and the policy allows that. `env` in a subprocess shows no credential variable.

## References

- `$PROVISION_ROOT/docs/decisions/VIRT-0001 Coding harness Seatbelt sandbox.md`
- `$PROVISION_ROOT/docs/decisions/PROV-0019 Codex as a cross-reference coding agent.md`
- <https://code.claude.com/docs/en/sandboxing>
- <https://developers.openai.com/codex/sandbox>
