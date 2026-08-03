import re
import json
import subprocess
import tempfile
import os
import sys
from typing import Dict, List
from src.agents.base import BaseAgent, AgentResult


class SecurityAgent(BaseAgent):

    def __init__(self):
        super().__init__("SecurityAgent")

    async def analyze(self, data: Dict) -> AgentResult:
        code = data.get("code", "")
        filename = data.get("filename", "")

        findings = []

        if filename.endswith(".py"):
            findings.extend(await self._run_bandit(code))

        findings.extend(self._detect_patterns(code))

        return AgentResult(
            agent_name=self.name,
            findings=findings,
            confidence=0.85,
            metadata={
                "file": filename,
                "total": len(findings)
            },
        )

    async def _run_bandit(self, code: str) -> List[Dict]:
        findings = []

        temp_file = None

        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                suffix=".py",
                delete=False,
                encoding="utf-8"
            ) as f:
                f.write(code)
                temp_file = f.name

            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "bandit",
                    "-f",
                    "json",
                    temp_file,
                ],
                capture_output=True,
                text=True,
            )

            if result.stdout:
                report = json.loads(result.stdout)

                for issue in report.get("results", []):
                    findings.append(
                        {
                            "type": "Security",
                            "subtype": issue.get("test_name", "Bandit"),
                            "line": issue.get("line_number", 0),
                            "severity": issue.get(
                                "issue_severity",
                                "MEDIUM"
                            ).upper(),
                            "message": issue.get("issue_text", ""),
                            "suggestion": "Review and fix this security issue",
                        }
                    )

        except Exception as e:
            print("Bandit Error:", e)

        finally:
            if temp_file and os.path.exists(temp_file):
                os.remove(temp_file)

        return findings

    def _detect_patterns(self, code: str) -> List[Dict]:
        findings = []

        patterns = [
            (
                r'password\s*=\s*["\'][^"\']+["\']',
                "CRITICAL",
                "Hardcoded Password",
                "Move password to environment variables",
            ),
            (
                r'api[_-]?key\s*=\s*["\'][^"\']+["\']',
                "CRITICAL",
                "Hardcoded API Key",
                "Move API key to environment variables",
            ),
            (
                r'eval\s*\(',
                "HIGH",
                "Use of eval()",
                "Avoid eval()",
            ),
        ]

        for pattern, severity, subtype, suggestion in patterns:
            for match in re.finditer(pattern, code, re.IGNORECASE):
                findings.append(
                    {
                        "type": "Security",
                        "subtype": subtype,
                        "line": code[: match.start()].count("\n") + 1,
                        "severity": severity,
                        "message": subtype,
                        "suggestion": suggestion,
                    }
                )

        return findings