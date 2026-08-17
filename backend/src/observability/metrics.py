from datetime import datetime
from typing import Dict, List

class MetricsCollector:
    def __init__(self):
        self.reviews_total = 0
        self.findings_total = 0
        self.errors_total = 0
        self.response_times: List[float] = []

    def record_review(self, total_findings: int, response_time: float):
        self.reviews_total += 1
        self.findings_total += total_findings
        self.response_times.append(response_time)

    def record_error(self):
        self.errors_total += 1

    def get_stats(self) -> Dict:
        avg_time = (
            sum(self.response_times) / len(self.response_times)
            if self.response_times else 0
        )
        return {
            "reviews_total": self.reviews_total,
            "findings_total": self.findings_total,
            "errors_total": self.errors_total,
            "avg_response_time_ms": round(avg_time, 2),
        }

metrics = MetricsCollector()
