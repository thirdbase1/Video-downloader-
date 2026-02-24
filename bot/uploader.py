import os
import aiohttp
import asyncio
import aiofiles
from .config import BOT_TOKEN
from .logger import logger

class TelegramUploader:
    def __init__(self):
        self._session = None
        self._lock = asyncio.Lock()

    async def _get_session(self):
        async with self._lock:
            if self._session is None or self._session.closed:
                # 50MB upload might take time. 5 mins timeout.
                timeout = aiohttp.ClientTimeout(total=300, connect=60)
                self._session = aiohttp.ClientSession(timeout=timeout)
            return self._session

    async def close(self):
        async with self._lock:
            if self._session and not self._session.closed:
                await self._session.close()

    async def upload_chunk(self, chat_id, file_path, caption, progress_callback=None):
        """
        Uploads a file to Telegram using aiohttp with progress tracking.
        progress_callback: async function(current, total)
        """
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
        filename = os.path.basename(file_path)
        try:
            file_size = os.path.getsize(file_path)
        except OSError:
            logger.error(f"File not found for upload: {file_path}")
            return False

        retries = 3
        backoff = 2

        for attempt in range(retries):
            try:
                # Use a custom async iterator for streaming with progress
                async def file_sender():
                    async with aiofiles.open(file_path, 'rb') as f:
                        sent = 0
                        chunk_size = 64 * 1024 # 64KB chunks
                        while True:
                            chunk = await f.read(chunk_size)
                            if not chunk:
                                break
                            sent += len(chunk)
                            if progress_callback:
                                try:
                                    await progress_callback(sent, file_size)
                                except Exception:
                                    pass
                            yield chunk

                data = aiohttp.FormData()
                data.add_field('chat_id', str(chat_id))
                data.add_field('caption', caption)
                # Important: filename must be set.
                # Use python's built-in file object for simplicity and reliability with aiohttp if possible,
                # but we want async progress.
                # aiohttp accepts an async generator if we wrap it properly or just pass it directly in newer versions?
                # Actually, passing the generator directly works in recent aiohttp versions for streaming uploads.
                # However, to be safe and explicit, let's just pass the generator.

                data.add_field('document', file_sender(), filename=filename)

                session = await self._get_session()

                async with session.post(url, data=data) as response:
                    if response.status == 200:
                        return await response.json()
                    elif response.status == 429:
                        retry_after = int(response.headers.get("Retry-After", 10))
                        logger.warning(f"Rate limited. Waiting {retry_after}s.")
                        await asyncio.sleep(retry_after)
                        continue # Retry
                    else:
                        text = await response.text()
                        logger.error(f"Upload failed: {response.status} - {text}")
                        raise Exception(f"Telegram API Error: {response.status} {text}")

            except Exception as e:
                logger.warning(f"Upload attempt {attempt+1} failed: {e}")
                if attempt < retries - 1:
                    await asyncio.sleep(backoff)
                    backoff *= 2
                else:
                    raise e

        return False

uploader = TelegramUploader()
