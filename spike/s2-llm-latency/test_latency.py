"""
S2 Spike — DeepSeek API Agent Decision Latency Test

测试完整 Agent 决策请求的端到端延迟。
模拟真实 Prompt（System Prompt + 感知 + 记忆 + Tool 列表），
测量 TTFB、总耗时、输出 tokens/秒。

目标: P50 < 10s

DeepSeek API 兼容 OpenAI SDK，也可直接 HTTP。

Usage:
    # 设置 API Key
    set DEEPSEEK_API_KEY=sk-xxxx   (Windows PowerShell: $env:DEEPSEEK_API_KEY="sk-xxxx")

    # 运行测试
    pip install openai httpx
    python test_latency.py
"""

import os
import time
import json
import statistics
import sys

# --- System Prompt Template (模拟 NPC Agent) ---
NPC_SYSTEM_PROMPT = """你是一个生活模拟游戏中的 NPC，名叫"艾米莉"。

## 身份
- 年龄: 28岁
- 职业: 咖啡店老板
- 性格: 开朗、勤劳、热心，偶尔会为新菜单焦虑
- 当前位置: 小镇中心广场东侧 艾米莉咖啡馆

## 当前感知
- 时间: 上午 9:30，晴天
- 店内: 3 位顾客在喝咖啡
- 店外: 广场上有行人在散步
- 咖啡豆库存: 剩 40%，需要补货

## 最近记忆 (Top-3 相关)
1. (3天前) 邻居"汤姆"说想办生日派对，预定了 20 人份的咖啡和蛋糕
2. (昨天) 玩家角色"小明"来店里聊了半小时，说想创业
3. (今早) 供货商发消息说咖啡豆涨价了 15%

## 可用工具
你可以使用以下 JSON 格式调用工具:
- talk_to(target, message) — 与目标角色对话
- move_to(x, y) — 移动到地图坐标
- prepare_order(items[]) — 准备订单
- order_supplies(item, quantity) — 订购供应品
- clean_store() — 打扫店铺
- open_door() / close_door() — 开关店门

## 长期目标
- 把咖啡馆经营成全小镇最受欢迎的店
- 赚够钱扩展二楼做烘焙工坊

## 行为约束
- 只做合理、符合角色设定的事
- 不能伤害他人或偷窃
- 保持对话自然、友好

---
根据以上信息，决定你接下来要做什么。以 JSON 格式输出:
{
  "thought": "你的内心想法 (一句)",
  "action": "工具名称 或 'idle'",
  "params": {},
  "emotion": "当前情绪"
}
"""


def build_agent_request(prompt_length: str = "full") -> list[dict]:
    """构建 Agent 决策请求消息"""
    system = NPC_SYSTEM_PROMPT

    if prompt_length == "short":
        # 简短版 (约 500 tokens)
        system = NPC_SYSTEM_PROMPT[:500]
    elif prompt_length == "medium":
        # 中等版 (约 1000 tokens)
        system = NPC_SYSTEM_PROMPT[:1000]

    return [
        {"role": "system", "content": system},
        {"role": "user", "content": "现在该做什么？请用 JSON 回复你的决策。"},
    ]


def estimate_tokens(messages: list[dict]) -> int:
    """粗略估算 tokens (英文: ~1 token/4 chars)"""
    total_chars = sum(len(m["content"]) for m in messages)
    return total_chars // 4


def test_single(
    client,
    model: str,
    messages: list[dict],
    max_tokens: int = 256,
) -> dict:
    """单次请求，返回延迟数据"""
    start = time.time()

    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=0.7,
            stream=False,
        )
    except Exception as e:
        return {"error": str(e)}

    total_ms = (time.time() - start) * 1000

    return {
        "total_ms": total_ms,
        "prompt_tokens": response.usage.prompt_tokens if response.usage else 0,
        "completion_tokens": response.usage.completion_tokens if response.usage else 0,
        "total_tokens": response.usage.total_tokens if response.usage else 0,
        "finish_reason": response.choices[0].finish_reason if response.choices else "unknown",
    }


def test_streaming(
    client,
    model: str,
    messages: list[dict],
    max_tokens: int = 256,
) -> dict:
    """Streaming 请求，测量 TTFB"""
    start = time.time()
    ttfb = None
    token_count = 0
    first_token = None

    try:
        stream = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=0.7,
            stream=True,
        )
        for chunk in stream:
            if ttfb is None and chunk.choices:
                if chunk.choices[0].delta.content:
                    ttfb = (time.time() - start) * 1000
                    first_token = chunk.choices[0].delta.content
            if chunk.choices and chunk.choices[0].delta.content:
                token_count += 1
    except Exception as e:
        return {"error": str(e)}

    total_ms = (time.time() - start) * 1000

    return {
        "ttfb_ms": ttfb or total_ms,
        "total_ms": total_ms,
        "token_count": token_count,
        "tokens_per_sec": token_count / (total_ms / 1000) if total_ms > 0 else 0,
        "first_token": first_token,
    }


def print_stats(name: str, values: list[float], unit: str = "ms"):
    """打印延迟统计"""
    sorted_v = sorted(values)
    n = len(sorted_v)

    def pct(p):
        return sorted_v[min(int(n * p / 100), n - 1)]

    print(f"\n  {name}:")
    print(f"    Min / P50 / P95 / P99 / Max = "
          f"{sorted_v[0]:.0f} / {pct(50):.0f} / {pct(95):.0f} / {pct(99):.0f} / {sorted_v[-1]:.0f} {unit}")


def main():
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        print("=" * 60)
        print("  ⚠️  DEEPSEEK_API_KEY not set")
        print("=" * 60)
        print("\n  Set your API key first:\n")
        print("    PowerShell: $env:DEEPSEEK_API_KEY=\"sk-xxxx\"")
        print("    CMD       : set DEEPSEEK_API_KEY=sk-xxxx")
        print("    Bash      : export DEEPSEEK_API_KEY=sk-xxxx")
        print("\n  Then run:  python test_latency.py")
        print("\n=" * 60)
        sys.exit(0)

    try:
        from openai import OpenAI
    except ImportError:
        print("[SETUP] Install openai first: pip install openai")
        sys.exit(1)

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com",
    )

    model = "deepseek-chat"
    test_count = 10  # 测试次数（控制成本）

    print("=" * 60)
    print("  S2 Spike: DeepSeek API Agent Decision Latency")
    print("=" * 60)
    print(f"  Model       : {model}")
    print(f"  Test count  : {test_count} (per variant)")
    print(f"  Target      : P50 < 10s (10000ms)")
    print("=" * 60)

    # === Test 1: Non-streaming (模拟批量 NPC 心跳) ===
    print("\n[TEST 1] Non-streaming — Agent Decision (full prompt)")
    messages = build_agent_request("full")
    est_tokens = estimate_tokens(messages)
    print(f"  Estimated input tokens: ~{est_tokens}")

    results = []
    for i in range(test_count):
        print(f"  [{i+1}/{test_count}] ", end="", flush=True)
        r = test_single(client, model, messages)
        if "error" in r:
            print(f"ERROR: {r['error']}")
        else:
            print(f"{r['total_ms']:.0f}ms  "
                  f"(in:{r['prompt_tokens']} out:{r['completion_tokens']} "
                  f"total:{r['total_tokens']}tokens)")
            results.append(r)

    if results:
        totals = [r["total_ms"] for r in results]
        print_stats("Total latency (non-streaming)", totals, "ms")

        p50 = sorted(totals)[len(totals)//2]
        if p50 < 10000:
            print(f"\n  ✅ PASSED: P50 = {p50:.0f}ms < 10000ms")
        else:
            print(f"\n  ❌ FAILED: P50 = {p50:.0f}ms >= 10000ms")

    # === Test 2: Streaming (模拟玩家 Agent 实时响应) ===
    print(f"\n{'='*60}")
    print("[TEST 2] Streaming — TTFB (Time to First Byte)")
    print(f"{'='*60}")

    stream_results = []
    for i in range(test_count):
        print(f"  [{i+1}/{test_count}] ", end="", flush=True)
        r = test_streaming(client, model, messages)
        if "error" in r:
            print(f"ERROR: {r['error']}")
        else:
            print(f"TTFB:{r['ttfb_ms']:.0f}ms  "
                  f"Total:{r['total_ms']:.0f}ms  "
                  f"Tokens:{r['token_count']} "
                  f"({r['tokens_per_sec']:.0f} tok/s)")
            stream_results.append(r)

    if stream_results:
        ttfbs = [r["ttfb_ms"] for r in stream_results]
        print_stats("TTFB (first token)", ttfbs, "ms")
        totals_s = [r["total_ms"] for r in stream_results]
        print_stats("Total latency (streaming)", totals_s, "ms")

    # === Test 3: Short prompt (模拟简单反射) ===
    print(f"\n{'='*60}")
    print("[TEST 3] Short prompt — Simple reflex (no memory context)")
    print(f"{'='*60}")
    short_msgs = build_agent_request("short")

    short_results = []
    for i in range(5):
        print(f"  [{i+1}/5] ", end="", flush=True)
        r = test_single(client, model, short_msgs, max_tokens=128)
        if "error" in r:
            print(f"ERROR: {r['error']}")
        else:
            print(f"{r['total_ms']:.0f}ms  ({r['total_tokens']} tokens)")
            short_results.append(r)

    if short_results:
        print_stats("Short prompt latency", [r["total_ms"] for r in short_results], "ms")

    # === Summary ===
    all_results = results + short_results
    if all_results:
        all_totals = sorted([r["total_ms"] for r in all_results])
        n = len(all_totals)
        p50 = all_totals[n // 2]
        p95 = all_totals[min(int(n * 0.95), n - 1)]

        print(f"\n{'='*60}")
        print(f"  FINAL VERDICT")
        print(f"{'='*60}")
        print(f"  P50: {p50:.0f}ms  |  P95: {p95:.0f}ms")
        if p50 < 10000:
            print(f"  ✅ SPIKE PASSED: Agent decision P50 < 10s")
        else:
            print(f"  ❌ SPIKE FAILED: Consider prompt optimization or faster model")
        print(f"{'='*60}")


if __name__ == "__main__":
    main()
