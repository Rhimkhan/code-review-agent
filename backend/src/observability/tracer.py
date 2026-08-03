import uuid
from datetime import datetime
from typing import Dict, Any


class AgentTracer:

    def __init__(self):
        self.current_trace = None

    def start_trace(self, label: str) -> str:
        trace_id = str(uuid.uuid4())[:8]
        self.current_trace = {
            'trace_id': trace_id,
            'label': label,
            'start_time': datetime.now().isoformat(),
            'steps': []
        }
        return trace_id

    def log_step(self, agent: str, action: str, reasoning: str, result: Any):
        if not self.current_trace:
            return
        self.current_trace['steps'].append({
            'timestamp': datetime.now().isoformat(),
            'agent': agent,
            'action': action,
            'reasoning': str(reasoning)[:300],
            'result': str(result)[:300]
        })

    def end_trace(self, final_result: Dict) -> Dict:
        if not self.current_trace:
            return {}
        self.current_trace['end_time'] = datetime.now().isoformat()
        self.current_trace['final_result'] = final_result
        self.current_trace['total_steps'] = len(self.current_trace['steps'])
        return self.current_trace