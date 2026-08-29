# 设计调研与原创取舍

- 调研日期：2026-08-29
- 目标：创建一个少交互、研究驱动、能真正落地和验证 Skill 的个人元 Skill。
- 复用边界：本版本只吸收公开工作流机制与判断原则，未复制候选的长段指令、脚本、品牌资产或发布器代码。

## 用户参考素材

用户上传的两张截图提供了三个可取机制：先做外部调研、只问关键产品问题、按标准直接落架构。本版本没有沿用原文和固定“三步走”，而是把它们改造成能力合同、同题候选 PK、原型实跑、行为对照和发布门禁。

## 公开候选

| 候选 | 学到的机制 | 采用或改造 | 明确拒绝 |
| --- | --- | --- | --- |
| [Anthropic skill-creator](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md) | 先访谈与研究；with-skill / baseline；行为评测与迭代 | 采用“先研究、后实测、再迭代”，改成平台中立协议 | 不绑定 Claude CLI、专属评测器或固定 UI |
| [OpenAI skill-creator](https://github.com/openai/skills/blob/main/skills/.system/skill-creator/SKILL.md) | 精简入口、渐进披露、按风险决定细节、独立前向测试 | 采用精简根入口与按需 references | 不把结构校验冒充行为质量 |
| [Vercel find-skills](https://github.com/vercel-labs/skills/tree/main/skills/find-skills) | 用 `npx skills find` 发现社区候选 | 作为可选发现入口，并要求回源审计 | 不把搜索排名、安装量当质量或安装许可 |
| [Qiaomu Meta Skill](https://github.com/joeseesun/qiaomu-meta-skill) | 社区 prior-art、来源核验、取舍账本、发布证明 | 采用来源账本、候选审计和“保留/改造/拒绝/原创”思路 | 拒绝第三方品牌前缀、默认作者信息、重型自动发布器和固定个人风格 |
| [Yao Meta Skill](https://github.com/yaojingang/yao-meta-skill) | 可移植性、证据治理、不同成熟度门禁 | 缩成轻量/标准/发布三种模式 | 不为个人 Skill 默认引入 Skill OS、遥测和大规模治理 |
| [Dao Skill](https://github.com/gnipbao/dao-skill) | 先找根问题、根据失败证据进化 | 采用“能力合同”和保留旧成功行为 | 不采用哲学命名、庞大模式体系和自我演化存储层 |

## 本版本的原创组合

1. **做过再固化**：社区调研不能替代真实任务；先复盘一次成功过程或做最小原型，再决定规则。
2. **交互压缩**：先读取上下文，最多只问会改变路线的 1–3 个问题，其余用显式低风险假设推进。
3. **双层决策**：候选层记录保留、改造、拒绝、原创；产品层最后选择采用、改造、组合或净室新建。
4. **四类证据分开**：结构、组件、完整行为、对照与人工质量不能互相冒充。
5. **本地复用不等于公开授权**：用户说“以后用”可以授权本地安装，但 GitHub、SkillHub 或商店提交仍需单独确认。
6. **公共核心不带他人品牌**：技术名为 `skill-product-manager`，界面名为“Skill 产品经理”，不自动写入任何第三方作者、前缀或社交账号。

## 当前缺失证据

- 尚未验证所有 Agent 的自动触发与工具差异。
- 尚未公开发布，也没有干净机器的远端安装证据。
- 主观创作类子 Skill 仍需目标用户人审，元 Skill 不能自动替代这一步。
- 如未来直接复用任何候选代码或脚本，必须重新核对该文件对应的许可证和署名要求。
