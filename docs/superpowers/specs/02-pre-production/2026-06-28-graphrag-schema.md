# AI Town — GraphRAG Schema 定义

> 日期: 2026-06-28 | 类型: 设计模板 | 关联: PRD §5.4 (P0-6, P1-6)
> 依赖: 无 | 被依赖: Prompt Chain (T-9), 存档结构 (T-12)

---

## 1. 概述

GraphRAG 是 AI Town 的知识图谱引擎。所有实体和关系以图结构存储，Agent 通过图谱查询获取自身相关的结构化知识，驱动社交推理和记忆整合。

**核心原则**: 记忆是"发生了什么"，GraphRAG 是"谁和谁是什么关系"。两者互补——记忆提供时间序列，图谱提供关系拓扑。

### 1.1 设计目标

| 目标 | 依据 |
|---|---|
| 查询延迟 < 1s | PRD 验收标准 AC 4-5 |
| 支持三层访问控制 | PRD §5.4 三层访问 |
| Schema 向后兼容扩展 | PRD 非功能性需求 |
| 支持关系变化历史追踪 | 观察者工具需求 |

---

## 2. 五类实体定义

### 2.1 Character (角色)

游戏中所有有名字的可交互角色（玩家 + NPC）。

```json
{
  "entity_type": "Character",
  "id": "char_<uuid>",
  "properties": {
    "name": "string (必需，唯一可读标识)",
    "age": "integer",
    "gender": "string enum: male/female/other",
    "occupation": "string (职业名称)",
    "personality_bigfive": {
      "openness": "float 0-1",
      "conscientiousness": "float 0-1",
      "extraversion": "float 0-1",
      "agreeableness": "float 0-1",
      "neuroticism": "float 0-1"
    },
    "wealth": "float (总资产估值，经济系统衍生)",
    "reputation": "float 0-100 (社会声望)",
    "health_status": "string enum: healthy/sick/injured/disabled/deceased",
    "is_player": "boolean",
    "is_alive": "boolean",
    "birth_date": "string ISO date",
    "death_date": "string ISO date | null",
    "traits": ["string"] (性格标签: "勤劳"/"懒惰"/"善良"/"贪婪"...),
    "skills": {
      "<skill_id>": "integer (等级 1-10)"
    }
  }
}
```

**入图时机**: 角色创建时
**更新频率**: 每次状态变化（等级提升/财富变化/声望增减/死亡）
**向量嵌入**: name × backstory 联合嵌入 → `character_name_bio` 索引

---

### 2.2 Location (地点)

地图上有意义的坐标区域或建筑。

```json
{
  "entity_type": "Location",
  "id": "loc_<uuid>",
  "properties": {
    "name": "string (地点名称，如'老王咖啡店')",
    "type": "string enum: building/natural_landmark/public_square/road/water/forest",
    "building_type": "string | null (shop/restaurant/residence/government/school/hospital/farm/workshop)",
    "coordinates": {
      "center_x": "integer",
      "center_y": "integer",
      "radius": "integer (覆盖 Tile 范围)"
    },
    "plot_id": "string | null (关联 Plot 编号)",
    "owner_id": "string | null (char_xxx，产权人)",
    "capacity": "integer (最大容纳人数)",
    "is_public": "boolean (公共场所任何人都能进)",
    "description": "string (一句话描述)",
    "tags": ["string"] ("咖啡"/"购物"/"办事"/"休闲"...)
  }
}
```

**入图时机**: 建筑建造完成 / 地图初始化
**更新频率**: 产权变更 / 建筑升级 / 改名
**向量嵌入**: name × description × tags 联合嵌入 → `location_index`

---

### 2.3 Organization (组织)

角色组成的正式/非正式团体。

```json
{
  "entity_type": "Organization",
  "id": "org_<uuid>",
  "properties": {
    "name": "string (组织名，如'小镇商会')",
    "type": "string enum: government/business/union/club/family/gang/religious/school",
    "purpose": "string (成立目的简介)",
    "founded_date": "string ISO date",
    "headquarters": "string | null (loc_xxx，总部地点)",
    "member_count": "integer",
    "is_active": "boolean",
    "membership_open": "boolean (是否开放加入)",
    "influence": "float 0-100 (组织影响力)",
    "tags": ["string"]
  }
}
```

**入图时机**: 组织注册/家庭形成/商会成立
**更新频率**: 成员变动 / 影响力变化 / 解散
**向量嵌入**: name × purpose × tags 联合嵌入

---

### 2.4 Event (事件)

有意义的时空发生点，可能影响多个角色的记忆。

```json
{
  "entity_type": "Event",
  "id": "evt_<uuid>",
  "properties": {
    "title": "string (事件标题，如'2024年暴风雪断电')",
    "type": "string enum: natural_disaster/accident/crime/celebration/election/economic/birth/death/wedding/law_change/other",
    "severity": "integer 1-10 (影响程度)",
    "description": "string (事件简述 100-300字)",
    "occurred_at": "string ISO datetime",
    "duration": "string (持续时间：instant/hour/day/week/month)",
    "location_id": "string | null (loc_xxx，发生地点)",
    "is_resolved": "boolean (是否已解决/结束)",
    "public_knowledge": "boolean (是否为公共知情事件)",
    "tags": ["string"]
  }
}
```

**入图时机**: 
- 系统生成事件（天气灾害/节日/经济波动）
- Agent 行为触发重大事件（结婚/死亡/犯罪/选举结果）
- 反射系统总结出"值得记录的事件"

**更新频率**: 发生后即不可变（只追加不修改）
**向量嵌入**: title × description 联合嵌入 → `event_index`

---

### 2.5 Item (物品)

有追踪价值的特殊物品（不仅存在于背包中，而是有独立故事的物品）。

```json
{
  "entity_type": "Item",
  "id": "item_<uuid>",
  "properties": {
    "name": "string (物品名)",
    "type": "string enum: tool/artifact/heirloom/document/key/weapon/art/jewelry/other",
    "rarity": "string enum: common/uncommon/rare/legendary",
    "value": "float (市场估价)",
    "description": "string (物品描述 50-200字)",
    "origin": "string (来源：crafted/purchased/found/gifted/inherited)",
    "created_date": "string ISO date",
    "is_unique": "boolean (是否独一无二)",
    "history": ["string"] (历任所有者+关键事件的简短描述列表),
    "current_owner_id": "string | null (char_xxx)",
    "current_location": "string | null (loc_xxx 或 'char_xxx_inventory')"
  }
}
```

**入图时机**: 特殊物品创建/传家宝登记/传奇物品出现
**注意**: 不是所有物品都入图——只有"有故事"的物品才入图。普通消耗品（面包、咖啡豆）不在此列。
**向量嵌入**: name × description × history 联合嵌入

---

## 3. 关系类型定义

### 3.1 关系类型枚举

| # | 关系类型 | 英文 | 方向 | 示例 | 强度 |
|---|---|---|---|---|---|
| R01 | 血缘 | blood | 双向 | 小明 -(父子)→ 老陈 | strong |
| R02 | 婚姻 | marriage | 双向 | 小明 ⚭ 小美 | strong |
| R03 | 恋爱 | dating | 双向 | 小明 ♥ 小芳 (未婚) | moderate |
| R04 | 师徒 | mentor_student | 单向 | 老王 -(师傅)→ 小明 | strong |
| R05 | 朋友 | friend | 双向 | 小明 — 小张 | moderate |
| R06 | 至交 | best_friend | 双向 | 小明 ≡ 小刘 | strong |
| R07 | 同事 | colleague | 双向 | 小明·小李 (同咖啡店) | weak |
| R08 | 雇主 | employer | 单向 | 老王 -(雇佣)→ 小明 | moderate |
| R09 | 邻居 | neighbor | 双向 | 小明↔小周 (相邻 Plot) | weak |
| R10 | 仇敌 | enemy | 双向 | 小明 ✕ 小张 (冲突后) | strong |
| R11 | 所有 | owns | 单向 | 小明 -(拥有)→ 咖啡机 | — |
| R12 | 位于 | located_at | 单向 | 老王咖啡店 -(位于)→ 中心广场 | — |
| R13 | 属于 | belongs_to | 单向 | 小镇商会 -(属于)→ 小镇 | — |
| R14 | 参与 | participated | 单向 | 小明 -(参与)→ 面包节 | — |
| R15 | 见证 | witnessed | 单向 | 小明 -(目击)→ 广场斗殴 | — |
| R16 | 发起 | initiated | 单向 | 小明 -(发起)→ 咖啡节提案 | — |
| R17 | 受害 | victim_of | 单向 | 小明 -(受害)→ 被偷钱包 | — |
| R18 | 加害 | perpetrator_of | 单向 | 小偷 -(作案)→ 偷钱包事件 | — |
| R19 | 隶属 | member_of | 单向 | 小明 -(加入)→ 小镇商会 | — |
| R20 | 领导 | leader_of | 单向 | 老王 -(领导)→ 小镇商会 | — |

### 3.2 关系数据结构

```json
{
  "relationship_id": "rel_<uuid>",
  "type": "string (R01-R20 之一)",
  "from_entity": "string (char_xxx / loc_xxx / ...) ",
  "to_entity": "string",
  "properties": {
    "strength": "string enum: weak/moderate/strong",
    "affinity_value": "float 0-100 | null (仅角色间关系，null=不适用)",
    "started_at": "string ISO datetime",
    "ended_at": "string ISO datetime | null",
    "is_active": "boolean",
    "metadata": "object (扩展字段，如雇佣关系的 salary、师徒关系的教授技能)"
  },
  "history": [
    {
      "changed_at": "string ISO datetime",
      "previous_strength": "string | null",
      "reason": "string (变化原因，可关联 evt_xxx)"
    }
  ]
}
```

---

## 4. 三层访问控制

| 层级 | 访问者 | 查询范围 | 允许的操作 | 用途 |
|---|---|---|---|---|
| **L1 Agent 内部** | NPC/玩家 Agent | 只返回与查询 Agent 直接相关的实体+关系（2 跳以内） | 读取+写入自己参与的关系 | Agent 决策时"认识谁？关系怎样？" |
| **L2 玩家记忆** | 玩家（通过游戏 UI） | 玩家角色的 L1 范围 + 去隐私敏感内容 | 只读 + 时间线浏览 | 角色日记/记忆查询面板 |
| **L3 全局浏览器** | 社会观察者（外部工具） | 完整图谱 + 变化历史 + 关系展开 | 只读 + 搜索/过滤/导出 | 观察者工具 / 调试 / 数据分析导出 |

### 4.1 Agent 查询接口 (L1)

```
query_related(entity_id, relation_types[], max_hops=2) → entities[], relationships[]
search_entities(query_text, top_k=5) → entities[]   (向量检索)
get_relation(rel_id) → relationship
get_neighbors(entity_id, hop=1) → entities[]
```

### 4.2 全局浏览器接口 (L3)

```
graph_full_dump() → {entities, relationships}
graph_diff(since_timestamp) → {added, removed, changed}
search_global(query, filters) → entities[]
get_entity_history(entity_id) → 变化时间线
expand_node(entity_id, depth) → 子图
```

---

## 5. 图查询与 Agent 决策对接

### 5.1 查询注入 System Prompt 的方式

```
## 与当前情境相关的知识图谱
你认识的人:
- 老王 (R05 朋友 · 好感度 78 · 咖啡店老板 · 5年前认识)
- 小美 (R03 恋爱 · 好感度 92 · 银行职员 · 3个月前开始约会)
- 小李 (R07 同事 · 好感度 55 · 咖啡店员工 · 你雇佣了他)

你所在的场所和组织:
- 老王咖啡店 (R12 位于 中心广场 · 你是老板)
- 小镇商会 (R19 隶属 · 上个月加入)
```

### 5.2 知识图谱与记忆的联动

```
情景记忆: → "昨天我和老王讨论了咖啡豆涨价的事"
              │
              ▼ (入图检查)
图谱更新:    [新增关系?] 否，已有朋友关系
            [更新强度?] 好友讨论 → 好感 +2
            [新增事件?] "咖啡豆涨价" → 创建 Event 实体
            [物品入图?] 否，普通对话
```

---

## 6. 向量嵌入规格

| 实体类型 | 嵌入维度 | 嵌入字段 | 模型 | 索引 |
|---|---|---|---|---|
| Character | 768 | name + backstory | text-embedding (本地/API) | `idx_char_emb` |
| Location | 768 | name + description + tags | 同上 | `idx_loc_emb` |
| Organization | 768 | name + purpose + tags | 同上 | `idx_org_emb` |
| Event | 768 | title + description | 同上 | `idx_evt_emb` |
| Item | 768 | name + description + history | 同上 | `idx_item_emb` |

**嵌入策略**: 
- 新实体创建时生成嵌入（一次性）
- 仅 `description` / `backstory` 等大段文本发生变化时重新嵌入
- 使用本地嵌入模型（Ollama / sentence-transformers），避免 API 调用开销
- 候选: `bge-small-zh-v1.5`（中文优化，512维可选降维到 384）

---

## 7. 存储设计概要

### 7.1 图存储

| 组件 | 技术选择 | 说明 |
|---|---|---|
| 属性图存储 | SQLite + JSON 列 | 实体和关系存 SQLite，properties 存 JSON 列 |
| 向量索引 | ChromaDB / lanceDB | 实体嵌入存储与向量检索 |
| 图谱快照 | JSON Lines 文件 | 存档时完整序列化 |
| 变化日志 | SQLite WAL 模式 | 每次写入自动记录变更 |

### 7.2 SQLite 表设计（草图）

```sql
-- 实体表
CREATE TABLE graph_entities (
    id TEXT PRIMARY KEY,
    entity_type TEXT NOT NULL,  -- Character/Location/Organization/Event/Item
    name TEXT NOT NULL,
    properties JSON NOT NULL,
    embedding BLOB,            -- 向量嵌入（二进制存储）
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

-- 关系表
CREATE TABLE graph_relationships (
    id TEXT PRIMARY KEY,
    type TEXT NOT NULL,        -- R01-R20
    from_entity TEXT NOT NULL REFERENCES graph_entities(id),
    to_entity TEXT NOT NULL REFERENCES graph_entities(id),
    properties JSON NOT NULL,
    is_active INTEGER DEFAULT 1,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

-- 关系变化历史
CREATE TABLE graph_relationship_history (
    id TEXT PRIMARY KEY,
    relationship_id TEXT NOT NULL,
    changed_at TEXT NOT NULL,
    change_type TEXT NOT NULL,  -- created/updated/ended
    previous_state JSON,
    new_state JSON,
    reason TEXT
);

-- 索引
CREATE INDEX idx_entities_type ON graph_entities(entity_type);
CREATE INDEX idx_relationships_from ON graph_relationships(from_entity);
CREATE INDEX idx_relationships_to ON graph_relationships(to_entity);
CREATE INDEX idx_relationships_type ON graph_relationships(type);
```

---

## 8. 设计决策与待调整项

### 已确定的设计

| 决策 | 理由 |
|---|---|
| 实体属性用 JSON 列 | Schema 灵活，新加字段不需要 ALTER TABLE |
| 关系变化记录全量历史 | 社会观察者核心需求——看关系如何演化 |
| 嵌入维度 768 | 与主流 embedding 模型兼容（text-embedding-3-small, bge 系列） |
| Agent 查询限制 2 跳 | 限制 Token 消耗，2 跳覆盖"朋友的朋友" |
| Item 图只收特殊物品 | 普通物品（食物/材料/消耗品）不入图，避免图谱膨胀 |

### ⚠️ 需要你确认

| # | 待定项 | 当前设计 | 需要确认 |
|---|---|---|---|
| 1 | 20 种关系类型是否够？ | R01-R20 | 还需要加：亲属(spouse以外)/债主/担保人/室友...? |
| 2 | Agent 查询跳数 | 2 hop | 是否需要扩展到 3 hop（朋友的朋友的朋友）？ |
| 3 | Character 是否有 `backstory` 字段 | 没有在 properties 里放（仅 name 用于嵌入） | 但 T-1 System Prompt 引用了 backstory，是否该存入？ |
| 4 | 嵌入模型 | bge-small-zh-v1.5 (512维) | 用 768 还是 384？本地还是 API？ |
| 5 | 向量DB 选型 | ChromaDB / lanceDB | 最终选哪个？ChromaDB 生态好但重，lanceDB 不用单独服务 |
| 6 | Character.skills 存储方式 | JSON 字段 `{skill_id: level}` | 是否单独建 Skill 实体类型？（PRD 有三级 Tool 学习） |
| 7 | Event 的 `public_knowledge` | 布尔值 | 真实情况是部分知情的渐进式——需要改成角色→事件的知识权限矩阵吗？ |

---

## 9. 实体关系示例图

```
                ┌──────────────────────────────────────────┐
                │              星露镇知识图谱 (局部)          │
                │                                          │
                │  [老王咖啡店]─────(位于)──→ [中心广场]      │
                │       │                        │         │
                │    (所有)                   (位于)        │
                │       │                        │         │
                │     [老王]──────(雇佣)──→ [小李]           │
                │       │                      │           │
                │    (朋友)                  (同事)          │
                │       │                      │           │
                │  ┌─[小明]─┐                   │           │
                │  │        │                   │           │
                │(拥有)  (恋爱)                  │           │
                │  │        │                   │           │
                │[咖啡机] [小美]←────────────────┘           │
                │           │                               │
                │        (隶属)                              │
                │           │                               │
                │     [小镇商会]────(领导)──→ [镇长张]        │
                │                                          │
                └──────────────────────────────────────────┘
```

---

*关联文档: [PRD §5.4 GraphRAG](../../01-concept/2026-06-26-ai-town-prd.md#54-graphrag-知识图谱-p0-6--p1-6) · [System Prompt 模板](./2026-06-28-agent-system-prompt.md) · [行动清单 §T-3](./2026-06-26-ai-town-action-checklist.md#t-3--graphrag-schema-定义)*
