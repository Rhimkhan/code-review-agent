import pytest
from src.utils.code_parser import detect_language, count_lines, truncate_code
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
    assert result["comments"] == 1
    assert result["blank"] == 1

def test_truncate_code():
    code = "x" * 20000
    result = truncate_code(code, max_chars=10000)
    assert "truncated" in result

def test_calculate_score_perfect():
    score = calculate_score({})
    assert score == 100

def test_calculate_score_with_issues():
    score = calculate_score({"CRITICAL": 1, "HIGH": 2})
    assert score == 100 - 25 - 30

def test_format_finding():
    finding = {"severity": "HIGH", "line": 10, "message": "SQL injection"}
    result = format_finding(finding)
    assert "HIGH" in result
    assert "10" in result
    assert "SQL injection" in result
