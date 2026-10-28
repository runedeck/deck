## 1. Module

- [x] 1.1 Create `runes/provisioning/` with its module identity, defaults that give `PROVISION_ROOT`, README, license, and the schema files of each kind
- [x] 1.2 Find how the cli selects modules, then make the default deployment leave the module out, with a fixture test
- [x] 1.3 Add `scripts/check-provisioning-module`, its hook entry, and a test that an executable file fails
- [x] 1.4 Add `scripts/record-comparison` and `scripts/check-provisioning-evidence`, with a test that a rune without a comparison fails

## 2. Whole skills

- [x] 2.1 BrowserbaseToolkit moved to the development module instead, through the change automate-cloud-browsers-browserbase
- [x] 2.2 Move HomebrewToolkit and record its comparison
- [x] 2.3 Move GhosttyToolkit and record its comparison
- [x] 2.4 Move DmgInstall, fix the `-quiet` contradiction, record its comparison
- [x] 2.5 Move TmuxToolkit and record its comparison

## 3. Rewritten skills

- [x] 3.1 Rewrite GpgToolkit to owner facts, write cases that ask for them, record its comparison
- [x] 3.2 Rewrite Chezmoi to owner facts, write cases, record its comparison
- [x] 3.3 Rewrite SshToolkit to owner facts, write cases, record its comparison
- [x] 3.4 Rewrite PasswordToolkit to owner facts, write cases, record its comparison
- [x] 3.5 Rewrite SandboxToolkit to owner facts, write cases, record its comparison
- [x] 3.6 Rewrite HarnessSecurity to owner facts, write cases, record its comparison
- [x] 3.7 Rewrite the dotfiles boundary rule with frontmatter and record its comparison

## 4. Provisioning codebase

- [x] 4.1 Clone the old codebase with history to `~/Developer/runedeck/provision`, colocate it with jj, remove the skills, the rule, and the module identity in one commit
- [x] 4.2 Rewrite the links from records and scripts to the skills, which now sit in the deck
- [x] 4.3 Add a check in the codebase that resolves every script path the provisioning module names
- [x] 4.4 Add the Multica server and CLI drift check under `scripts/verify/`
- [x] 4.5 Add the codebase to the workshop's list of active clones

## 5. Retirement

- [ ] 5.1 Review the codebase for personal data before any publish, with the owner
- [ ] 5.2 Point the old codebase's README at the new homes, and have the owner archive it on GitHub
- [x] 5.3 Update the memory that called the old scripts out of scope

## 6. Verification

- [x] 6.1 Run `rune spec validate`, `rune validate --skill-layers`, `mdschema check`, and the new checks
- [x] 6.2 Record a proof: a consumer installs the whole deck and receives no provisioning rune, then names the module and receives it
