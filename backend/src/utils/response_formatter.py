from typing import Dict
from datetime import datetime

def calculate_score(severity_counts: Dict) -> int:
    deductions = {"CRITICAL": 25, "HIGH": 15, "MEDIUM": 5, "LOW": 2}
    score = 100
    for severity, count in severity_counts.items():
        score -= deductions.get(severity, 0) * count
    return max(0, score)

def format_finding(finding: Dict) -> str:
    return f"[{finding.get('severity')}] Line {finding.get('line')}: {finding.get('message')}"
