# My Spec-Kit Workflow Constitution

## Core Principles

### I. 默认公开（Public by Default）

本仓库是公开仓库，提交的每一个文件都视为对外发布的内容。

- 任何提交 MUST NOT 包含密钥、令牌、密码、个人隐私信息或本机绝对路径（如
  `/Users/<name>/...`）。
- 示例与配置 MUST 使用占位符或通用路径，使陌生读者无需作者的本机环境即可理解。
- 文档 MUST 面向外部读者书写：读者仅凭仓库内容就能看懂工作流的目的与用法。

**理由**：公开内容一旦推送即可能被缓存或索引，无法真正撤回；面向外部读者书写也是
这个仓库存在的意义。

### II. 工作流即产品（Workflow as the Product）

本仓库的核心交付物是"我的 spec-kit 工作流"本身，而不是某个应用程序。

- 工作流的组成部分（Spec Kit 配置、`.specify/` 下的模板与脚本、`.claude/skills/`
  下的技能、宪章本身）MUST 纳入版本控制。
- 对工作流的每一次调整 MUST 说明"改了什么"和"为什么改"，并能从提交记录或变更日志中
  追溯。
- 引入的第三方技能或工具 MUST 在文档中注明来源与用途。

**理由**：记录工作流的价值在于可追溯的演进过程，只有结果而没有原因的记录无法复用。

### III. 版本改动必经 Chef's Pick 文档同步（NON-NEGOTIABLE）

所有版本改动 MUST 使用 `chefs-pick-oss-starter` 技能更新仓库文档。

- 每次发布新版本（即产生新的版本号或 tag）之前，MUST 运行 `chefs-pick-oss-starter`
  技能，以其当次获取的最新模板快照为准，对仓库文档与社区文件执行对齐（align）。
- 对齐结果中每一项的决定（`accepted` / `declined` / `deferred`）MUST 记录在该版本的
  PR 描述或变更日志中；被拒绝或推迟的项 MUST 附简短理由。
- 作者有意采用的替代方案（如不同的许可证或自写的 README）是合法选择，MUST 保留并记为
  `alternative`，不得被模板覆盖。
- 模板的引导层（`.github/README*.md`、`.github/chefs-pick/`）MUST NOT 提交进本仓库。
- 未完成文档对齐的改动 MUST NOT 打版本号或发布。

**理由**：以统一、可重复的方式维护开源文档，避免文档随版本漂移，也让读者始终看到符合
开源社区惯例的仓库形态。

### IV. 语义化版本与变更记录

- 仓库版本 MUST 遵循语义化版本（`MAJOR.MINOR.PATCH`），并以 `vX.Y.Z` 形式打 git tag。
  - MAJOR：工作流中不兼容的改变（如删除或重定义某个阶段、命令或约定）。
  - MINOR：新增命令、技能、模板或实质性扩展的指引。
  - PATCH：措辞、错别字、不改变行为的修正。
- 每个版本 MUST 在 `CHANGELOG.md` 中有对应条目，说明改动内容与原因。
- 提交信息 SHOULD 遵循 Conventional Commits（如 `docs:`、`feat:`、`chore:`），以便
  生成与核对变更日志。

**理由**：版本号与变更日志让读者快速判断某次更新是否影响其对工作流的复用。

### V. 可复现与版本锁定

- 工作流依赖的工具版本 MUST 被锁定并提交：Spec Kit 版本记录于
  `.specify/init-options.json`，第三方技能记录于 `skills-lock.json`（含来源与哈希）。
- 升级 Spec Kit 或任一被锁定的技能 MUST 视为一次版本改动，适用原则 III 与原则 IV。
- 仓库中自动生成的文件 MUST 由其生成工具重新生成，而非手工修改；若确需手工修改，
  MUST 在变更日志中注明。

**理由**：他人照着仓库复现工作流时，只有锁定的版本才能得到相同的结果。

## 仓库内容边界

- **属于本仓库**：Spec Kit 配置与模板、Claude Code 技能与设置、工作流说明文档、
  由 `chefs-pick-oss-starter` 管理的社区文件（README、LICENSE、CONTRIBUTING、
  CHANGELOG 等）、以及用于演示工作流的示例 spec。
- **不属于本仓库**：私有项目的真实代码或需求、任何凭据、个人机器专属配置
  （如 `settings.local.json`）、临时产物与缓存。
- 演示用的 spec、plan、tasks 等产物 MUST 使用虚构或已公开的示例内容。

## 版本发布流程

每次版本改动按以下顺序进行：

1. 在独立分支（或 worktree）上完成工作流改动，提交信息说明改动与原因。
2. 如改动涉及治理原则，先通过 `/speckit-constitution` 修订本宪章。
3. 运行 `chefs-pick-oss-starter` 技能对齐仓库文档，逐项决定并应用对齐计划（原则 III）。
4. 按原则 IV 确定新版本号，更新 `CHANGELOG.md`。
5. 发起 PR；PR 描述 MUST 包含：改动摘要、版本号及其理由、Chef's Pick 对齐结果摘要。
6. 合并后在 `main` 上打 `vX.Y.Z` tag。

## Governance

- 本宪章优先于仓库内的其他约定与习惯；两者冲突时以本宪章为准。
- **修订流程**：宪章修订 MUST 通过 `/speckit-constitution` 进行，并在 PR 中说明修订内容、
  版本号变化及理由。宪章文件顶部的 Sync Impact Report 仅供评审，提交前 SHOULD 移除。
- **宪章版本策略**：
  - MAJOR：删除原则或以不兼容方式重定义原则或治理规则。
  - MINOR：新增原则或章节，或实质性扩展既有指引。
  - PATCH：澄清、措辞与错别字等非语义修改。
- **合规检查**：每个 PR 在合并前 MUST 自查是否符合本宪章，重点核对原则 I（无敏感信息）
  与原则 III（已完成 Chef's Pick 文档对齐）。`/speckit-plan` 的 Constitution Check
  MUST 以本宪章为依据。

**Version**: 1.0.0 | **Ratified**: 2026-09-23 | **Last Amended**: 2026-09-23
