# Skill Library · 个人技能库

精选的科研、公文与单位写作、财务研究、演示汇报、Notebook 和知识整理技能。每项保留来源、固定版本、许可证、适配记录与实际校验材料。

**当前收录 12 项，校验日期 2026-10-15。** 完整开源仓库保存在 6 个公开 fork；这里管理经过选择与适配的技能。校验范围限于下表，不能延伸为对整个上游仓库的认可。

## 按用途选择

| 技能 | 适合解决什么问题 | 当前验证范围 |
|---|---|---|
| [official-document-drafting](skills/official-document-drafting) | 请示、报告、通知、纪要与工作材料起草，导出可编辑 Word | 23 项导出与保护检查；4 份 Word 打开及渲染通过，另有 1 个独立纪要案例 |
| [nsfc-benzi-audit](skills/nsfc-benzi-audit) | 审查已有国自然本子、科学问题与验证逻辑、修改稿复审 | 8 项结构测试、4 项复算；2 份作者审查及 1 个独立复审案例，限文本路线 |
| [thesis-tracker](skills/thesis-tracker) | 留存原始投资观点，用新披露检验支持与反证 | 2 组作者案例及 47 项自检；1 个独立历史案例、8 项复算，未做收益回测 |
| [exploratory-data-analysis](skills/exploratory-data-analysis) | 先看懂数据结构、缺失值、异常与分布 | 33 项测试通过、1 项权限跳过；另做合成数据复算，修复原始数据覆盖及 Windows 链接路径问题 |
| [statistical-analysis](skills/statistical-analysis) | 选择统计检验、检查前提并解释结果 | 33 项测试通过，另做合成结果复算；可选贝叶斯采样及 Linux 未验证 |
| [model-update](skills/model-update) | 财报发布后更新季度与全年盈利预测 | 2 个独立合成场景通过：140 条直接断言及 10 条报告审查 |
| [sector-overview](skills/sector-overview) | 界定行业、比较公司与估算市场份额 | 2 个独立合成场景通过：101 条直接断言及 10 条报告审查 |
| [scientific-slides](skills/scientific-slides) | 科研汇报、组会与答辩的证据叙事和可编辑 PPTX | 19 项文件及异常检查、1 项 Windows 路径回归通过；3 页渲染复核完成，PowerPoint 应用内编辑未验证 |
| [jupyter-notebook](skills/jupyter-notebook) | 创建可复现的实验或教学 Notebook | 17 项 CLI、格式、算术、独立内核运行检查通过 |
| [defuddle](skills/defuddle) | 把网页 HTML 整理为正文与 Markdown | 8 项合成 HTML 测试通过；锁定依赖，避免覆盖原文 |
| [obsidian-markdown](skills/obsidian-markdown) | 整理带属性、双链和嵌入的笔记 | 与 Bases 共用 12 项文件检查；应用内渲染未验证 |
| [obsidian-bases](skills/obsidian-bases) | 为笔记建立筛选、公式和表格视图 | 与 Markdown 共用同组 12 项检查；公式求值与界面未验证 |

报告：[公文](validation/gongwen/report.md) · [国自然审查](validation/nsfc/report.md) · [观点跟踪](validation/thesis/report.md) · [科研 PPT](validation/ppt/report.md) · [科研](validation/research/report.md) · [金融](validation/finance/report.md) · [Notebook](skills/jupyter-notebook/validation/README.md) · [知识管理](validation/knowledge/report.md)。金融案例是合成数据行为测试，不是投资收益回测。上游工具可运行也不代表所有真实数据任务都会正确。

## 上游与个人 fork

| 来源 | 个人公开 fork | 固定版本 |
|---|---|---|
| [OpenAI Skills](https://github.com/openai/skills) | [xakCHDUT/openai-skills](https://github.com/xakCHDUT/openai-skills) | `49f948faa9258a0c61caceaf225e179651397431` |
| [K-Dense Scientific Agent Skills](https://github.com/K-Dense-AI/scientific-agent-skills) | [xakCHDUT/scientific-agent-skills](https://github.com/xakCHDUT/scientific-agent-skills) | `a1043ef544e3a100c28e70a736b6cf32554d0677` |
| [Anthropic Financial Services](https://github.com/anthropics/financial-services) | [xakCHDUT/financial-services](https://github.com/xakCHDUT/financial-services) | `574ed3624aebd0418c7e96cd101262f30210ab26` |
| [Kepano Obsidian Skills](https://github.com/kepano/obsidian-skills) | [xakCHDUT/obsidian-skills](https://github.com/xakCHDUT/obsidian-skills) | `3ccff5338ea700537839b21900aa5358a0402c98` |
| [Official Document Drafting](https://github.com/zhaohui-yang/official-document-drafting) | [xakCHDUT/official-document-drafting](https://github.com/xakCHDUT/official-document-drafting) | `6b4166a50b96733684b36da6336ea85a847cf3be` |
| [NSFC Benzi Audit](https://github.com/jiankang1991/nsfc-benzi-audit) | [xakCHDUT/nsfc-benzi-audit](https://github.com/xakCHDUT/nsfc-benzi-audit) | `9a6010b94a165473f3c4ad71a522b7957381ed5e` |

个人 fork 保留上游主分支，便于后续同步；本库的 `skills/` 保存适配版本。版本与状态的机器可读目录在 [catalog.json](catalog.json)。更新流程见 [MAINTENANCE.md](MAINTENANCE.md)，上游检查工具只检查新版本，不自动合并或安装。

## 使用与安装

这些目录已为单独安装整理。本轮仅做隔离校验和 GitHub 归档，未安装到当前 Codex。可以在 Codex 中说：

> 从 xakCHDUT/skill-library 安装 skills/jupyter-notebook，只安装这一项；先检查是否与现有同名技能冲突。

安装时选择需要的具体目录；若要重现本次结果，使用本库相应提交版本，并按每项说明建立独立依赖环境。科研脚本需要 Python 依赖，Defuddle 需要 Node.js；金融两项主要使用宿主已有工具，Notebook 建立脚手架只需要 Python 标准库。公文导出器使用 Python 标准库并调用本机可用字体，字体不随包分发；国自然与观点跟踪的纯文本路线可用宿主现有能力。Obsidian 应用内效果需另行验证。

## 维护约定与许可证

- 来源和适配都可追溯：每项有 `PROVENANCE.md` 与原许可证，固定上游提交后再验证。
- 保留合成输入、真实输出和检查程序；没有完成的运行或宿主效果直接标注。
- 本库只收录公开开源来源及原创适配，不包含私人笔记、课程资料、账号凭据或运行环境。
- [根目录 MIT 许可证](LICENSE) 适用于原创管理代码和文档。各技能遵循其自身 MIT／Apache-2.0 许可证，详见 [第三方声明](THIRD_PARTY_NOTICES.md)。
