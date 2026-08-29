# Skill 产品经理

把“我想做一个 Skill”，直接推进成一个能安装、能复用、做过基本验证的 Skill。

你不用陪 AI 一路开会。它会先读懂现有上下文，确有必要时找 2–3 个成熟方案，自己做取舍，然后直接搭建和试跑。

## 它能帮你做什么

- 把重复工作、SOP、提示词或一次跑通的流程沉淀成 Skill。
- 快速调研同类 Skill，选择复用、改造或最小新建。
- 优化已有 Skill 的触发、流程和输出稳定性。
- 准备公开发布时，检查结构、隐私和兼容性。

它不会把一次性任务强行做成 Skill，也不会在你没同意时擅自发布。

## 安装

最简单的方式：

```bash
npx skills add kanshao2077/skill-product-manager
```

安装器会让你选择 Agent 和安装位置。

如果要一次装到几个常用 Agent：

```bash
npx skills add kanshao2077/skill-product-manager \
  --skill skill-product-manager -g \
  -a codex -a claude-code -a cursor -a gemini-cli -a opencode -y
```

安装后新开一个会话，让 Agent 重新加载 Skill。

不想用命令行，可以在 [Releases](https://github.com/kanshao2077/skill-product-manager/releases) 下载 ZIP，解压后把完整的 `skill-product-manager` 文件夹导入 Agent。根目录里的 `SKILL.md` 和其他文件要一起保留。

## 怎么用

直接说：

```text
把我这套流程做成一个 Skill。能合理假设就直接推进，只在会改变核心结果时问我。
```

想先看社区方案：

```text
用 Skill 产品经理做这个 Skill。先快速找成熟底子，选好后直接搭建并验证。
```

改造现有 Skill：

```text
用 Skill 产品经理优化这个 Skill，保留已经好用的部分，先不要发布。
```

## 默认流程

1. 先读聊天、素材和旧成果，不让你重复说明。
2. 需要时才看 2–3 个真正相关的方案。
3. 自己决定复用、改造、组合还是新建。
4. 做一次正常任务和一次边界任务。
5. 交付可安装版本；远程发布仍会单独确认。

简单需求直接做，不默认上大表格、重评测和连续追问。

## 跨 Agent 说明

核心使用标准 `SKILL.md` 和相对路径，不依赖 Codex 私有功能。`agents/openai.yaml` 只是 Codex 的可选界面信息，其他 Agent 可以忽略。

Vercel `skills` CLI 可以把它安装到多种 Agent 目录。当前已验证 Codex 本地调用和通用结构；Claude Code、Cursor、Gemini CLI、OpenCode 等宿主的自动触发与工具差异，仍以各平台实际表现为准。这里不虚假承诺“所有 Agent 百分百一键可用”。

宿主只要能读取 `SKILL.md` 和写文件，就能执行核心流程。联网只在外部调研时需要；Python 3 只用于可选结构检查，没有 Python 也能人工检查后继续。

## 验证

在 Skill 目录运行：

```bash
python3 scripts/validate_skill.py .
```

看到 `0 error(s), 0 warning(s)` 后，再拿一个真实流程试跑。

## 目录结构

```text
skill-product-manager/
├── SKILL.md              核心工作流
├── README.md             使用说明
├── LICENSE               MIT 许可证
├── agents/               可选宿主界面信息
├── evals/                触发边界样例
├── references/           需要时才读取的详细规则
├── reports/              设计来源和评测记录
└── scripts/              零依赖结构校验器
```

## 常见问题

- **装完没触发：** 新开会话，再明确说一次“用 Skill 产品经理”。
- **一直调研不动手：** 要求最多看 2–3 个方案，然后直接落地。
- **结构通过但不好用：** 用真实材料再跑一次；格式正确不等于行为有效。

## 更新、隐私和许可证

- 更新：`npx skills update skill-product-manager -g -y`
- 不要把 Token、Cookie、私人聊天或未授权附件放进公开 Skill。
- 外部调研会经过你正在使用的 Agent、模型和搜索工具，敏感内容先脱敏。
- 本项目使用 [MIT License](LICENSE)，可以使用、修改和分发，但请保留许可证与版权声明。

详细设计取舍见 [设计调研](reports/design-research.md)，本版本测试见 [评测记录](reports/evaluation.md)。
