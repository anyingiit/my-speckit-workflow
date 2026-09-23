# Align mode

Align brings an existing repository to the recommended form defined by the template snapshot. Follow [the safety rules](safety.md) throughout.

## 1. Find the starting point

Decide which of these the repository is. Check them in this order and stop at the first that matches:

| Starting point | How to tell |
|---|---|
| `empty` | The target does not exist, or it has no files and no commits. |
| `in-setup` | `.github/chefs-pick/` exists and contains `SETUP.md`. |
| `generated` | The first non-blank line of at least one project file is identical to the first non-blank line (the source comment) of the file with the same path in the snapshot. A project file is a file whose path also exists in the snapshot outside the guide layer (`.github/README*.md`, `.github/chefs-pick/`). |
| `foreign` | None of the above. |

Tell the user which starting point you found and why.

- `empty`: stop. Align needs something to align; suggest create mode instead.
- `in-setup`: the repository was made from the template but setup was never finished. Continue from the first unfinished step in the snapshot's `.github/chefs-pick/SETUP.md` rather than treating the guide layer as the user's own files.
- `generated` or `foreign`: build the gap report below.

Three special cases change how you treat what you find:

- **The repository is not on GitHub.** If the git remote is not on github.com, tell the user which modules depend on GitHub's own features, such as issue forms, the pull request template, Dependabot and the GitHub Actions workflow. Handle only the parts that do not depend on the platform, or stop if the user prefers. Never run a `gh` command in this case.
- **A file has the template's name but a different job.** For example, the repository's own `.github/workflows/ci.yml` already runs its tests. Treat such a file as the user's content: report how it differs from the snapshot, and never replace it.
- **The user chose an alternative.** A different license, Renovate instead of Dependabot (`renovate.json`), another tool doing a module's job, or the user's own file under the template's file name (a README the user wrote, for example) is a valid choice. Record it as `alternative`.

### Origin version

For a `generated` or `in-setup` repository, work out which template version it started from. Try these sources of evidence in order:

1. **`content-match`.** List the template's release tags with `git ls-remote --tags https://github.com/chefs-pick-oss-starter/chefs-pick-oss-starter`. For each `vX.Y.Z` tag, fetch that version with `git clone --depth 1 --branch vX.Y.Z` into a temporary directory. Replace its placeholders with the user's confirmed identity, then compare it with the repository's files. The version whose files match the user's unmodified files byte for byte is the origin. Several versions can ship identical project files, for example when a release changed only the guide layer. If more than one version matches, report all of them as candidates. They give the same gap report, so do not pick one.
2. **`changelog-line`.** The user's own `CHANGELOG.md` contains `Created from Chef's Pick OSS Starter vX.Y.Z`.
3. **`date`.** Use the method in the "Tracing the template version" section of the snapshot's `.github/chefs-pick/GUIDE.md`.

Tell the user which version you inferred and from which evidence. If the sources disagree, list what each one says and do not choose between them. If none of them gives an answer, record the origin as `unknown` and carry on: compare every file against the snapshot. An `unknown` origin never stops the run. Delete the temporary directories when you are done.

## 2. Build the gap report

Read the module list M01–M16 and each module's tier (required, recommended or optional) from "What you get" in the snapshot's `.github/README.md`. Then write one row per module with these fields:

| Field | Values |
|---|---|
| Module | M01–M16 |
| Tier | required / recommended / optional, from the snapshot's "What you get" |
| State | `missing` — not present · `matches` — identical to the snapshot once placeholders are replaced · `modified` — came from the template but has been changed · `alternative` — the user uses another solution · `outdated` — identical to the starting version, but the snapshot has changed since · `n/a` — the module ships no files (M10, for example) |
| Proposed action | `add` · `update` · `keep` · `remove` (only when the snapshot has removed the module) · `none` |
| Basis | The module's entry in the snapshot's `.github/chefs-pick/SOURCES.md`, or an entry in its `.github/chefs-pick/CHANGELOG.md` |
| User decision | `accepted` · `declined` · `deferred` |

Version changes need a basis:

- Every `outdated` or `remove` row must cite the specific entry in the snapshot's `.github/chefs-pick/CHANGELOG.md` that caused it. The entry must come from a version after the origin and no later than the snapshot. Give the version number and the entry's first sentence.
- Propose `remove` only when the snapshot has removed that module. Even when the user has `accepted` it, confirm once more before deleting anything.
- When the origin is `unknown`, record every row that would have been `outdated` as `modified` instead, because without an origin you cannot tell the user's own edits from template updates.

These rules always hold:

- The proposed action for an `alternative` row can only be `keep`, and for such a row `accepted` means "keep it as it is": nothing is written.
- A `modified` row is written only after the user marks that row `accepted`.
- An `n/a` row always has the action `none`.
- If every required and recommended row is `matches` or `n/a`, the repository needs nothing. Optional modules that are not installed are the user's choice: print the "nothing to change" line from [the summary rules](summary.md), add one line naming them, and stop. Offer them only if the user asks.

The report also covers two things outside the rows:

- **S06.** Language-specific additions (`.gitignore` rules, CI steps, Dependabot ecosystems) are listed under "For you to do" unless the user asks you to add them.
- **Links into kept files.** If a file you would add links to an anchor or section that does not exist in a file the user kept, such as `README.md#getting-started`, say so in the plan.

## 3. Agree the plan

Turn the gap report into a change plan: every file to add, update or remove, plus the placeholder replacements the added files need. Ask about each optional-tier module here, as part of the plan. Show the whole plan once, then take a decision on each item. Nothing is written before this.

## 4. Apply

- Write only the items marked `accepted` in §3. Ask no new questions here.
- Take each file you add from the file with the same path in the snapshot, then replace its placeholders using the snapshot's `.github/chefs-pick/SETUP.md` placeholder table and the identity details the user has confirmed.
- When the starting point is `in-setup` and you reach step S08, run the cleanup command from "Clean up when done" in the snapshot's `.github/README.md` once the user agrees. Read the command from the snapshot; it is not written here.

## 5. Never do

1. Never write `.github/README.md`, `.github/README.zh-CN.md` or anything under `.github/chefs-pick/` into the repository.
2. Never replace an alternative the user has chosen.
3. Never delete a file without the user's approval of that deletion.
