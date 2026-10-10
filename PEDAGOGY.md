# Learning principles and repository teaching

Repo Teacher references the [CMU Eberly Center Learning Principles](https://www.cmu.edu/teaching/principles/learning.html) and [Teaching Principles](https://www.cmu.edu/teaching/principles/teaching.html). The mappings below are this project's engineering interpretation, written for repository onboarding. They are not a CMU certification or evidence that this plugin improves learning outcomes.

## CMU 学习原则怎样应用

| 概念 | 本项目的应用 |
|---|---|
| 已有知识影响学习 | 识别读者基础；首次使用特有字段时先补必要前提 |
| 知识组织影响运用 | 用系统地图与一条因果链连接文件、执行者和状态 |
| 学习目标影响投入 | 从读者真正想理解的行为选择案例与阅读路线 |
| 分项能力需要整合 | 先理解文件读取和数据转换，再贯穿一次完整任务 |
| 练习需要针对性反馈 | 改变条件让读者预测结果，提供答案并修复首个理解断点 |
| 学习环境影响体验 | 允许提出不懂之处，根据读者经验调整解释方式 |
| 学习者需要自我监控 | 提供复述、自检和深读路线，区分已理解与待确认问题 |

These choices connect to the learner profile and modes in [teach-repo](skills/teach-repo/SKILL.md), the worked-example and feedback guidance in [teaching.md](skills/teach-repo/references/teaching.md), and the staged exploration in [large-repos.md](skills/teach-repo/references/large-repos.md).

A chapter's goal, example, and self-check should address the same mechanism: if the goal is understanding how a local path becomes remote prompt text, show the before/after request and ask what happens if the referenced file changes. This also reflects CMU's teaching guidance on aligning goals, activities, and assessment.

## What is implementation and what is evidence

The skill implements an authoring workflow. It does not measure a learner's knowledge or motivation automatically. The limited forward trials in [VALIDATION.md](VALIDATION.md) assess agent behavior, not learner mastery.

Source hashes, line-range checks, configuration/runtime boundaries, and coverage records are this project's engineering verification methods. They complement teaching; they are not presented as CMU research findings.

## Attribution and licensing boundary

CMU's linked pages identify their own CC BY-NC-SA 4.0 terms. This project includes links and independently written application notes, not copies of the webpage prose, diagrams, or logos. The MIT license does not replace third-party terms. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
