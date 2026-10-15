# Scientific-slides 专项校验

2026-10-15，范围为中文科研叙事与可编辑 PPTX 路线。上游版本固定为 `a1043ef544e3a100c28e70a736b6cf32554d0677`。MIT 许可证已按同一提交的仓库根文件核验并保留。

## 结果

- 生成 3 页中文合成汇报：研究问题、数据图表、结论与局限。数据为对照组 20/24/30、训练组 22/30/39 项/分钟，明确标注合成，未杜撰作者、机构、引文或统计显著性。
- **19 项文件和拒绝路径检查通过**：页数、16:9、原生中文文本、每页合成标注、证据边界、演讲备注、原生图表、系列值、类别、页内几何、内嵌工作簿、无整页栅格替代、ZIP CRC、正常文件，以及空页、损坏、缺失、未知格式、缺解析器的拒绝行为。完整清单见 `results.json`。
- **Windows 中文及 emoji 路径回归通过**：GBK 输出环境下，上游验证器退出 1，适配后退出 0，见 `unicode-cli.json`。这是单独的第 20 项运行检查。
- **LibreOffice 导出 PDF 成功，3 页均已渲染并逐页目视检查**。首次图表的数据标签有局部拥挤，改为轴刻度、原生数据及侧边差值后复核通过。内容复核还将首页的“反应速度”纠正为“训练过程中的任务完成量”，与项/分钟这一实际指标一致，数据不变。中文、图例、证据边界和结论未见截断或非预期遮挡。
- Codex `quick_validate.py` 通过；Windows 运行该系统检查器时设置 `PYTHONUTF8=1`。

## 实际修复

1. 上游在缺少 python-pptx 时仍把检查标为通过，零页 PPTX 也通过。两种情况均已先复现，再修正为失败；未知扩展名同样不再误报有效。PDF 缺解析器共享相同修正，但 PDF 的完整负向路径未专项测试。
2. 上游 PPT 入口把付费 AI 配图列为必经步骤，并强制依赖同仓库的 research-lookup。适配入口优先使用宿主已有演示工具、可编辑图表和原始科研图，外部技能和付费图片均为可选路线。参考文件保留，并明确其中配图、引用数量、页数是可选示例，不能替代用户要求。
3. 前置 metadata 适配 Codex，验证器统一 UTF-8 输出，避免路径中的 emoji 使验证在打印阶段中断。

## 可复现环境与运行

实际使用 Windows、Python 3.12、python-pptx 1.0.2、Node.js 24、PptxGenJS 4.0.1、LibreOffice 26.2.3.2、Poppler。未安装或调用任何有费用的 AI 图片 API。字体使用本机 Microsoft YaHei，未在仓库中复制字体。

下列命令从技能库根目录运行。依赖应装入任务自己的环境；Node 依赖放在 `validation/ppt`，Python 依赖放在独立虚拟环境。原生宿主工具可替代这些制作依赖。

```text
npm install --prefix validation/ppt --no-save pptxgenjs@4.0.1
python -m pip install python-pptx==1.0.2
node validation/ppt/make_synthetic_deck.cjs work/ppt-test/synthetic-research.pptx
python validation/ppt/check_deck.py work/ppt-test/synthetic-research.pptx skills/scientific-slides/scripts/validate_presentation.py work/ppt-test/results.json
soffice --headless --convert-to pdf --outdir work/ppt-test work/ppt-test/synthetic-research.pptx
pdftoppm -scale-to 1400 -png work/ppt-test/synthetic-research.pdf work/ppt-test/slide
```

`make_synthetic_deck.cjs` 拒绝覆盖既有输出，重跑时使用新路径。`check_deck.py` 在结果文件的父目录创建并清理临时反例。生成的 PPTX、PDF 和预览图保留于本地交付目录，公共仓库只保留制作脚本、结果、版本信息和本报告。

## 尚未验证

没有在 PowerPoint 应用中打开、人工编辑或保存，不能声称 PowerPoint UI 验收通过。可编辑性结论来自原生文本、原生 chart 和内嵌工作簿的文件检查。未检验屏幕阅读器顺序、跨平台字体替换、真实研究的科学准确性、AI 图片、Beamer、全部上游脚本或模板。格式检查与一个合成案例不代表全部科研报告质量保证。
