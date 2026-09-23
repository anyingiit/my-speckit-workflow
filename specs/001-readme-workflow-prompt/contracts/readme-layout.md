# Contract: README Layout

The public interface of this feature is the README a visitor reads. This contract fixes the
structure both READMEs must follow; `tools/check_readme.py` relies on the marked parts.

## README.md (English, canonical)

In this order:

1. The existing source comment and `<a id="readme-top"></a>` (kept from Chef's Pick).
2. `# My Spec-Kit Workflow`
3. Language switcher, alone on its line: `**English** · [简体中文](README.zh-CN.md)`
4. Description, badges, issue links and table of contents (unchanged six entries).
5. `## About The Project` — unchanged purpose text.
6. `## Getting Started` → `### Prerequisites` listing (FR-001a):
   - Spec Kit, verified with version 1.0.6, with a repository-relative link to
     `.specify/init-options.json` (the file that pins it), providing `/speckit-plan`,
     `/speckit-tasks`, `/speckit-analyze`, `/speckit-implement` and `/speckit-converge`.
   - Claude Code as the verified agent for the `/goal` command; other agents supporting `/goal`
     and the Spec Kit commands may work but are unverified.
   - An existing feature spec.
   The generic `git clone` installation instructions are removed.
7. `## Usage` containing, in order:
   1. One sentence stating the prompt is used only after specification work is finished (FR-004).
   2. A numbered overview (FR-004a):
      1. `/speckit-constitution` — set the project's principles.
      2. `/speckit-specify` — write the feature spec.
      3. `/speckit-clarify` — optional, resolve open questions in the spec.
      4. Paste the workflow prompt below — plan, tasks, analyze, implement and converge run in a
         loop until done.
   3. What the prompt does, that it can be rerun after the spec changes, and what the final status
      summary contains, with the report message cases (FR-004, User Story 2).
   4. A note that the prompt is intentionally kept in its original Chinese (FR-003).
   5. The prompt region:

      ````markdown
      <!-- workflow-prompt:start -->
      **Workflow version**: v1.0.0

      ```text
      <canonical prompt, verbatim>
      ```
      <!-- workflow-prompt:end -->
      ````
8. `## Contributing`, `## License`, `## Contact` — unchanged.

## README.zh-CN.md (Simplified Chinese translation)

Same section order and anchors' meaning, with:

1. `# My Spec-Kit Workflow` (project name is not translated).
2. Switcher: `[English](README.md) · **简体中文**`
3. Notice: `> 英文版是规范版本。本页与 [README.md](README.md) 不一致时，以英文版为准。`
4. Marker: `<!-- translation-of: README.md sha256:<16 hex> -->`
5. Section headings and prose in Chinese; command names, file paths and version numbers unchanged.
6. The prompt region with `**工作流版本**：v1.0.0` and the identical ` ```text ` block.

## Invariants (checked by CI)

| ID | Invariant |
|---|---|
| L1 | Each README has exactly one `workflow-prompt:start` and one `workflow-prompt:end`, in order, enclosing one ` ```text ` fence and one version label |
| L2 | The two fenced blocks are identical |
| L3 | The ZH marker digest equals the current `README.md` digest |
| L4 | Both version labels equal the highest `## [X.Y.Z] - YYYY-MM-DD` in `CHANGELOG.md` |
