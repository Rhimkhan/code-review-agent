import pytest
from src.agents.orchestrator import Orchestrator

@pytest.mark.asyncio
async def test_orchestrator_returns_findings():
    orch = Orchestrator()
    result = await orch.review_code(
        code="def foo(a,b,c,d,e,f,g):\n    try:\n        pass\n    except:\n        pass",
        filename="test.py"
    )
    assert "findings" in result
    assert "summary" in result
    assert "severity_counts" in result
    assert "total_findings" in result

@pytest.mark.asyncio
async def test_orchestrator_clean_code():
    orch = Orchestrator()
    result = await orch.review_code(
        code="def add(a, b):\n    return a + b",
        filename="clean.py"
    )
    assert isinstance(result["findings"], list)
    assert isinstance(result["total_findings"], int)
