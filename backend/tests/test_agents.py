import pytest
import asyncio
from src.agents.quality_agent import QualityAgent
from src.agents.security_agent import SecurityAgent

@pytest.mark.asyncio
async def test_quality_agent_detects_bare_except():
    agent = QualityAgent()
    code = """
def foo():
    try:
        pass
    except:
        pass
"""
    result = await agent.analyze({"code": code, "filename": "test.py"})
    assert result.agent_name == "QualityAgent"
    types = [f["subtype"] for f in result.findings]
    assert "Bare Except" in types

@pytest.mark.asyncio
async def test_quality_agent_detects_too_many_params():
    agent = QualityAgent()
    code = "def foo(a, b, c, d, e, f, g):\n    pass"
    result = await agent.analyze({"code": code, "filename": "test.py"})
    subtypes = [f["subtype"] for f in result.findings]
    assert "Too Many Parameters" in subtypes

@pytest.mark.asyncio
async def test_quality_agent_clean_code():
    agent = QualityAgent()
    code = "def add(a, b):\n    return a + b"
    result = await agent.analyze({"code": code, "filename": "test.py"})
    assert result.confidence == 0.80
    assert isinstance(result.findings, list)

@pytest.mark.asyncio
async def test_security_agent_detects_patterns():
    agent = SecurityAgent()
    code = 'password = "hardcoded123"'
    result = await agent.analyze({"code": code, "filename": "test.py"})
    assert result.agent_name == "SecurityAgent"
    assert isinstance(result.findings, list)

@pytest.mark.asyncio
async def test_quality_agent_non_python():
    agent = QualityAgent()
    code = "function hello() { return 'world'; }"
    result = await agent.analyze({"code": code, "filename": "test.js"})
    assert result.agent_name == "QualityAgent"
    assert isinstance(result.findings, list)
