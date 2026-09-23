# Getting the template snapshot

The snapshot is the template's current published content. It is the only source for what the recommended form looks like. Never work from memory, from an earlier run, or from any other copy of the template.

## Steps

1. Clone the template's default branch into a temporary directory:

   ```sh
   git clone --depth 1 https://github.com/chefs-pick-oss-starter/chefs-pick-oss-starter <temporary-directory>
   ```

   The default branch is the current published version. Do not fetch a tag instead.

2. Read the snapshot's version: the highest `## [X.Y.Z] - YYYY-MM-DD` heading in `.github/chefs-pick/CHANGELOG.md` inside the snapshot. Tell the user which version you are working from.

3. Read these files from the snapshot as you need them:

   | File in the snapshot | What it gives you |
   |---|---|
   | `.github/chefs-pick/SETUP.md` | The placeholder table and the setup steps S01–S09, each with how to verify it |
   | `.github/chefs-pick/SOURCES.md` | The pick for each module and the reasons behind it |
   | `.github/chefs-pick/CHANGELOG.md` | What changed in each template version, and why |
   | `.github/README.md` | The module list with its tiers ("What you get") and the cleanup command ("Clean up when done") |

4. If any step above fails, stop. Write nothing to the user's repository, and tell the user what failed and why.

   In Codex, network access is off by default. Ask the user to allow it, for example by restarting with -c sandbox_workspace_write.network_access=true, and try again. Do not continue from memory or from any other copy of the template.

5. Compare the snapshot's major version with the major version of `min-template-version` in this skill's metadata. If the snapshot's major version is higher, tell the user these instructions may be out of date for that template version, and carry out only the steps these instructions clearly cover.

6. When the run ends, delete the temporary directory.
