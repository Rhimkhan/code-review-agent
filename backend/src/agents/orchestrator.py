import asyncio
from typing import Dict, List
from src.agents.base import AgentResult
from src.agents.security_agent import SecurityAgent
from src.agents.quality_agent import QualityAgent
from src.agents.analyst_agent import AnalystAgent
from src.observability.tracer import AgentTracer


class Orchestrator:

    def __init__(self):
        self.security = SecurityAgent()
        self.quality = QualityAgent()
        self.analyst = AnalystAgent()
        self.tracer = AgentTracer()

    async def review_code(self, code: str, filename: str) -> Dict:
        trace_id = self.tracer.start_trace(filename)
        data = {'code': code, 'filename': filename}

        results: List[AgentResult] = await asyncio.gather(
            self.security.analyze(data),
            self.quality.analyze(data),
            self.analyst.analyze(data),
            return_exceptions=True
        )

        all_findings = []
        metadata = {}

        for result in results:
            if isinstance(result, Exception):
                continue
            all_findings.extend(result.findings)
            metadata[result.agent_name] = result.metadata

        categorized = {
            'security': [f for f in all_findings if f.get('type') == 'Security'],
            'quality': [f for f in all_findings if f.get('type') == 'Quality'],
            'bugs': [f for f in all_findings if f.get('type') == 'Bug'],
            'performance': [f for f in all_findings if f.get('type') == 'Performance'],
        }

        severity_counts = {'CRITICAL': 0, 'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}
        for f in all_findings:
            s = f.get('severity', 'LOW').upper()
            if s in severity_counts:
                severity_counts[s] += 1

        total = len(all_findings)
        summary = "✅ No issues found!" if total == 0 else \
            f"🔍 Found {total} issues: " + ", ".join(
                f"{v} {k}" for k, v in severity_counts.items() if v > 0
            )

        final = {
            'trace_id': trace_id,
            'filename': filename,
            'findings': all_findings,
            'categorized': categorized,
            'summary': summary,
            'severity_counts': severity_counts,
            'total_findings': total,
            'metadata': metadata
        }

        self.tracer.end_trace(final)
        return final