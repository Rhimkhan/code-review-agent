import pytest
from src.observability.metrics import MetricsCollector

def test_initial_state():
    m = MetricsCollector()
    assert m.reviews_total == 0
    assert m.findings_total == 0

def test_record_review():
    m = MetricsCollector()
    m.record_review(total_findings=5, response_time=1.2)
    assert m.reviews_total == 1
    assert m.findings_total == 5

def test_avg_response_time():
    m = MetricsCollector()
    m.record_review(0, 1.0)
    m.record_review(0, 3.0)
    stats = m.get_stats()
    assert stats["avg_response_time_ms"] == 2.0

def test_record_error():
    m = MetricsCollector()
    m.record_error()
    assert m.errors_total == 1

def test_get_stats():
    m = MetricsCollector()
    stats = m.get_stats()
    assert "reviews_total" in stats
    assert "findings_total" in stats
