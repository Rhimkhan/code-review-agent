from typing import Tuple

def validate_code_input(code: str, filename: str) -> Tuple[bool, str]:
    if not code or not code.strip():
        return False, "Code cannot be empty"
    if len(code) > 50000:
        return False, "Code too large (max 50000 chars)"
    if not filename:
        return False, "Filename is required"
    allowed = [".py", ".js", ".ts", ".java", ".go", ".rs", ".cpp", ".rb"]
    if not any(filename.endswith(ext) for ext in allowed):
        return False, "Unsupported file type"
    return True, "Valid"
