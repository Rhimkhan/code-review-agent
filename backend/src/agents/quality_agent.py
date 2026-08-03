import ast
import re
from typing import Dict, List
from src.agents.base import BaseAgent, AgentResult


class QualityAgent(BaseAgent):

    def __init__(self):
        super().__init__("QualityAgent")

    async def analyze(self, data: Dict) -> AgentResult:
        code = data.get('code', '')
        filename = data.get('filename', '')
        findings = []
        metrics = self._calculate_metrics(code)

        if filename.endswith('.py'):
            findings.extend(self._analyze_ast(code))

        return AgentResult(
            agent_name=self.name,
            findings=findings,
            confidence=0.80,
            metadata={'file': filename, 'metrics': metrics, 'total': len(findings)}
        )

    def _analyze_ast(self, code: str) -> List[Dict]:
        findings = []
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    if hasattr(node, 'end_lineno') and (node.end_lineno - node.lineno) > 50:
                        findings.append({
                            'type': 'Quality', 'subtype': 'Long Function',
                            'line': node.lineno, 'severity': 'MEDIUM',
                            'message': f'Function {node.name} is too long',
                            'suggestion': 'Break into smaller functions'
                        })
                    if len(node.args.args) > 5:
                        findings.append({
                            'type': 'Quality', 'subtype': 'Too Many Parameters',
                            'line': node.lineno, 'severity': 'MEDIUM',
                            'message': f'Function {node.name} has {len(node.args.args)} parameters',
                            'suggestion': 'Use a config object'
                        })
                if isinstance(node, ast.ClassDef):
                    methods = [n for n in node.body if isinstance(n, ast.FunctionDef)]
                    if len(methods) > 10:
                        findings.append({
                            'type': 'Quality', 'subtype': 'God Class',
                            'line': node.lineno, 'severity': 'HIGH',
                            'message': f'Class {node.name} has {len(methods)} methods',
                            'suggestion': 'Split into smaller classes'
                        })
                if isinstance(node, ast.ExceptHandler) and node.type is None:
                    findings.append({
                        'type': 'Quality', 'subtype': 'Bare Except',
                        'line': node.lineno, 'severity': 'HIGH',
                        'message': 'Bare except catches everything',
                        'suggestion': 'Catch specific exceptions'
                    })
        except SyntaxError:
            pass
        return findings

    def _calculate_metrics(self, code: str) -> Dict:
        lines = code.split('\n')
        return {
            'total_lines': len(lines),
            'blank_lines': sum(1 for l in lines if not l.strip()),
            'comment_lines': sum(1 for l in lines if l.strip().startswith('#')),
            'branches': len(re.findall(r'\b(if|elif|for|while|except)\b', code))
        }