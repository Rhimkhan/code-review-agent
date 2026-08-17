import pytest
from src.security.scanner import scan_patterns

def test_detects_eval():
    findings = scan_patterns("result = eval(user_input)")
    assert len(findings) > 0
    assert any(f["severity"] == "HIGH" for f in findings)

def test_detects_hardcoded_password():
    findings = scan_patterns('password = "secret123"')
    assert len(findings) > 0
    assert any(f["severity"] == "CRITICAL" for f in findings)

def test_clean_code():
    findings = scan_patterns("def add(a, b):\n    return a + b")
    assert len(findings) == 0

def test_detects_os_system():
    findings = scan_patterns("os.system('rm -rf /')")
    assert any(f["severity"] == "CRITICAL" for f in findings)
