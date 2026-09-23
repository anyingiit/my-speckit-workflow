# Safety rules

These rules apply to every run, in both modes. When a step elsewhere seems to conflict with them, these rules win.

1. Before writing anything, show the user the complete change plan — every file you would add, change or delete, and why — and wait for their approval.
2. Never overwrite, rewrite or delete a file that already exists in the repository unless the user has explicitly approved that change to that file.
3. If the working tree has uncommitted changes, tell the user and ask them to commit or stash first. Continue only after they explicitly say you may.
4. Do not push, force-push, rewrite existing commit history, or do anything else that changes a remote repository. The only exceptions are the repository settings the user approves one by one as described in [the settings steps](settings.md), and a specific remote operation the user explicitly asks for.
5. Ask only for the identity details the plan will actually use, for example not a copyright holder when the user keeps their own license. Use only project identity details the user has given or confirmed. When you infer a value — an owner name from the git remote, for example — show it and ask the user to confirm it. When you cannot infer a value, ask for it. Never make one up.
6. Never write the template author's identity into the user's repository: not the template repository's owner, its copyright holder, its sponsor links, nor its contact details.
7. One approval covers one item. Never treat approval of one change or setting as approval of any other.
8. Write only the files in the approved plan. Do not run the project's code unless the user asks, and if one of your own checks creates a by-product such as `__pycache__/`, remove it before you finish.
9. If the user declines or interrupts, stop. Leave the changes already made in place for them to review, do not leave any file half-written, and report what was done and what was not, following [the summary rules](summary.md).
