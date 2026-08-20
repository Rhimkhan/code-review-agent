import re
from typing import List, Dict

DANGEROUS_PATTERNS = [
    (r"eval\s*\(", "Dangerous eval() usage", "HIGH"),
    (r"exec\s*\(", "Dangerous exec() usage", "HIGH"),
    (r"os\.system\s*\(", "Shell injection risk", "CRITICAL"),
    (r"password\s*=\s*['\"][^'\"]+['\"]", "Hardcoded password", "CRITICAL"),
    (r"api_key\s*=\s*['\"][^'\"]+['\"]", "Hardcoded API key", "CRITICAL"),
    (r"secret\s*=\s*['\"][^'\"]+['\"]", "Hardcoded secret", "HIGH"),
]

def scan_patterns(code: str) -> List[Dict]:
    findings = []
    for line_num, line in enumerate(code.split("\n"), 1):
        for pattern, message, severity in DANGEROUS_PATTERNS:
            if re.search(pattern, line, re.IGNORECASE):
                findings.append({
                    "type": "Security",
                    "subtype": "Pattern Match",
                    "line": line_num,
                    "severity": severity,
                    "message": message,
                    "suggestion": "Remove or secure this code"
                })
    return findings
