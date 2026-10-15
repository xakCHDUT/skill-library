# Skill Library · 个人技能库

精选的科研、财务研究、Notebook 和知识整理技能。每项保留来源、固定版本、许可证、适配记录与实际校验材料。

**当前收录 8 项，校验日期 2026-10-15。** 完整开源仓库保存在 4 个公开 fork；这里管理经过选择与适配的技能。校验范围限于下表，不能延伸为对整个上游仓库的认可。

## 按用途选择

| 技能 | 适合解决什么问题 | 当前验证范围 |
|---|---|---|
| [exploratory-data-analysis](skills/exploratory-data-analysis) | 先看懂数据结构、缺失值、异常与分布 | 33 项测试通过、1 项权限跳过；另做合成数据复算，修复原始数据覆盖及 Windows 链接路径问题 |
| [statistical-analysis](skills/statistical-analysis) | 选择统计检验、检查前提并解释结果 | 33 项测试通过，另做合成结果复算；可选贝叶斯采样及 Linux 未验证 |
| [model-update](skills/model-update) | 财报发布后更新季度与全年盈利预测 | 2 个独立合成场景通过：140 条直接断言及 10 条报告审查 |
| [sector-overview](skills/sector-overview) | 界定行业、比较公司与估算市场份额 | 2 个独立合成场景通过：101 条直接断言及 10 条报告审查 |
| [jupyter-notebook](skills/jupyter-notebook) | 创建可复现的实验或教学 Notebook | 17 项 CLI、格式、算术、独立内核运行检查通过 |
| [defuddle](skills/defuddle) | 把网页 HTML 整理为正文与 Markdown | 8 项合成 HTML 测试通过；锁定依赖，避免覆盖原文 |
| [obsidian-markdown](skills/obsidian-markdown) | 整理带属性、双链和嵌入的笔记 | 与 Bases 共用 12 项文件检查；应用内渲染未验证 |
| [obsidian-bases](skills/obsidian-bases) | 为笔记建立筛选、公式和表格视图 | 与 Markdown 共用同组 12 项检查；公式求值与界面未验证 |

报告：[科研](validation/research/report.md) · [金融](validation/finance/report.md) · [Notebook](skills/jupyter-notebook/validation/README.md) · [知识管理](validation/knowledge/report.md)。金融案例是合成数据行为测试，不是投资收益回测。上游工具可运行也不代表所有真实数据任务都会正确。

## 上游与个人 fork

| 来源 | 个人公开 fork | 固定版本 |
|---|---|---|
| [OpenAI Skills](https://github.com/openai/skills) | [xakCHDUT/openai-skills](https://github.com/xakCHDUT/openai-skills) | `49f948faa9258a0c61caceaf225e179651397431` |
| [K-Dense Scientific Agent Skills](https://github.com/K-Dense-AI/scientific-agent-skills) | [xakCHDUT/scientific-agent-skills](https://github.com/xakCHDUT/scientific-agent-skills) | `a1043ef544e3a100c28e70a736b6cf32554d0677` |
| [Anthropic Financial Services](https://github.com/anthropics/financial-services) | [xakCHDUT/financial-services](https://github.com/xakCHDUT/financial-services) | `574ed3624aebd0418c7e96cd101262f30210ab26` |
| [Kepano Obsidian Skills](https://github.com/kepano/obsidian-skills) | [xakCHDUT/obsidian-skills](https://github.com/xakCHDUT/obsidian-skills) | `3ccff5338ea700537839b21900aa5358a0402c98` |

个人 fork 保留上游主分支，便于后续同步；本库的 `skills/` 保存适配版本。版本与状态的机器可读目录在 [catalog.json](catalog.json)。更新流程见 [MAINTENANCE.md](MAINTENANCE.md)，上游检查工具只检查新版本，不自动合并或安装。

## 使用与安装

这些目录已为单独安装整理。本轮仅做隔离校验和 GitHub 归档，未安装到当前 Codex。可以在 Codex 中说：

> 从 xakCHDUT/skill-library 安装 skills/jupyter-notebook，只安装这一项；先检查是否与现有同名技能冲突。

安装时选择需要的具体目录；若要重现本次结果，使用本库相应提交版本，并按每项说明建立独立依赖环境。科研脚本需要 Python 依赖，Defuddle 需要 Node.js；金融两项主要使用宿主已有工具，Notebook 建立脚手架只需要 Python 标准库。Obsidian 应用内效果需另行验证。

## 维护约定与许可证

- 来源和适配都可追溯：每项有 `PROVENANCE.md` 与原许可证，固定上游提交后再验证。
- 保留合成输入、真实输出和检查程序；没有完成的运行或宿主效果直接标注。
- 本库只收录公开开源来源及原创适配，不包含私人笔记、课程资料、账号凭据或运行环境。
- [根目录 MIT 许可证](LICENSE) 适用于原创管理代码和文档。各技能遵循其自身 MIT／Apache-2.0 许可证，详见 [第三方声明](THIRD_PARTY_NOTICES.md)。
