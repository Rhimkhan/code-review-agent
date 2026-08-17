import pytest
from src.utils.code_parser import detect_language, count_lines
from src.utils.response_formatter import calculate_score, format_finding

def test_detect_python():
    assert detect_language("main.py") == "python"

def test_detect_javascript():
    assert detect_language("app.js") == "javascript"

def test_detect_unknown():
    assert detect_language("file.xyz") == "unknown"

def test_count_lines():
    code = "def foo():\n    pass\n\n# comment"
    result = count_lines(code)
    assert result["total"] == 4

def test_calculate_score_perfect():
    assert calculate_score({}) == 100

def test_calculate_score_with_issues():
    assert calculate_score({"CRITICAL": 1}) == 75

def test_format_finding():
    finding = {"severity": "HIGH", "line": 10, "message": "SQL injection"}
    assert "HIGH" in format_finding(finding)
