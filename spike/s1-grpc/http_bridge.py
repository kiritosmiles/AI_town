"""
S1 Spike — HTTP Bridge for Godot↔Python Communication

Usage:
    python http_bridge.py
    # 默认监听 http://localhost:8080
"""

import time
import json
from urllib.parse import urlparse, parse_qs
from http.server import HTTPServer, BaseHTTPRequestHandler


class BridgeHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/ping":
            self._handle_ping()
        elif path == "/echo":
            self._handle_echo_get(parse_qs(parsed.query))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'{"error": "not found"}')

    def do_POST(self):
        if self.path == "/echo":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length) if content_length > 0 else b'{}'
            try:
                data = json.loads(body)
            except json.JSONDecodeError:
                data = {}
            self._handle_echo(data)
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'{"error": "not found"}')

    def _handle_ping(self):
        self._send_json({"status": "ok", "server_ts_ns": time.time_ns()})

    def _handle_echo_get(self, qs: dict):
        """GET /echo?msg=N&ts=NS&payload=N — 延迟测试 (给 Godot HTTPRequest 用)"""
        client_ts_ns = int(qs.get("ts", [0])[0])
        message = qs.get("msg", [""])[0]

        self._send_json({
            "message": f"echo: {message}",
            "client_ts_ns": client_ts_ns,
            "server_ts_ns": time.time_ns(),
        })

    def _handle_echo(self, data: dict):
        """POST /echo — 延迟测试 (备用)"""
        client_ts_ns = data.get("client_ts_ns", 0)

        self._send_json({
            "message": f"echo: {data.get('message', '')}",
            "client_ts_ns": client_ts_ns,
            "server_ts_ns": time.time_ns(),
        })

    def _send_json(self, obj: dict):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(obj).encode())

    def log_message(self, format, *args):
        print(f"[HTTP] {args[0]}")


def serve(port: int = 8080):
    server = HTTPServer(("localhost", port), BridgeHandler)
    print(f"[HTTP Bridge] Listening on http://localhost:{port}")
    print(f"[HTTP Bridge] GET /ping | GET /echo?msg=N&ts=NS | POST /echo")
    print(f"[HTTP Bridge] Press Ctrl+C to stop")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[HTTP Bridge] Server stopped.")
        server.server_close()


if __name__ == "__main__":
    serve()
