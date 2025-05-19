import pytest
import asyncio
from utils.fetcher import fetch

class DummySession:
    async def get(self, url, headers=None, timeout=None):
        class DummyResp:
            status = 200
            async def text(self):
                return 'ok'
            def raise_for_status(self):
                pass
        return DummyResp()

@pytest.mark.asyncio
async def test_fetch():
    sem = asyncio.Semaphore(1)
    session = DummySession()
    result = await fetch(session, 'http://test', {}, sem, [0, 0])
    assert result == 'ok'
