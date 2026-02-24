import yt_dlp
import os
import asyncio
from concurrent.futures import ThreadPoolExecutor
from .config import THREAD_POOL_SIZE
from .logger import logger

class VideoDownloader:
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=THREAD_POOL_SIZE)

    async def download_video(self, url, format_id, output_dir, progress_callback=None):
        """
        Downloads video using yt-dlp in a separate thread.
        progress_callback should be an async function taking (status, percent_str).
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            self.executor,
            self._download_sync,
            url, format_id, output_dir, progress_callback, loop
        )

    def _download_sync(self, url, format_id, output_dir, progress_callback, loop):
        def progress_hook(d):
            if d['status'] == 'downloading':
                percent_str = d.get('_percent_str', '0%')
                # Remove ANSI codes if any
                percent_str = percent_str.replace('\x1b[0;94m', '').replace('\x1b[0m', '').strip()

                if progress_callback:
                    asyncio.run_coroutine_threadsafe(
                        progress_callback("downloading", percent_str),
                        loop
                    )
            elif d['status'] == 'finished':
                if progress_callback:
                    asyncio.run_coroutine_threadsafe(
                        progress_callback("finished", "100%"),
                        loop
                    )

        ydl_opts = {
            'format': format_id, # format_id or 'best'
            'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
            'concurrent_fragment_downloads': 8,
            'buffersize': 16384,
            'nopart': True, # Write directly to final file
            'quiet': True,
            'no_warnings': True,
            'progress_hooks': [progress_hook],
            # Ensure we don't download playlists
            'noplaylist': True,
            # Restrict filenames to ASCII to avoid filesystem issues
            'restrictfilenames': True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)

                filepath = ydl.prepare_filename(info)

                # Verify file exists
                if not os.path.exists(filepath):
                    # Sometimes formats are merged, extension might differ
                    # info['requested_downloads'] has the actual path
                    if 'requested_downloads' in info:
                        filepath = info['requested_downloads'][0]['filepath']

                if not os.path.exists(filepath):
                    raise Exception("File not found after download.")

                return filepath
        except Exception as e:
            logger.error(f"Download error for {url}: {e}")
            raise e

downloader = VideoDownloader()
