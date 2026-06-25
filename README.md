# AI Town

> LLM 驱动的单机生活模拟游戏 · RPG Maker 风格 · Steam 分发

| 项目 | 简介 | 状态 |
|---|---|---|
| **AI Town** | Godot 4 单机生活模拟游戏 (Steam)。每个角色为独立 LLM Agent (DeepSeekV4-pro)，分层记忆(工作+情景+语义+遗忘曲线)，GraphRAG 五类实体知识图谱，1000×1000 Tile+Plot 双层地图，实时制，NPC 三种心跳模式，货币+材料+证书经济，寿命制+子嗣继承，玩家议会立法。 | 🏗️ Design |

[![Status](https://img.shields.io/badge/status-design-7B61FF)](docs/superpowers/specs/2026-06-26-ai-town-prd.md)
[![Godot](https://img.shields.io/badge/Godot-4-478CBF?logo=godot-engine)](https://godotengine.org/)
[![Python](https://img.shields.io/badge/Python-Agent_服务-3776AB?logo=python)](https://www.python.org/)
[![Steam](https://img.shields.io/badge/Steam-分发-000000?logo=steam)](https://store.steampowered.com/)
[![DeepSeek](https://img.shields.io/badge/LLM-DeepSeekV4--pro-4B88C2)](https://www.deepseek.com/)

[English](README_EN.md)

---

## 概述

**AI Town** 是一款 AI 原生的单机生活模拟游戏。每个角色由独立的 LLM agent 驱动，拥有接近人类的记忆系统——工作记忆、情景记忆、语义记忆和遗忘曲线。世界中有上千个 NPC agent 过着真实的生活——工作、社交、结婚、生子。你可以是面包师、地产商、市长，或者只是一个在小镇上找寻意义的普通人。

### 🧠 核心亮点

| 特性 | 说明 |
|---|---|
| **真正的 AI 灵魂** | 每个行为由 LLM 实时决策，不是脚本 |
| **分层记忆** | 工作记忆+情景记忆+语义记忆+遗忘曲线，最接近人类的 Agent 记忆 |
| **活的世界** | ~1500 个 NPC agent 拥有自己的工作、家庭、社交圈 |
| **GraphRAG 知识图谱** | 角色/地点/组织/事件/物品五类实体互联，驱动 NPC 关系推理 |
| **人机协作** | 设定高层目标，agent 自主规划执行，随时介入 |
| **透明 AI** | 实时查看 agent 的 🧠感知 → 📋规划 → ⚡决策 → 后果 |
| **社会涌现** | 法律由玩家议会+NPC共同制定，随社会发展演变 |

---

## 🎮 游戏特征

```
┌──────────────────────────────────────────────┐
│                                              │
│  🗺️  1000×1000 Tile 地图（双层 Plot 地产）    │
│  🕐  实时制（1年≈2天，可调1天~1周）            │
│  👤  1 用户 = 1 角色（Prompt 引导创建）        │
│  💀  寿命制 + 子嗣继承 + 成就积分              │
│  💰  货币 + 材料 + 证书 三层经济               │
│  🏗️  蓝图式建造（买地 → 盖楼 → 经营）          │
│  💒  好感度 + LLM 自然恋爱结婚                 │
│  ⚖️  NPC 宪法底线 + 玩家议会立法               │
│  🧑‍🏫  知识 → 练习 → 师徒 综合学习系统          │
│  🧠  分层记忆 + 遗忘曲线 + GraphRAG            │
│                                              │
└──────────────────────────────────────────────┘
```

---

## 🏗️ 技术架构

```
┌─────────────────────────────────────────────┐
│               Steam 客户端                    │
│  ┌───────────────────────────────────────┐  │
│  │        Godot 4 游戏端 (GDScript)       │  │
│  │  · 2D Tilemap + RPG Maker 风格渲染     │  │
│  │  · 游戏 UI（Agent 面板/对话/菜单/背包） │  │
│  │  · 存档管理 (SQLite)                   │  │
│  │  · Steamworks SDK 集成                 │  │
│  └──────────────┬────────────────────────┘  │
│                 │ gRPC (localhost)            │
│  ┌──────────────▼────────────────────────┐  │
│  │     Python Agent 服务（本地子进程）      │  │
│  │  · 分层记忆 (工作+情景+语义+遗忘)       │  │
│  │  · GraphRAG 知识图谱                   │  │
│  │  · LLM 网关 (云端API / 本地模型)        │  │
│  │  · NPC 心跳调度（C/B/A 三模式）         │  │
│  └──────────────┬────────────────────────┘  │
│                 │                            │
│  ┌──────────────▼────────────────────────┐  │
│  │           本地数据层                     │  │
│  │  SQLite + 向量数据库 + 图存储           │  │
│  └───────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
```

| 层级 | 技术栈 | 职责 |
|---|---|---|
| 游戏引擎 | **Godot 4** | RPG Maker 风格 Tile 地图、UI、存档、Steam 集成 |
| Agent 服务 | **Python** | LLM 调用、分层记忆、GraphRAG、NPC 心跳 |
| LLM | **DeepSeekV4-pro** | 所有 agent 的大脑驱动（云端/本地可选） |
| 持久化 | **SQLite** | 游戏状态、角色、技能、经济、法律 |
| 记忆向量 | **向量数据库** | 情景记忆嵌入存储与检索 |
| 图谱 | **图存储** | GraphRAG 五类实体+关系 |

### 为什么是 Godot 4 + Python？

- **Godot 4**：原生 2D Tilemap 系统，完美契合 RPG Maker 风格；轻量可执行文件（~30MB），Steam 友好；开源免费无授权费
- **Python**：LLM/AI 生态最成熟，分层记忆和 GraphRAG 都依赖 Python 生态
- **本机进程通信**: gRPC 连接 Godot 与 Python，低延迟，无需外部服务

---

## 🚀 快速开始

> ⚠️ 项目处于设计阶段，开发尚未开始。以下为规划中的启动方式。

### 环境要求

- Godot 4.3+
- Python 3.12+
- DeepSeek API Key（云端模式）或 Ollama（本地模式）

### 启动（规划）

```bash
# 1. 克隆仓库
git clone <repo-url>
cd AI_town

# 2. 安装 Python Agent 依赖
cd agent && pip install -r requirements.txt

# 3. 启动 Python Agent 服务
python -m ai_town

# 4. 用 Godot 4 打开并运行 game/ 目录下的项目
```

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
│   │   ├── heartbeat/      # NPC 心跳调度（C/B/A）
│   │   └── learning/       # Tool 学习/技能解锁
├── proto/                  # gRPC Protobuf 定义
├── docs/                   # 文档
│   └── superpowers/specs/  # 设计规格 + PRD + 竞品分析
└── README.md
```

---

## 📖 文档

| 文档 | 说明 |
|---|---|
| [PRD (产品需求文档)](docs/superpowers/specs/2026-06-26-ai-town-prd.md) | 用户画像、功能矩阵(P0-P3)、验收标准、技术架构 |
| [竞品分析](docs/superpowers/specs/2026-06-26-ai-town-competitive-analysis.md) | AI Town(a16z) / Generative Agents / AIvilization / Project Sid |
| [设计规格 v1.0](docs/superpowers/specs/2026-06-17-ai-town-design.md) | 初始设计规格（部分内容已由 PRD 更新） |

---

## 🎯 路线图

| 阶段 | 内容 | 状态 |
|---|---|---|
| **Phase 0** | 设计规格 + PRD + 竞品分析 | ✅ 已完成 |
| **Phase 1** | 技术原型（Godot4 + Python 通信 + Tile 地图） | 🔲 待开始 |
| **Phase 2** | P0 功能（角色创建、分层记忆、GraphRAG、Agent 面板） | 🔲 待开始 |
| **Phase 3** | P1 功能（技能学习、遗忘曲线、反思、Plot 地产、经济、建造） | 🔲 待开始 |
| **Phase 4** | P2 功能（社交关系、事件死亡、子嗣继承、法律治理） | 🔲 待开始 |
| **Phase 5** | P3 功能 + Steam 集成 + 公测 | 🔲 待开始 |

---

## 🤝 贡献

项目目前处于早期设计阶段，欢迎讨论和想法反馈。

---

## 📄 许可

MIT License
