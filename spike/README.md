# Technical Spikes — AI Town 技术验证

> 日期: 2026-06-27 | 关联: [行动清单](../docs/superpowers/specs/02-pre-production/2026-06-26-ai-town-action-checklist.md)

---

## 目录

| # | Spike | 目录 | 状态 | 目标 |
|---|---|---|---|---|
| S1 | Godot 4 + Python gRPC Echo | `s1-grpc/` | ✅ | 本机通信延迟 < 50ms |
| S2 | DeepSeek API Agent 决策延迟 | `s2-llm-latency/` | ✅ | 端到端 P50 < 10s |
| S3 | Godot Tilemap 分块渲染 | (待 S1 通过后) | 🔲 | 1000×1000 分块 60 FPS |

---

## 快速启动

### S1 — gRPC 通信测试

```bash
cd spike/s1-grpc

# 1. 安装依赖 + 编译 proto
pip install -r requirements.txt
python -m grpc_tools.protoc -Iproto --python_out=. --grpc_python_out=. proto/echo.proto

# 2. 启动 gRPC 服务端
python grpc_server.py

# 3. 另一终端，运行 gRPC 客户端延迟测试
python grpc_client.py

# 4. (可选) 启动 HTTP Bridge 给 Godot 用
python http_bridge.py

# 5. 用 Godot 4 打开 game/project.godot，运行场景
```

### S2 — LLM 延迟测试

```bash
cd spike/s2-llm-latency

# 1. 安装依赖
pip install -r requirements.txt

# 2. 设置 API Key
# PowerShell:
$env:DEEPSEEK_API_KEY = "sk-xxxx"
# CMD:
set DEEPSEEK_API_KEY=sk-xxxx

# 3. 运行
python test_latency.py
```

---

## 结果记录

| Spike | 日期 | P50 | P95 | 结论 | 备注 |
|---|---|---|---|---|---|
| S1 gRPC | 2026-06-27 | 0.3ms | — | ✅ PASS | 远超预期 (目标<50ms) |
| S1 HTTP Bridge | 2026-06-28 | 30.3ms | 48.3ms | ✅ PASS | Godot→Python GET /echo, 127.0.0.1 |
| S2 DeepSeek | 2026-06-27 | 1449ms | 3828ms | ✅ PASS | 远超预期 (目标<10s) |
| S3 Tilemap | | | | | 待 S1 确认后启动 |

---

*关联: [预生产行动清单](../docs/superpowers/specs/02-pre-production/2026-06-26-ai-town-action-checklist.md)*
