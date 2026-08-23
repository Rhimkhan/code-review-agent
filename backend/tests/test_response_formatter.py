import pytest
from src.utils.response_formatter import calculate_score, get_score_label, format_finding

def test_perfect_score():
    assert calculate_score({}) == 100

def test_score_with_critical():
    assert calculate_score({"CRITICAL": 1}) == 75

def test_score_with_high():
    assert calculate_score({"HIGH": 2}) == 70

def test_score_never_negative():
    assert calculate_score({"CRITICAL": 10}) == 0

def test_score_label_excellent():
    assert get_score_label(95) == "Excellent"

def test_score_label_good():
    assert get_score_label(75) == "Good"

def test_score_label_fair():
    assert get_score_label(55) == "Fair"

def test_score_label_needs_work():
    assert get_score_label(30) == "Needs Work"

def test_format_finding():
    f = {"severity": "HIGH", "line": 5, "message": "eval usage"}
    assert "HIGH" in format_finding(f)
    assert "5" in format_finding(f)
