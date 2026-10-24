## ADDED Requirements

### Requirement: Lightest capability answers the task

The skill MUST rank the platform's capabilities from the one that starts no browser to the one that needs a paid plan. It MUST direct the session to the lightest capability that answers the task.

#### Scenario: User needs page content without interaction

- **WHEN** the user needs the content of a page that loads without JavaScript or a click
- **THEN** the session uses the fetch capability and starts no browser session

### Requirement: Blocked page fallback

The skill MUST call a page blocked when the session's own fetch tool is refused, stops at a redirect, or returns a summary instead of the page text. It MUST direct the session to the platform's fetch first, and to one browser session only when that fetch fails or the page needs JavaScript. The session MUST stop that browser session after the read.

#### Scenario: Own fetch tool returns a summary

- **WHEN** the session's own fetch tool returns HTTP 403 or a summary instead of the page text
- **THEN** the session reads the exact page text through the platform's fetch capability and starts no browser session

#### Scenario: Platform fetch cannot read the page

- **WHEN** the platform's fetch capability fails on a page that needs JavaScript
- **THEN** the session reads the page in one browser session and stops that session after the read

### Requirement: Blocked page stops for the user

The skill MUST tell the session to stop and ask the user when a blocked page needs a paid plan or a login, or when its content is private.

#### Scenario: Blocked page asks for a login

- **WHEN** the browser session for a blocked page shows a login form
- **THEN** the session signs in nowhere, stops, and asks the user how to go on

### Requirement: Stagehand code matches the current major version

The skill MUST lead the session to write startup code for the current major Stagehand version. It MUST forbid code that this version removed.

#### Scenario: User asks for a Stagehand script

- **WHEN** the user asks for a script that drives a page with Stagehand
- **THEN** the session writes startup code of the current major version and none of the removed forms

### Requirement: One secret identifies the project

The skill MUST state that the API key alone resolves its default project and MUST NOT ask the user for a project identifier. It MUST allow one only to pin a non-default project on a multi-project key.

#### Scenario: Template asks for a project identifier

- **WHEN** a starter template or an older document asks for a project identifier
- **THEN** the session leaves that value empty and continues on the API key alone

### Requirement: Misleading errors name their real cause

The skill MUST map each failure whose message points at the wrong cause to its real cause. The causes are a placeholder provider key, a used-up free token allowance, a bot-protected site, and old code on the new version.

#### Scenario: Model call fails after the browser session started

- **WHEN** a model call reports an invalid key while the browser session started without error
- **THEN** the session empties every placeholder provider key, says that the Browserbase key is not the cause, and runs the script again

### Requirement: Command reference stays upstream

The skill MUST point at the vendor's published skill file for the full command reference and MUST NOT contain a copy of that file.

#### Scenario: Reviewer lists the skill directory

- **WHEN** a reviewer lists the files of the skill directory
- **THEN** the directory contains the canon and its companions, and no copy of the vendor's published skill file
