# Quickstart: Validate the README Workflow Prompt

**Feature**: [spec.md](spec.md) | **Plan**: [plan.md](plan.md)

Run from the repository root. Requires `python3` (3.9 or later) and `git`.

## 1. Automated checks (FR-009, SC-005)

```sh
python3 tools/check_readme.py
python3 -m unittest discover -s tools/tests -v
```

**Expected**: `README checks passed (workflow version 1.0.0).` and all unit tests `OK`.

## 2. Prompt is the canonical text (FR-002, SC-002)

Compare the README block with the canonical prompt in the spec's Input:

```sh
python3 tools/check_readme.py --print-prompt README.md > /tmp/readme-prompt.txt
awk '/^````text$/{f=1;next} /^````$/{f=0} f' specs/001-readme-workflow-prompt/spec.md > /tmp/spec-prompt.txt
diff /tmp/spec-prompt.txt /tmp/readme-prompt.txt && echo IDENTICAL
```

**Expected**: `IDENTICAL`.

## 3. Checks catch drift (SC-005)

Each of these must make `python3 tools/check_readme.py` exit `1` with the named check; restore the
file with `git checkout -- <file>` afterwards.

| Change | Expected failing check |
|---|---|
| Edit one character inside the prompt block of `README.zh-CN.md` | `prompt-identical` |
| Add a word anywhere in `README.md` | `translation-current` |
| Change `v1.0.0` to `v1.0.1` in the label of `README.md` | `version-matches` |
| Delete `<!-- workflow-prompt:end -->` from `README.md` | `layout` |

## 4. Reader checks on GitHub (SC-001, SC-003, User Stories 1–4)

After the branch is pushed, open the README on GitHub:

1. From the table of contents, open **Usage**; click the copy button on the prompt block and paste
   into a text editor. It matches step 2's output, including `“”（）`, and steps `0.`–`11.`.
2. **Getting Started** names Spec Kit 1.0.6 (linked to `.specify/init-options.json`), Claude Code
   as the verified agent, and an existing feature spec.
3. **Usage** says the prompt is used only after specification is finished, shows the four-step
   overview, and describes the final status summary.
4. The switcher leads to `README.zh-CN.md`, which shows the same `v1.0.0` and the same block.
5. The CI workflow run for the push is green.

## 5. Release (author, after review)

Per the constitution's Release Workflow: open the pull request with the change summary, version
`1.0.0` and its reasoning, and the Chef's Pick align summary; after merge, tag `v1.0.0` on `main`.
