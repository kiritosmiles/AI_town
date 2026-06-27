# AI Town — 文档目录索引

> 最后更新: 2026-06-27

---

## 目录结构

```
docs/superpowers/specs/
│
├── 00-directory-index.md                     ← 你在这里
│
├── 01-concept/                               [1] 概念设计阶段 ✅ 已完成
│   ├── 2026-06-17-ai-town-design.md          设计规格 v1.0 (初始多人方向)
│   ├── 2026-06-26-ai-town-prd.md             产品需求文档 (当前核心文档)
│   └── 2026-06-26-ai-town-competitive-analysis.md  竞品分析 (4 项目)
│
├── 02-pre-production/                        [2] 预生产阶段 🔲 当前
│   ├── 2026-06-26-ai-town-development-workflow.md  开发全流程 (6 阶段)
│   ├── 2026-06-26-ai-town-action-checklist.md      预生产行动清单 (23 项, 进行中 4%)
│   └── 2026-06-27-tile-spec-decision.md            Tile 规格决策记录 ✅
│
├── 03-prototype/                             [3] 原型验证阶段 🔲 待进入
├── 04-production/                            [4] 正式生产阶段 🔲
├── 05-polish/                                [5] 打磨阶段 🔲
└── 06-launch/                                [6] 发行阶段 🔲
```

---

## 按角色推荐阅读

| 我想... | 先看这个 | 再看这个 |
|---|---|---|
| 快速了解项目 | [README (中文)](../../README.md) | — |
| 理解产品全貌 | [PRD](01-concept/2026-06-26-ai-town-prd.md) | — |
| 理解为什么这样设计 | [竞品分析](01-concept/2026-06-26-ai-town-competitive-analysis.md) | [PRD §13 借鉴追溯](01-concept/2026-06-26-ai-town-prd.md#13-竞品借鉴追溯) |
| 知道下一步做什么 | [行动清单](02-pre-production/2026-06-26-ai-town-action-checklist.md) | — |
| 理解整体开发节奏 | [开发全流程](02-pre-production/2026-06-26-ai-town-development-workflow.md) | [行动清单 §4 依赖图](02-pre-production/2026-06-26-ai-town-action-checklist.md#4-依赖关系图) |
| 看 Tile/分辨率决策 | [Tile 规格决策](02-pre-production/2026-06-27-tile-spec-decision.md) | — |
| 看原技术方案 | [设计规格 v1.0](01-concept/2026-06-17-ai-town-design.md) | — |
| 美术方向参考 | [美术参考指南](../../references/art-references/README.md) | — |

---

## 文档更新规则

- 新产出放入对应阶段目录，命名格式: `YYYY-MM-DD-<topic>.md`
- 更新本索引文档
- 更新对应 README 的文档表格
- 跨文档引用使用相对路径（同目录: `./doc.md`，跨阶段: `../0X-phase/doc.md`）

---

*本文档由 AI Town 项目组维护，随文档增删同步更新。*
