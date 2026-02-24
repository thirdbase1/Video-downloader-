import os
import asyncio
from .logger import logger

class TelegramUploader:
    async def upload_chunk(self, bot, chat_id, file_path, caption, progress_callback=None):
        """
        Uploads a file using the official python-telegram-bot instance.
        """
        retries = 3
        backoff = 2

        for attempt in range(retries):
            try:
                # Use standard 'open' and let python-telegram-bot handle it.
                # This ensures we use all official stuff (httpx underneath).
                # Progress is sacrificed for simplicity and standard compliance.

                # We can simulate progress "start" and "end" if needed in the handler.
                if progress_callback:
                    try:
                        # Fake start
                        file_size = os.path.getsize(file_path)
                        await progress_callback(0, file_size)
                    except:
                        pass

                # 5 minute timeout for 50MB is generous.
                with open(file_path, 'rb') as f:
                    await bot.send_document(
                        chat_id=chat_id,
                        document=f,
                        caption=caption,
                        read_timeout=300,
                        write_timeout=300,
                        connect_timeout=60
                    )

                if progress_callback:
                    try:
                        # Fake end
                        await progress_callback(file_size, file_size)
                    except:
                        pass

                return True

            except Exception as e:
                logger.warning(f"Upload attempt {attempt+1} failed: {e}")
                if attempt < retries - 1:
                    await asyncio.sleep(backoff)
                    backoff *= 2
                else:
                    # Let the handler deal with final failure
                    raise e
        return False

uploader = TelegramUploader()
