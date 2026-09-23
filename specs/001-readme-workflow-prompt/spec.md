# Feature Specification: Copyable Workflow Prompt in the README

**Feature Branch**: `claude/speckit-constitution-workflow-1f7fe3`

**Created**: 2026-09-23

**Status**: Draft

**Input**: User description: "用户可以在readme完整看到我的spec-kit工作流并复制。当前版本的完整内容为" followed by
the workflow prompt below, which is the **canonical content of the current workflow version**
and is reproduced here verbatim:

````text
/goal 按照顺序串行执行。

0. 如果plan和tasks已存在（例如修改spec后重跑），跳转到3
1. /speckit-plan
2. /speckit-tasks
3. /speckit-analyze
4. 确认是否有medium及以上的问题（不满足第2步要求的任务也视为medium问题）。如果有问题的根源在spec（如需求模糊、冲突或缺失，需指出spec的具体条目），跳转到10，并携带“以下问题需要人工修改spec”的报告消息（附问题清单）；如果只有其他问题，跳转到5；无问题跳转到6
5. 如果本步骤已执行满20次（每次进入第6步时计数清零），跳转到10，并携带“为什么对计划反复修复了20次都无法完整修复”的报告消息；否则修复medium及以上的问题（只修改plan和tasks，使其与spec保持一致，不得修改spec，不得改变任务的完成状态），然后跳转到3
6. /speckit-implement 只执行未完成的任务，单个任务失败不中断，失败任务保持未完成状态，交由后续converge处理。
7. /speckit-converge
8. 确认是否有缺口，如果有缺口跳转到9，无缺口跳转到10
9. 如果本步骤已执行满10次，跳转到10，并携带“为什么反复修复了10次缺口后仍然有缺口”的报告消息；否则确认每个缺口都已写入tasks（新增任务或将相关任务重新标记为未完成，并记录上一轮失败的原因），然后跳转到3
10. 输出状态摘要（已完成任务、未完成任务、spec相关问题）；有报告消息则附在摘要之前
11. Done，结束goal
````

## Clarifications

### Session 2026-09-23

- Q: Besides the `/goal` prompt itself, should the README also describe the whole workflow (from
  `/speckit-constitution` through `/speckit-specify` and `/speckit-clarify` to pasting the prompt)?
  → A: Yes — a short numbered overview of the whole cycle (constitution → specify → clarify → paste
  the `/goal` prompt), with the prompt shown in full as one of its steps; the README must make
  clear that the prompt is used only once specification work is finished.
- Q: What version number does the first published workflow get? → A: v1.0.0, as the first stable
  release; the workflow version is the repository version (no separate numbering).
- Q: Where in the README does the workflow go? → A: In the existing template sections — "Usage"
  holds the workflow overview and the complete prompt; "Getting Started" lists the prerequisites.
- Q: Should the README's prerequisites state a Spec Kit version? → A: Yes — "verified with Spec Kit
  1.0.6", linking to the repository file that pins that version; updated whenever Spec Kit is
  upgraded.
- Q: Should the prerequisites name the agent that runs the prompt's `/goal` command? → A: Name
  Claude Code as the verified agent, and state that other agents supporting `/goal` and the Spec
  Kit commands may also work but are unverified.
- Q: Should CI automatically check README consistency before release? → A: Yes, all three checks:
  the prompt is identical in both READMEs, the Chinese README's `translation-of` marker matches the
  current English README, and the README version label matches the latest `CHANGELOG.md` version.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Copy the complete workflow prompt from the README (Priority: P1)

A visitor opens the repository's front page (the README) and, without leaving the page or opening
any other file, sees the complete workflow prompt of the current version in a single block. They
copy it in one action and paste it into their coding agent, getting exactly the text the author
uses.

**Why this priority**: This is the whole point of the feature: the workflow is the repository's
product (Constitution Principle II), and a reader who cannot see and copy it gets no value.

**Independent Test**: Open the README as a first-time visitor, copy the prompt block with the
page's copy control (or by selecting the block), paste it into a plain text editor, and compare it
character by character with the canonical prompt in this spec's Input.

**Acceptance Scenarios**:

1. **Given** a visitor on the README, **When** they open "Usage" from the table of contents,
   **Then** they find the full workflow prompt, with no step omitted, abbreviated, or hidden behind
   a link.
2. **Given** the prompt block is displayed, **When** the visitor copies it in one action, **Then**
   the pasted text is identical to the canonical prompt: same steps 0–11, same wording, same
   punctuation (including full-width quotation marks and parentheses), and same line breaks.
3. **Given** the README is viewed on the repository hosting site, **When** the prompt block
   renders, **Then** none of its characters are reinterpreted as formatting (no numbered-list
   reflow, no lost slashes, no merged lines).

---

### User Story 2 - Understand when and how to use the prompt (Priority: P2)

Before copying, a visitor who has never used this workflow reads a short explanation next to the
prompt: what the prompt does, what must already be in place, at which point of the Spec Kit cycle
to paste it, and what they get back when it finishes.

**Why this priority**: A copied prompt that fails because a prerequisite is missing, or that is run
at the wrong moment, wastes the reader's time; but the prompt remains usable by experienced Spec
Kit users even without this explanation, so it ranks below P1.

**Independent Test**: Give the README to someone familiar with coding agents but new to this
repository; after reading only the README, they can state the prerequisites, the moment to run the
prompt, and what its final output contains.

**Acceptance Scenarios**:

1. **Given** a visitor reading the README, **When** they look for prerequisites, **Then** the
   "Getting Started" section lists them: Spec Kit (verified with version 1.0.6) installed in their
   project with the commands the prompt calls (`/speckit-plan`, `/speckit-tasks`, `/speckit-analyze`, `/speckit-implement`,
   `/speckit-converge`), Claude Code as the verified agent for the prompt's leading `/goal` command
   (other agents that support `/goal` and the Spec Kit commands may work but are marked
   unverified), and an existing feature spec.
2. **Given** a visitor who wants to know when to run it, **When** they read the section, **Then** it
   states explicitly that the prompt is used only after specification work is finished (the spec
   has been written with `/speckit-specify` and, if used, clarified with `/speckit-clarify`), and
   that it can be rerun after the spec changes.
3. **Given** a visitor who wants to know the outcome, **When** they read the section, **Then** it
   states that the run ends with a status summary of completed tasks, unfinished tasks, and
   spec-related issues, preceded by a report message when a retry limit was hit or the spec needs
   manual changes.
4. **Given** a visitor who wants the whole picture, **When** they read the section, **Then** they
   see a short numbered overview of the full cycle — `/speckit-constitution` → `/speckit-specify`
   → `/speckit-clarify` → paste the `/goal` prompt — with the prompt shown in full at its step.

---

### User Story 3 - Know which version of the workflow is shown (Priority: P3)

A returning visitor wants to know whether the prompt has changed since they last copied it. The
prompt section names the workflow version it shows, and the changelog records what changed in each
version and why.

**Why this priority**: Useful for repeat readers and required by the constitution's versioning
rules (Principle IV), but a first-time reader gets full value without it.

**Independent Test**: Compare the version named in the prompt section with the latest released
entry in the changelog; they match, and that changelog entry describes the prompt's introduction or
latest change.

**Acceptance Scenarios**:

1. **Given** the prompt section, **When** a visitor reads its heading or caption, **Then** it names
   the workflow version shown.
2. **Given** the changelog, **When** a visitor looks up that version, **Then** its entry states what
   changed in the workflow prompt and why.

---

### User Story 4 - Read the same workflow in Chinese (Priority: P3)

A Chinese-speaking visitor switches to the Simplified Chinese README and finds the same prompt
section, the same version, and a Chinese explanation, as required by Constitution Principle VI.

**Why this priority**: Required by the constitution for every README change, but it mirrors
Stories 1–3 rather than adding new value.

**Independent Test**: Follow the language switcher from the English README to the Chinese README
and back; both show the same version label and a prompt block, and the Chinese page carries the
canonical-English notice and the `translation-of` marker matching the current English README.

**Acceptance Scenarios**:

1. **Given** the English README, **When** the visitor uses the language switcher, **Then** they
   reach the Chinese README, which contains the prompt section with the same version label.
2. **Given** the Chinese README, **When** it is compared with the English README, **Then** its
   `translation-of` marker matches the English README's current digest.

---

### Edge Cases

- The prompt contains its own slash commands and a numbered list starting at 0; if rendered as
  normal page text instead of a verbatim block, numbering and slashes could be altered. The block
  MUST be displayed verbatim.
- The prompt contains full-width punctuation (“ ” （ ） ，) and mixed Chinese/English text; copying
  MUST NOT convert or drop these characters.
- A future workflow version changes the prompt: the README, the Chinese README, and the changelog
  would drift apart if only one is updated. All three MUST change together in the same version
  change (Constitution Principles IV and VI), and the CI checks in FR-009 fail if they do not.
- A visitor copies only part of the block by hand-selecting text: out of scope; a one-action copy
  of the whole block is the supported path.
- On the English README the prompt is in Chinese while the page is in English (see FR-003): the
  page MUST make clear which text is the prompt to copy and which is explanation, so an English
  reader knows what the prompt does without reading it.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The README MUST show the complete workflow prompt of the current version in its
  existing "Usage" section, reachable from the README's table of contents; "Usage" replaces its
  placeholder content with the workflow overview (FR-004a) and the prompt. The README MUST NOT add
  a new top-level section for the workflow.
- **FR-001a**: The README's existing "Getting Started" section MUST list the prerequisites from
  User Story 2 (acceptance scenario 1) in place of its generic clone instructions. The prerequisites
  MUST state the Spec Kit version the workflow was verified with (currently 1.0.6) and link to
  the repository file that pins it (`.specify/init-options.json`); this statement MUST be updated
  in the same version change whenever the pinned Spec Kit version changes (Constitution
  Principle V). They MUST also name Claude Code as the agent the workflow was verified with, and
  state that other agents supporting the `/goal` command and the Spec Kit commands may work but
  are unverified.
- **FR-002**: The prompt MUST be displayed as a single verbatim block that visitors can copy in one
  action, and the copied text MUST be identical, character for character and line for line, to the
  canonical prompt of that version.
- **FR-003**: Both the English README and the Chinese README MUST show the prompt in its original
  Chinese text, exactly as the canonical prompt; the prompt MUST NOT be translated. Only the
  surrounding explanation is written in each README's own language, and the English README MUST
  state that the prompt is intentionally kept in its original Chinese.
- **FR-004**: The prompt section MUST explain, in the README's language, what the prompt does, its
  prerequisites, when in the Spec Kit cycle to run it, and what its final output contains (see
  User Story 2 acceptance scenarios). It MUST state explicitly that the prompt is used only after
  specification work (`/speckit-specify`, and `/speckit-clarify` if used) is finished.
- **FR-004a**: The README MUST present a short numbered overview of the whole workflow cycle —
  `/speckit-constitution` → `/speckit-specify` → `/speckit-clarify` → paste the `/goal` prompt —
  with the complete prompt block placed at its step. The earlier steps are named and briefly
  described, not given their own copyable prompt blocks; the `/goal` prompt remains the only
  copyable block of the workflow.
- **FR-005**: The prompt section MUST name the workflow version it shows, and that version MUST
  match an entry in `CHANGELOG.md` describing the change to the prompt and its reason. The workflow
  version is the repository version; the prompt given in Input is published as `v1.0.0`, recorded
  as the `1.0.0` changelog entry and tagged `v1.0.0`.
- **FR-006**: The Simplified Chinese README MUST contain the equivalent prompt section with the same
  version label, the language switcher, the canonical-English notice, and an up-to-date
  `translation-of` marker, per Constitution Principle VI.
- **FR-007**: The README and its Chinese translation MUST NOT contain secrets, private personal
  information, or local absolute paths (Constitution Principle I).
- **FR-008**: Any later change to the prompt MUST update the README prompt section, the Chinese
  README, and the changelog in the same version change.
- **FR-009**: The repository's continuous integration MUST run on every push and pull request and
  fail when any of these checks fails:
  1. The prompt block in `README.zh-CN.md` is identical, character for character, to the prompt
     block in `README.md`.
  2. The `translation-of` marker in `README.zh-CN.md` matches the digest of the current
     `README.md`.
  3. The workflow version named in both READMEs equals the highest released version in
     `CHANGELOG.md`.
  A failure MUST name which check failed and which file to fix.

### Key Entities

- **Workflow Prompt**: The text a visitor pastes into their agent to run the plan → tasks →
  analyze → implement → converge loop. Attributes: version, text (canonical content given in
  Input, in Chinese, shown untranslated in both READMEs).
- **Workflow Version**: The version number of the repository release in which a given prompt text
  was published; links the README prompt section to a changelog entry.
- **README pair**: The English `README.md` (canonical) and its Simplified Chinese translation
  `README.zh-CN.md`, which must show the same prompt version.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A first-time visitor finds and copies the complete prompt within 30 seconds of
  opening the README.
- **SC-002**: 100% of copies taken with the block's one-action copy control are identical to the
  canonical prompt (zero character or line differences).
- **SC-003**: After reading only the README, a reader new to the repository correctly names the
  prerequisites, the moment to run the prompt, and the contents of its final output (3 of 3).
- **SC-004**: The version shown in the English README, the version shown in the Chinese README, and
  the latest released changelog entry agree in 100% of released versions.
- **SC-005**: A change that leaves the two READMEs' prompts different, the Chinese README's
  translation marker outdated, or the README version out of step with the changelog is flagged by
  CI 100% of the time, before it can be merged.

## Assumptions

- The README targets readers on the public repository hosting site (GitHub), whose Markdown
  rendering offers a copy control on verbatim blocks.
- The README is the single place where readers get the prompt; no separate download or install
  step is required.
- The explanation around the prompt is a concise overview (purpose, prerequisites, when to run,
  output), not a line-by-line commentary on each of steps 0–11. The workflow overview names the
  earlier Spec Kit steps without documenting those commands in depth.
- The prompt text given in Input is the first published workflow version, `v1.0.0`; later changes
  to the prompt bump the version under Constitution Principle IV.
- The prompt's leading `/goal` command is provided by the agent, not by Spec Kit; the README names
  Claude Code as the verified agent but does not document Claude Code or any other agent itself.
- The release follows the constitution's Release Workflow, including the Chef's Pick documentation
  align (Principle III).
