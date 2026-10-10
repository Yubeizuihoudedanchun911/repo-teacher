# Repo Teacher 0.1.0 验证范围

## 结构与工具

- Codex skill-creator 的 quick_validate.py：通过。名称与 frontmatter 检查不代表教学质量。
- Python 标准库行为测试：11 项通过。覆盖盘点截断与排除、失效哈希、越界来源、行号、缺失链接、路径加行号、裸文件名被 URL 解析器误识别，以及运行证据记录要求。
- 两个工具只读输入、JSON 输出到 stdout；测试使用包内合成材料，不调用业务服务。
- 对固定版本的 Financial Services 仓库：40 文件预算时明确返回 inventory_complete=false、eligible_file_count=null；1,000 文件预算下返回 363 个文件条目。结构盘点不表示已理解 363 个文件。
- 包内部署教学示例：5 条关键结论、7 个源码引用通过 SHA-256、行号与固定 revision 核对；无云端 API 调用。远端链接、Mermaid 渲染和读者理解未由该工具验证。

## 场景试用

先进行了两个无技能基线试讲。它们已能正确区分部署、执行和运行证据；不能把这些已有能力归功于插件。

随后四个使用技能的试用：

1. **配置型插件**：给出文件读取者、提示词文字变化、技能引用变化、任务未启动的状态和变化条件练习。
2. **8 万文件 monorepo 情景**：使用题目给定资料形成范围地图，保留客户端绑定、外部 MQ 注册、生产开关与支付实现的未知范围。文件数量是情景条件，未构造或扫描 8 万个实际文件。
3. **真实 Financial Services 部署链**：独立读取实际源码，核对提示词文件头、路径解析基准、技能与子 Agent 转换。发现对话交付检查条件与本地行号链接两项缺口；修订后复核通过，并追加裸文件名行号漏检回归。
4. **TypeScript SDK 情景**：从业务程序调用进入讲解，将构建入口、SDK、Transport、编码、响应与测试替身分开；未编造编码格式或服务端行为。

这些是有限场景的行为试用，不是统计评测，也不能证明所有仓库或所有读者都能理解。尚无真实学习者的前后测或对照实验。CMU 方法映射见 [PEDAGOGY.md](PEDAGOGY.md)。

## 安装、打包与持续检查

核对了 codex-cli 0.145.0 的 marketplace add、plugin add 与 list 命令帮助，以及官方插件格式。包包含便携 manifest、Codex 兼容 manifest 与本地 marketplace；自身引用路径已检查。

实际桌面端加载与新会话调用尚未验收。项目测试和文件检查不能替代宿主安装测试；README 提供当前 CLI 的安装命令。

归档使用显式文件清单，排除编辑记录、缓存和运行时文件。`PACKAGE-CONTENTS.json` 保存除清单自身外的分发文件 SHA-256；检查时要求内容与这些哈希一致。包内示例与测试材料注明教学或合成用途。

GitHub Actions 工作流使用 Python 3.10 和 3.13 运行行为测试、核对 manifest 一致性与分发哈希。最新结果以 [仓库 Actions](https://github.com/Yubeizuihoudedanchun911/repo-teacher/actions) 为准；本文件不把尚未执行的未来 CI 视为通过。Actions 依赖固定的第三方 commit，工作流令牌仅授予 contents: read。
