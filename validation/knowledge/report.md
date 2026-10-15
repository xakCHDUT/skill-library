# 知识管理技能校验报告

日期：2026-10-15。

## 交付与范围

已准备 `defuddle`、`obsidian-markdown`、`obsidian-bases` 三项可公开发布的 Codex 适配稿。没有安装到用户技能目录，没有修改私人笔记，没有写入 GitHub。

技能上游固定为 `kepano/obsidian-skills@3ccff5338ea700537839b21900aa5358a0402c98`（2026-09-15）。下载了三个技能及其引用资源、MIT LICENSE，共 8 个上游文件；全部与 GitHub Git blob SHA-1 一致。原件及完整 SHA-256 清单保留在本次本地校验工作区；本库每个技能的 `PROVENANCE.md` 记录公开来源和原始 Git blob 哈希。

## 适配

- Defuddle：保留上游能力说明，新增本地 UTF-8 HTML 解析入口。通过 `useAsync: false` 关闭可选第三方内容回退；`--source-url` 仅作为元数据和相对链接基准。输出使用独占创建，已有文件不会被覆盖。原始 URL CLI 保留为明确说明联网行为的可选路径。
- Defuddle 依赖：官方 npm `defuddle@0.19.5`、`linkedom@0.18.12`，含完整 `package-lock.json`，独立目录安装，禁用安装脚本。未进行全局安装。用第二个空目录执行离线 `npm ci` 成功，随后测试通过。
- Obsidian Markdown：增加指定资料库范围、保留已有属性/链接和区分文件检查与宿主渲染的指导。
- Obsidian Bases：增加版本条件及验证边界。公开版 Bases 从 1.9.10 提供，分组、表格汇总与 List 视图从 1.10 提供；Maps 依赖另一个社区插件。未更改上游函数参考。
- 三项均保留 MIT LICENSE、固定版本来源、原件哈希、公开合成样例和实际验证 JSON。

## 实际验证

环境：Windows，Node.js 24.19.0，Python 3.12，PyYAML 6.0.3。

1. 三份 `SKILL.md` 均通过 Codex skill-creator 的 `quick_validate.py`。
2. Defuddle 8 项实际测试通过：中文正文与数字、文章元数据、导航/广告剔除、相对链接还原、Markdown 输出及页面脚本不执行、原输出文件保留、输入等于输出时保留原文、URL 输入拒绝、空 X 页面不触发 fetch 回退。其中第一项联合检查正文和元数据；测试总数为 8。
3. 合成 Obsidian 资料库的 12 项文件检查通过：三份 Markdown 的唯一键 YAML；属性类型；数字与日期；6 个笔记/标题/块/Base 嵌入目标；Base 的 YAML 结构和公式引用；字段存在性；重复 YAML 键、断链、丢失标题锚点、丢失块锚点、未定义公式、歧义过滤器等反例被拒绝。
4. Obsidian 两项复用同一组 12 项检查，不能累加为 24 项独立检查。
5. 发布目录已扫描本机用户名、绝对路径及常见凭据标记，未发现匹配。未复制 node_modules、运行环境、npm 日志或私人资料到发布目录。

## 明确未验证的部分

- 本次没有打开 Obsidian UI，没有验证公式实际求值或 Base 视图渲染。已发现 Obsidian 启动器及较新的 1.12.7 更新包，因此不能仅凭启动器的旧版本号判断用户软件不支持 Bases。
- Defuddle 本次验收使用公开合成 HTML；没有宣称所有网站、登录页、动态页或所有财报表格均可完整提取。
- 本地解析适配器只处理已有 HTML。用户指定网页的获取应由已授权浏览器/获取工具完成，不能把源码中的网页文字当作系统指令。

## 复现

Defuddle：在技能目录安装锁定依赖后，执行 `node --test --test-concurrency=1 tests/extract-local.test.mjs`。单独依赖目录可以通过 `DEFUDDLE_TEST_RUNTIME` 指定。

Obsidian：安装 `tests/requirements.txt` 后，执行 `python tests/validate_fixture.py tests/fixtures/vault`。这是样例文件检查器，不是通用 Obsidian 公式解释器或渲染器。

## 一手依据

- https://github.com/kepano/obsidian-skills/tree/3ccff5338ea700537839b21900aa5358a0402c98
- https://github.com/kepano/defuddle/tree/556d74e8c8fd68c49912d4b11a4ae9ec04d7b2b5
- https://github.com/kepano/defuddle#third-party-services
- https://obsidian.md/changelog/2025-08-18-desktop-v1.9.10/
- https://obsidian.md/changelog/2025-10-01-desktop-v1.10.0/
