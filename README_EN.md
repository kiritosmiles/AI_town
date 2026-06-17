# AI Town

> LLM-Powered Multiplayer Life Simulation Game · 21st Century RPG Maker Style

| Project | Description | Status |
|---|---|---|
| **AI Town** | Go + Python multiplayer life-sim with RPG Maker aesthetics. Each character is an independent LLM agent (DeepSeekV4-pro). 1000×1000 tile+plot dual-layer map, real-time world, ~1500 NPC heartbeat simulation, currency+materials+certificates economy, lifespan+heir inheritance, player parliament legislation. | 🏗️ Design |

[![Status](https://img.shields.io/badge/status-design-7B61FF)](docs/superpowers/specs/2026-06-17-ai-town-design.md)
[![Python](https://img.shields.io/badge/Python-Agent_Service-3776AB?logo=python)](https://www.python.org/)
[![Go](https://img.shields.io/badge/Go-Game_Server-00ADD8?logo=go)](https://go.dev/)
[![Phaser](https://img.shields.io/badge/Phaser.js-Game_Rendering-FF6C37)](https://phaser.io/)
[![React](https://img.shields.io/badge/React-UI-61DAFB?logo=react)](https://react.dev/)
[![DeepSeek](https://img.shields.io/badge/LLM-DeepSeekV4--pro-4B88C2)](https://www.deepseek.com/)

[中文](README.md)

---

## Overview

**AI Town** is a truly AI-native game. Every character is driven by an independent LLM agent with its own perception, planning, and decision-making capabilities. Thousands of NPC agents live real lives in the world — working, socializing, marrying, raising children. You can be a baker, a real estate tycoon, a mayor, or just an ordinary person seeking meaning in a small town. The world keeps turning whether you're online or not.

### 🧠 Core Highlights

| Feature | Description |
|---|---|
| **True AI Souls** | Every action decided by LLM in real-time, not scripts |
| **Living World** | ~1,500 NPC agents with jobs, families, and social circles |
| **Human-AI Co-op** | Set high-level goals; your agent plans and executes autonomously |
| **Transparent AI** | Watch your agent's perception → planning → decision → consequences |
| **Emergent Society** | Laws co-created by player parliament + NPCs, evolving with society |

---

## 🎮 Game Features

```
┌──────────────────────────────────────────────┐
│                                              │
│  🗺️  1000×1000 Tile Map (Dual-layer Plot)    │
│  🕐  Real-Time (24/7 world simulation)       │
│  👤  1 User = 1 Character (Prompt creation)  │
│  💀  Lifespan + Heir Inheritance + Score     │
│  💰  3-Tier Economy (Money+Materials+Certs)  │
│  🏗️  Blueprint Building (Buy→Build→Operate)  │
│  💒  Affinity + LLM Natural Romance          │
│  ⚖️  NPC Constitution + Player Parliament    │
│  🧑‍🏫  Knowledge→Practice→Mentorship Learning  │
│                                              │
└──────────────────────────────────────────────┘
```

---

## 🏗️ Architecture

```
Browser (React + Phaser.js)
        │
        │ WebSocket
        ▼
   API Gateway (Nginx)
        │
   ┌────┴────┐
   │         │
   ▼         ▼
Go Game    ◄──gRPC──►  Python Agent
Server                 Service
World State            LLM Brain
Real-time Sync         DeepSeekV4-pro
                       
   └────┬────┘
        │
   ┌────┴────┐
   ▼         ▼
PostgreSQL   Redis
Persistence  Real-time State
```

| Layer | Stack | Responsibility |
|---|---|---|
| Game Rendering | **Phaser.js** | RPG Maker-style top-down tile map |
| UI Framework | **React** | Panels, menus, Agent awareness panel |
| Game Server | **Go** | World state, real-time sync, physics rules |
| Agent Service | **Python** | LLM calls, tool system, NPC heartbeat |
| LLM | **DeepSeekV4-pro** | Brain driving all agents |
| Persistence | **PostgreSQL** | Characters, buildings, economy, laws |
| Cache/Messaging | **Redis** | Online state, heartbeat queues, real-time pub/sub |

### Why Go + Python?

- **Go**: goroutines effortlessly manage millions of concurrent connections, naturally suited for real-time multiplayer games
- **Python**: the most mature LLM/AI ecosystem — prompt management and tool orchestration are indispensable
- **Separation = Decoupling**: game logic and AI logic iterate independently without interference

---

## 🚀 Quick Start

> ⚠️ The project is in the design phase; development has not yet started. The following is the planned startup method.

### Prerequisites

- Go 1.22+
- Python 3.12+
- PostgreSQL 16+
- Redis 7+
- Node.js 20+

### Launch (Planned)

```bash
# 1. Clone the repository
git clone <repo-url>
cd AI_town

# 2. Start infrastructure
docker compose up -d postgres redis

# 3. Initialize the database
cd server && go run cmd/migrate/main.go

# 4. Start the Go game server
go run cmd/gameserver/main.go

# 5. Start the Python Agent service
cd ../agent && python -m ai_town

# 6. Start the frontend dev server
cd ../web && npm run dev
```

Visit `http://localhost:3000` to enter the game.

---

## 📁 Project Structure (Planned)

```
AI_town/
├── web/                    # Frontend (React + Phaser.js)
│   ├── src/
│   │   ├── game/           # Phaser.js game scenes
│   │   ├── ui/             # React UI components
│   │   └── hooks/          # WebSocket connection hooks
├── server/                 # Go game server
│   ├── cmd/gameserver/     # Entry point
│   ├── internal/
│   │   ├── world/          # World state (Tile + Plot)
│   │   ├── sync/           # Real-time sync (AOI)
│   │   ├── economy/        # Economy system
│   │   ├── law/            # Legal system
│   │   └── grpc/           # gRPC client
├── agent/                  # Python Agent service
│   ├── ai_town/
│   │   ├── agents/         # Player Agent + NPC Agent management
│   │   ├── tools/          # Tool definitions & execution
│   │   ├── llm/            # DeepSeek API integration
│   │   ├── heartbeat/      # World heartbeat scheduler
│   │   └── learning/       # Tool learning/unlock system
├── proto/                  # gRPC Protobuf definitions
├── docs/                   # Documentation
│   └── superpowers/specs/  # Design specification
└── docker-compose.yml
```

---

## 📖 Documentation

- [Design Specification](docs/superpowers/specs/2026-06-17-ai-town-design.md) — Complete design and architecture specification

---

## 🎯 Roadmap

| Phase | Scope | Status |
|---|---|---|
| **Phase 0** | Design specification | ✅ Done |
| **Phase 1** | Tech prototype (Go + Python comms + Phaser map rendering) | 🔲 Pending |
| **Phase 2** | Single-character agent (creation, basic tools, movement) | 🔲 Pending |
| **Phase 3** | World systems (economy, building, NPC heartbeat) | 🔲 Pending |
| **Phase 4** | Multiplayer real-time sync | 🔲 Pending |
| **Phase 5** | Social & relationships (affinity, marriage, heirs) | 🔲 Pending |
| **Phase 6** | Law & governance | 🔲 Pending |
| **Phase 7** | Public beta launch | 🔲 Pending |

---

## 🤝 Contributing

The project is in the early design phase. Discussions and feedback are welcome.

---

## 📄 License

MIT License
