# Data Model: Copyable Workflow Prompt in the README

**Feature**: [spec.md](spec.md) | **Plan**: [plan.md](plan.md)

There is no database. The "data" is text held in Markdown files; this document names each piece,
where it lives, and the rules the checker enforces.

## Workflow Prompt

| Field | Description |
|---|---|
| text | The canonical prompt, in its original Chinese; for v1.0.0 exactly the block in the spec's Input |
| location | Between `<!-- workflow-prompt:start -->` and `<!-- workflow-prompt:end -->`, inside a ` ```text ` fence, in both `README.md` and `README.zh-CN.md` |

**Validation rules**

- The fenced block content in `README.zh-CN.md` equals the one in `README.md`, byte for byte after
  normalising line endings to `\n` (FR-003, FR-009 check 1).
- Each README contains exactly one start marker and one end marker, in that order, with exactly one
  fenced block between them (otherwise the checker reports a layout error).
- The text is never translated (FR-003).

## Workflow Version

| Field | Description |
|---|---|
| value | `X.Y.Z` (SemVer); `1.0.0` for this feature |
| label (EN) | `**Workflow version**: vX.Y.Z` inside the prompt markers of `README.md` |
| label (ZH) | `**工作流版本**：vX.Y.Z` inside the prompt markers of `README.zh-CN.md` |
| changelog | `## [X.Y.Z] - YYYY-MM-DD` heading in `CHANGELOG.md` |

**Validation rules**

- Both labels exist and carry the same value (FR-006).
- That value equals the highest released version in `CHANGELOG.md` (FR-005, FR-009 check 3).

**Lifecycle**: a change to the prompt or the pinned Spec Kit version creates a new version: update
the prompt block in both READMEs, both labels, and add a changelog entry in one version change
(FR-008). The tag `vX.Y.Z` is created after merge.

## README pair

| Field | Description |
|---|---|
| source | `README.md`, English, canonical |
| translation | `README.zh-CN.md`, Simplified Chinese |
| switcher (EN) | `**English** · [简体中文](README.zh-CN.md)` directly under the title |
| switcher (ZH) | `[English](README.md) · **简体中文**` directly under the title |
| notice (ZH) | A blockquote stating the English version is canonical |
| marker (ZH) | `<!-- translation-of: README.md sha256:<16 hex> -->` |

**Validation rules**

- `<16 hex>` equals the first 16 lowercase hex digits of SHA-256 over the bytes of the current
  `README.md` (FR-006, FR-009 check 2).
- Both files contain the prompt section, and neither contains secrets, private information or
  local absolute paths (FR-007; reviewed, not machine-checked).

## Check result

The checker's output, one line per failed check:

| Field | Description |
|---|---|
| check | `prompt-identical`, `translation-current`, `version-matches`, or `layout` |
| file | The file to fix |
| message | What differs and how to fix it |

Exit code `0` when every check passes, `1` otherwise. See
[contracts/check-readme-cli.md](contracts/check-readme-cli.md).
