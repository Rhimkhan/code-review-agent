import pytest
from src.utils.validators import validate_code_input, validate_filename

def test_swift_file_supported():
    valid, msg = validate_code_input("func hello() {}", "main.swift")
    assert valid == True

def test_php_file_supported():
    valid, msg = validate_code_input("<?php echo 'hi'; ?>", "index.php")
    assert valid == True

def test_filename_with_path_rejected():
    valid, msg = validate_filename("../../etc/passwd")
    assert valid == False
    assert "path" in msg.lower()

def test_empty_filename_rejected():
    valid, msg = validate_filename("")
    assert valid == False

def test_valid_filename():
    valid, msg = validate_filename("main.py")
    assert valid == True
