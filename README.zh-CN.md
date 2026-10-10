# Repo Teacher

[English](README.md) · [教学原则对照](PEDAGOGY.md) · [教学示例](examples/financial-services/GUIDE.md)

一个根据真实仓库生成工程教学文档的 Codex 插件。默认读者懂一般编程，但没有看过这个工程的源码。

讲解从一个具体场景开始：谁读取了哪个文件，内容在每一步怎样变化，哪个程序负责执行，结果交给谁。先解释陌生概念，再介绍源码中的技术名字。源码机制、教学假设、测试结果和实际运行记录分别说明。

## 安装

使用支持插件的 Codex CLI：

```bash
codex plugin marketplace add Yubeizuihoudedanchun911/repo-teacher --ref v0.1.0
codex plugin add repo-teacher@repo-teacher-local
```

安装后，在新会话中使用 `$teach-repo`。命令能力以当前 `codex plugin --help` 为准；桌面端发现与刷新由宿主决定。

也可以克隆仓库或解压 [Release ZIP](https://github.com/Yubeizuihoudedanchun911/repo-teacher/releases)，将目录放在稳定位置，把第一条命令换成：

```bash
codex plugin marketplace add /absolute/path/to/repo-teacher
```

这些命令会修改用户的 Codex 配置和插件缓存。插件不会自动安装自己；编辑源目录后，已安装副本可能需要重新加载。

## 使用

```text
使用 $teach-repo，为 /path/to/repo 生成教学文档。
我懂编程但没读过源码，先讲一次请求如何完成，再解释特有文件。
```

```text
使用 $teach-repo，把这份看不懂的工程讲解重写。
重点检查缺失前提、术语、执行者和配置转换，中间步骤要有具体例子。
```

```text
使用 $teach-repo，讲解这个大型 monorepo。
先建立模块地图，再追踪下单主线与消息失败分支；
明确已经核实的范围和无法取得的外部实现。
```

支持生成、改写、更新三种模式。语言和格式服从用户请求。普通代码修改、单独绘图和简短 API 查阅不需要触发完整教学工作流。

## 教学方法与大型项目

先确认读者已经知道什么、希望学会什么；再找到真实入口，沿调用者、被调者、配置读取点、存储和输出追踪一个完整行为。文档用贯穿案例展示输入、中间状态和结果，并给出与学习目标对应的自测问题。

方法参考了 [CMU Eberly Center 的学习原则](https://www.cmu.edu/teaching/principles/learning.html)。[PEDAGOGY.md](PEDAGOGY.md) 逐项说明原则怎样落实到插件行为，以及哪些检查属于工程校验。项目与 CMU 无隶属关系，尚未测量真实读者的学习效果。

大型仓库先建立模块关系，再讲代表性链路，按需要扩展模块章节。文件盘点完成不代表读懂全部实现；跨仓库依赖、运行开关、有效配置和真实执行保持可见。详见 [大型仓库探索](skills/teach-repo/references/large-repos.md)。

## 配套工具

只需要 Python 3.10+ 标准库：

```bash
python3 skills/teach-repo/scripts/inspect_repo.py --repo /path/to/repo
python3 skills/teach-repo/scripts/check_lesson.py --repo /path/to/repo --lesson /path/to/GUIDE.md --evidence /path/to/evidence.json
python3 -B -m unittest discover -s tests -v
```

两个脚本只读本地输入，JSON 写到 stdout，不启动被讲解的应用、不安装业务依赖、不上传源码。

- `inspect_repo.py` 盘点元数据和入口候选；默认预算为 10,000 个文件、5,000 个目录、20 秒。它不解析全部代码，不证明调用关系；使用自身排除规则，不完整复现 Git 的忽略机制。
- `check_lesson.py` 核对本地来源、行号、内容哈希、revision 与文档链接；不能证明语义正确、生产执行成功或读者已经理解。远端 URL、标题锚点和图的实际渲染不在检查范围内。

AI 宿主可能通过自己的服务处理材料，本地脚本只读不代表整个 AI 工作流离线。

## 图、示例和验证

已有 Archify 时可配合绘图；缺少时使用 Mermaid 或文字步骤。插件没有打包 Archify，也不要求 MCP 服务器、外部账号或固定浏览器。

[Financial Services 教学片段](examples/financial-services/GUIDE.md) 配有固定版本的 [证据](examples/financial-services/evidence.json) 和 [覆盖范围](examples/financial-services/coverage.json)。示例解释文件读取者、字段变化，以及创建 Agent 与运行任务的区别；没有执行云端任务。

[VALIDATION.md](VALIDATION.md) 记录 11 项行为测试、有限场景试用和验证边界。GitHub Actions 使用 Python 3.10、3.13 检查工具，并核对包元数据与文件哈希。

## 参与和许可

参看 [贡献指南](CONTRIBUTING.md)、[行为准则](CODE_OF_CONDUCT.md)、[安全报告](SECURITY.md) 与 [更新记录](CHANGELOG.md)。提交教学反馈时说明不懂的句子、已有知识和想理解的行为，只提供获准披露的材料。

原创插件代码和文档采用 [MIT 许可](LICENSE)。Financial Services 示例中注明出处的上游 YAML 片段保留 Apache-2.0 许可，完整许可位于 [LICENSES/Apache-2.0.txt](LICENSES/Apache-2.0.txt)。详情见 [NOTICE](NOTICE) 和 [第三方说明](THIRD_PARTY_NOTICES.md)。CMU 原始网页与可选外部工具各自保留原有许可。

根 `plugin.json` 是便携声明，`.codex-plugin/plugin.json` 是 Codex 兼容声明，`.agents/plugins/marketplace.json` 是插件来源目录。结构参考 [OpenAI 插件打包文档](https://developers.openai.com/plugins/build/plugins)。
