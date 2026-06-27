"""
S1 Spike — HTTP Bridge for Godot↔Python Communication

Godot 4 没有原生 gRPC 支持，使用 HTTP JSON 作为桥接层。
Python 侧运行此 HTTP 服务，Godot 通过 HTTPRequest 节点调用。

此方案优势:
  - Godot 原生支持 HTTP (HTTPRequest 节点)
  - JSON 序列化简单，调试方便
  - localhost HTTP 延迟通常 < 5ms
  - 后续可升级为 gRPC + GDExtension 或 WebSocket

Usage:
    python http_bridge.py
    # 默认监听 http://localhost:8080
"""

import time
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import sys


class BridgeHandler(BaseHTTPRequestHandler):
    """处理 Godot 的 HTTP 请求"""

    def do_GET(self):
        if self.path == "/ping":
            self._handle_ping()
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'{"error": "not found"}')

    def do_POST(self):
        if self.path == "/echo":
            self._handle_echo()
        elif self.path == "/ping":
            self._handle_ping()
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'{"error": "not found"}')

    def _handle_ping(self):
        """GET /ping — 快速连通性检查"""
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps({
            "status": "ok",
            "server_ts_ns": time.time_ns(),
        }).encode())

    def _handle_echo(self):
        """POST /echo — 延迟测试"""
        content_length = int(self.headers.get("Content-Length", 0))
        server_recv_ts = time.time_ns()

        body = self.rfile.read(content_length)
        server_process_ts = time.time_ns()
        recv_overhead_ms = (server_process_ts - server_recv_ts) / 1_000_000

        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'{"error": "invalid json"}')
            return

        client_ts_ns = data.get("client_ts_ns", 0)
        payload = data.get("payload", "")
        payload_size = len(body)

        response = {
            "message": f"echo: {data.get('message', '')}",
            "client_ts_ns": client_ts_ns,
            "server_recv_ts_ns": server_recv_ts,
            "server_send_ts_ns": time.time_ns(),
            "recv_overhead_ms": recv_overhead_ms,
            "payload_size_bytes": payload_size,
        }

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

    def do_OPTIONS(self):
        """CORS preflight"""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def log_message(self, format, *args):
        """简洁日志"""
        print(f"[HTTP] {args[0]}")


def serve(port: int = 8080):
    server = HTTPServer(("localhost", port), BridgeHandler)
    print(f"[HTTP Bridge] Listening on http://localhost:{port}")
    print(f"[HTTP Bridge] Endpoints: GET /ping | POST /echo")
    print(f"[HTTP Bridge] Press Ctrl+C to stop")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[HTTP Bridge] Server stopped.")
        server.server_close()


if __name__ == "__main__":
    serve()
