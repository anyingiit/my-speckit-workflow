# Implementation Plan: Copyable Workflow Prompt in the README

**Branch**: `claude/speckit-constitution-workflow-1f7fe3` | **Date**: 2026-09-23 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/001-readme-workflow-prompt/spec.md`

## Summary

Publish the author's Spec Kit `/goal` workflow prompt as version `v1.0.0` in the README so a
visitor can read the whole workflow and copy the prompt with one click. `README.md` keeps the
Chef's Pick skeleton: "Getting Started" lists the prerequisites (Spec Kit 1.0.6, Claude Code as the
verified agent, an existing spec) and "Usage" gives a four-step overview of the cycle
(constitution → specify → clarify → paste prompt), explains the prompt, and shows it verbatim in a
marked ` ```text ` block. A Simplified Chinese `README.zh-CN.md` mirrors it with the same untranslated
prompt, a language switcher and a `translation-of` digest marker. A standard-library Python checker,
`tools/check_readme.py`, run in CI, fails when the two prompt blocks differ, the translation
marker is stale, or the README version disagrees with `CHANGELOG.md`, which gains a `1.0.0` entry.

## Technical Context

**Language/Version**: Markdown (GitHub Flavored) for content; Python 3.9+ standard library for the
checker

**Primary Dependencies**: None added. CI uses the existing, SHA-pinned `actions/checkout` and the
runner's preinstalled `python3`

**Storage**: Files in the repository (`README.md`, `README.zh-CN.md`, `CHANGELOG.md`)

**Testing**: `python3 -m unittest` (standard library) for the checker; `python3
tools/check_readme.py` against the real files; manual reader checks in [quickstart.md](quickstart.md)

**Target Platform**: GitHub repository page (rendering and copy button); GitHub Actions
`ubuntu-latest` for CI; the checker also runs on macOS/Linux locally

**Project Type**: Documentation repository with a small validation script

**Performance Goals**: Checker finishes in under 1 second on the repository; a reader finds and
copies the prompt within 30 seconds (SC-001)

**Constraints**: Prompt shown byte-identical to the canonical text (FR-002); no new dependency or
action (Principle V); no secrets or local paths in committed files (Principle I)

**Scale/Scope**: 2 README files, 1 changelog entry, 1 script (~150 lines) with tests, 1 CI file
edit

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Gate | Pre-design | Post-design |
|---|---|---|---|
| I. Public by Default | No secrets, private data or local absolute paths in READMEs, script or tests | PASS | PASS — test fixtures use temporary directories created at run time; no paths hard-coded |
| II. Workflow as the Product | The workflow is versioned and its change states what and why | PASS | PASS — `CHANGELOG.md` 1.0.0 entry states what and why |
| III. Chef's Pick Documentation Sync | Align ran for this version change and its decisions are recorded | PASS | PASS — align ran 2026-09-23 against v1.2.1; decisions recorded in the 1.0.0 entry ([research R6](research.md#r6-how-the-first-release-satisfies-constitution-principle-iii)); guide layer not committed |
| IV. Semantic Versioning | Version `1.0.0`, changelog entry, `v1.0.0` tag after merge | PASS | PASS |
| V. Reproducibility and Pinned Tooling | No unpinned tool added; Spec Kit version stated | PASS | PASS — standard library only; README states Spec Kit 1.0.6 from `.specify/init-options.json` |
| VI. English-First Documentation | `README.md` canonical, `README.zh-CN.md` with switcher, notice and current marker | PASS | PASS — enforced in CI by check L3 |
| Repository Scope | Only in-scope content added | PASS | PASS — `tools/` holds documentation tooling for the README, which belongs with "workflow documentation" |

No violations; Complexity Tracking is empty.

## Project Structure

### Documentation (this feature)

```text
specs/001-readme-workflow-prompt/
├── plan.md              # This file
├── research.md          # Phase 0 decisions R1–R8
├── data-model.md        # Workflow Prompt, Workflow Version, README pair, Check result
├── quickstart.md        # Validation guide
├── contracts/
│   ├── readme-layout.md      # Structure of both READMEs and invariants L1–L4
│   └── check-readme-cli.md   # CLI of tools/check_readme.py
├── checklists/
│   └── requirements.md  # Spec quality checklist
└── tasks.md             # Created by /speckit-tasks
```

### Source Code (repository root)

```text
README.md                      # modified: switcher, Getting Started, Usage with prompt v1.0.0
README.zh-CN.md                # new: Simplified Chinese translation with marker
CHANGELOG.md                   # modified: [Unreleased] → [1.0.0] entry
tools/
├── check_readme.py            # new: checks L1–L4, --update-digest, --print-prompt, --root
└── tests/
    ├── __init__.py
    └── test_check_readme.py   # new: unit tests using temporary directories
.github/workflows/ci.yml       # modified: push on all branches; lint runs the checker; test runs unit tests
```

**Structure Decision**: Single repository with content at the root and one `tools/` directory for
the checker, mirroring the Chef's Pick template's `python3 tools/…` convention. No application
source tree exists or is needed.

## Complexity Tracking

No constitution violations to justify.
