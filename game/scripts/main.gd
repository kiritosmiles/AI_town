"""
S1 Spike — Godot 4 GDScript: HTTP ↔ Python Bridge 延迟测试

启动 Python HTTP Bridge 后再运行此场景:
    cd spike/s1-grpc && python http_bridge.py
"""

extends Node2D

const PYTHON_BRIDGE_URL = "http://127.0.0.1:8080"
const TEST_COUNT = 50

var http_request: HTTPRequest
var latencies: Array[float] = []
var test_index: int = 0
var test_done: bool = false
var ping_done: bool = false


func _ready() -> void:
	print("=".repeat(50))
	print("  S1 Spike: Godot ↔ Python HTTP Bridge 延迟测试")
	print("=".repeat(50))
	print("  Python Bridge: ", PYTHON_BRIDGE_URL)
	print("  Test count   : ", TEST_COUNT)
	print("=".repeat(50))

	http_request = HTTPRequest.new()
	add_child(http_request)
	http_request.request_completed.connect(_on_request_completed)

	_ping_check()


func _ping_check() -> void:
	print("\n[INFO] Checking connectivity...")
	var err = http_request.request(PYTHON_BRIDGE_URL + "/ping")
	if err != OK:
		printerr("[ERROR] Cannot send ping request: ", err)


func _start_tests() -> void:
	print("\n[TEST] Starting latency tests...")
	test_index = 0
	latencies.clear()
	_send_next_test()


func _send_next_test() -> void:
	if test_index >= TEST_COUNT:
		_print_stats()
		return

	var ts_ns = Time.get_ticks_usec() * 1000

	# GET /echo?msg=N&ts=NS — 纯 GET，避开 Godot POST body 的解析延迟
	var url = PYTHON_BRIDGE_URL + "/echo?msg=test_%d&ts=%d" % [test_index, ts_ns]

	var send_ts = Time.get_ticks_usec()
	var err = http_request.request(url)

	if err != OK:
		printerr("[ERROR] Request %d failed: %d" % [test_index, err])
		test_index += 1
		_send_next_test()
	else:
		http_request.set_meta("send_ts_us", send_ts)


func _on_request_completed(
	result: int, response_code: int, headers: PackedStringArray, body: PackedByteArray
) -> void:
	if test_done:
		return

	var recv_ts = Time.get_ticks_usec()

	# /ping 响应
	if not ping_done:
		ping_done = true
		if response_code == 200:
			print("[OK] Bridge connected!")
			await get_tree().create_timer(0.1).timeout
			_start_tests()
		else:
			printerr("[ERROR] Bridge responded with code: ", response_code)
		return

	# /echo 响应
	var send_ts = http_request.get_meta("send_ts_us", recv_ts)
	var rtt_ms = float(recv_ts - send_ts) / 1000.0
	latencies.append(rtt_ms)

	if test_index % 10 == 9:
		print("[TEST] %2d/%2d  latest RTT: %.2f ms" % [test_index + 1, TEST_COUNT, rtt_ms])

	test_index += 1
	_send_next_test()


func _print_stats() -> void:
	test_done = true
	latencies.sort()
	var n = latencies.size()
	if n == 0:
		printerr("[ERROR] No test results collected.")
		return

	var p50_idx = int(float(n) * 50.0 / 100.0)
	var p95_idx = int(float(n) * 95.0 / 100.0)
	var p99_idx = int(float(n) * 99.0 / 100.0)
	var p50_val = latencies[p50_idx]

	print("\n" + "=".repeat(50))
	print("  Godot ↔ Python HTTP Bridge — Latency Report")
	print("=".repeat(50))
	print("  Samples : %d" % n)
	print("  Min     : %.2f ms" % latencies[0])
	print("  P50     : %.2f ms" % p50_val)
	print("  P95     : %.2f ms" % latencies[p95_idx])
	print("  P99     : %.2f ms" % latencies[p99_idx])
	print("  Max     : %.2f ms" % latencies[n - 1])

	var avg = 0.0
	for l in latencies:
		avg += l
	avg /= float(n)
	print("  Mean    : %.2f ms" % avg)
	print("=".repeat(50))

	if p50_val < 50.0:
		print("  ✅ SPIKE PASSED: P50 = %.1f ms < 50ms" % p50_val)
	else:
		print("  ❌ SPIKE FAILED: P50 = %.1f ms >= 50ms" % p50_val)
	print("=".repeat(50))
