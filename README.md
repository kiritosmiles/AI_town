# AI Town

> LLM 驱动的单机生活模拟游戏 · RPG Maker 风格 · Steam 分发

| 项目 | 简介 | 状态 |
|---|---|---|
| **AI Town** | Godot 4 单机生活模拟游戏 (Steam)。每个角色为独立 LLM Agent (DeepSeekV4-pro)，分层记忆(工作+情景+语义+遗忘曲线)，GraphRAG 五类实体知识图谱(角色/地点/组织/事件/物品)，1000×1000 Tile+Plot 双层地图，实时制(1年≈2天)，NPC C/B/A 三种心跳模式，货币+材料+证书经济，寿命制+子嗣继承+成就积分，NPC宪法+玩家议会立法。预计安装包 500-750MB，源码 8-14 万行。 | 🏗️ Design |

[![Status](https://img.shields.io/badge/status-PRD_Design-7B61FF)](docs/superpowers/specs/01-concept/2026-06-26-ai-town-prd.md)
[![Godot](https://img.shields.io/badge/Godot-4-478CBF?logo=godot-engine)](https://godotengine.org/)
[![Python](https://img.shields.io/badge/Python-Agent_服务-3776AB?logo=python)](https://www.python.org/)
[![Steam](https://img.shields.io/badge/Steam-分发-000000?logo=steam)](https://store.steampowered.com/)
[![DeepSeek](https://img.shields.io/badge/LLM-DeepSeekV4--pro-4B88C2)](https://www.deepseek.com/)

[English](README_EN.md)

---

## 概述

**AI Town** 是一款 AI 原生单机生活模拟游戏。每个角色由独立的 LLM agent 驱动，拥有接近人类的记忆系统——工作记忆、情景记忆、语义记忆和遗忘曲线。1500+ NPC agent 在 1000×1000 的 Tile 世界中过着真实的生活。玩家通过编写 Prompt 创建角色，与 NPC 自然社交、买地建楼、参与立法。观察社会如何从一个小镇开始自发演化。

### 🧠 核心亮点

| 特性 | 说明 |
|---|---|
| **真正的 AI 灵魂** | 每个行为由 LLM 实时决策，不是脚本 |
| **分层记忆** | 工作记忆+情景记忆+语义记忆+遗忘曲线，最接近人类的 Agent 记忆 |
| **GraphRAG 知识图谱** | 五类实体(角色/地点/组织/事件/物品)互联，驱动 NPC 关系推理 |
| **活的世界** | ~1500 个 NPC agent，拥有职业、家庭、社交圈，世界 24/7 运转 |
| **人机协作** | 设定高层目标，Agent 自主规划执行，随时介入 |
| **透明 AI** | Agent 意识面板：🧠感知 → 📋规划 → ⚡决策 → 后果 |
| **社会涌现** | 经济竞争、法律演化、人际关系网自发形成 |

---

## 🎮 游戏特征

```
┌──────────────────────────────────────────────┐
│                                              │
│  🗺️  1000×1000 Tile 地图（双层 Plot 地产）    │
│  🕐  实时制（1年≈2天，可调1天~1周）            │
│  👤  1 用户 = 1 角色（Prompt 引导创建）        │
│  💀  寿命制 (60-90岁) + 子嗣继承 + 成就积分    │
│  💰  货币 + 材料 + 证书 三层经济               │
│  🏗️  蓝图式建造（买地 → 盖楼 → 经营）          │
│  💒  好感度 + LLM 自然恋爱结婚                 │
│  ⚖️  NPC 宪法底线 + 玩家议会立法               │
│  🧑‍🏫  知识 → 练习 → 师徒 三级 Tool 学习        │
│  🧠  分层记忆 + 遗忘曲线 + GraphRAG            │
│                                              │
└──────────────────────────────────────────────┘
```

### 三类玩家画像

| 画像 | 核心乐趣 | 关键系统 |
|---|---|---|
| **人生模拟党** | 体验完整 AI 人生：出生→成长→恋爱→老去→子嗣继承 | Agent 意识面板、分层记忆、自然对话、继承 |
| **建造经营党** | 成为镇上首富，超越 NPC 富豪排行榜 | 经济面板、排行榜、地产、蓝图建造 |
| **社会观察者** | 观察 NPC 社会如何自发演化，法律如何推进 | GraphRAG 全局浏览器、决策日志、社会演化时间线 |

---

## 🏗️ 技术架构

```
┌─────────────────────────────────────────────┐
│               Steam 客户端                    │
│  ┌───────────────────────────────────────┐  │
│  │        Godot 4 游戏端 (GDScript)       │  │
│  │  · 2D Tilemap + RPG Maker 风格渲染     │  │
│  │  · 游戏 UI（Agent 面板/对话/背包/菜单） │  │
│  │  · 存档管理 (SQLite)                   │  │
│  │  · Steamworks SDK 集成                 │  │
│  └──────────────┬────────────────────────┘  │
│                 │ gRPC (localhost)            │
│  ┌──────────────▼────────────────────────┐  │
│  │     Python Agent 服务（本地子进程）      │  │
│  │  · 分层记忆 (工作+情景+语义+遗忘曲线)    │  │
│  │  · GraphRAG 五类实体知识图谱            │  │
│  │  · LLM 网关 (云端API / 本地模型)         │  │
│  │  · NPC 心跳调度（C/B/A 三模式可选）      │  │
│  │  · 反思提炼 + 技能自动解锁               │  │
│  └──────────────┬────────────────────────┘  │
│                 │                            │
│  ┌──────────────▼────────────────────────┐  │
│  │           本地数据层                     │  │
│  │  SQLite + 向量数据库 + 图存储           │  │
│  │  存档单文件 ~35MB                       │  │
│  └───────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
```

| 层级 | 技术栈 | 职责 |
|---|---|---|
| 游戏引擎 | **Godot 4** | RPG Maker 风格 Tile 地图、UI、存档、Steam 集成 |
| Agent 服务 | **Python** | LLM 调用、分层记忆、GraphRAG、NPC 心跳、反思提炼 |
| LLM | **DeepSeekV4-pro** | 所有 agent 的大脑驱动（云端 API / 本地 Ollama 可选） |
| 持久化 | **SQLite** | 游戏状态、角色、技能、经济、法律 |
| 记忆向量 | **向量数据库** | 情景记忆嵌入存储与检索 (ChromaDB/lanceDB) |
| 图谱 | **图存储** | GraphRAG 五类实体 + 关系 + 变化历史 |

---

## 📊 项目规模

| 指标 | 数值 |
|---|---|
| Steam 安装包 | **500-750 MB** (压缩下载 ~400-600 MB) |
| 运行时内存 (推荐 B 模式) | **~1.5 GB** |
| 运行时内存 (峰值 A 模式) | **~3 GB** |
| 单存档 | **~35 MB** |
| 源代码 | **~80,000-145,000 行** (GDScript + Python) |
| 开发周期 (1 人) | **~12-17 个月** |

---

## 📁 项目结构（规划）

```
AI_town/
├── game/                   # Godot 4 游戏项目
│   ├── scenes/             # 游戏场景
│   ├── scripts/            # GDScript 脚本
│   ├── assets/             # 美术/音频素材
│   └── ui/                 # UI 场景
├── agent/                  # Python Agent 服务
│   ├── ai_town/
│   │   ├── agents/         # 玩家/NPC Agent 管理
│   │   ├── memory/         # 分层记忆（工作/情景/语义/遗忘）
│   │   ├── graphrag/       # GraphRAG 知识图谱
│   │   ├── tools/          # Tool 定义与执行
│   │   ├── llm/            # LLM 网关（云端+本地）
│   │   ├── heartbeat/      # NPC 心跳调度（C/B/A 三模式）
│   │   └── learning/       # Tool 学习/技能解锁
├── proto/                  # gRPC Protobuf 定义
├── docs/                   # 文档
│   └── superpowers/specs/  # 按阶段分层 (00-索引/01-概念/02-预生产/03-原型/04-生产/05-打磨/06-发行)
└── README.md
```

---

## 📖 文档

| 阶段 | 文档 | 说明 |
|---|---|---|
| 🟢 概念 | [PRD (产品需求文档)](docs/superpowers/specs/01-concept/2026-06-26-ai-town-prd.md) | 三画像、P0-P3 功能矩阵 (56 项)、验收标准 (37 条)、技术架构、项目规模预估、竞品借鉴追溯 |
| 🟢 概念 | [竞品分析](docs/superpowers/specs/01-concept/2026-06-26-ai-town-competitive-analysis.md) | 4 项目深度对比 (AI Town a16z / Generative Agents / AIvilization / Project Sid)，16 维度横向矩阵 |
| 🟢 概念 | [设计规格 v1.0](docs/superpowers/specs/01-concept/2026-06-17-ai-town-design.md) | 初始设计规格（部分内容已由 PRD 更新） |
| 🟡 预生产 | [开发全流程](docs/superpowers/specs/02-pre-production/2026-06-26-ai-town-development-workflow.md) | 6 阶段流程 (概念→预生产→原型→生产→打磨→发行) |
| 🟡 预生产 | [行动清单](docs/superpowers/specs/02-pre-production/2026-06-26-ai-town-action-checklist.md) | 23 项可追踪任务，含依赖图和进度看板 |
| ⬜ 全部 | [目录索引](docs/superpowers/specs/00-directory-index.md) | 完整文档目录与导航 |

---

## 🎯 开发阶段

| 阶段 | 内容 | 状态 | 预估 |
|---|---|---|---|
| **[1] 概念设计** | PRD + 竞品分析 + 设计决策 | ✅ 已完成 | 2026-06 |
| **[2] 预生产** | GDD + 美术风格 + 数值策划 + AI 行为设计 + 技术验证 | 🔲 待进入 | 1-2 月 |
| **[3] 原型验证** | 可玩 Demo (P0 核心循环) | 🔲 | 2-3 月 |
| **[4] 正式生产** | Alpha (P1) → Beta (P2) | 🔲 | 6-8 月 |
| **[5] 打磨** | 数值平衡 + 性能优化 + 本地化 + QA | 🔲 | 2-3 月 |
| **[6] 发行** | Steam 上架 + 营销 + 首发 | 🔲 | 1-2 月 |

---

## 🚀 快速开始

> ⚠️ 项目处于设计阶段，开发尚未开始。

### 环境要求

- Godot 4.3+
- Python 3.12+
- DeepSeek API Key（云端模式）或 Ollama（本地模式）

### 启动（规划）

```bash
git clone <repo-url>
cd AI_town

# 安装 Python Agent 依赖
cd agent && pip install -r requirements.txt

# 启动 Python Agent 服务
python -m ai_town

# 用 Godot 4 打开并运行 game/ 目录下的项目
```

---

## 🤝 贡献

项目目前处于预生产阶段，欢迎讨论和想法反馈。

---

## 📄 许可

MIT License
