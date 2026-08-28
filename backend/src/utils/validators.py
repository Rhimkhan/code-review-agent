from typing import Tuple, List

ALLOWED_EXTENSIONS = [
    ".py", ".js", ".ts", ".java", ".go",
    ".rs", ".cpp", ".rb", ".php", ".cs", ".swift"
]

def validate_code_input(code: str, filename: str) -> Tuple[bool, str]:
    if not code or not code.strip():
        return False, "Code cannot be empty"
    if len(code) > 50000:
        return False, "Code too large (max 50000 chars)"
    if not filename:
        return False, "Filename is required"
    if not any(filename.endswith(ext) for ext in ALLOWED_EXTENSIONS):
        return False, f"Unsupported file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
    return True, "Valid"

def validate_filename(filename: str) -> Tuple[bool, str]:
    if not filename:
        return False, "Filename is required"
    if len(filename) > 255:
        return False, "Filename too long"
    if "/" in filename or "\\" in filename:
        return False, "Filename cannot contain path separators"
    return True, "Valid"
