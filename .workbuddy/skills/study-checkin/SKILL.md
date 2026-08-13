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
