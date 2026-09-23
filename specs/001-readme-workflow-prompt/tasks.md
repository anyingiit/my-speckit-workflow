---

description: "Task list for the copyable workflow prompt in the README"
---

# Tasks: Copyable Workflow Prompt in the README

**Input**: Design documents from `specs/001-readme-workflow-prompt/`

**Prerequisites**: [plan.md](plan.md), [spec.md](spec.md), [research.md](research.md),
[data-model.md](data-model.md), [contracts/](contracts/), [quickstart.md](quickstart.md)

**Tests**: Included. FR-009 and SC-005 require automated CI checks, and the plan's Testing field
specifies `python3 -m unittest` tests for the checker. Test tasks are written before the check they
cover and must fail first.

**Organization**: Tasks are grouped by user story so each story can be implemented and tested on
its own.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies on incomplete tasks)
- **[Story]**: Which user story this task belongs to (US1–US4)
- Paths are relative to the repository root

## Canonical sources used by several tasks

- **Canonical prompt**: the content of the ` ````text ` block in the **Input** section of
  [spec.md](spec.md) (lines starting with `/goal 按照顺序串行执行。` through `11. Done，结束goal`),
  copied byte for byte — never retyped or translated.
- **Prompt region** (contract [readme-layout.md](contracts/readme-layout.md)): the lines
  `<!-- workflow-prompt:start -->`, a version label line, a blank line, a ` ```text ` fence
  containing the canonical prompt, the closing ` ``` `, and `<!-- workflow-prompt:end -->`.
- **Checker CLI**: [contracts/check-readme-cli.md](contracts/check-readme-cli.md).

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create the directories for the checker and its tests

- [X] T001 Create the `tools/` and `tools/tests/` directories and an empty `tools/tests/__init__.py`
  so `python3 -m unittest discover -s tools/tests` can import the test package

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: The checker's command-line frame and the `layout` check (invariant L1), which every
other check and every story's verification depends on

**⚠️ CRITICAL**: Checks L2–L4 (US3, US4) and the CI wiring cannot start until this phase is done

- [X] T002 Write failing unit tests in `tools/tests/test_check_readme.py` (standard library
  `unittest`, each test builds its own files in `tempfile.TemporaryDirectory()` and runs the checker
  through `main(["--root", tmp, ...])`; no hard-coded absolute paths). A shared fixture helper
  writes all three files — `README.md`, `README.zh-CN.md` and `CHANGELOG.md` — in a state that
  satisfies invariants L1–L4 (identical prompt blocks, labels `v1.0.0`, a `## [1.0.0] - 2026-09-23`
  changelog heading, and a `translation-of` marker computed from the fixture's `README.md` bytes), and
  each test changes only what it exercises; layout tests assert on the presence or absence of
  `layout:` lines in stderr rather than on the overall exit code, so they keep passing once checks
  L2–L4 exist. Cover: a README with a valid prompt region produces no `layout:` line; a README missing `<!-- workflow-prompt:end -->` fails with a
  line starting `layout: README.md:`; a README with two start markers fails `layout`; a region
  without a ` ```text ` fence fails `layout`; a region without a version label line fails `layout`
  (contract invariant L1); deleting `README.md` from the fixture exits `2`; `--print-prompt
  README.md` prints exactly the fenced block content with `\n` line endings and exits `0`
- [X] T003 Implement the frame of `tools/check_readme.py` (Python 3.9+, standard library only,
  executable with `python3 tools/check_readme.py`, exposing `main(argv) -> int`): `argparse` options
  `--root` (default: current directory), `--update-digest`, `--print-prompt FILE`; read files as
  UTF-8 and normalise line endings to `\n`; exit `2` with a message when `README.md`,
  `README.zh-CN.md` or `CHANGELOG.md` is missing (for `--print-prompt`, only the named file is
  required); a function that extracts the prompt region per data-model rule "Each README contains
  exactly one start marker and one end marker, in that order, with exactly one fenced block between
  them (otherwise the checker reports a layout error)", plus exactly one version label line inside
  the region (contract invariant L1; a missing or duplicated label is a `layout` failure), and
  returns the fenced content and the version label line; report every failure as `<check>: <file>: <message>` on stderr, collect all failures
  before exiting, exit `1` if any failed, else print `README checks passed (workflow version X.Y.Z).`
  and exit `0`; make T002's tests pass (depends on T001, T002)

**Checkpoint**: `python3 -m unittest discover -s tools/tests -v` passes the layout tests

---

## Phase 3: User Story 1 - Copy the complete workflow prompt from the README (Priority: P1) 🎯 MVP

**Goal**: A visitor opens "Usage" in `README.md` and copies the complete canonical prompt in one
click (FR-001, FR-002, FR-003)

**Independent Test**: `python3 tools/check_readme.py --print-prompt README.md` output is identical
to the canonical prompt (quickstart step 2 prints `IDENTICAL`); on GitHub the block has a copy
button and renders steps `0.`–`11.` unchanged

- [X] T004 [US1] In `README.md`, replace the placeholder content of the existing `## Usage` section
  (the `sh` block containing `/speckit-constitution → /speckit-specify → …`) with the prompt region:
  `<!-- workflow-prompt:start -->`, the line `**Workflow version**: v1.0.0`, a blank line, a
  ` ```text ` fence holding the canonical prompt byte for byte (steps `0.`–`11.`, full-width
  `“”（），` preserved, no trailing spaces added), the closing ` ``` `, and
  `<!-- workflow-prompt:end -->`; keep the `## Usage` heading and the table of contents unchanged
  (FR-001: "The README MUST NOT add a new top-level section for the workflow")
- [X] T005 [US1] Verify the block: run `python3 tools/check_readme.py --print-prompt README.md` and
  diff it against the canonical prompt extracted from `specs/001-readme-workflow-prompt/spec.md` as
  in quickstart step 2; fix `README.md` until the diff is empty (depends on T003, T004)

**Checkpoint**: The MVP works: the complete prompt is on the README and copies verbatim

---

## Phase 4: User Story 2 - Understand when and how to use the prompt (Priority: P2)

**Goal**: The README states prerequisites, the whole-cycle overview, when to run the prompt, and
what it returns (FR-001a, FR-004, FR-004a)

**Independent Test**: After reading only `README.md`, a reader can name the prerequisites, the
moment to run the prompt, and the contents of its final output (SC-003); quickstart step 4 items
2–3 hold

- [X] T006 [US2] In `README.md`, replace the content of `## Getting Started` (the
  `### Prerequisites` list containing only `Git` and the `### Installation` `git clone` block) with a
  `### Prerequisites` list per [readme-layout.md](contracts/readme-layout.md) item 6: Spec Kit,
  "verified with version 1.0.6", linking to `.specify/init-options.json` (the file that pins it),
  providing `/speckit-plan`, `/speckit-tasks`, `/speckit-analyze`, `/speckit-implement` and
  `/speckit-converge`; Claude Code as the verified agent for the prompt's `/goal` command, stating
  that other agents supporting `/goal` and the Spec Kit commands may work but are unverified; an
  existing feature spec; remove the `### Installation` subsection (edits the same file as T004 and
  T007, so run it after T004, not in parallel)
- [X] T007 [US2] In `README.md`, above the prompt region inside `## Usage` (after T004), add in
  this order per [readme-layout.md](contracts/readme-layout.md) item 7: (1) one sentence that the
  prompt is used only after specification work is finished (`/speckit-specify`, and
  `/speckit-clarify` if used); (2) the numbered overview — 1. `/speckit-constitution` sets the
  project's principles, 2. `/speckit-specify` writes the feature spec, 3. `/speckit-clarify`
  (optional) resolves open questions, 4. paste the workflow prompt below, which runs plan, tasks,
  analyze, implement and converge in a loop; (3) what the prompt does: runs `/speckit-plan` and
  `/speckit-tasks` unless plan and tasks already exist, repeats analyze-and-fix (at most 20 fix
  rounds) and implement-and-converge (at most 10 gap rounds), never edits the spec, and can be rerun
  after the spec changes; (4) what it returns: a status summary of completed tasks, unfinished
  tasks and spec-related issues, preceded by a report message when a retry limit is hit or the spec
  needs manual changes; (5) a note that the prompt is intentionally kept in its original Chinese;
  do not add any other copyable block (FR-004a: "the `/goal` prompt remains the only copyable block
  of the workflow") (depends on T004, T006)

**Checkpoint**: `README.md` alone explains and delivers the workflow

---

## Phase 5: User Story 3 - Know which version of the workflow is shown (Priority: P3)

**Goal**: The README's version label matches the changelog's latest release, enforced in CI
(FR-005, FR-009 check 3)

**Independent Test**: `python3 tools/check_readme.py` reports no `version-matches` failure;
changing the label to `v1.0.1` makes it fail with `version-matches` (quickstart step 3)

- [X] T008 [US3] Add failing unit tests to `tools/tests/test_check_readme.py` for
  `version-matches`: labels `**Workflow version**: v1.0.0` (EN) and `**工作流版本**：v1.0.0` (ZH)
  with a `CHANGELOG.md` whose highest `## [X.Y.Z] - YYYY-MM-DD` heading is `1.0.0` pass;
  `## [Unreleased]` is ignored; `## [1.10.0]` ranks above `## [1.9.0]` (numeric comparison); a label of
  `v1.0.1` fails with `version-matches: README.md: label v1.0.1 != CHANGELOG.md latest release
  1.0.0`; a changelog with no released version fails `version-matches` (a missing label is a
  `layout` failure covered by T002, not a `version-matches` one)
  (depends on T003)
- [X] T009 [US3] Implement the `version-matches` check (invariant L4) in `tools/check_readme.py`:
  parse the label in each README's prompt region with the patterns `^\*\*Workflow version\*\*:
  v(\d+\.\d+\.\d+)$` and `^\*\*工作流版本\*\*：v(\d+\.\d+\.\d+)$`, find the highest released version
  in `CHANGELOG.md` per data-model rule "That value equals the highest released version in
  `CHANGELOG.md`" (headings `## [X.Y.Z] - YYYY-MM-DD`, numeric compare), and report each mismatch
  against the file to fix; make T008's tests pass (depends on T008)
- [X] T010 [P] [US3] In `CHANGELOG.md`, replace `## [Unreleased]` and its `- Initial project
  structure.` item with an empty `## [Unreleased]` followed by `## [1.0.0] - 2026-09-23` containing
  `### Added` items: the README "Usage" section with the Spec Kit `/goal` workflow prompt v1.0.0 and
  why (so readers can see and copy the complete workflow); the prerequisites in "Getting Started";
  the Simplified Chinese `README.zh-CN.md`; community files from Chef's Pick OSS Starter v1.2.1 with
  the align decisions (M01–M09, M11, M12 accepted; M13–M16 declined by the author; M10 ships no
  files) per [research R6](research.md#r6-how-the-first-release-satisfies-constitution-principle-iii);
  the project constitution; `tools/check_readme.py` and its CI checks; update the link references at
  the bottom to `[Unreleased]: https://github.com/anyingiit/my-speckit-workflow/compare/v1.0.0...HEAD`
  and `[1.0.0]: https://github.com/anyingiit/my-speckit-workflow/releases/tag/v1.0.0`

**Checkpoint**: Version label, changelog and check agree on `1.0.0`

---

## Phase 6: User Story 4 - Read the same workflow in Chinese (Priority: P3)

**Goal**: `README.zh-CN.md` mirrors the English README with the identical untranslated prompt, and
CI enforces identity and translation freshness (FR-003, FR-006, FR-009 checks 1–2)

**Independent Test**: The switcher links both ways; `python3 tools/check_readme.py` reports no
`prompt-identical` or `translation-current` failure; the edits in quickstart step 3 rows 1–2 make
the matching check fail

- [X] T011 [US4] Add failing unit tests to `tools/tests/test_check_readme.py` for
  `prompt-identical` (identical blocks pass; one changed character in the ZH block fails with a line
  starting `prompt-identical: README.zh-CN.md:` naming the first differing line; CRLF vs LF endings
  still pass) and `translation-current` (a marker `<!-- translation-of: README.md sha256:<16 hex>
  -->` equal to the first 16 lowercase hex digits of SHA-256 over the raw bytes of `README.md`
  passes; any other digest or a missing marker fails with `translation-current: README.zh-CN.md:`;
  `--update-digest` rewrites only the marker line, leaves `README.md` byte-identical, and the
  following check passes) (depends on T003)
- [X] T012 [US4] Implement `prompt-identical` (L2) and `translation-current` (L3) and
  `--update-digest` in `tools/check_readme.py` per data-model rules "The fenced block content in
  `README.zh-CN.md` equals the one in `README.md`, byte for byte after normalising line endings to
  `\n`" and "`<16 hex>` equals the first 16 lowercase hex digits of SHA-256 over the bytes of the
  current `README.md`"; failure messages follow the examples in
  [check-readme-cli.md](contracts/check-readme-cli.md); make T011's tests pass (depends on T011)
- [X] T013 [US4] In `README.md`, add the language switcher line `**English** ·
  [简体中文](README.zh-CN.md)` directly under `# My Spec-Kit Workflow`, followed by a blank line
  (depends on T004, T006, T007)
- [X] T014 [US4] Create `README.zh-CN.md` as the Simplified Chinese translation of the final
  `README.md`, per [readme-layout.md](contracts/readme-layout.md) "README.zh-CN.md": keep the source
  comment and `<a id="readme-top"></a>`; title `# My Spec-Kit Workflow`; switcher `[English](README.md)
  · **简体中文**`; notice `> 英文版是规范版本。本页与 [README.md](README.md) 不一致时，以英文版为准。`;
  a placeholder marker `<!-- translation-of: README.md sha256:0000000000000000 -->`; badges and links
  unchanged; every section translated (headings in Chinese, with the table of contents pointing at
  the Chinese headings' anchors), command names, file paths, links and version numbers unchanged;
  the prompt region with the label `**工作流版本**：v1.0.0` and the fenced block copied byte for byte
  from `README.md` (never translated) (depends on T013)
- [X] T015 [US4] Run `python3 tools/check_readme.py --update-digest` to write the real digest into
  `README.zh-CN.md`, then confirm `python3 tools/check_readme.py` exits `0` (depends on T009, T010,
  T012, T014)

**Checkpoint**: Both READMEs agree and every check passes locally

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: CI wiring, end-to-end validation, and constitution compliance

- [X] T016 In `.github/workflows/ci.yml`, in the `lint` job, insert directly below the comment
  `# Add your project's linters below this line.` (keep the comment) a step
  `name: Check README consistency` running `python3 tools/check_readme.py`; in the `on:` block
  change `push:` to trigger on every branch by removing its `branches: [main]` filter (keep
  `pull_request` and `workflow_dispatch` unchanged), so CI runs on every push and pull request as
  FR-009 requires; in the `test` job
  replace the `Run tests` placeholder step's `run` with `python3 -m unittest discover -s tools/tests
  -v`; add no new `uses:` lines (plan: "No new actions are added") (depends on T012, T009)
- [X] T017 Review `README.md`, `README.zh-CN.md`, `CHANGELOG.md`, `tools/check_readme.py` and
  `tools/tests/test_check_readme.py` for Constitution Principle I (FR-007): no secrets, private
  personal information, or local absolute paths such as `/Users/...`; fix any found and, if
  `README.md` changed, update `README.zh-CN.md` to match and rerun T015; run this before T018, not
  in parallel with it, because T018 checks and restores the same files (depends on T015)
- [X] T018 Run quickstart steps 1–3 from [quickstart.md](quickstart.md): all checks and unit tests
  pass; the prompt diff prints `IDENTICAL`; each of the four drift edits fails with its named check;
  restore every file with `git checkout -- <file>` (or re-save) afterwards and confirm `git status`
  shows only intended changes (depends on T015, T016, T017)
- [X] T019 Remove any by-products created while testing (for example `__pycache__/` under `tools/`)
  and confirm `git status` lists only: `README.md`, `README.zh-CN.md`, `CHANGELOG.md`,
  `.github/workflows/ci.yml`, `tools/check_readme.py`, `tools/tests/__init__.py`,
  `tools/tests/test_check_readme.py`, and files under `specs/001-readme-workflow-prompt/`
  (depends on T018, T017)

---

## Dependencies & Execution Order

### Phase dependencies

- **Setup (Phase 1)** → **Foundational (Phase 2)** → user stories
- **US1 (Phase 3)**: T004 can start any time; T005 needs T003
- **US2 (Phase 4)**: T006 after T004; T007 after T006 (same file)
- **US3 (Phase 5)**: T008–T009 after T003; T010 any time
- **US4 (Phase 6)**: T011–T012 after T003; T013 after all `README.md` content edits (T004, T006,
  T007); T014 after T013; T015 last, after T009, T010, T012, T014
- **Polish (Phase 7)**: after the stories it validates

### Why `README.md` edits are ordered

Every byte of `README.md` feeds the `translation-of` digest, so all English edits (T004, T006,
T007, T013) finish before the translation (T014) and the digest update (T015). Any later
`README.md` change requires updating `README.zh-CN.md` and rerunning T015.

### Story completion order

US1 (MVP) → US2 → US3 and US4 (US4's full check also needs US3's version check to pass).

---

## Parallel Execution Examples

- After T003: T004 (`README.md`), T008 (tests) and T010 (`CHANGELOG.md`) touch different files.
- In US2: T006 and T007 both edit `README.md`, so they run after T004, one after another; they
  can run alongside T008 and T010, which touch other files.
- Tasks T008 and T011 both edit `tools/tests/test_check_readme.py`, and T009 and T012 both edit
  `tools/check_readme.py`, so they run one after another.
- T017 runs before T018 (T018 validates the files T017 may change).

---

## Implementation Strategy

### MVP first (User Story 1 only)

1. Phase 1 (T001) and Phase 2 (T002–T003)
2. Phase 3 (T004–T005)
3. Stop and validate: the prompt copies verbatim from `README.md`

### Incremental delivery

1. Add US2 (T006–T007): the README explains the workflow
2. Add US3 (T008–T010): version label, changelog and check
3. Add US4 (T011–T015): Chinese README and freshness checks
4. Polish (T016–T019): CI wiring and final validation

### Out of implementation scope

Pushing, opening the pull request, merging, and tagging `v1.0.0` remain for the author
([research R8](research.md#r8-release-mechanics-that-stay-outside-implementation), quickstart
step 5).

---

## Phase 8: Convergence

- [X] T020 Keep the Python ignore rules (`__pycache__/`, `*.pyc`) appended to `.gitignore` during implementation, since `tools/` produces `__pycache__/` when the checker and tests run; mention them in the `1.0.0` entry of `CHANGELOG.md`; then complete T019's check with `.gitignore` added to its allowed file list (previous round failed because `git status` also listed `.gitignore`, which T019's list omitted) per plan: Source Code layout / T019 (unrequested)
