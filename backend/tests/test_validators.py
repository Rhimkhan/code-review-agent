import pytest
from src.utils.validators import validate_code_input

def test_valid_python_code():
    valid, msg = validate_code_input("def foo(): pass", "main.py")
    assert valid == True

def test_empty_code():
    valid, msg = validate_code_input("", "main.py")
    assert valid == False
    assert "empty" in msg.lower()

def test_empty_filename():
    valid, msg = validate_code_input("print('hi')", "")
    assert valid == False

def test_unsupported_extension():
    valid, msg = validate_code_input("code", "file.html")
    assert valid == False

def test_code_too_large():
    valid, msg = validate_code_input("x" * 60000, "main.py")
    assert valid == False
    assert "large" in msg.lower()
