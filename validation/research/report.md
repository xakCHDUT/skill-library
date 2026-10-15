# 科研候选验收

结论：两项均可在本机使用，已完成必要修复并放入发布暂存目录；没有安装到当前 Codex，也没有写 GitHub。

固定上游为 `K-Dense-AI/scientific-agent-skills`，提交 `a1043ef544e3a100c28e70a736b6cf32554d0677`（2026-10-12）。源目录分别为 `skills/exploratory-data-analysis`、`skills/statistical-analysis`。许可证为 MIT。原版 39 个文件（技能、上游测试与必需基础设施、许可）逐一核对 Git blob SHA 后保存在本次本地工作区，未随公开库复制。公开的 `source-manifest.json` 提供固定提交与逐文件哈希，可从上游重新取得；原版没有被覆盖。

| 项目 | 原版结果 | 最终结果 | 改动 |
|---|---|---|---|
| exploratory-data-analysis 1.4，fork revision 1 | 25 通过、2 失败、1 跳过 | 33 通过、1 跳过 | 修复同名 JSON 输出覆盖原始数据；在解析真实路径前拒绝符号链接/Windows junction；明确 Windows 继承目录 ACL；兼容 Codex 元数据校验 |
| statistical-analysis 2.0，fork revision 1 | 32 通过 | 33 通过 | 补充 Pingouin CI95 默认仅两位小数的精度处理；兼容 Codex 元数据校验。未改统计算法 |

最终共 **66 个 pytest 用例通过，1 个跳过**；另有 **30 个真实合成任务检查通过**。pytest subtest 数未重复累加。两项 Codex frontmatter 校验均通过。

EDA 原版的两个 Windows 测试问题分别是把 POSIX `0600` 模式直接用于 Windows 断言，以及测试自己打开的 NumPy 内存映射未关闭导致临时文件无法删除。已仅在测试副本中修正平台断言和句柄释放，保留原始失败日志。原版直接 symlink 测试因 Windows 未授予该权限跳过；新增用例使用真实 Windows junction，分别验证输入、输出和 root 路径，三项全部通过。没有把跳过项算通过。

实际任务使用 12 行自造 CSV，正确识别 2 个缺失值、1 个植入极端值、1 个跨训练/测试集重复受试者；计算均值 105.1、中位数 6.5，原始文件哈希不变。CSV/JSON 核心命令在 Python `-S`（禁用第三方 site-packages）下实际运行。缺失文件、不规则 CSV、非有限 JSON 和尝试以 `--force` 覆盖原始 JSON 均以错误状态退出；已有输出未获覆盖授权时保留原内容。

统计任务以独立公式复算 Welch t 值、自由度、p 值、置信区间及有符号效应量：均差 2.68055556，t=0.72365317，df=10.68247917，p=0.48482386，95% CI=[-5.50199589, 10.86310700]，Cohen d=0.33592835；样本量规划向上取整为每组 64。合成回归准确恢复截距 2、斜率 3，实际生成并查看四联诊断图，内容清晰、无溢出。数据不足以支持均值有差异，也不证明效应为零。

最初复算发现 Pingouin 默认 CI95 仅保留两位小数；这属于依赖默认行为。对小单位变量会显示近似零宽区间，因此技能示例现显式保留完整计算精度，最后呈现时再按变量单位舍入。新增微量级数据回归用例与 SciPy 独立区间一致。

触发范围人工核对：EDA 用于实际本地研究文件的建模前体检，不代替年报估值或论文润色；statistics 用于研究数据检验、假设诊断和规划，不代替 DOI 检索或图形排版。账号/API：两项已测范围均不需要账号；执行期间无网络/付费调用。

复现：使用 Python 3.12 独立环境，安装每项 `validation/requirements-tested.txt` 后，从技能目录运行 `python -m pytest validation` 可复现新增回归。完整上游测试需要取回本报告固定提交、应用同目录的 `skill-changes.patch` 与 `windows-test-compatibility.patch`；完整命令见 `REPRODUCE.md`。每个技能分别执行 `python -m pytest tests/<skill>`，不要把多个技能放在同一 pytest 进程里。环境快照是 Windows 实测依赖集合，不是跨平台完整锁文件；核心 EDA 无需安装这些第三方包。

限制：未在本轮 Linux 环境重新跑测试；统计的可选 PyMC/ArviZ 贝叶斯采样未安装或执行。EDA 的参考级别格式仍不代表自动支持，统计诊断不证明独立性、因果关系或模型正确。公开证据只有合成数据、版本、相对路径及上游链接，不含本机用户名、绝对路径或虚拟环境。

可公开机器结果：`validation.json`。两个发布目录内各有 `LICENSE.md`、`PROVENANCE.md`、`validation/validation.json`、测试依赖清单及新增回归测试。
