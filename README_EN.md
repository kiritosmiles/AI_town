# AI Town

> LLM-Powered Single-Player Life Simulation Game · RPG Maker Style · Steam Distribution

| Project | Description | Status |
|---|---|---|
| **AI Town** | Godot 4 single-player life-sim (Steam). Each character = independent LLM agent (DeepSeekV4-pro). Layered memory (working+episodic+semantic+forgetting curve), GraphRAG 5-entity knowledge graph, 1000×1000 tile+plot dual-layer map, real-time, NPC heartbeat modes (C/B/A), currency+materials+certificates economy, lifespan+heir inheritance, player parliament legislation. | 🏗️ Design |

[![Status](https://img.shields.io/badge/status-design-7B61FF)](docs/superpowers/specs/2026-06-26-ai-town-prd.md)
[![Godot](https://img.shields.io/badge/Godot-4-478CBF?logo=godot-engine)](https://godotengine.org/)
[![Python](https://img.shields.io/badge/Python-Agent_Service-3776AB?logo=python)](https://www.python.org/)
[![Steam](https://img.shields.io/badge/Steam-Distribution-000000?logo=steam)](https://store.steampowered.com/)
[![DeepSeek](https://img.shields.io/badge/LLM-DeepSeekV4--pro-4B88C2)](https://www.deepseek.com/)

[中文](README.md)

---

## Overview

**AI Town** is an AI-native single-player life simulation game. Every character is driven by an independent LLM agent with a near-human memory system—working memory, episodic memory, semantic memory, and a forgetting curve. Thousands of NPC agents live real lives in the world—working, socializing, marrying, raising children. You can be a baker, a real estate tycoon, a mayor, or just an ordinary person seeking meaning in a small town.

### 🧠 Core Highlights

| Feature | Description |
|---|---|
| **True AI Souls** | Every action decided by LLM in real-time, not scripts |
| **Layered Memory** | Working+Episodic+Semantic+Forgetting curve—the most human-like agent memory |
| **Living World** | ~1,500 NPC agents with jobs, families, and social circles |
| **GraphRAG Knowledge Graph** | 5 entity types (character/location/organization/event/item) driving NPC reasoning |
| **Human-AI Co-op** | Set high-level goals; your agent plans and executes autonomously |
| **Transparent AI** | Watch your agent's 🧠perception → 📋planning → ⚡decision → consequences |
| **Emergent Society** | Laws co-created by player parliament + NPCs, evolving with society |

---

## 🎮 Game Features

```
┌──────────────────────────────────────────────┐
│                                              │
│  🗺️  1000×1000 Tile Map (Dual-layer Plot)    │
│  🕐  Real-Time (1yr≈2days, adjustable 1-7d)  │
│  👤  1 User = 1 Character (Prompt creation)  │
│  💀  Lifespan + Heir Inheritance + Score     │
│  💰  3-Tier Economy (Money+Materials+Certs)  │
│  🏗️  Blueprint Building (Buy→Build→Operate)  │
│  💒  Affinity + LLM Natural Romance          │
│  ⚖️  NPC Constitution + Player Parliament    │
│  🧑‍🏫  Knowledge→Practice→Mentorship Learning  │
│  🧠  Layered Memory + Forgetting + GraphRAG  │
│                                              │
└──────────────────────────────────────────────┘
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│               Steam Client                   │
│  ┌───────────────────────────────────────┐  │
│  │        Godot 4 Game Client              │  │
│  │  · 2D Tilemap + RPG Maker rendering    │  │
│  │  · Game UI (Agent panel/Dialogue/Menu) │  │
│  │  · Save system (SQLite)                │  │
│  │  · Steamworks SDK integration          │  │
│  └──────────────┬────────────────────────┘  │
│                 │ gRPC (localhost)            │
│  ┌──────────────▼────────────────────────┐  │
│  │     Python Agent Service (local)       │  │
│  │  · Layered memory (W/E/S+Forgetting)   │  │
│  │  · GraphRAG knowledge graph            │  │
│  │  · LLM gateway (Cloud API / Local)     │  │
│  │  · NPC heartbeat (C/B/A modes)         │  │
│  └──────────────┬────────────────────────┘  │
│                 │                            │
│  ┌──────────────▼────────────────────────┐  │
│  │           Local Data Layer             │  │
│  │  SQLite + Vector DB + Graph Store      │  │
│  └───────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
```

| Layer | Stack | Responsibility |
|---|---|---|
| Game Engine | **Godot 4** | RPG Maker-style tile map, UI, saves, Steam integration |
| Agent Service | **Python** | LLM calls, layered memory, GraphRAG, NPC heartbeat |
| LLM | **DeepSeekV4-pro** | Brain driving all agents (cloud/local option) |
| Persistence | **SQLite** | Game state, characters, skills, economy, laws |
| Memory Vectors | **Vector DB** | Episodic memory embedding storage & retrieval |
| Graph | **Graph Store** | GraphRAG 5 entities + relationships |

### Why Godot 4 + Python?

- **Godot 4**: Native 2D Tilemap system, perfect for RPG Maker style; lightweight executable (~30MB), Steam-friendly; open-source, royalty-free
- **Python**: The most mature LLM/AI ecosystem—layered memory and GraphRAG all depend on Python
- **Local IPC**: gRPC connects Godot to Python with low latency, no external services required

---

## 🚀 Quick Start

> ⚠️ The project is in the design phase; development has not yet started. The following is the planned startup method.

### Prerequisites

- Godot 4.3+
- Python 3.12+
- DeepSeek API Key (cloud mode) or Ollama (local mode)

### Launch (Planned)

```bash
# 1. Clone the repository
git clone <repo-url>
cd AI_town

# 2. Install Python Agent dependencies
cd agent && pip install -r requirements.txt

# 3. Start Python Agent service
python -m ai_town

# 4. Open and run the Godot 4 project in game/
```

---

## 📁 Project Structure (Planned)

```
AI_town/
├── game/                   # Godot 4 game project
│   ├── scenes/             # Game scenes
│   ├── scripts/            # GDScript scripts
│   ├── assets/             # Art/audio assets
│   └── ui/                 # UI scenes
├── agent/                  # Python Agent service
│   ├── ai_town/
│   │   ├── agents/         # Player/NPC Agent management
│   │   ├── memory/         # Layered memory (working/episodic/semantic/forgetting)
│   │   ├── graphrag/       # GraphRAG knowledge graph
│   │   ├── tools/          # Tool definitions & execution
│   │   ├── llm/            # LLM gateway (cloud + local)
│   │   ├── heartbeat/      # NPC heartbeat scheduler (C/B/A)
│   │   └── learning/       # Tool learning/skill unlock
├── proto/                  # gRPC Protobuf definitions
├── docs/                   # Documentation
│   └── superpowers/specs/  # Design spec + PRD + competitive analysis
└── README.md
```

---

## 📖 Documentation

| Doc | Description |
|---|---|
| [PRD](docs/superpowers/specs/2026-06-26-ai-town-prd.md) | User personas, feature matrix (P0-P3), acceptance criteria, architecture |
| [Competitive Analysis](docs/superpowers/specs/2026-06-26-ai-town-competitive-analysis.md) | AI Town(a16z) / Generative Agents / AIvilization / Project Sid |
| [Design Spec v1.0](docs/superpowers/specs/2026-06-17-ai-town-design.md) | Original design spec (partially superseded by PRD) |

---

## 🎯 Roadmap

| Phase | Scope | Status |
|---|---|---|
| **Phase 0** | Design spec + PRD + competitive analysis | ✅ Done |
| **Phase 1** | Tech prototype (Godot4 + Python comms + Tile map) | 🔲 Pending |
| **Phase 2** | P0 features (character creation, layered memory, GraphRAG, Agent panel) | 🔲 Pending |
| **Phase 3** | P1 features (skill learning, forgetting curve, reflection, Plot system, economy, building) | 🔲 Pending |
| **Phase 4** | P2 features (social & relationships, event death, heir inheritance, law & governance) | 🔲 Pending |
| **Phase 5** | P3 features + Steam integration + public beta | 🔲 Pending |

---

## 🤝 Contributing

The project is in the early design phase. Discussions and feedback are welcome.

---

## 📄 License

MIT License
