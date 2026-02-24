import os
import aiofiles
from .utils import get_chunk_suffix
from .config import MAX_CHUNK_SIZE_MB
from .logger import logger

class FileSplitter:
    def __init__(self):
        self.chunk_size = MAX_CHUNK_SIZE_MB * 1024 * 1024
        self.buffer_size = 8 * 1024 * 1024 # 8 MB buffer for reading

    async def split_file(self, file_path):
        """
        Splits the file into chunks of size MAX_CHUNK_SIZE_MB.
        Returns a list of paths to the chunks.
        """
        try:
            file_size = os.path.getsize(file_path)
        except OSError:
            logger.error(f"File not found: {file_path}")
            return []

        if file_size <= self.chunk_size:
            return [file_path]

        dir_name = os.path.dirname(file_path)
        base_name = os.path.basename(file_path)
        name_without_ext, ext = os.path.splitext(base_name)

        chunk_paths = []
        chunk_index = 0
        bytes_written_to_chunk = 0
        current_chunk_file = None

        try:
            async with aiofiles.open(file_path, 'rb') as src:
                while True:
                    data = await src.read(self.buffer_size)
                    if not data:
                        break

                    data_len = len(data)
                    cursor = 0

                    while cursor < data_len:
                        if current_chunk_file is None:
                            suffix = get_chunk_suffix(chunk_index)
                            chunk_name = f"{name_without_ext} - {suffix}{ext}"
                            chunk_path = os.path.join(dir_name, chunk_name)
                            current_chunk_file = await aiofiles.open(chunk_path, 'wb')
                            chunk_paths.append(chunk_path)

                        remaining_space = self.chunk_size - bytes_written_to_chunk
                        bytes_to_write = min(data_len - cursor, remaining_space)

                        await current_chunk_file.write(data[cursor:cursor+bytes_to_write])

                        bytes_written_to_chunk += bytes_to_write
                        cursor += bytes_to_write

                        if bytes_written_to_chunk >= self.chunk_size:
                            await current_chunk_file.close()
                            current_chunk_file = None
                            bytes_written_to_chunk = 0
                            chunk_index += 1

            if current_chunk_file:
                await current_chunk_file.close()

            return chunk_paths

        except Exception as e:
            logger.error(f"Error splitting file {file_path}: {e}")
            # Clean up partial chunks?
            for p in chunk_paths:
                if os.path.exists(p):
                    try:
                        os.remove(p)
                    except:
                        pass
            raise e

splitter = FileSplitter()
