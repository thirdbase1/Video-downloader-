import yt_dlp
from .logger import logger
from .utils import human_readable_size

class AuthenticationError(Exception):
    """Raised when the video requires authentication."""
    pass

class VideoExtractor:
    def get_info(self, url):
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'noplaylist': True,
            'extract_flat': False, # We need formats, so extract_flat might be too shallow if True
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return self._process_info(info)
        except yt_dlp.utils.DownloadError as e:
            error_msg = str(e)
            logger.error(f"Extraction failed for {url}: {error_msg}")

            # Detect authentication/login requirements
            auth_keywords = [
                "Sign in", "login", "account", "authenticate",
                "password", "private", "members-only"
            ]
            if any(keyword.lower() in error_msg.lower() for keyword in auth_keywords):
                raise AuthenticationError("This link requires authentication or a login to access and is not supported. Please send a publicly accessible video link.")
            raise e
        except Exception as e:
            logger.error(f"Unexpected error extracting {url}: {e}")
            raise e

    def _process_info(self, info):
        """
        Process the raw info dictionary from yt-dlp.
        """
        title = info.get('title', 'Unknown Title')
        duration = info.get('duration', 0)
        uploader = info.get('uploader', 'Unknown Uploader')
        extractor = info.get('extractor', 'Unknown Platform')
        formats = info.get('formats', [])

        # Filter and process formats
        processed_formats = []
        seen_resolutions = set()

        # We want video formats, preferably with audio or we can merge.
        # yt-dlp 'best' usually handles merging.
        # But for manual selection, we need to show options.
        # Usually users want 360p, 480p, 720p, 1080p.
        # We should look for formats that have video.

        # Sort formats by resolution/quality
        # yt-dlp sorts them worst to best usually.

        for f in formats:
            # Skip audio only formats
            if f.get('vcodec') == 'none':
                continue

            # Skip video only if we can't merge easily (but we can let yt-dlp merge)
            # However, for the selection UI, we want to show "1080p (approx 50MB)"

            resolution = f.get('resolution') or f.get('format_note')
            if not resolution:
                height = f.get('height')
                if height:
                    resolution = f"{height}p"
                else:
                    continue # Skip if no resolution info

            # Simple deduplication based on resolution
            # This is tricky because there might be multiple codecs (av01, vp9, h264).
            # We should probably pick the best for each resolution or list them all?
            # Prompt says: "Display format choices to the user... e.g. 360p, 480p..."
            # So unique resolutions.

            # We prefer mp4 containers for compatibility
            ext = f.get('ext')

            # Estimate size
            filesize = f.get('filesize') or f.get('filesize_approx')

            if resolution not in seen_resolutions:
                processed_formats.append({
                    'format_id': f['format_id'],
                    'resolution': resolution,
                    'ext': ext,
                    'filesize': filesize,
                    'filesize_str': human_readable_size(filesize) if filesize else "Unknown",
                    'vcodec': f.get('vcodec'),
                    'acodec': f.get('acodec'),
                })
                seen_resolutions.add(resolution)
            else:
                # If we already have this resolution, check if this one is "better" (e.g. mp4 vs webm, or has filesize)
                # This is a simplified logic.
                for existing in processed_formats:
                    if existing['resolution'] == resolution:
                        if (existing['filesize'] is None and filesize is not None) or \
                           (existing['ext'] != 'mp4' and ext == 'mp4'):
                                existing['format_id'] = f['format_id']
                                existing['ext'] = ext
                                existing['filesize'] = filesize
                                existing['filesize_str'] = human_readable_size(filesize) if filesize else "Unknown"
                        break

        # Sort by height/resolution if possible?
        # Typically they are already sorted by yt-dlp.
        # Let's ensure they are meaningful.

        return {
            'title': title,
            'duration': duration,
            'uploader': uploader,
            'platform': extractor,
            'formats': processed_formats
        }

extractor = VideoExtractor()
