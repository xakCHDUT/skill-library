# 来源与适配

- 原项目：[zhaohui-yang/official-document-drafting](https://github.com/zhaohui-yang/official-document-drafting)
- 固定提交：`6b4166a50b96733684b36da6336ea85a847cf3be`，2026-08-19；2026-10-15 获取。
- 原样 fork：[xakCHDUT/official-document-drafting](https://github.com/xakCHDUT/official-document-drafting)。本目录为单独适配版本，不是上游原样副本。
- 许可：保留原 `LICENSE`，MIT 仅适用于原项目代码与文档；第三方字体及其他二进制不因此获得授权。本适配包没有复制任何字体、图片、示例 Word 或其他二进制。

保留 `dist/skill/references` 的 22 类文种和 6 类共享参考、必要的字体/版式文本配置、文种元数据，以及原有 Python 标准库导出器。移除在线采集子技能、离线提示词打包器、重复样例、字体下载/安装脚本和所有宿主代理配置。没有改动用户模型、权限、全局配置或已安装技能。

主要改动：

1. 入口改为 Codex 按需读取；共享规则与脚本全部自包含。导出器的文种配置直接引用本包文种参考，不依赖仓库外目录或重复规范文件。
2. 明确学校、企事业日常材料的适用语境；保留预算来源、批准状态、不确定性和日期地点缺口；报告与请示混杂时说明分写处理，不悄悄删去审批诉求。固定句数、附注等上游习惯不作为全部单位的硬性要求。
3. 输出位置改为当前任务目录；不写主目录。移除丢失字体文件的路径声明，只使用字体名称配置，不安装字体。`official-standard` 配置和首页隐藏页码不作为完全符合国标的承诺。
4. 导出器默认拒绝覆盖，`--overwrite` 为显式更新；拒绝输入/图片同路径、同文件别名与符号链接输出；临时文件唯一，失败不损坏旧输出，默认提交在 Windows 使用不覆盖的重命名、POSIX 使用不覆盖的硬链接。保留 Python 3.11+ 标准库运行路径。
5. 标题标记为 Word `Title` 样式，统一黑色，不继承装饰线；CLI 输出为 UTF-8，避免中文路径输出失败。

原始保留文件的路径与 SHA-256 在技能库 `validation/gongwen/source-manifest.json`。验证范围、改动依据、可复现材料和未覆盖项见 `validation/gongwen/report.md`；该报告不等于对全部 22 文种、国标或所有 Word 环境的认证。
