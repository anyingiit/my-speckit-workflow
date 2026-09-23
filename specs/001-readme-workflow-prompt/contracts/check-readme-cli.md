# Contract: `tools/check_readme.py`

Command-line interface of the README consistency checker (FR-009). Python 3 standard library only;
run from the repository root.

## Invocations

| Command | Behavior | Exit code |
|---|---|---|
| `python3 tools/check_readme.py` | Runs checks L1–L4 from [readme-layout.md](readme-layout.md) | `0` all pass · `1` any fail · `2` a required file is missing |
| `python3 tools/check_readme.py --update-digest` | Rewrites the `translation-of` marker in `README.zh-CN.md` with the current `README.md` digest, then runs all checks | as above |
| `python3 tools/check_readme.py --print-prompt README.md` | Prints the prompt block of the given README to stdout, exactly, for manual comparison | `0` found · `1` layout error |
| `python3 tools/check_readme.py --root <dir>` | Same as above against another directory (used by tests) | as above |

## Output

- Success: one line, `README checks passed (workflow version X.Y.Z).`
- Failure: one line per failed check on stderr, in the form
  `<check>: <file>: <message>`, where `<check>` is `layout`, `prompt-identical`,
  `translation-current` or `version-matches`. Examples:
  - `prompt-identical: README.zh-CN.md: prompt block differs from README.md at line 4; copy the block from README.md`
  - `translation-current: README.zh-CN.md: marker sha256:1111111111111111 != README.md sha256:<actual>; update the translation, then run --update-digest`
  - `version-matches: README.md: label v1.0.0 != CHANGELOG.md latest release 1.1.0`
- All failing checks are reported in one run; the checker does not stop at the first failure.

## Rules

- Files are read as UTF-8; line endings are normalised to `\n` before comparing blocks.
- The digest is computed over the raw bytes of `README.md` (no normalisation).
- `--update-digest` modifies only the marker line and never touches `README.md`.

## CI usage

In `.github/workflows/ci.yml`:

- Triggers: `push` on every branch (the template's `branches: [main]` filter is removed),
  `pull_request` to `main`, and `workflow_dispatch`, so the checks run on every push and pull
  request (FR-009).
- `lint` job: a step running `python3 tools/check_readme.py`.
- `test` job: the placeholder step replaced by `python3 -m unittest discover -s tools/tests -v`.

No new actions are added; existing actions stay pinned to commit SHAs.
