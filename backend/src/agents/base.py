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


class BaseAgent(ABC):

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    async def analyze(self, data: Dict) -> AgentResult:
        pass