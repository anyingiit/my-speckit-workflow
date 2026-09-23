# Research: Copyable Workflow Prompt in the README

**Feature**: [spec.md](spec.md) | **Plan**: [plan.md](plan.md) | **Date**: 2026-09-23

The Technical Context had no open `NEEDS CLARIFICATION` items after `/speckit-clarify`; the
decisions below settle the remaining design choices.

## R1. How the prompt is displayed so one action copies it verbatim

- **Decision**: A fenced code block with the `text` info string, placed between the HTML comments
  `<!-- workflow-prompt:start -->` and `<!-- workflow-prompt:end -->`.
- **Rationale**: GitHub renders every fenced code block with a one-click copy button and copies
  its content byte for byte; the `text` info string disables syntax highlighting, so no character
  is restyled. A fenced block also stops Markdown from reflowing the prompt's `0.`–`11.` list or
  touching its slashes and full-width punctuation (spec Edge Cases). The prompt contains no
  backticks, so a three-backtick fence cannot be closed early. The comment markers are invisible
  on the rendered page and give the checker an unambiguous way to find the block.
- **Alternatives considered**: A blockquote or plain numbered list (rejected: Markdown reflows the
  list, starting it at 1, and there is no copy button); a separate file linked from the README
  (rejected: FR-001 and User Story 1 require the prompt on the README itself).

## R2. How the version label is written and found

- **Decision**: A caption line directly above the prompt block: `**Workflow version**: v1.0.0` in
  `README.md` and `**工作流版本**：v1.0.0` in `README.zh-CN.md` (full-width colon, as in Chinese
  prose), both inside the prompt markers.
- **Rationale**: Visible to readers (User Story 3), and a fixed pattern the checker can match with
  one regular expression per language.
- **Alternatives considered**: Version only in the section heading (rejected: headings produce
  anchors, and a version in the anchor would break links on every release); a hidden comment only
  (rejected: readers must see the version).

## R3. What tool enforces the three CI checks (FR-009)

- **Decision**: One Python script, `tools/check_readme.py`, using only the Python 3 standard
  library, with unit tests in `tools/tests/` run by `python3 -m unittest`. CI calls it with the
  `python3` preinstalled on the `ubuntu-latest` runner.
- **Rationale**: The checks are plain text comparisons and one SHA-256 digest; the standard
  library covers them. No new dependency means nothing new to pin (Constitution Principle V), no
  new Dependabot ecosystem, and no new GitHub Action to pin to a commit SHA. The same `tools/`
  layout and `python3 tools/…` invocation are used by the Chef's Pick template for its own
  translation checks, which Principle VI names as the reference.
- **Alternatives considered**: Shell script with `grep`/`sha256sum` (rejected: fragile with
  multi-line blocks and Unicode, and `sha256sum` differs on macOS); a Node.js or third-party
  Markdown linter (rejected: adds a dependency and a setup action for three text checks);
  `actions/setup-python` (rejected: the runner's system Python suffices, and the action would need
  SHA pinning and Dependabot updates).

## R4. How the `translation-of` digest is computed and refreshed

- **Decision**: The digest is the first 16 lowercase hex digits of SHA-256 over the exact bytes of
  `README.md`. The marker is `<!-- translation-of: README.md sha256:<16 hex> -->`, placed after the
  canonical-English notice in `README.zh-CN.md`. `python3 tools/check_readme.py --update-digest`
  rewrites the marker; nobody computes it by hand.
- **Rationale**: Matches the format fixed in Constitution Principle VI and the Chef's Pick
  practice ("do not compute the digest by hand"). Hashing raw bytes makes the result identical on
  every platform.
- **Alternatives considered**: Hashing only the prompt block (rejected: the constitution ties the
  marker to the whole English source, so any English edit must prompt a translation review);
  git blob IDs (rejected: differ from the constitution's stated SHA-256 format).

## R5. How "the highest released version in CHANGELOG.md" is determined

- **Decision**: The highest `X.Y.Z` among headings of the form `## [X.Y.Z] - YYYY-MM-DD`, compared
  numerically; `## [Unreleased]` is ignored.
- **Rationale**: This is the Keep a Changelog 1.1.0 format the repository adopted from Chef's Pick
  (module M09), and the same rule Chef's Pick uses to read its own snapshot version.
- **Alternatives considered**: Latest git tag (rejected: tags are created after merge, so the check
  could not pass on the pull request that introduces a version).

## R6. How the first release satisfies Constitution Principle III

- **Decision**: The Chef's Pick align for this version change already ran on 2026-09-23 against
  template v1.2.1 (commit `468f3af`). The `1.0.0` changelog entry records its result: modules
  M01–M09, M11 and M12 accepted; M13–M16 declined by the author; M10 has no files. `README.md`
  becomes the author's own modified content after this feature, which the skill records as
  `modified`/`alternative` on later runs.
- **Rationale**: Principle III requires the align before versioning and its decisions recorded in
  the pull request or changelog; the run exists, so recording it is what remains.
- **Alternatives considered**: Re-running the skill inside `/speckit-implement` (rejected: the
  skill requires the author's approval of every item and cannot run unattended; a re-run before
  tagging stays available to the author).

## R7. How the README sections are restructured

- **Decision**: Keep the Chef's Pick README skeleton. Replace "Getting Started" content with the
  prerequisites (FR-001a) and "Usage" content with the numbered workflow overview (FR-004a), the
  explanation (FR-004), and the prompt block (FR-001/FR-002). Add the language switcher under the
  title. The table of contents keeps its six entries.
- **Rationale**: Chosen in clarification Q3; keeps later Chef's Pick align diffs small.
- **Alternatives considered**: See spec Clarifications.

## R8. Release mechanics that stay outside implementation

- **Decision**: `/speckit-implement` produces the files and the passing checks. Pushing, opening
  the pull request, merging and tagging `v1.0.0` remain steps for the author (Constitution Release
  Workflow steps 6–7), listed in [quickstart.md](quickstart.md).
- **Rationale**: These change the remote repository, which needs the author's explicit decision.
