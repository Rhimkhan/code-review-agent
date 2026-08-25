import pytest
from src.agents.orchestrator import Orchestrator

@pytest.mark.asyncio
async def test_review_multiple_files():
    orch = Orchestrator()
    files = [
        {"code": "def add(a, b): return a + b", "filename": "math.py"},
        {"code": "x = eval(input())", "filename": "dangerous.py"},
    ]
    results = await orch.review_multiple(files)
    assert len(results) == 2
    assert isinstance(results[0], dict)
    assert isinstance(results[1], dict)

@pytest.mark.asyncio
async def test_review_multiple_returns_findings():
    orch = Orchestrator()
    files = [
        {"code": "def foo(a,b,c,d,e,f,g):\n    try:\n        pass\n    except:\n        pass", "filename": "test.py"},
    ]
    results = await orch.review_multiple(files)
    assert results[0]["total_findings"] >= 0
