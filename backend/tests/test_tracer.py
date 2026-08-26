import pytest
from src.observability.tracer import AgentTracer

def test_start_trace_returns_id():
    tracer = AgentTracer()
    trace_id = tracer.start_trace("test.py")
    assert trace_id is not None
    assert len(trace_id) > 0

def test_trace_status_running():
    tracer = AgentTracer()
    trace_id = tracer.start_trace("test.py")
    trace = tracer.get_trace(trace_id)
    assert trace["status"] == "running"

def test_end_trace_updates_status():
    tracer = AgentTracer()
    trace_id = tracer.start_trace("test.py")
    tracer.end_trace({"trace_id": trace_id, "total_findings": 3})
    trace = tracer.get_trace(trace_id)
    assert trace["status"] == "complete"
    assert trace["total_findings"] == 3

def test_total_traces_counter():
    tracer = AgentTracer()
    tracer.start_trace("a.py")
    tracer.start_trace("b.py")
    assert tracer.total_traces == 2

def test_get_stats():
    tracer = AgentTracer()
    stats = tracer.get_stats()
    assert "total_traces" in stats
    assert "completed" in stats
