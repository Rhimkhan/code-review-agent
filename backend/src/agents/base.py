from abc import ABC, abstractmethod
from typing import Dict, List
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class AgentResult:
    agent_name: str
    findings: List[Dict]
    confidence: float
    metadata: Dict
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict:
        return {
            "agent_name": self.agent_name,
            "findings": self.findings,
            "confidence": self.confidence,
            "metadata": self.metadata,
            "timestamp": self.timestamp
        }

class BaseAgent(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    async def analyze(self, data: Dict) -> AgentResult:
        pass

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} name={self.name}>"
