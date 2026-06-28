# AI Town — Tool 完整清单 (API 规格)

> 日期: 2026-06-28 | 类型: 设计模板 | 关联: PRD §5.2, §3 (P0-3, P1-1)
> 依赖: 无 | 被依赖: System Prompt (T-1), Prompt Chain (T-9), Godot 开发

---

## 1. 概述

Tool 是 Agent 与游戏世界交互的唯一接口。每个 Tool 由 LLM 决策调用（JSON 格式），由 Godot 引擎执行并返回结果。

**核心原则**: Tool 是 Agent 的"手脚"——没有 Tool，Agent 只能思考和说话，不能对世界产生任何影响。

### 1.1 Tool 分类

| 优先级 | 类别 | 数量 | 说明 |
|---|---|---|---|
| P0 | 基础生存 | 10 | 移动、对话、吃喝、睡觉、观察、物品操作 |
| P1 | 社交+经济 | 12 | 买卖、建造、送礼、结婚、雇佣、学习 |
| P2 | 政治+高级 | 8 | 法律提案、投票、竞选、创业、抗议 |
| **合计** | | **30** | |

### 1.2 Tool 通用字段

每个 Tool 定义包含以下字段:

```json
{
  "name": "string",           // 唯一标识符 (snake_case)
  "display_name": "string",   // 中文显示名
  "description": "string",    // LLM 可读的一句话描述
  "priority": "P0|P1|P2",
  "category": "basic|social|economy|building|politics",
  "params": {},               // 参数 JSON Schema
  "returns": {},              // 返回值 JSON Schema
  "permission": "public|restricted|admin",  // 权限级别
  "unlock_condition": null | "string",      // 学习/解锁条件
  "cost": {                   // 执行成本
    "stamina": 0,             // 体力消耗
    "time_minutes": 0         // 游戏内时间消耗（分钟）
  }
}
```

---

## 2. P0 — 基础生存 Tool（10 个）

### T-001 move_to
```json
{
  "name": "move_to",
  "display_name": "移动到",
  "description": "移动到地图上的指定坐标或地点",
  "priority": "P0",
  "category": "basic",
  "params": {
    "target": {
      "type": "string",
      "description": "目标描述，可以是坐标('120,45') 或地点名('老王咖啡店') 或实体名('小明')"
    },
    "speed": {
      "type": "string",
      "enum": ["walk", "run"],
      "default": "walk",
      "description": "移动速度：走路或跑步（跑步体力消耗加倍）"
    }
  },
  "returns": {
    "type": "object",
    "properties": {
      "success": { "type": "boolean" },
      "arrived_at": { "type": "string", "description": "到达的位置描述" },
      "time_cost_minutes": { "type": "number" },
      "stamina_cost": { "type": "number" },
      "obstacles": { "type": "array", "description": "途中遇到的有趣事物（如有）" }
    }
  },
  "permission": "public",
  "unlock_condition": null,
  "cost": { "stamina": 1, "time_minutes": 5 }
}
```

### T-002 talk_to
```json
{
  "name": "talk_to",
  "display_name": "对话",
  "description": "与指定角色进行自然语言对话",
  "priority": "P0",
  "category": "social",
  "params": {
    "target": {
      "type": "string",
      "description": "对话对象的名字或身份描述"
    },
    "message": {
      "type": "string",
      "description": "你要说的话（自然语言，Agent 生成）",
      "max_length": 500
    },
    "tone": {
      "type": "string",
      "enum": ["friendly", "neutral", "formal", "angry", "sad", "joking", "romantic"],
      "default": "neutral",
      "description": "语气"
    },
    "topic": {
      "type": "string",
      "description": "话题标签（可选）：gossip / business / personal / news / ask_help / give_advice"
    }
  },
  "returns": {
    "type": "object",
    "properties": {
      "success": { "type": "boolean" },
      "target_response": { "type": "string", "description": "对方的回复（自然语言）" },
      "affinity_change": { "type": "number", "description": "好感度变化（正数增加，负数减少）" },
      "new_info": { "type": "array", "description": "对话中获得的新信息/线索" }
    }
  },
  "permission": "public",
  "unlock_condition": null,
  "cost": { "stamina": 0, "time_minutes": 5 }
}
```

### T-003 eat
```json
{
  "name": "eat",
  "display_name": "吃东西",
  "description": "消耗背包中的食物来减少饥饿值",
  "priority": "P0",
  "category": "basic",
  "params": {
    "item_name": {
      "type": "string",
      "description": "要吃的食物名称（必须背包中有）"
    },
    "where": {
      "type": "string",
      "enum": ["here", "restaurant", "home"],
      "default": "here",
      "description": "在哪里吃：现场吃/去餐厅/回家吃"
    }
  },
  "returns": {
    "type": "object",
    "properties": {
      "success": { "type": "boolean" },
      "hunger_restored": { "type": "number", "description": "恢复的饥饿值" },
      "mood_change": { "type": "number", "description": "美味程度带来的心情变化" },
      "item_consumed": { "type": "string" }
    }
  },
  "permission": "public",
  "unlock_condition": null,
  "cost": { "stamina": 0, "time_minutes": 15 }
}
```

### T-004 sleep
```json
{
  "name": "sleep",
  "display_name": "睡觉",
  "description": "睡觉休息，恢复体力。只能在可睡觉的地点（家/旅馆）执行",
  "priority": "P0",
  "category": "basic",
  "params": {
    "duration_hours": {
      "type": "number",
      "minimum": 1,
      "maximum": 12,
      "default": 8,
      "description": "睡眠时长（游戏小时）"
    },
    "location": {
      "type": "string",
      "description": "睡觉地点：home / inn / friend_house"
    }
  },
  "returns": {
    "type": "object",
    "properties": {
      "success": { "type": "boolean" },
      "stamina_restored": { "type": "number" },
      "mood_change": { "type": "number" },
      "health_change": { "type": "number", "description": "充足睡眠对健康的正面影响" },
      "dream": { "type": "string", "description": "做的梦（随机生成，可能触发记忆/洞察）" }
    }
  },
  "permission": "public",
  "unlock_condition": null,
  "cost": { "stamina": -30, "time_minutes": 480 }
}
```

### T-005 observe
```json
{
  "name": "observe",
  "display_name": "观察周围",
  "description": "仔细观察当前位置的周围环境，获取更详细的感知信息",
  "priority": "P0",
  "category": "basic",
  "params": {
    "focus": {
      "type": "string",
      "description": "观察重点：surroundings（环境）/ people（人物）/ items（物品）/ 或具体目标名"
    },
    "detail_level": {
      "type": "string",
      "enum": ["quick", "normal", "thorough"],
      "default": "normal",
      "description": "仔细程度（越仔细耗时越长）"
    }
  },
  "returns": {
    "type": "object",
    "properties": {
      "success": { "type": "boolean" },
      "observation": { "type": "string", "description": "观察到的详细描述" },
      "discovered": { "type": "array", "description": "新发现的实体（人/物/事件线索）" }
    }
  },
  "permission": "public",
  "unlock_condition": null,
  "cost": { "stamina": 0, "time_minutes": 2 }
}
```

### T-006 pickup_item
```json
{
  "name": "pickup_item",
  "display_name": "拾取物品",
  "description": "拾取地面上的物品放入背包",
  "priority": "P0",
  "category": "basic",
  "params": {
    "item": {
      "type": "string",
      "description": "要拾取的物品名称或描述"
    }
  },
  "returns": {
    "type": "object",
    "properties": {
      "success": { "type": "boolean" },
      "item_picked": { "type": "string" },
      "inventory_remaining_slots": { "type": "number" }
    }
  },
  "permission": "public",
  "unlock_condition": null,
  "cost": { "stamina": 1, "time_minutes": 1 }
}
```

### T-007 drop_item
```json
{
  "name": "drop_item",
  "display_name": "丢弃物品",
  "description": "丢弃背包中的指定物品",
  "priority": "P0",
  "category": "basic",
  "params": {
    "item": {
      "type": "string",
      "description": "要丢弃的物品名称"
    },
    "reason": {
      "type": "string",
      "description": "丢弃原因（可选，用于记忆记录）"
    }
  },
  "returns": {
    "type": "object",
    "properties": {
      "success": { "type": "boolean" },
      "item_dropped": { "type": "string" },
      "location_dropped_at": { "type": "string" }
    }
  },
  "permission": "public",
  "unlock_condition": null,
  "cost": { "stamina": 1, "time_minutes": 1 }
}
```

### T-008 use_item
```json
{
  "name": "use_item",
  "display_name": "使用物品",
  "description": "使用背包中的物品（工具/药品/钥匙等）",
  "priority": "P0",
  "category": "basic",
  "params": {
    "item": {
      "type": "string",
      "description": "要使用的物品名称"
    },
    "target": {
      "type": "string",
      "description": "使用目标（可选，如：用钥匙开门 → target='门'）"
    }
  },
  "returns": {
    "type": "object",
    "properties": {
      "success": { "type": "boolean" },
      "effect": { "type": "string", "description": "使用效果的描述" },
      "item_consumed": { "type": "boolean", "description": "是否为消耗品" }
    }
  },
  "permission": "public",
  "unlock_condition": null,
  "cost": { "stamina": 0, "time_minutes": 2 }
}
```

### T-009 open_door
```json
{
  "name": "open_door",
  "display_name": "开关门",
  "description": "打开或关闭一扇门，进入建筑或房间",
  "priority": "P0",
  "category": "basic",
  "params": {
    "action": {
      "type": "string",
      "enum": ["open", "close"],
      "description": "打开或关闭"
    },
    "door_location": {
      "type": "string",
      "description": "门的位置描述或坐标"
    }
  },
  "returns": {
    "type": "object",
    "properties": {
      "success": { "type": "boolean" },
      "room_entered": { "type": "string", "description": "进入的房间/建筑名" },
      "inside_description": { "type": "string" }
    }
  },
  "permission": "public",
  "unlock_condition": null,
  "cost": { "stamina": 0, "time_minutes": 1 }
}
```

### T-010 examine
```json
{
  "name": "examine",
  "display_name": "仔细检查",
  "description": "仔细检查一个物品、建筑或角色，获取详细信息",
  "priority": "P0",
  "category": "basic",
  "params": {
    "target": {
      "type": "string",
      "description": "要检查的目标名称或描述"
    }
  },
  "returns": {
    "type": "object",
    "properties": {
      "success": { "type": "boolean" },
      "description": { "type": "string", "description": "详细描述" },
      "hidden_detail": { "type": "string", "description": "可能发现的隐藏信息" },
      "skill_check": { "type": "string", "description": "触发技能检定（如有）" }
    }
  },
  "permission": "public",
  "unlock_condition": null,
  "cost": { "stamina": 0, "time_minutes": 2 }
}
```

---

## 3. P1 — 社交+经济 Tool（12 个）

### T-011 buy_item
```json
{
  "name": "buy_item",
  "display_name": "购买物品",
  "description": "从商店购买物品，需要足够金钱",
  "priority": "P1",
  "category": "economy",
  "params": {
    "item": { "type": "string", "description": "购买的物品名称" },
    "quantity": { "type": "integer", "minimum": 1, "default": 1 },
    "shop": { "type": "string", "description": "商店名" }
  },
  "returns": {
    "type": "object",
    "properties": {
      "success": { "type": "boolean" },
      "total_cost": { "type": "number" },
      "money_remaining": { "type": "number" },
      "items_received": { "type": "array" }
    }
  },
  "permission": "public",
  "unlock_condition": null,
  "cost": { "stamina": 1, "time_minutes": 5 }
}
```

### T-012 sell_item
```json
{
  "name": "sell_item",
  "display_name": "出售物品",
  "description": "向商店出售背包中的物品换取金钱",
  "priority": "P1",
  "category": "economy",
  "params": {
    "item": { "type": "string", "description": "出售的物品名称" },
    "quantity": { "type": "integer", "minimum": 1, "default": 1 },
    "shop": { "type": "string", "description": "商店名" }
  },
  "returns": {
    "type": "object",
    "properties": {
      "success": { "type": "boolean" },
      "income": { "type": "number" },
      "money_current": { "type": "number" }
    }
  },
  "permission": "public",
  "unlock_condition": null,
  "cost": { "stamina": 1, "time_minutes": 5 }
}
```

### T-013 give_gift
```json
{
  "name": "give_gift",
  "display_name": "赠送礼物",
  "description": "把背包中的物品赠送给指定角色",
  "priority": "P1",
  "category": "social",
  "params": {
    "target": { "type": "string", "description": "接收者姓名" },
    "item": { "type": "string", "description": "礼物（背包中的物品名）" },
    "message": { "type": "string", "description": "送礼时说的话（可选）" }
  },
  "returns": {
    "type": "object",
    "properties": {
      "success": { "type": "boolean" },
      "reaction": { "type": "string", "description": "对方的反应" },
      "affinity_change": { "type": "number", "description": "好感度变化（正负取决于是否喜欢）" },
      "preference_match": { "type": "string", "description": "loved/liked/neutral/disliked/hated" }
    }
  },
  "permission": "public",
  "unlock_condition": null,
  "cost": { "stamina": 0, "time_minutes": 5 }
}
```

### T-014 craft
```json
{
  "name": "craft",
  "display_name": "制作",
  "description": "使用材料和工具制作新物品",
  "priority": "P1",
  "category": "economy",
  "params": {
    "recipe": { "type": "string", "description": "配方名称" },
    "quantity": { "type": "integer", "minimum": 1, "default": 1 }
  },
  "returns": {
    "type": "object",
    "properties": {
      "success": { "type": "boolean" },
      "produced": { "type": "array", "description": "制作出的物品列表" },
      "materials_consumed": { "type": "object", "description": "消耗的材料" },
      "skill_gain": { "type": "object", "description": "技能经验增长" }
    }
  },
  "permission": "public",
  "unlock_condition": "需要对应配方和技能等级",
  "cost": { "stamina": 5, "time_minutes": 30 }
}
```

### T-015 build
```json
{
  "name": "build",
  "display_name": "建造",
  "description": "在拥有的 Plot 上建造建筑（PRD §5.6）",
  "priority": "P1",
  "category": "building",
  "params": {
    "plot_id": { "type": "string", "description": "Plot 编号" },
    "blueprint_name": { "type": "string", "description": "建筑蓝图名称" }
  },
  "returns": {
    "type": "object",
    "properties": {
      "success": { "type": "boolean" },
      "building_name": { "type": "string" },
      "construction_days": { "type": "number", "description": "预计完工天数" },
      "materials_required": { "type": "object" },
      "total_cost": { "type": "number" },
      "progress": { "type": "number", "description": "当前进度 0-1" }
    }
  },
  "permission": "public",
  "unlock_condition": "需要拥有 Plot 产权",
  "cost": { "stamina": 0, "time_minutes": 10 }
}
```

### T-016 plant
```json
{
  "name": "plant",
  "display_name": "种植",
  "description": "在农田/花园种植作物",
  "priority": "P1",
  "category": "economy",
  "params": {
    "seed": { "type": "string", "description": "种子名称" },
    "location": { "type": "string", "description": "种植位置（自己的农田 Plot/Garden）" }
  },
  "returns": {
    "type": "object",
    "properties": {
      "success": { "type": "boolean" },
      "expected_harvest_date": { "type": "string" },
      "expected_yield": { "type": "number" }
    }
  },
  "permission": "public",
  "unlock_condition": null,
  "cost": { "stamina": 3, "time_minutes": 15 }
}
```

### T-017 cook
```json
{
  "name": "cook",
  "display_name": "烹饪",
  "description": "使用食材烹饪食物",
  "priority": "P1",
  "category": "basic",
  "params": {
    "recipe": { "type": "string", "description": "菜谱名称" },
    "location": { "type": "string", "description": "烹饪地点（需要厨房）" }
  },
  "returns": {
    "type": "object",
    "properties": {
      "success": { "type": "boolean" },
      "dish": { "type": "string", "description": "做好的菜" },
      "quality": { "type": "string", "enum": ["burnt", "poor", "normal", "good", "excellent"] },
      "ingredients_used": { "type": "array" }
    }
  },
  "permission": "public",
  "unlock_condition": "需要菜谱和厨房",
  "cost": { "stamina": 2, "time_minutes": 20 }
}
```

### T-018 propose_marriage
```json
{
  "name": "propose_marriage",
  "display_name": "求婚",
  "description": "向好感度足够高的角色求婚",
  "priority": "P1",
  "category": "social",
  "params": {
    "target": { "type": "string", "description": "求婚对象姓名" },
    "ring_item": { "type": "string", "description": "求婚戒指（背包中的物品）", "default": null }
  },
  "returns": {
    "type": "object",
    "properties": {
      "accepted": { "type": "boolean" },
      "response": { "type": "string", "description": "对方的回应" },
      "requirements_check": {
        "type": "object",
        "properties": {
          "affinity": { "type": "boolean", "description": "好感度 ≥ 80？" },
          "relationship_status": { "type": "boolean", "description": "已确认恋爱关系？" },
          "housing": { "type": "boolean", "description": "有共同住所？" },
          "stability": { "type": "boolean", "description": "有稳定收入？" }
        }
      }
    }
  },
  "permission": "public",
  "unlock_condition": "好感度 ≥ 80，已确认恋爱关系",
  "cost": { "stamina": 2, "time_minutes": 5 }
}
```

### T-019 teach_skill
```json
{
  "name": "teach_skill",
  "display_name": "传授技能",
  "description": "向其他角色传授你掌握的技能（PRD §5.1 Tool 学习-师徒）",
  "priority": "P1",
  "category": "social",
  "params": {
    "target": { "type": "string", "description": "学生姓名" },
    "skill": { "type": "string", "description": "要传授的技能名称" }
  },
  "returns": {
    "type": "object",
    "properties": {
      "success": { "type": "boolean" },
      "student_progress": { "type": "number", "description": "学生技能增长" },
      "bond_strengthened": { "type": "number", "description": "师徒关系加深" }
    }
  },
  "permission": "public",
  "unlock_condition": "教授者技能等级 ≥ 学生技能等级+1",
  "cost": { "stamina": 3, "time_minutes": 60 }
}
```

### T-020 learn_skill
```json
{
  "name": "learn_skill",
  "display_name": "学习技能",
  "description": "通过练习/阅读/上课学习新技能或提升已有技能",
  "priority": "P1",
  "category": "basic",
  "params": {
    "skill": { "type": "string", "description": "要学习的技能名称" },
    "method": {
      "type": "string",
      "enum": ["practice", "read_book", "take_class", "online", "apprentice"],
      "description": "学习方式"
    },
    "cost_money": { "type": "number", "description": "学费/材料费（如适用）", "default": 0 }
  },
  "returns": {
    "type": "object",
    "properties": {
      "success": { "type": "boolean" },
      "skill_progress": { "type": "number", "description": "技能经验增加" },
      "level_up": { "type": "boolean", "description": "是否升级" }
    }
  },
  "permission": "public",
  "unlock_condition": "需要对应的学习材料或教师",
  "cost": { "stamina": 3, "time_minutes": 60 }
}
```

### T-021 hire_employee
```json
{
  "name": "hire_employee",
  "display_name": "雇佣员工",
  "description": "为自己的商铺/农场雇佣 NPC 员工",
  "priority": "P1",
  "category": "economy",
  "params": {
    "target": { "type": "string", "description": "雇佣对象" },
    "role": { "type": "string", "description": "职位" },
    "salary": { "type": "number", "description": "日薪" }
  },
  "returns": {
    "type": "object",
    "properties": {
      "accepted": { "type": "boolean" },
      "negotiation_result": { "type": "string" },
      "employee_added": { "type": "boolean" }
    }
  },
  "permission": "public",
  "unlock_condition": "拥有商业建筑",
  "cost": { "stamina": 0, "time_minutes": 15 }
}
```

---

## 4. P2 — 政治+高级 Tool（8 个）

### T-022 propose_law
```json
{
  "name": "propose_law",
  "display_name": "提出法案",
  "description": "向镇议会提出新的法律提案（PRD §5.5）",
  "priority": "P2",
  "category": "politics",
  "params": {
    "title": { "type": "string", "description": "法案标题" },
    "content": { "type": "string", "description": "法案详细内容（200字以内）" },
    "category": { "type": "string", "enum": ["tax", "crime", "business", "environment", "social", "other"] }
  },
  "returns": {
    "type": "object",
    "properties": {
      "submitted": { "type": "boolean" },
      "proposal_id": { "type": "string" },
      "required_signatures": { "type": "number", "description": "进入投票所需联署数" },
      "current_signatures": { "type": "number" }
    }
  },
  "permission": "public",
  "unlock_condition": "身份为成年公民",
  "cost": { "stamina": 1, "time_minutes": 30 }
}
```

### T-023 vote_law
```json
{
  "name": "vote_law",
  "display_name": "投票",
  "description": "对正在表决的法案投赞成或反对票",
  "priority": "P2",
  "category": "politics",
  "params": {
    "proposal_id": { "type": "string", "description": "法案编号" },
    "vote": { "type": "string", "enum": ["yes", "no", "abstain"] },
    "reason": { "type": "string", "description": "投票理由（可选，可能影响他人）" }
  },
  "returns": {
    "type": "object",
    "properties": {
      "voted": { "type": "boolean" },
      "current_count": { "type": "object", "description": "{yes, no, abstain} 当前票数" }
    }
  },
  "permission": "public",
  "unlock_condition": "已成年公民",
  "cost": { "stamina": 0, "time_minutes": 5 }
}
```

### T-024 run_for_office
```json
{
  "name": "run_for_office",
  "display_name": "竞选公职",
  "description": "参选镇政府公职（镇长/议员/法官）",
  "priority": "P2",
  "category": "politics",
  "params": {
    "position": { "type": "string", "enum": ["mayor", "councilor", "judge"] },
    "campaign_slogan": { "type": "string", "description": "竞选口号" },
    "platform": { "type": "string", "description": "政纲简述" }
  },
  "returns": {
    "type": "object",
    "properties": {
      "candidacy_accepted": { "type": "boolean" },
      "election_date": { "type": "string" },
      "current_polling": { "type": "number", "description": "当前民调支持率 0-1" }
    }
  },
  "permission": "public",
  "unlock_condition": "年龄 ≥ 25，良好声誉",
  "cost": { "stamina": 2, "time_minutes": 30 }
}
```

### T-025 start_business
```json
{
  "name": "start_business",
  "display_name": "创业注册",
  "description": "正式注册一家企业/商铺",
  "priority": "P2",
  "category": "economy",
  "params": {
    "business_name": { "type": "string", "description": "企业名称" },
    "type": { "type": "string", "enum": ["shop", "restaurant", "workshop", "farm", "service"] },
    "location_plot": { "type": "string", "description": "经营地址 Plot ID" },
    "initial_investment": { "type": "number", "description": "初始投资金额" }
  },
  "returns": {
    "type": "object",
    "properties": {
      "registered": { "type": "boolean" },
      "license_fee": { "type": "number" },
      "tax_rate": { "type": "number", "description": "适用税率" },
      "business_id": { "type": "string" }
    }
  },
  "permission": "public",
  "unlock_condition": "需要注册资金 + 营业执照",
  "cost": { "stamina": 1, "time_minutes": 60 }
}
```

### T-026 file_lawsuit
```json
{
  "name": "file_lawsuit",
  "display_name": "提起诉讼",
  "description": "对违反法律的角色提起诉讼",
  "priority": "P2",
  "category": "politics",
  "params": {
    "defendant": { "type": "string", "description": "被告姓名" },
    "charge": { "type": "string", "description": "罪名" },
    "evidence": { "type": "array", "description": "证据列表（物品/目击者）" }
  },
  "returns": {
    "type": "object",
    "properties": {
      "filed": { "type": "boolean" },
      "case_id": { "type": "string" },
      "court_date": { "type": "string" }
    }
  },
  "permission": "public",
  "unlock_condition": null,
  "cost": { "stamina": 1, "time_minutes": 30 }
}
```

### T-027 donate
```json
{
  "name": "donate",
  "display_name": "捐款",
  "description": "向组织或个人捐款",
  "priority": "P2",
  "category": "social",
  "params": {
    "target": { "type": "string", "description": "接收方：组织名/人名" },
    "amount": { "type": "number", "minimum": 1 },
    "anonymous": { "type": "boolean", "default": false }
  },
  "returns": {
    "type": "object",
    "properties": {
      "success": { "type": "boolean" },
      "reputation_change": { "type": "number" },
      "target_response": { "type": "string" }
    }
  },
  "permission": "public",
  "unlock_condition": null,
  "cost": { "stamina": 0, "time_minutes": 5 }
}
```

### T-028 investigate
```json
{
  "name": "investigate",
  "display_name": "调查",
  "description": "深入调查某个事件、角色或线索",
  "priority": "P2",
  "category": "basic",
  "params": {
    "subject": { "type": "string", "description": "调查对象" },
    "method": { "type": "string", "enum": ["ask_around", "follow_clues", "stake_out", "research_archive", "hire_detective"] }
  },
  "returns": {
    "type": "object",
    "properties": {
      "success": { "type": "boolean" },
      "findings": { "type": "array", "description": "调查发现的线索" },
      "new_lead": { "type": "string", "description": "新线索指向" }
    }
  },
  "permission": "public",
  "unlock_condition": null,
  "cost": { "stamina": 3, "time_minutes": 60 }
}
```

---

## 5. P3 — 预留扩展（示例）

| # | Tool | 简述 | 状态 |
|---|---|---|---|
| T-029 | `summon_meeting` | 召集组织成员开会 | 🔲 待设计 |
| T-030 | `publish_newspaper` | 办报纸/发布公告 | 🔲 待设计 |
| T-031 | `adopt_child` | 领养孩子 | 🔲 待设计 |
| T-032 | `bury_deceased` | 安葬逝者 | 🔲 待设计 |
| T-033 | `protest` | 组织抗议活动 | 🔲 待设计 |
| T-034 | `take_loan` | 银行贷款 | 🔲 待设计 |
| T-035 | `insure` | 购买保险 | 🔲 待设计 |

---

## 6. 设计决策与待调整项

### 已确定的设计

| 决策 | 理由 |
|---|---|
| Tool 调用用 JSON | 结构明确，Godot 直接解析 |
| `talk_to` 自然语言交由 LLM 生成 | 对话天然适合 LLM，不需要模板 |
| 每个 Tool 有体力+时间成本 | 防止 Agent 无限刷行为，引入资源约束 |
| NPC 也可以调用全部 Tool | 但受限于角色设定（警察不会开店、店主不会执法）|
| P2 法律 Tool 全员可用 | 实现"人人可参政"的议会民主设计 |

### ⚠️ 需要你确认

| # | 待定项 | 当前填入 | 需要确认 |
|---|---|---|---|
| 1 | Tool 总数 | 28 (P0+P1+P2) + 7 (P3 预留) | 是否够？是否太多？ |
| 2 | 体力/时间成本数值 | 见各 Tool cost 字段 | 只是个初始猜测，需要 T-6 经济数值表对齐 |
| 3 | `talk_to` 消息最大长度 | 500 字 | 太长浪费 Token，太短限制表达 |
| 4 | 是否加 `wait` Tool | 当前没加 | Agent 可以 tool_call=null 来"不做任何事"，是否需要一个显式的 wait/rest Tool？ |
| 5 | 技能系统对接 | T-014 craft / T-020 learn_skill 引用技能 | 技能列表(skill_catalog)需要单独定义还是放进此文档？ |
| 6 | `examine` vs `observe` | 两个相似 Tool | examine=仔细检查具体目标，observe=扫描环境，是否合并？ |
| 7 | NPC 是否能自主调用 `build` | 目前权限为 public | 如果 NPC 可以自己建房子，小镇发展可能失控 |

---

## 7. Tool 交互流程图

```
Agent 决策输出 JSON
  │
  ▼
Godot 解析 tool_call
  │
  ├─ 权限检查 (permission)
  ├─ 解锁条件检查 (unlock_condition)
  ├─ 资源检查 (cost: stamina + money)
  │
  ├─ 全部通过 → 执行 → 返回 returns JSON
  └─ 检查失败 → 返回 {"success": false, "reason": "..."}
       │
       ▼
Agent 收到结果 → 写入情景记忆 → 下个决策周期
```

---

*关联文档: [PRD §5.2 Agent 决策循环](../../01-concept/2026-06-26-ai-town-prd.md#52-agent-决策循环-p0-4) · [System Prompt 模板](./2026-06-28-agent-system-prompt.md) · [行动清单 §T-2](./2026-06-26-ai-town-action-checklist.md#t-2--tool-完整清单-api-规格)*
