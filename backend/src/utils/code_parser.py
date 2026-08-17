from typing import Dict

def detect_language(filename: str) -> str:
    ext = filename.split(".")[-1].lower()
    languages = {
        "py": "python",
        "js": "javascript",
        "ts": "typescript",
        "java": "java",
        "go": "go",
        "rs": "rust",
    }
    return languages.get(ext, "unknown")

def count_lines(code: str) -> Dict:
    lines = code.split("\n")
    return {
        "total": len(lines),
        "blank": sum(1 for l in lines if not l.strip()),
        "code": sum(1 for l in lines if l.strip() and not l.strip().startswith("#")),
        "comments": sum(1 for l in lines if l.strip().startswith("#"))
    }
