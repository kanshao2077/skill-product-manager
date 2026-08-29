# Skill 产品经理

你只管说一句“把这件事做成 Skill”，剩下的调研、选型、搭建和最小验证，让 Agent 自己跑完。

很多人做 Skill 的过程是：先和 AI 聊半天，再找模板，再反复改 `SKILL.md`，最后还不知道到底能不能用。这个 Skill 做的事，就是把这段流程压短：能从现有上下文判断的就直接判断，能复用成熟方案的就不重新造，只有真的会影响结果时才问你。

## 它适合什么情况

- 你有一套经常重复的工作，想固化成 Skill。
- 你只有一个想法，希望 Agent 自己找同类方案并做出来。
- 你已经有 Skill，但触发不准、流程太重或结果不稳定。
- 你准备公开一个 Skill，想先检查结构、兼容性和发布风险。

它不会把普通的一次性任务强行做成 Skill，也不会在你没同意时擅自发布到 GitHub、SkillHub 或商店。

## 一条命令安装

电脑已经安装 Node.js 时，可以使用开源的 `skills` 命令行工具。

小白最稳的装法，是让安装器先识别并询问你要装到哪个 Agent：

```bash
npx skills add kanshao2077/skill-product-manager
```

也可以明确指定一个 Agent，并全局安装：

```bash
# Codex
npx skills add kanshao2077/skill-product-manager --skill skill-product-manager -g -a codex -y

# Claude Code
npx skills add kanshao2077/skill-product-manager --skill skill-product-manager -g -a claude-code -y

# Cursor
npx skills add kanshao2077/skill-product-manager --skill skill-product-manager -g -a cursor -y

# Gemini CLI
npx skills add kanshao2077/skill-product-manager --skill skill-product-manager -g -a gemini-cli -y

# OpenCode
npx skills add kanshao2077/skill-product-manager --skill skill-product-manager -g -a opencode -y
```

安装后新开一次会话，让 Agent 重新加载 Skill。

想确认全局安装器把它放到了哪里，可以运行：

```bash
npx skills ls -g -a codex -a claude-code -a cursor -a gemini-cli -a opencode
```

确实想一次装到 CLI 登记的全部 Agent 时，只建议在一个项目里使用：

```bash
npx skills add kanshao2077/skill-product-manager --skill skill-product-manager -a '*' -y
```

这会创建很多 Agent 目录，不适合作为日常默认命令。不要和 `-g` 一起使用：当前 CLI 有少数 Agent 不支持全局 Skills 目录。安装到目录也不代表每个 Agent 的实际工具能力都已经验证。

## 不想用命令行？

1. 在 [Releases](https://github.com/kanshao2077/skill-product-manager/releases) 下载最新版 ZIP。
2. 解压后保留完整的 `skill-product-manager` 文件夹。
3. 用你的 Agent 的“导入 Skill”功能选择这个文件夹；如果它没有导入按钮，就把该文件夹复制到它的 Skills 目录。
4. 确认文件夹根目录能看到 `SKILL.md`，不要只复制其中一个文件。
5. 新开会话后，用下面的示例试一次。

只要宿主能识别标准 `SKILL.md`、读取相对路径里的文件，并能完成普通文件操作，就能使用核心流程。联网调研、运行脚本和远程发布仍取决于宿主有没有相应工具与权限。

## 怎么叫它干活

最省事的说法：

```text
把我这套流程做成一个 Skill。能合理假设就直接推进，只在会改变核心结果时问我。
```

想先找社区方案：

```text
用 Skill 产品经理把这个想法做成 Skill。先快速看看有没有成熟底子，选好后直接搭建并验证。
```

改造现有 Skill：

```text
用 Skill 产品经理检查并改造这个 Skill。保留已经好用的部分，重点修触发边界和输出稳定性，先不要发布。
```

## 它实际怎么做

默认只有五步：

1. 先读现有聊天、素材和旧成果，不让你重新交代一遍。
2. 确有必要时才看 2–3 个本地、官方或社区方案。
3. 自己决定复用、改造、组合还是最小新建，然后直接落文件。
4. 做一次正常任务和一次边界任务，避免只检查格式不检查效果。
5. 交付可安装的 Skill；远程发布仍会单独确认。

默认不做大表格、不跑重型评测，也不连续追问。简单需求直接做，公开发布或高风险场景才增加检查。

## 兼容性说明

| 场景 | 当前状态 |
| --- | --- |
| Codex 本地安装与调用 | 已验证 |
| `skills` CLI 跨 Agent 安装 | 支持官方 `-a` 选择目标；发布后会从 GitHub 对代表性 Agent 做干净安装验证 |
| Claude Code、Cursor、Gemini CLI、OpenCode | `skills` CLI 支持对应安装目录；本 Skill 的真实自动触发和行为尚未逐一实测 |
| 其他支持 `SKILL.md` 的 Agent | 核心结构兼容，可用 CLI 或 ZIP 导入；自动触发和工具差异需由具体宿主验证 |
| 不支持 `SKILL.md` 的聊天工具 | 不能直接安装，可把核心流程作为参考提示词使用 |

这里不会写“所有 Agent 百分百一键可用”。不同 Agent 对联网、终端、文件写入和自动触发的支持并不相同；这个仓库解决的是通用 Skill 包和安装入口，宿主能力仍以各平台实际表现为准。

## 需要什么

- **运行核心流程：** 一个支持 `SKILL.md` 和文件读取的 Agent。
- **一条命令安装：** Node.js 22.20 或更高版本，以及可运行 `npx` 的终端；这是当前 `skills` CLI 的运行要求。
- **运行自带结构检查：** Python 3；脚本只使用标准库，不需要另装 Python 包。
- **调研社区方案：** Agent 具备联网或网页搜索能力。
- **发布到远程平台：** 对应账号、权限，以及你的明确确认。

没有网络时，它仍然可以从本地素材和已有流程创建 Skill，只会如实标明缺少外部调研证据。

## 自己验证是否装好

先检查结构：

```bash
python3 scripts/validate_skill.py .
```

看到 `0 error(s), 0 warning(s)` 后，再在新会话里发送：

```text
用 Skill 产品经理，把“每周整理客户反馈”做成一个最小 Skill。现在只做本地版本，不安装、不发布。
```

成功标准：Agent 少问或不问重复问题，创建一个以 `SKILL.md` 为根入口的 Skill，并说明它实际测了什么。

## 文件都放了什么

```text
skill-product-manager/
├── SKILL.md                         核心工作流，也是唯一必需入口
├── README.md                        你正在看的使用说明
├── LICENSE                          MIT 开源许可证
├── agents/
│   └── openai.yaml                  Codex 可选界面信息，不是核心依赖
├── evals/
│   └── trigger-cases.json           应触发和不应触发的测试题
├── references/
│   ├── research-and-selection.md    需要认真选型时再读
│   ├── evaluation-and-iteration.md  需要加强评测时再读
│   └── release-and-portability.md   准备公开发布时再读
├── reports/
│   ├── design-research.md           参考来源和取舍说明
│   └── evaluation.md                当前版本的验证记录
└── scripts/
    └── validate_skill.py             零依赖结构检查
```

核心流程不会一上来加载所有资料。只有任务真的需要调研、严格评测或公开发布时，才读取对应参考文件。

## 常见问题

### 装完了，但它没自动触发

先新开会话，再明确说一次“用 Skill 产品经理”。有些宿主不会自动刷新已安装 Skill，也有些宿主只支持手动调用。

### 它一直调研，不开始做

告诉它：“最多看 2–3 个真正相关的方案，然后直接选一个路线落地。”这也是 Skill 内置的默认上限。

### 结构检查通过，结果还是不好

结构正确不等于行为好用。拿一份真实材料跑一次，再补一个不该触发或信息缺失的边界任务。

### 没有 Python 或 Node.js

Node.js 只用于一条命令安装，Python 只用于自带校验器。你仍可以下载 ZIP、手动导入，并让 Agent 按 `SKILL.md` 执行核心流程。

## 更新、隐私和许可证

- 更新可运行 `npx skills update skill-product-manager -g -y`，也可以重新运行安装命令或下载新版 Release；覆盖前先保留你自己的改动。
- 不再使用时可运行 `npx skills remove skill-product-manager -g -y`。
- 不要把 Token、Cookie、私人聊天、未授权附件或个人绝对路径放进公开 Skill。
- 外部调研可能会把搜索关键词发送给搜索服务；敏感业务先脱敏再查。
- 这个 Skill 本身没有后台服务或遥测；你交给它的材料仍会经过你正在使用的 Agent、模型和搜索工具。`skills` CLI 会收集匿名使用数据，如需关闭，可在安装命令前加 `DISABLE_TELEMETRY=1`。
- 根 `SKILL.md` 和参考资料使用相对路径；`agents/openai.yaml` 只是可选的 Codex 适配层。
- 本项目使用 [MIT License](LICENSE)，可以使用、修改和分发，但请保留许可证与版权声明。

设计参考和实际取舍见 [设计调研](reports/design-research.md)，当前测试证据见 [评测记录](reports/evaluation.md)。
