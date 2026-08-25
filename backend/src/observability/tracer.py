import uuid
from datetime import datetime
from typing import Dict, Optional

class AgentTracer:
    def __init__(self):
        self.traces: Dict[str, dict] = {}
        self.total_traces = 0

    def start_trace(self, filename: str) -> str:
        trace_id = str(uuid.uuid4())
        self.traces[trace_id] = {
            "id": trace_id,
            "filename": filename,
            "started_at": datetime.now().isoformat(),
            "status": "running"
        }
        self.total_traces += 1
        return trace_id

    def end_trace(self, result: dict):
        trace_id = result.get("trace_id")
        if trace_id and trace_id in self.traces:
            self.traces[trace_id].update({
                "ended_at": datetime.now().isoformat(),
                "status": "complete",
                "total_findings": result.get("total_findings", 0)
            })

    def get_trace(self, trace_id: str) -> Optional[dict]:
        return self.traces.get(trace_id)

    def get_stats(self) -> Dict:
        completed = sum(1 for t in self.traces.values() if t["status"] == "complete")
        return {
            "total_traces": self.total_traces,
            "completed": completed,
            "running": self.total_traces - completed
        }
