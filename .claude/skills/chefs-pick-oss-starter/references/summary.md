# Run summary

End every run — finished, declined or interrupted — with a summary in these four sections, in this order.

### Done

Every change you made: each file added, changed or deleted, and each repository setting you applied. One line per item, naming the file or setting.

### Declined or skipped

Every proposed item that was not carried out, and why: the user declined it, deferred it, or the run stopped before reaching it.

### For you to do

Every step the user still has to do themselves, such as a repository setting that has to be changed on the web. For each one, give the step and add the matching "How to verify" text from the snapshot's `.github/chefs-pick/SETUP.md`, so the user can check it is done.

### Final check (S09)

The result of each check in step S09 of the snapshot's setup checklist. Mark each one as passed, failed, or not yet possible, and say why for anything not passed.

## When nothing needs to change

If an align run finds the repository already matches the snapshot, do not print the four sections. Print only this line, with the snapshot's version:

`Nothing to change: this repository already matches template vX.Y.Z.`

If some optional modules are not installed, add one more line naming them, for example `Optional modules not installed: M15 Code owners, M16 Funding.`

## When the run stops before the snapshot

If the run stops before the template snapshot is fetched, because of a network failure, uncommitted changes the user wants to deal with first, or anything else, still print all four sections. Where a section needs text from the snapshot (a "How to verify" line or the S09 checks), write `Not possible yet: the template was not fetched.` and say what the user needs to do before running again.
