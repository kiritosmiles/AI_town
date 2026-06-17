# AI Town

> LLM 驱动的多人在线生活模拟游戏 · 21 世纪 RPG Maker 风格

| 项目 Project | 简介 Description | 状态 Status |
|---|---|---|
| **AI Town**<br>LLM 驱动的在线生活模拟游戏 | Go + Python 多人在线生活模拟游戏，RPG Maker 风格。每个角色为独立 LLM Agent (DeepSeekV4-pro)，1000×1000 Tile+Plot 双层地图，实时制世界，NPC 全量心跳模拟，货币+材料+证书经济，寿命制+子嗣继承，玩家议会立法。<br>Go + Python multiplayer life-sim. Each character = independent LLM agent. 1000×1000 tile+plot map, real-time world, ~1500 NPC heartbeat simulation, economy with currency+materials+certificates, lifespan+heir inheritance, player parliament legislation. | 🏗️ Design |

[![Status](https://img.shields.io/badge/status-design-7B61FF)](docs/superpowers/specs/2026-06-17-ai-town-design.md)
[![Python](https://img.shields.io/badge/Python-Agent_服务-3776AB?logo=python)](https://www.python.org/)
[![Go](https://img.shields.io/badge/Go-游戏服务器-00ADD8?logo=go)](https://go.dev/)
[![Phaser](https://img.shields.io/badge/Phaser.js-游戏渲染-FF6C37)](https://phaser.io/)
[![React](https://img.shields.io/badge/React-UI-61DAFB?logo=react)](https://react.dev/)
[![DeepSeek](https://img.shields.io/badge/LLM-DeepSeekV4--pro-4B88C2)](https://www.deepseek.com/)

---

## 概述

**AI Town** 是一个真正的 AI 原生游戏。每个角色由一个独立的 LLM agent 驱动，拥有自己的感知、规划、决策能力。世界中有上千个 NPC agent 过着真实的生活——工作、社交、结婚、生子。你可以是面包师、地产商、市长，或者只是一个在小镇上找寻意义的普通人。无论你在线与否，世界都在运转。

### 🧠 核心亮点

| 特性 | 说明 |
|---|---|
| **真正的 AI 灵魂** | 每个行为由 LLM 实时决策，不是脚本 |
| **活的世界** | ~1500 个 NPC agent 拥有自己的工作、家庭、社交圈 |
| **人机协作** | 设定高层目标，agent 自主规划执行，随时介入 |
| **透明 AI** | 实时查看 agent 的感知 → 规划 → 决策 → 后果 |
| **社会涌现** | 法律由玩家议会+ NPC 共同制定，随社会发展演变 |

---

## 🎮 游戏特征

```
┌──────────────────────────────────────────┐
│                                          │
│  🗺️  1000×1000 Tile 地图（双层地产系统）  │
│  🕐  实时制（24/7 世界运行）              │
│  👤  1 用户 = 1 角色（Prompt 创建）       │
│  💀  寿命制 + 子嗣继承 + 成就积分         │
│  💰  货币 + 材料 + 证书 三层经济          │
│  🏗️  蓝图式建造（买地 → 盖楼 → 经营）     │
│  💒  好感度 + LLM 自然恋爱结婚            │
│  ⚖️  NPC 宪法底线 + 玩家议会立法          │
│  🧑‍🏫  知识 → 练习 → 师徒 综合学习系统     │
│                                          │
└──────────────────────────────────────────┘
```

---

## 🏗️ 技术架构

```
浏览器 (React + Phaser.js)
        │
        │ WebSocket
        ▼
   API 网关 (Nginx)
        │
   ┌────┴────┐
   │         │
   ▼         ▼
Go 游戏服  ◄──gRPC──►  Python Agent 服
世界状态               LLM 大脑
实时同步               DeepSeekV4-pro
                       
   └────┬────┘
        │
   ┌────┴────┐
   ▼         ▼
PostgreSQL   Redis
持久数据     实时状态
```

| 层级 | 技术栈 | 职责 |
|---|---|---|
| 游戏渲染 | **Phaser.js** | RPG Maker 风格俯视 Tile 地图 |
| UI 框架 | **React** | 面板、菜单、Agent 意识面板 |
| 游戏服务器 | **Go** | 世界状态、实时同步、物理规则 |
| Agent 服务 | **Python** | LLM 调用、Tool 系统、NPC 心跳 |
| LLM | **DeepSeekV4-pro** | 所有 agent 的大脑驱动 |
| 持久化 | **PostgreSQL** | 角色、建筑、经济、法律 |
| 缓存/消息 | **Redis** | 在线状态、心跳队列、实时广播 |

### 为什么是 Go + Python？

- **Go**：goroutine 轻松管理百万并发连接，天然适合实时多人游戏
- **Python**：LLM/AI 生态最成熟，prompt 管理、tool 编排不可或缺
- **分离即解耦**：游戏逻辑与 AI 逻辑独立迭代，互不影响

---

## 🚀 快速开始

> ⚠️ 项目处于设计阶段，开发尚未开始。以下为规划中的启动方式。

### 环境要求

- Go 1.22+
- Python 3.12+
- PostgreSQL 16+
- Redis 7+
- Node.js 20+

### 启动（规划）

```bash
# 1. 克隆仓库
git clone <repo-url>
cd AI_town

# 2. 启动基础设施
docker compose up -d postgres redis

# 3. 初始化数据库
cd server && go run cmd/migrate/main.go

# 4. 启动 Go 游戏服务器
go run cmd/gameserver/main.go

# 5. 启动 Python Agent 服务
cd ../agent && python -m ai_town

# 6. 启动前端开发服务器
cd ../web && npm run dev
```

访问 `http://localhost:3000` 进入游戏。

---

## 📁 项目结构（规划）

```
AI_town/
├── web/                    # 前端 (React + Phaser.js)
│   ├── src/
│   │   ├── game/           # Phaser.js 游戏场景
│   │   ├── ui/             # React UI 组件
│   │   └── hooks/          # WebSocket 连接 hooks
├── server/                 # Go 游戏服务器
│   ├── cmd/gameserver/     # 入口
│   ├── internal/
│   │   ├── world/          # 世界状态 (Tile + Plot)
│   │   ├── sync/           # 实时同步 (AOI)
│   │   ├── economy/        # 经济系统
│   │   ├── law/            # 法律系统
│   │   └── grpc/           # gRPC 客户端
├── agent/                  # Python Agent 服务
│   ├── ai_town/
│   │   ├── agents/         # 玩家 Agent + NPC Agent 管理
│   │   ├── tools/          # Tool 定义与执行
│   │   ├── llm/            # DeepSeek API 集成
│   │   ├── heartbeat/      # 世界心跳调度
│   │   └── learning/       # Tool 学习/解锁系统
├── proto/                  # gRPC Protobuf 定义
├── docs/                   # 文档
│   └── superpowers/specs/  # 设计规格
└── docker-compose.yml
```

---

## 📖 文档

- [设计规格文档](docs/superpowers/specs/2026-06-17-ai-town-design.md) — 完整的设计与架构规格

---

## 🎯 路线图

| 阶段 | 内容 | 状态 |
|---|---|---|
| **Phase 0** | 设计规格 | ✅ 已完成 |
| **Phase 1** | 技术原型（Go + Python 通信 + Phaser 地图渲染） | 🔲 待开始 |
| **Phase 2** | 单角色 Agent 驱动（角色创建、基础 Tool、移动交互） | 🔲 待开始 |
| **Phase 3** | 世界系统（经济、建造、NPC 心跳） | 🔲 待开始 |
| **Phase 4** | 多人实时同步 | 🔲 待开始 |
| **Phase 5** | 社交关系（好感度、婚姻、子嗣） | 🔲 待开始 |
| **Phase 6** | 法律与治理 | 🔲 待开始 |
| **Phase 7** | 公测上线 | 🔲 待开始 |

---

## 🤝 贡献

项目目前处于早期设计阶段，欢迎讨论和想法反馈。

---

## 📄 许可

MIT License
