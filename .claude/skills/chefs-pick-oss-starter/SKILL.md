---
name: chefs-pick-oss-starter
description: Create a new open source repository from the Chef's Pick OSS Starter template, or align an existing repository with it — adding missing community files, updating a repository made from an older template version, and walking through the setup checklist. Use when the user asks to start a repo from Chef's Pick, to "align", "update" or "bring up to standard" a repository against it, or pastes the Chef's Pick setup prompt.
license: MIT
compatibility: Requires git and read access to github.com. The GitHub CLI (gh), signed in, is optional and only used for repository settings the user approves one by one.
metadata:
  min-template-version: "1.1.0"
  template-repository: "https://github.com/chefs-pick-oss-starter/chefs-pick-oss-starter"
---

# Chef's Pick OSS Starter

## What this skill does

This skill works in one of two modes. **Create** makes a new repository from the Chef's Pick OSS Starter template: it starts from the template's current published content, fills in the project's own identity, walks the setup checklist, and removes the template's guide layer at the end.

**Align** brings an existing repository to the template's recommended form. The repository may never have used the template, or it may have been made from an older version of it. Align compares the repository module by module, explains every difference, and changes only what the user accepts.

Everything this skill knows about what the recommended form looks like comes from the template itself, fetched fresh at the start of every run. These instructions hold rules and steps only.

## Read the safety rules first

Before you write anything, read [the safety rules](references/safety.md) and follow them for the whole run.

## Get the template snapshot

Fetch the template's current published content as described in [the snapshot steps](references/snapshot.md); stop if you cannot.

## Choose the mode

First find the repository's starting point as described in section 1 of [the align steps](references/align.md).

- If the starting point is not `empty` and the user asked to create a new repository, refuse to create it. Write nothing, explain why, and suggest aligning the repository instead. Then stop and wait: enter align mode only after the user explicitly asks for it.
- If the starting point is `empty` and the user asked to create a new repository, use create mode and follow [the create steps](references/create.md).
- In every other case, use align mode and follow [the align steps](references/align.md).

## Repository settings

Handle the repository settings in the setup checklist (S02–S04) as described in [the settings steps](references/settings.md).

## Finish

End every run with a summary in the format given in [the summary rules](references/summary.md).
