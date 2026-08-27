import pytest
from src.agents.quality_agent import QualityAgent

@pytest.mark.asyncio
async def test_detects_syntax_error():
    agent = QualityAgent()
    result = await agent.analyze({"code": "def foo(:\n    pass", "filename": "test.py"})
    subtypes = [f["subtype"] for f in result.findings]
    assert "Syntax Error" in subtypes

@pytest.mark.asyncio
async def test_detects_god_class():
    agent = QualityAgent()
    methods = "\n".join([f"    def method_{i}(self): pass" for i in range(12)])
    code = f"class BigClass:\n{methods}"
    result = await agent.analyze({"code": code, "filename": "test.py"})
    subtypes = [f["subtype"] for f in result.findings]
    assert "God Class" in subtypes

@pytest.mark.asyncio
async def test_metrics_calculated():
    agent = QualityAgent()
    code = "def foo():\n    pass\n\n# comment"
    result = await agent.analyze({"code": code, "filename": "test.py"})
    assert "metrics" in result.metadata
    assert result.metadata["metrics"]["total_lines"] == 4
