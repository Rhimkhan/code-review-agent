import re
import json
import subprocess
import tempfile
import os
from typing import Dict, List
from src.agents.base import BaseAgent, AgentResult


class SecurityAgent(BaseAgent):

    def __init__(self):
        super().__init__("SecurityAgent")

    async def analyze(self, data: Dict) -> AgentResult:
        code = data.get('code', '')
        filename = data.get('filename', '')
        findings = []

        if filename.endswith('.py'):
            findings.extend(await self._run_bandit(code))

        findings.extend(self._detect_patterns(code))

        return AgentResult(
            agent_name=self.name,
            findings=findings,
            confidence=0.85,
            metadata={'file': filename, 'total': len(findings)}
        )

    async def _run_bandit(self, code: str) -> List[Dict]:
        findings = []
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(code)
                tmp = f.name
            result = subprocess.run(['bandit', '-f', 'json', tmp], capture_output=True, text=True)
            os.unlink(tmp)
            if result.returncode in [0, 1]:
                for issue in json.loads(result.stdout).get('results', []):
                    findings.append({
                        'type': 'Security',
                        'subtype': issue.get('test_name', 'Unknown'),
                        'line': issue.get('line_number', 0),
                        'severity': issue.get('issue_severity', 'MEDIUM').upper(),
                        'message': issue.get('issue_text', ''),
                        'suggestion': 'Fix this security issue'
                    })
        except Exception as e:
            print(f"Bandit error: {e}")
        return findings

    def _detect_patterns(self, code: str) -> List[Dict]:
        findings = []
        patterns = [
            (r'execute\s*\(\s*["\'].*?\+.*?["\']\s*\)', 'CRITICAL', 'SQL Injection', 'Use parameterized queries'),
            (r'cursor\.execute\s*\(\s*f["\']', 'CRITICAL', 'SQL Injection via f-string', 'Use parameterized queries'),
            (r'password\s*=\s*["\'][^"\']+["\']', 'CRITICAL', 'Hardcoded Password', 'Use environment variables'),
            (r'api[_-]?key\s*=\s*["\'][^"\']+["\']', 'CRITICAL', 'Hardcoded API Key', 'Use environment variables'),
            (r'token\s*=\s*["\'][^"\']+["\']', 'HIGH', 'Hardcoded Token', 'Use environment variables'),
            (r'os\.system\s*\(', 'HIGH', 'OS Command Injection Risk', 'Use subprocess with list args'),
            (r'eval\s*\(', 'HIGH', 'Dangerous eval()', 'Use ast.literal_eval()'),
            (r'pickle\.loads\s*\(', 'HIGH', 'Insecure Deserialization', 'Use JSON instead'),
            (r'yaml\.load\s*\(', 'MEDIUM', 'Unsafe YAML load', 'Use yaml.safe_load()'),
        ]
        for pattern, severity, subtype, suggestion in patterns:
            for match in re.finditer(pattern, code, re.IGNORECASE):
                line_no = code[:match.start()].count('\n') + 1
                findings.append({
                    'type': 'Security', 'subtype': subtype,
                    'line': line_no, 'severity': severity,
                    'message': f'Found: {subtype}', 'suggestion': suggestion
                })
        return findings