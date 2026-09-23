# Create mode

Create makes a new repository from the template snapshot. Follow [the safety rules](safety.md) throughout.

## 1. Confirm the target is empty

Create runs only on an empty target: the target directory does not exist, or it has no files and no commits. A clone of a new, empty GitHub repository counts as empty: it has only its `.git` directory and no commits.

If the target has any file or any commit, refuse. Write nothing, tell the user why, and suggest aligning the repository instead ([the align steps](align.md)). Then stop and wait for the user's choice. Never switch to align mode on your own.

The same applies when the repository is to be created on GitHub and the name is already taken there. Check with `gh repo view <owner>/<name>` before creating anything, and if it exists, treat the target as not empty.

## 2. Agree the plan

Before creating anything, gather every answer the plan depends on. That means the identity values from the placeholder table in the snapshot's `.github/chefs-pick/SETUP.md`, the project's language (for S06), a keep-or-remove decision for each recommended and each optional module (S07 asks for both; required modules always stay), whether to create the repository on GitHub, and whether each commit may be pushed. Where you can, infer a value first, for example the owner and name from the git remote or the copyright holder from `git config user.name`. Show each inferred value for confirmation, and ask for anything you cannot infer.

Then show the complete plan once and take the user's approval before any step below. A module the user removes needs no placeholder replacement, so leave its placeholders out of the plan.

## 3. Create

The new repository's default branch is always `main`, because the template's CI runs only on `main`.

Use the first of these that applies.

- **The user wants the repository on GitHub, and `gh auth status` succeeds.** Ask the user for the owner, the name and the visibility, and get their approval to create the repository on GitHub. This is a remote operation, so it needs its own approval. Then run:

  ```sh
  gh repo create <owner>/<name> --template chefs-pick-oss-starter/chefs-pick-oss-starter --clone --<visibility>
  ```

  Afterwards, confirm the clone is on `main`.

- **The user wants the repository on GitHub, but `gh auth status` fails.** Do not fall back to a local repository on your own. Tell the user that the GitHub CLI is not signed in, and offer two choices: they sign in themselves (never run `gh auth login` for them) and ask again, or they explicitly approve creating a local repository instead, which changes the plan. Wait for their answer.

- **The target is a clone of an existing empty GitHub repository** (it has an `origin` remote and no commits). Do not run `gh repo create`. Switch the empty clone to `main` first (`git symbolic-ref HEAD refs/heads/main`), then copy the snapshot's file tree into it, leaving out the snapshot's own `.git`, and commit once with the message `Initial commit`. Pushing is a separate remote operation that needs its own approval.

- **Otherwise** (the user wants a local repository only). Copy the snapshot's file tree into the target, leaving out the snapshot's own `.git`. Run `git init -b main` and commit once with the message `Initial commit`.

A repository made from the template on GitHub also starts with exactly one commit. Keeping that shape means the template-version tracing described in the snapshot's module guide still works.

## 4. Fill in the project identity

Replace the placeholders in the files the placeholder table lists, using the values agreed in step 2. Remove the files of every recommended or optional module the user declined, following the "Remove" notes in the snapshot's `.github/chefs-pick/GUIDE.md`. Commit the result with the message `chore: fill in project identity`. Pushing that commit is a separate remote operation and needs its own approval.

## 5. Walk the local steps

Go through S01, S05, S06 and S07 of the snapshot's setup checklist in that order, using the answers from step 2. After each step, run that step's "How to verify" check.

Handle S02–S04 as described in [the settings steps](settings.md).

## 6. Remove the guide layer

Once the user agrees, run the cleanup command given under "Clean up when done" in the snapshot's `.github/README.md`. Read the command from the snapshot; it is not written here. Afterwards, run the final placeholder search given in the snapshot's `.github/chefs-pick/SETUP.md` (the one for after the guide layer is removed) and confirm it prints nothing.
