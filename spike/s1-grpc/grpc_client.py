"""
S1 Spike — Python gRPC Client (Latency Test)

测试 Python↔Python 纯 gRPC 通信延迟。
目标: P50 < 50ms, P99 < 100ms (localhost)。

Usage:
    python grpc_client.py
"""

import time
import json
import sys
import os
import statistics

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import grpc

try:
    import echo_pb2
    import echo_pb2_grpc
except ImportError:
    print("[SETUP] Proto not compiled. Run:")
    print("  cd spike/s1-grpc")
    print("  python -m grpc_tools.protoc -Iproto --python_out=. --grpc_python_out=. proto/echo.proto")
    sys.exit(1)


def test_ping(stub, n: int = 100) -> list[float]:
    """Ping-Pong 测试，返回每次 RTT 毫秒列表"""
    latencies = []
    for i in range(n):
        client_ts = time.time_ns()
        response = stub.Ping(echo_pb2.PingRequest(
            message=f"ping_{i}",
            client_ts_ns=client_ts,
        ))
        rtt_ms = (time.time_ns() - client_ts) / 1_000_000  # ns → ms
        latencies.append(rtt_ms)
    return latencies


def test_payload(stub, payload_size: int = 4096, n: int = 50) -> list[float]:
    """Payload Echo 测试，模拟实际 Agent 消息大小 (2-10KB)"""
    latencies = []
    # 生成模拟 Agent 请求 JSON
    sample_payload = json.dumps({
        "agent_id": "npc_001",
        "type": "decision_request",
        "system_prompt": "..." * 100,  # padding
        "perception": {"tile": 1234, "nearby_npcs": ["npc_002", "npc_003"]},
        "memories": [{"id": i, "content": f"Memory {i}"} for i in range(5)],
        "tools": ["move_to", "talk_to", "eat", "sleep"],
        "padding": "x" * (payload_size - 300),  # fill to target size
    }, ensure_ascii=False)

    for i in range(n):
        client_ts = time.time_ns()
        response = stub.EchoPayload(echo_pb2.EchoPayloadRequest(
            payload=sample_payload,
            client_ts_ns=client_ts,
            payload_size_bytes=len(sample_payload.encode('utf-8')),
        ))
        rtt_ms = (time.time_ns() - client_ts) / 1_000_000
        latencies.append(rtt_ms)
    return latencies


def print_stats(name: str, latencies: list[float]):
    """打印延迟统计"""
    sorted_lat = sorted(latencies)
    n = len(sorted_lat)

    def pct(p):
        idx = int(n * p / 100)
        return sorted_lat[min(idx, n - 1)]

    print(f"\n{'='*60}")
    print(f"  {name}")
    print(f"{'='*60}")
    print(f"  Samples : {n}")
    print(f"  Min     : {min(sorted_lat):.2f} ms")
    print(f"  P50     : {pct(50):.2f} ms")
    print(f"  P95     : {pct(95):.2f} ms")
    print(f"  P99     : {pct(99):.2f} ms")
    print(f"  Max     : {max(sorted_lat):.2f} ms")
    print(f"  Mean    : {statistics.mean(sorted_lat):.2f} ms")


def warmup(stub):
    """预热连接"""
    print("[WARMUP] 预热 gRPC 连接 (5 次)...")
    for _ in range(5):
        stub.Ping(echo_pb2.PingRequest(message="warmup", client_ts_ns=time.time_ns()))


def main():
    # 连接服务端
    channel = grpc.insecure_channel("localhost:50051")
    stub = echo_pb2_grpc.EchoStub(channel)

    try:
        grpc.channel_ready_future(channel).result(timeout=5)
        print("[OK] gRPC channel connected to localhost:50051")
    except grpc.FutureTimeoutError:
        print("[ERROR] Cannot connect to gRPC server. Start it first:")
        print("  python grpc_server.py")
        sys.exit(1)

    warmup(stub)

    # Test 1: 简单 Ping-Pong
    ping_lat = test_ping(stub, n=100)
    print_stats("Ping-Pong (100 samples)", ping_lat)

    # Test 2: 2KB payload (模拟短 Agent 请求)
    small_lat = test_payload(stub, payload_size=2048, n=50)
    print_stats("Payload Echo 2KB (50 samples)", small_lat)

    # Test 3: 8KB payload (模拟完整 Agent 决策请求)
    large_lat = test_payload(stub, payload_size=8192, n=50)
    print_stats("Payload Echo 8KB (50 samples)", large_lat)

    # Test 4: 16KB payload (上限压力测试)
    huge_lat = test_payload(stub, payload_size=16384, n=20)
    print_stats("Payload Echo 16KB (20 samples)", huge_lat)

    # 判定
    all_lat = ping_lat + small_lat + large_lat
    p50 = sorted(all_lat)[len(all_lat) // 2]
    print(f"\n{'='*60}")
    if p50 < 50:
        print(f"  ✅ SPIKE PASSED: P50 = {p50:.1f} ms < 50ms")
    else:
        print(f"  ❌ SPIKE FAILED: P50 = {p50:.1f} ms >= 50ms")
    print(f"{'='*60}")

    channel.close()


if __name__ == "__main__":
    main()
