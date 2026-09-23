<!-- Source: Best-README-Template BLANK_README (Unlicense) — https://github.com/othneildrew/Best-README-Template -->
<a id="readme-top"></a>

# My Spec-Kit Workflow

[English](README.md) · **简体中文**

> 英文版是规范版本。本页与 [README.md](README.md) 不一致时，以英文版为准。

<!-- translation-of: README.md sha256:c8877f68ea3dccf0 -->

记录我的 Spec Kit 工作流：它的配置、技能、宪章，以及它们随时间的演进。

[![CI](https://github.com/anyingiit/my-speckit-workflow/actions/workflows/ci.yml/badge.svg)](https://github.com/anyingiit/my-speckit-workflow/actions/workflows/ci.yml)
[![License](https://img.shields.io/github/license/anyingiit/my-speckit-workflow)](LICENSE)

[报告问题](https://github.com/anyingiit/my-speckit-workflow/issues/new?template=bug_report.yml) · [功能建议](https://github.com/anyingiit/my-speckit-workflow/issues/new?template=feature_request.yml)

<details>
  <summary>目录</summary>
  <ol>
    <li><a href="#关于项目">关于项目</a></li>
    <li><a href="#快速开始">快速开始</a></li>
    <li><a href="#使用方法">使用方法</a></li>
    <li><a href="#参与贡献">参与贡献</a></li>
    <li><a href="#许可证">许可证</a></li>
    <li><a href="#联系方式">联系方式</a></li>
  </ol>
</details>

## 关于项目

记录我的 Spec Kit 工作流：它的配置、技能、宪章，以及它们随时间的演进。

计划中的功能和已知问题见 [open issues](https://github.com/anyingiit/my-speckit-workflow/issues)。

## 快速开始

### 前置条件

- **Spec Kit**：已在 1.0.6 版本上验证（版本锁定在
  [`.specify/init-options.json`](.specify/init-options.json)），需安装在你的项目中，并提供工作流提示词
  调用的命令：`/speckit-plan`、`/speckit-tasks`、`/speckit-analyze`、`/speckit-implement` 和
  `/speckit-converge`。
- **Claude Code**：用于执行提示词开头的 `/goal` 命令。本工作流已在 Claude Code 上验证；其他支持
  `/goal` 和 Spec Kit 命令的代理也可能可用，但未经验证。
- **已有的功能 spec**：用 `/speckit-specify` 编写（见[使用方法](#使用方法)）。

## 使用方法

只在 spec 准备完毕后使用这段工作流提示词：功能 spec 已用 `/speckit-specify` 写好，并且（如果你使用的话）
已用 `/speckit-clarify` 澄清。

完整的工作流分四步：

1. `/speckit-constitution` —— 确立项目原则。
2. `/speckit-specify` —— 编写功能 spec。
3. `/speckit-clarify` —— 可选：澄清 spec 中的待定问题。
4. 粘贴下方的工作流提示词 —— 它会循环执行 plan、tasks、analyze、implement 和 converge，直到功能完成。

**提示词做什么。** 它先运行 `/speckit-plan` 和 `/speckit-tasks`；如果 plan 和 tasks 已存在，则跳过这两步。
然后运行 `/speckit-analyze`，修复 plan 和 tasks 中所有 medium 及以上的问题，最多修复 20 轮，且从不修改
spec；如果问题的根源在 spec，它会停下来请你修改 spec。接着对未完成的任务运行 `/speckit-implement`，单个任务
失败不会中断；再运行 `/speckit-converge` 找出仍然缺失的部分；每个缺口都会写回 tasks 并重新循环，最多 10 轮。
修改 spec 后可以重新运行这段提示词。

**你会得到什么。** 一份状态摘要，列出已完成的任务、未完成的任务和与 spec 相关的问题。如果达到重试上限，或
spec 需要人工修改，摘要之前会附上一条报告消息。

提示词保留作者实际使用的中文原文。用代码块上的复制按钮复制：

<!-- workflow-prompt:start -->
**工作流版本**：v1.0.0

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

## 参与贡献

欢迎贡献。如何提交 issue 或 pull request 见 [CONTRIBUTING.md](CONTRIBUTING.md)，所有参与者应遵守的准则见 [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)。

请不要在公开的 issue 或 pull request 中报告安全问题。私下报告的方法见 [SECURITY.md](SECURITY.md)。

## 许可证

以 MIT 许可证发布。详见 [LICENSE](LICENSE)。

## 联系方式

项目地址：[https://github.com/anyingiit/my-speckit-workflow](https://github.com/anyingiit/my-speckit-workflow)

<p align="right">(<a href="#readme-top">回到顶部</a>)</p>
