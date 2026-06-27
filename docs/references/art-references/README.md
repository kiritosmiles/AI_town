# AI Town — 美术参考收集

> 日期: 2026-06-27 | 用途: 确定视觉方向，为后续美术制作提供参考
> 关联: [Tile 规格决策](../../superpowers/specs/02-pre-production/2026-06-27-tile-spec-decision.md)

---

## 参考清单

### 1. 星露谷物语 (Stardew Valley) ⭐ 首要参考

| 维度 | 参考点 |
|---|---|
| **为什么参考** | 俯视像素小镇、农场经营、NPC 社交，最接近 AI Town 的核心体验 |
| **Tile 风格** | 32×32 标准 Tile，暖色调，季节性变化 |
| **角色** | 像素角色 32×48 范围，4 方向行走帧，简约但表情丰富 |
| **建筑** | 多 Tile 组合建筑，室内外切换，建筑升级可视化 |
| **UI** | 右侧背包/菜单面板，简约字体，棕色木纹主题 |
| **截图搜索** | "Stardew Valley town map", "Stardew Valley NPC对话", "Stardew Valley farm layout" |

### 2. 宝可梦 心金/魂银 (Pokémon HGSS)

| 维度 | 参考点 |
|---|---|
| **为什么参考** | 日式小镇/城市俯视设计黄金标准，建筑排列、道路规划极佳 |
| **Tile 风格** | 16×16 Tile（较小），但场景组合逻辑值得学习 |
| **建筑** | 屋顶样式多样，公共建筑（精灵中心/道馆/商店）识别度高 |
| **自然** | 草地、水域、树木、山崖的层次感 |
| **截图搜索** | "Pokemon HGSS town map", "Pokemon HGSS cherrygrove city", "Pokemon HGSS ecruteak" |

### 3. RPG Maker MV/MZ RTP 素材

| 维度 | 参考点 |
|---|---|
| **为什么参考** | RPG Maker 风格的直接标准，AI Town 的美学基础 |
| **Tile** | 48×48 Tile（高于我们的 32px，但风格可参考） |
| **角色** | 48×48 行走图，4 方向 3 帧 |
| **获取方式** | 购买 RPG Maker MV/MZ 后可导出 RTP 素材作为参考 |
| **替代方案** | [itch.io RPG Maker tilesets](https://itch.io/game-assets/tag-rpg-maker) |

### 4. Omori

| 维度 | 参考点 |
|---|---|
| **为什么参考** | 现代像素 RPG 美术标杆，手绘感强，色彩运用大胆 |
| **色彩** | 梦幻/忧郁双色调，大面积色块 + 细节像素 |
| **UI** | 极简手绘风格 UI，战斗/菜单界面有很强的辨识度 |
| **截图搜索** | "Omori gameplay screenshot", "Omori town", "Omori UI" |

### 5. Eastward（风来之国）

| 维度 | 参考点 |
|---|---|
| **为什么参考** | 高品质像素风天花板，光影和动画表现力极强 |
| **光照** | 动态光影 + 像素风结合，氛围感极佳 |
| **动画** | 角色动画帧数多、动作流畅 |
| **注意** | Eastward 是高端商业水准，AI Town 降低一档追求可行性 |
| **截图搜索** | "Eastward gameplay", "Eastward town", "Eastward pixel art" |

### 6. 动物森友会 (Animal Crossing: New Horizons) — UI 参考

| 维度 | 参考点 |
|---|---|
| **为什么参考** | 生活模拟 UI/UX 最成熟的产品 |
| **UI** | 物品栏网格、对话气泡、NookPhone 应用式菜单 |
| **对话** | 气泡对话 + 情绪表情 + NPC 主动搭话 |
| **截图搜索** | "Animal Crossing dialogue UI", "Animal Crossing inventory", "Animal Crossing town layout" |

---

## 像素美术风格方向（3 选 1）

### 方向 A: 经典 RPG Maker（推荐 — 开发成本最低）

- **特征**: 干净线条、顶光阴影、饱和色适中
- **Tile 样板**: RPG Maker MV RTP Outside tileset
- **优点**: 素材生态最丰富，RPG Maker 社区直接可用，玩家认知度高
- **缺点**: 辨识度略低（和大量 RPG Maker 游戏撞脸）

### 方向 B: 柔和暖色调（星露谷风）

- **特征**: 暖色主导、低对比、柔和阴影、"温暖农场感"
- **Tile 样板**: Stardew Valley 草地/建筑 Tile
- **优点**: 情感共鸣强，适合生活模拟
- **缺点**: 需要统一调色板，素材需大量定制

### 方向 C: 现代像素（Omori/Eastward 风）

- **特征**: 高对比、大胆配色、手绘感、光影运用
- **优点**: 辨识度极高，截图营销效果好
- **缺点**: 美术工作量最大，需要专业像素画师

> **当前建议**: 以方向 A 为基底（快速出原型），逐步融入方向 B 的暖色调。方向 C 作为后续 DLC/增强版的视觉升级方向。

---

## 色彩板（初版）

```
主色调:
  草地    #7EC850  (翠绿)
  土地    #C89458  (黄褐)
  道路    #A0A0A0  (灰石)
  水域    #5090D0  (天蓝)
  建筑墙  #E8D8B8  (米白)
  建筑顶  #C05040  (红瓦)

UI:
  背景    #2B2B2B  (深灰)
  面板    #3C3C3C  (中灰)
  高亮    #FFD700  (金)
  文字    #F0F0F0  (近白)
```

---

## 免费像素素材资源

| 来源 | 说明 |
|---|---|
| [itch.io — Pixel Art Tilesets](https://itch.io/game-assets/free/tag-pixel-art/tag-tileset) | 大量免费/廉价像素 Tile 素材 |
| [OpenGameArt](https://opengameart.org/) | CC0 和 CC-BY 素材 |
| [kenney.nl](https://kenney.nl/assets) | 高质量免费游戏素材（含像素包） |
| [CraftPix.net](https://craftpix.net/freebies/) | 免费 + 付费像素素材 |
| [The Spriters Resource](https://www.spriters-resource.com/) | 老游戏精灵拆解参考（仅供研究） |

---

## 下一步

1. 从每个参考游戏截 1-2 张截图，放入 `screenshots/` 子目录
2. 标注每张截图中借鉴的具体元素
3. 最终确定方向后，更新 [Tile 规格决策](../../superpowers/specs/02-pre-production/2026-06-27-tile-spec-decision.md)

---

*关联: [行动清单 §T-4](../../superpowers/specs/02-pre-production/2026-06-26-ai-town-action-checklist.md#t-4--rpg-maker-美术参考图收集) · [开发全流程 §2.2 美术风格](../../superpowers/specs/02-pre-production/2026-06-26-ai-town-development-workflow.md#22-美术风格定义)*
