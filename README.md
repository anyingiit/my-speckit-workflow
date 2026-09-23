<!-- Source: Best-README-Template BLANK_README (Unlicense) — https://github.com/othneildrew/Best-README-Template -->
<a id="readme-top"></a>

# My Spec-Kit Workflow

**English** · [简体中文](README.zh-CN.md)

A record of my Spec Kit workflow: its configuration, skills, constitution, and how they evolve over time.

[![CI](https://github.com/anyingiit/my-speckit-workflow/actions/workflows/ci.yml/badge.svg)](https://github.com/anyingiit/my-speckit-workflow/actions/workflows/ci.yml)
[![License](https://img.shields.io/github/license/anyingiit/my-speckit-workflow)](LICENSE)

[Report a bug](https://github.com/anyingiit/my-speckit-workflow/issues/new?template=bug_report.yml) · [Request a feature](https://github.com/anyingiit/my-speckit-workflow/issues/new?template=feature_request.yml)

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#getting-started">Getting Started</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

## About The Project

A record of my Spec Kit workflow: its configuration, skills, constitution, and how they evolve over time.

See the [open issues](https://github.com/anyingiit/my-speckit-workflow/issues) for planned features and known issues.

## Getting Started

### Prerequisites

- **Spec Kit**, verified with version 1.0.6 (pinned in
  [`.specify/init-options.json`](.specify/init-options.json)), installed in your project and
  providing the commands the workflow prompt calls: `/speckit-plan`, `/speckit-tasks`,
  `/speckit-analyze`, `/speckit-implement` and `/speckit-converge`.
- **Claude Code** to run the prompt's leading `/goal` command. The workflow is verified with
  Claude Code; other agents that support `/goal` and the Spec Kit commands may work but are
  unverified.
- **An existing feature spec**, written with `/speckit-specify` (see [Usage](#usage)).

## Usage

Use the workflow prompt only after specification work is finished: the feature spec has been
written with `/speckit-specify` and, if you use it, clarified with `/speckit-clarify`.

The whole workflow runs in four steps:

1. `/speckit-constitution` — set the project's principles.
2. `/speckit-specify` — write the feature spec.
3. `/speckit-clarify` — optional: resolve open questions in the spec.
4. Paste the workflow prompt below — it runs plan, tasks, analyze, implement and converge in a
   loop until the feature is done.

**What the prompt does.** It runs `/speckit-plan` and `/speckit-tasks`, skipping both when a plan
and tasks already exist. It then runs `/speckit-analyze` and fixes every medium or higher issue in
the plan and tasks, up to 20 fix rounds, without ever editing the spec; if an issue comes from the
spec itself, it stops and asks you to fix the spec. Next it runs `/speckit-implement` on the
unfinished tasks, continuing past individual failures, and `/speckit-converge` to find anything
still missing; each gap goes back into the tasks and the loop repeats, up to 10 gap rounds. You
can rerun the prompt after changing the spec.

**What you get back.** A status summary of completed tasks, unfinished tasks and spec-related
issues. When a retry limit is reached, or the spec needs manual changes, a report message comes
before the summary.

The prompt is intentionally kept in its original Chinese, exactly as the author uses it. Copy it
with the copy button on the block:

<!-- workflow-prompt:start -->
**Workflow version**: v1.0.0

```text
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
```
<!-- workflow-prompt:end -->

## Contributing

Contributions are welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md) for how to open an issue or a pull request, and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for the standards expected of everyone taking part.

Please do not report security issues in public issues or pull requests. [SECURITY.md](SECURITY.md) explains how to report them privately.

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for details.

## Contact

Project link: [https://github.com/anyingiit/my-speckit-workflow](https://github.com/anyingiit/my-speckit-workflow)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
