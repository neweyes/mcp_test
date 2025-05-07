import aiohttp
import aiofiles
import asyncio
import random
import os
from loguru import logger

async def fetch(session, url, headers, sem, delay_range):
    async with sem:
        await asyncio.sleep(random.uniform(*delay_range))
        for _ in range(3):
            try:
                async with session.get(url, headers=headers, timeout=20) as resp:
                    resp.raise_for_status()
                    return await resp.text()
            except Exception as e:
                logger.warning(f"Fetch failed: {url}, retrying... {e}")
                await asyncio.sleep(2)
        logger.error(f"Failed to fetch: {url}")
        return None

async def download_file(session, url, save_path, headers, sem, delay_range):
    # 断点续传
    tmp_path = save_path + ".part"
    file_size = 0
    if os.path.exists(tmp_path):
        file_size = os.path.getsize(tmp_path)
    req_headers = headers.copy()
    if file_size > 0:
        req_headers['Range'] = f'bytes={file_size}-'
    async with sem:
        await asyncio.sleep(random.uniform(*delay_range))
        for _ in range(3):
            try:
                async with session.get(url, headers=req_headers, timeout=60) as resp:
                    if resp.status in (200, 206):
                        mode = 'ab' if file_size > 0 else 'wb'
                        async with aiofiles.open(tmp_path, mode) as f:
                            async for chunk in resp.content.iter_chunked(1024 * 32):
                                await f.write(chunk)
                        # 检查是否下载完成
                        content_length = resp.headers.get('Content-Length')
                        if content_length is None or os.path.getsize(tmp_path) >= int(content_length) + file_size:
                            os.rename(tmp_path, save_path)
                        return
            except Exception as e:
                logger.warning(f"Download failed: {url}, retrying... {e}")
                await asyncio.sleep(2)
        logger.error(f"Failed to download: {url}")
