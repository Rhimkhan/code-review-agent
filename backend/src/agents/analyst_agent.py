import os
import json
from typing import Dict
from groq import Groq
from src.agents.base import BaseAgent, AgentResult
from src.security.guardrails import PromptGuardrails, CostController
from src.observability.tracer import AgentTracer


class AnalystAgent(BaseAgent):

    def __init__(self):
        super().__init__("AnalystAgent")
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            raise RuntimeError("GROQ_API_KEY is not set")
        self.client = Groq(api_key=api_key)
        self.model = "llama3-70b-8192"
        self.guardrails = PromptGuardrails()
        self.cost_controller = CostController()
        self.tracer = AgentTracer()

    async def analyze(self, data: Dict) -> AgentResult:
        code = data.get('code', '')
        filename = data.get('filename', 'unknown.py')

        sanitized, warnings = self.guardrails.sanitize_code_input(code)
        wrapped = self.guardrails.wrap_code_for_llm(sanitized)

        prompt = f"""You are a senior code reviewer. Review this code for bugs, smells, and performance issues.
File: {filename}
{wrapped}
Respond ONLY in valid JSON:
{{
  "issues": [
    {{"type": "Bug|Performance|Style", "subtype": "...", "line": 1, "severity": "CRITICAL|HIGH|MEDIUM|LOW", "message": "...", "suggestion": "..."}}
  ],
  "summary": "..."
}}"""

        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a senior code reviewer. Always respond in valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=2000
            )
            self.cost_controller.track_usage(
                self.model,
                completion.usage.prompt_tokens,
                completion.usage.completion_tokens
            )
            text = completion.choices[0].message.content
            start = text.find('{')
            end = text.rfind('}') + 1
            review = json.loads(text[start:end]) if start >= 0 else {"issues": [], "summary": text[:200]}

            return AgentResult(
                agent_name=self.name,
                findings=review.get('issues', []),
                confidence=0.85,
                metadata={
                    'summary': review.get('summary', ''),
                    'warnings': warnings,
                    'tokens': completion.usage.prompt_tokens + completion.usage.completion_tokens
                }
            )
        except Exception as e:
            return AgentResult(
                agent_name=self.name,
                findings=[],
                confidence=0.0,
                metadata={'error': str(e)}
            )