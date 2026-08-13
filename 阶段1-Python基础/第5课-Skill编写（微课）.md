# 第 5 课 · Skill 编写（微课）

> 前置：Prompt 微课完成（Skill 正文 = Prompt 工程的应用）。
> 目标：掌握 SKILL.md 规范，动手写一个真实可用的 Skill。
> 参考：WorkBuddy 官方 skill-creator 指南。

---

## 一、Skill 的本质（30 秒回顾）

- **Skill = 给 AI 的标准作业指导书（SOP）**：让 AI 在特定任务上按你的流程干活。
- 一个 Skill = 一个文件夹 + 一份 SKILL.md（+ 可选 scripts/ references/ assets/）。
- **frontmatter 决定"何时用"（元数据）**，**正文决定"怎么干"（执行手册）**。

## 二、SKILL.md 规范（WorkBuddy 官方格式）

```markdown
---
name: skill-name          # 必填：简短 kebab-case 英文名（跨平台安全）
description: 触发条件描述   # 必填：写清"何时用"，第三人称（This skill should be used when...）
agent_created: true       # 必填：标记由 AI 创建，之后才能用工具修改/删除
---

# 技能名

## 步骤
1. ...
2. ...

## 验收标准 / 边界（不要做）
```

**三个必填字段**：`name`、`description`、`agent_created`。
- `description` 是**灵魂**——AI 靠它判断"什么时候该触发这个技能"，要写清场景、触发词
- 正文用**祈使句**（"更新学习进度.md"而不是"你应该更新…"）

## 三、正文写作五原则（= Prompt 微课心法的实战版）

1. **步骤有序**：编号步骤，先做什么后做什么
2. **给验收**：怎么算做完了（清单式验收标准）
3. **给边界**：明确"不要做什么"，防止跑偏
4. **给示例**：关键地方给格式/代码示例
5. **别写散文**：能列表就用列表，AI 是按指令执行的

## 四、可选资源目录

| 目录 | 放什么 | 何时用 |
|---|---|---|
| `scripts/` | 可执行脚本（Python/sh） | 技能要"动手"：跑脚本、解析文件 |
| `references/` | 参考资料（API 文档、规范） | 有大量背景知识要按需加载 |
| `assets/` | 输出用模板/素材 | 生成文档/PPT/图片模板 |

原则：**能放 references 就别塞进 SKILL.md**——保持 SKILL.md 精简，按需加载。

## 五、两种存放位置

| 类型 | 路径 | 范围 |
|---|---|---|
| 用户级 | `~/.workbuddy/skills/<name>/` | 所有项目可用 |
| 项目级 | `<工作区>/.workbuddy/skills/<name>/` | 仅当前项目 |

一般个人工作流选**用户级**；要和团队共享或绑定项目约定才用项目级。

## 六、实战：第一个 Skill「学习打卡」（已帮你装好 ✅）

已通过官方 `init_skill.py` 生成 + 校验，安装在项目级：
`C:\Users\YueLi\Desktop\AI大模型学习\.workbuddy\skills\study-checkin\SKILL.md`

```markdown
---
name: study-checkin
description: 学习打卡。用户说出"打卡""学完了""今天学了X"等学习结束语，或要求更新学习进度时使用。按固定流程更新本工作区的学习档案（学习进度.md、当天工作日志、MEMORY.md），确保跨设备接续学习。This skill should be used when the user finishes a study session and wants progress records updated.
agent_created: true
---

# 学习打卡：更新学习档案

学习结束时，按以下流程更新档案。不要省略或跳过步骤，保持文档一致性。

## 步骤

1. 更新 `学习进度.md`：
   - 在「当前状态」中把已完成的任务标记 ✅ 并注明日期
   - 在「已掌握清单」中勾选本次新学会的技能（注明日期）
2. 追加当天日志 `.workbuddy/memory/YYYY-MM-DD.md`（不存在则创建）：
   - 追加「## 学习打卡」小节，记录学了什么、完成什么、卡了什么
3. 若本次学习产生长期偏好或方向变化（如换模型、换学习方向），同步更新 `.workbuddy/memory/MEMORY.md`
4. 回复用户：本次收获小结 + 明确的下一步建议

## 验收标准

- [ ] 学习进度.md 已更新且标注日期
- [ ] 当天日志已追加（追加式，不覆盖旧内容）
- [ ] 回复包含下一步建议

## 边界（不要做）

- 不修改 `学习计划.md`，除非用户明确要求
- 不把临时性信息写进 MEMORY.md（只写长期事实）
- 不删除或覆盖已有日志内容
```

**验证方式**：官方 `package_skill.py` 校验（已通过 ✅），或直接使用触发它。

## 七、打卡任务

1. **测试**：现在对我说一句"打卡"，验证 study-checkin 技能被触发并按流程更新档案
2. **写你自己的 Skill**（选题参考）：
   - `python-explain`：用 C++ 视角逐行讲解 Python 代码（很符合你的学习场景）
   - `weekly-quiz`：每周学习测验出题（5 题 + 答案 + 讲解）
   - `rag-note`：学习笔记整理（把零散笔记转成结构化文档）
3. 用一句话说清：`description` 为什么是 Skill 的灵魂？

## 八、进阶预告

- **scripts/ 实战**：给 Skill 挂脚本，让它能"动手"（如解析文件、调 API）——模块 2 学到函数后更顺手
- **模块 6 衔接**：OpenClaw / MCP 生态里 SKILL.md 是通用语言，现在学会，到时候直接复用
