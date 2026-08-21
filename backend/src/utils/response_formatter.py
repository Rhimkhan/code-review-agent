from typing import Dict, List
from datetime import datetime

def calculate_score(severity_counts: Dict) -> int:
    deductions = {"CRITICAL": 25, "HIGH": 15, "MEDIUM": 5, "LOW": 2}
    score = 100
    for severity, count in severity_counts.items():
        score -= deductions.get(severity, 0) * count
    return max(0, score)

def get_score_label(score: int) -> str:
    if score >= 90: return "Excellent"
    if score >= 70: return "Good"
    if score >= 50: return "Fair"
    return "Needs Work"

def format_review_response(result: Dict) -> Dict:
    score = calculate_score(result.get("severity_counts", {}))
    return {
        "status": "success",
        "timestamp": datetime.now().isoformat(),
        "filename": result.get("filename", "unknown"),
        "total_findings": result.get("total_findings", 0),
        "summary": result.get("summary", ""),
        "severity_counts": result.get("severity_counts", {}),
        "findings": result.get("findings", []),
        "score": score,
        "score_label": get_score_label(score)
    }

def format_finding(finding: Dict) -> str:
    return f"[{finding.get('severity')}] Line {finding.get('line')}: {finding.get('message')}"
