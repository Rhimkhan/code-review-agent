import pytest
from httpx import AsyncClient, ASGITransport
from src.api.server import app

@pytest.mark.asyncio
async def test_health_check():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/health")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_review_endpoint_success():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/api/review/code", json={
            "code": "def foo(a,b,c,d,e,f,g):\n    try:\n        pass\n    except:\n        pass",
            "filename": "test.py"
        })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "review" in data

@pytest.mark.asyncio
async def test_review_endpoint_empty_code():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/api/review/code", json={
            "code": "",
            "filename": "test.py"
        })
    assert response.status_code in [200, 422]

@pytest.mark.asyncio
async def test_demo_endpoint():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/review/demo")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
