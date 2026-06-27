"""
S1 Spike — Python gRPC Echo Server

AI Town Godot↔Python 通信的 gRPC 服务端。
本机 localhost 通信，目标延迟 < 50ms。

Usage:
    python grpc_server.py
    # 或先编译 proto:
    # python -m grpc_tools.protoc -Iproto --python_out=. --grpc_python_out=. proto/echo.proto
"""

import time
import sys
import os

# Add proto-generated code path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from concurrent import futures
import grpc

# --- Proto generated imports ---
# 如果尚未编译 proto，先运行:
#   python -m grpc_tools.protoc -Iproto --python_out=. --grpc_python_out=. proto/echo.proto
try:
    import echo_pb2
    import echo_pb2_grpc
except ImportError:
    print("[SETUP] Proto not compiled. Run:")
    print("  cd spike/s1-grpc")
    print("  pip install -r requirements.txt")
    print("  python -m grpc_tools.protoc -Iproto --python_out=. --grpc_python_out=. proto/echo.proto")
    sys.exit(1)


class EchoService(echo_pb2_grpc.EchoServicer):
    """Echo 服务实现"""

    def Ping(self, request, context):
        """Ping-Pong 延迟测试"""
        server_ts = time.time_ns()
        reply = echo_pb2.PingReply(
            message=f"pong: {request.message}",
            client_ts_ns=request.client_ts_ns,
            server_ts_ns=server_ts,
        )
        return reply

    def EchoPayload(self, request, context):
        """带 Payload 的 Echo（模拟 Agent 请求 ~2-10KB）"""
        server_ts = time.time_ns()
        rtt_us = int((server_ts - request.client_ts_ns) / 1000)

        reply = echo_pb2.EchoPayloadReply(
            payload=request.payload,
            client_ts_ns=request.client_ts_ns,
            server_ts_ns=server_ts,
            roundtrip_us=rtt_us,
        )
        return reply


def serve(port: int = 50051):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    echo_pb2_grpc.add_EchoServicer_to_server(EchoService(), server)
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    print(f"[gRPC] Echo server listening on port {port}")
    print(f"[gRPC] Press Ctrl+C to stop")
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("\n[gRPC] Server stopped.")


if __name__ == "__main__":
    serve()
