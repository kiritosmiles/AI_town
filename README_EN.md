# AI Town

> LLM-Powered Single-Player Life Simulation Game · RPG Maker Style · Steam Distribution

| Project | Description | Status |
|---|---|---|
| **AI Town** | Godot 4 single-player life-sim (Steam). Independent LLM agents (DeepSeekV4-pro), layered memory (working+episodic+semantic+forgetting curve), GraphRAG 5-entity knowledge graph (character/location/organization/event/item), 1000×1000 tile+plot dual-layer map, real-time (1yr≈2days), NPC heartbeat modes (C/B/A), currency+materials+certificates economy, lifespan+heir inheritance+achievement score, NPC constitution+player parliament. Est. install 500-750MB, ~80k-145k LOC. | 🏗️ Design |

[![Status](https://img.shields.io/badge/status-PRD_Design-7B61FF)](docs/superpowers/specs/01-concept/2026-06-26-ai-town-prd.md)
[![Godot](https://img.shields.io/badge/Godot-4-478CBF?logo=godot-engine)](https://godotengine.org/)
[![Python](https://img.shields.io/badge/Python-Agent_Service-3776AB?logo=python)](https://www.python.org/)
[![Steam](https://img.shields.io/badge/Steam-Distribution-000000?logo=steam)](https://store.steampowered.com/)
[![DeepSeek](https://img.shields.io/badge/LLM-DeepSeekV4--pro-4B88C2)](https://www.deepseek.com/)

[中文](README.md)

---

## Overview

**AI Town** is an AI-native single-player life simulation game. Every character is driven by an independent LLM agent with a near-human memory system—working memory, episodic memory, semantic memory, and a forgetting curve. 1,500+ NPC agents live real lives across a 1000×1000 tile world. Players create characters via Prompt, socialize naturally with NPCs, buy land and build, and participate in legislation. Watch society spontaneously evolve from a small town.

### 🧠 Core Highlights

| Feature | Description |
|---|---|
| **True AI Souls** | Every action decided by LLM in real-time, not scripts |
| **Layered Memory** | Working+Episodic+Semantic+Forgetting curve—the most human-like agent memory |
| **GraphRAG Knowledge Graph** | 5 entity types (character/location/organization/event/item) driving NPC relationship reasoning |
| **Living World** | ~1,500 NPC agents with careers, families, and social circles; world runs 24/7 |
| **Human-AI Co-op** | Set high-level goals; your agent plans and executes autonomously |
| **Transparent AI** | Agent awareness panel: 🧠Perception → 📋Planning → ⚡Decision → Consequences |
| **Emergent Society** | Economic competition, legal evolution, spontaneous social networks |

---

## 🎮 Game Features

```
┌──────────────────────────────────────────────┐
│                                              │
│  🗺️  1000×1000 Tile Map (Dual-layer Plot)    │
│  🕐  Real-Time (1yr≈2days, adjustable 1-7d)  │
│  👤  1 User = 1 Character (Prompt creation)  │
│  💀  Lifespan (60-90yr) + Heir + Score       │
│  💰  3-Tier Economy (Money+Materials+Certs)  │
│  🏗️  Blueprint Building (Buy→Build→Operate)  │
│  💒  Affinity + LLM Natural Romance          │
│  ⚖️  NPC Constitution + Player Parliament    │
│  🧑‍🏫  Knowledge→Practice→Mentorship Learning  │
│  🧠  Layered Memory + Forgetting + GraphRAG  │
│                                              │
└──────────────────────────────────────────────┘
```

### Three Player Personas

| Persona | Core Joy | Key Systems |
|---|---|---|
| **Life Simmer** | Experience a full AI life: birth→growth→love→aging→heir | Agent panel, layered memory, natural dialogue, inheritance |
| **Builder Tycoon** | Become the richest in town, surpass NPC billionaire rankings | Economy panel, leaderboards, real estate, blueprint building |
| **Society Observer** | Watch NPC society emerge and evolve, laws progress | GraphRAG global browser, decision logs, social timeline |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│               Steam Client                   │
│  ┌───────────────────────────────────────┐  │
│  │        Godot 4 Game Client              │  │
│  │  · 2D Tilemap + RPG Maker rendering    │  │
│  │  · Game UI (Agent panel/Dialogue/Bag)  │  │
│  │  · Save system (SQLite)                │  │
│  │  · Steamworks SDK integration          │  │
│  └──────────────┬────────────────────────┘  │
│                 │ gRPC (localhost)            │
│  ┌──────────────▼────────────────────────┐  │
│  │     Python Agent Service (local)       │  │
│  │  · Layered memory (W/E/S+Forgetting)   │  │
│  │  · GraphRAG 5-entity knowledge graph   │  │
│  │  · LLM gateway (Cloud API / Local)     │  │
│  │  · NPC heartbeat (C/B/A modes)         │  │
│  │  · Reflection + Auto skill unlock      │  │
│  └──────────────┬────────────────────────┘  │
│                 │                            │
│  ┌──────────────▼────────────────────────┐  │
│  │           Local Data Layer             │  │
│  │  SQLite + Vector DB + Graph Store      │  │
│  │  Save file ~35MB                       │  │
│  └───────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
```

| Layer | Stack | Responsibility |
|---|---|---|
| Game Engine | **Godot 4** | RPG Maker-style tile map, UI, saves, Steam integration |
| Agent Service | **Python** | LLM calls, layered memory, GraphRAG, NPC heartbeat, reflection |
| LLM | **DeepSeekV4-pro** | Brain driving all agents (cloud API / local Ollama) |
| Persistence | **SQLite** | Game state, characters, skills, economy, laws |
| Memory Vectors | **Vector DB** | Episodic memory embedding storage & retrieval (ChromaDB/lanceDB) |
| Graph | **Graph Store** | GraphRAG 5 entities + relationships + change history |

---

## 📊 Project Scale

| Metric | Value |
|---|---|
| Steam Install | **500-750 MB** (compressed download ~400-600 MB) |
| Runtime RAM (recommended B mode) | **~1.5 GB** |
| Runtime RAM (peak A mode) | **~3 GB** |
| Single Save File | **~35 MB** |
| Source Code | **~80,000-145,000 lines** (GDScript + Python) |
| Dev Timeline (1 person) | **~12-17 months** |

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
│   │   ├── memory/         # Layered memory (W/E/S+Forgetting)
│   │   ├── graphrag/       # GraphRAG knowledge graph
│   │   ├── tools/          # Tool definitions & execution
│   │   ├── llm/            # LLM gateway (cloud + local)
│   │   ├── heartbeat/      # NPC heartbeat scheduler (C/B/A)
│   │   └── learning/       # Tool learning/skill unlock
├── proto/                  # gRPC Protobuf definitions
├── docs/                   # Documentation
│   └── superpowers/specs/  # PRD + Competitive Analysis + Design Spec + Dev Workflow
└── README.md
```

---

## 📖 Documentation

| Phase | Document | Description |
|---|---|---|
| 🟢 Concept | [PRD](docs/superpowers/specs/01-concept/2026-06-26-ai-town-prd.md) | 3 personas, P0-P3 feature matrix (56 items), acceptance criteria (37 items), architecture, project scale, competitive borrowing trace |
| 🟢 Concept | [Competitive Analysis](docs/superpowers/specs/01-concept/2026-06-26-ai-town-competitive-analysis.md) | 4-project deep comparison (AI Town a16z / Generative Agents / AIvilization / Project Sid), 16-dimension matrix |
| 🟢 Concept | [Design Spec v1.0](docs/superpowers/specs/01-concept/2026-06-17-ai-town-design.md) | Original design spec (partially superseded by PRD) |
| 🟡 Pre-Prod | [Development Workflow](docs/superpowers/specs/02-pre-production/2026-06-26-ai-town-development-workflow.md) | 6-stage process (Concept→Pre-Prod→Proto→Prod→Polish→Launch) |
| 🟡 Pre-Prod | [Action Checklist](docs/superpowers/specs/02-pre-production/2026-06-26-ai-town-action-checklist.md) | 23 trackable tasks with dependency graph and progress board |
| ⬜ All | [Directory Index](docs/superpowers/specs/00-directory-index.md) | Full document directory and navigation |

---

## 🎯 Development Phases

| Phase | Scope | Status | Est. |
|---|---|---|---|
| **[1] Concept** | PRD + competitive analysis + design decisions | ✅ Done | 2026-06 |
| **[2] Pre-Production** | GDD + art style + numerical design + AI behavior spec + tech spikes | 🔲 Next | 1-2 mo |
| **[3] Prototype** | Playable demo (P0 core loop) | 🔲 | 2-3 mo |
| **[4] Production** | Alpha (P1) → Beta (P2) | 🔲 | 6-8 mo |
| **[5] Polish** | Balance + performance + localization + QA | 🔲 | 2-3 mo |
| **[6] Launch** | Steam listing + marketing + release | 🔲 | 1-2 mo |

---

## 🚀 Quick Start

> ⚠️ Project is in the design phase. Development has not yet started.

### Prerequisites

- Godot 4.3+
- Python 3.12+
- DeepSeek API Key (cloud mode) or Ollama (local mode)

### Launch (Planned)

```bash
git clone <repo-url>
cd AI_town

# Install Python Agent dependencies
cd agent && pip install -r requirements.txt

# Start Python Agent service
python -m ai_town

# Open and run the Godot 4 project in game/
```

---

## 🤝 Contributing

The project is in the pre-production phase. Discussions and feedback are welcome.

---

## 📄 License

MIT License
