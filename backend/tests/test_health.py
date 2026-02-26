
import pytest
from httpx import AsyncClient, ASGITransport
from backend.server import app

@pytest.mark.asyncio
async def test_root_or_docs_reachable():
    """Smoke test: the app boots and responds."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/docs")
        assert response.status_code == 200
