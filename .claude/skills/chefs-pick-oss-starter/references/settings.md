# Repository settings

Steps S02, S03 and S04 of the snapshot's setup checklist are settings on GitHub, not files. You may change them for the user through the GitHub CLI, but only under these rules:

- First run `gh auth status`. If it fails, skip every `gh` command below and give all three as manual steps instead. Never install `gh`, never run `gh auth login`, and never ask the user for a token.
- Then check that the signed-in account can administer the repository: `gh api repos/OWNER/REPO --jq .permissions.admin` must print `true`. If it does not, give all three as manual steps.
- Each setting needs its own approval. Approving one says nothing about the others.
- If a command fails, for example because the user is not an admin of the repository, mark that setting `failed` and give its manual step.
- After applying a setting, run its check. Report it as applied only if the check confirms it.

For every setting, the manual step is the "Step" text of the matching row in the snapshot's `.github/chefs-pick/SETUP.md`, and the way to confirm it is that row's "How to verify" text.

## S02 Description and topics

1. **Tell the user** the description and topics you would set, and that they show on the repository's home page.
2. **Ask** for approval of this setting alone.
3. **Apply**: `gh repo edit OWNER/REPO -d "…" --add-topic a,b`
4. **Check**: `gh api repos/OWNER/REPO --jq '.description'` and `gh api repos/OWNER/REPO/topics`
5. **Manual step**: S02 in the snapshot's setup checklist.

Enabling reported content for a repository owned by an organization has no API. It is always a manual step.

## S03 Private vulnerability reporting

1. **Tell the user** that this lets people report security issues privately from the Security tab, and that it needs admin rights.
2. **Ask** for approval of this setting alone.
3. **Apply**: `gh api -X PUT repos/OWNER/REPO/private-vulnerability-reporting`
4. **Check**: `gh api repos/OWNER/REPO/private-vulnerability-reporting` returns `{"enabled": true}`
5. **Manual step**: S03 in the snapshot's setup checklist.

## S04 Discussions

1. **Tell the user** that this turns on the Discussions tab, which the issue forms and `CONTRIBUTING.md` point to for questions.
2. **Ask** for approval of this setting alone.
3. **Apply**: `gh repo edit OWNER/REPO --enable-discussions`
4. **Check**: `gh api repos/OWNER/REPO --jq '.has_discussions'` returns `true`
5. **Manual step**: S04 in the snapshot's setup checklist.

Two different answers are possible here. If the user only declines to have you turn Discussions on, give the manual step and leave the files alone. If the user does not want Discussions at all, follow S04 in the snapshot: point the discussions link in `.github/ISSUE_TEMPLATE/config.yml` and the Questions section of `CONTRIBUTING.md` at the user's own support channel. These are file changes, so each needs approval first.
