# High-Performance Telegram Video Splitter Bot

A production-ready, concurrent Telegram bot built with Python that downloads videos from any URL supported by `yt-dlp`, splits them into 50 MB chunks (Telegram Bot API limit), and sends them to the user. Designed to handle high concurrency (200+ users) with efficient resource management.

## Features

- **Universal Support**: Downloads videos from YouTube, Dailymotion, Vimeo, Twitter/X, TikTok, Reddit, Twitch, and 1000+ other platforms via `yt-dlp`.
- **Intelligent Quality Selection**: Extracts available resolutions and lets the user choose via an inline keyboard.
- **Smart Splitting**: Automatically splits files larger than 50 MB into 50 MB chunks without re-encoding (binary split).
- **Intelligent Naming**: Chunks are named based on the original video title (e.g., `My Video - Part A.mp4`).
- **High Concurrency**:
  - Asynchronous architecture using `asyncio` and `python-telegram-bot`.
  - ThreadPoolExecutor for blocking I/O (downloading).
  - Connection pooling for uploads via `aiohttp`.
  - Concurrent chunk uploads for maximum speed.
  - Global semaphore to limit active downloads.
  - Per-user task queue to prevent flooding.
- **Progress Tracking**: Real-time progress updates for downloading, splitting, and uploading.
- **Robust Error Handling**: Handles network errors, authentication requirements, and rate limits gracefully.

## Installation

### Prerequisites
- Python 3.9+
- FFmpeg (required by `yt-dlp` for some merges, though binary splitting is used primarily)

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/video-splitter-bot.git
   cd video-splitter-bot
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/macOS
   # venv\Scripts\activate  # Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configuration:**
   Copy `.env.example` to `.env` and fill in your details:
   ```bash
   cp .env.example .env
   ```

   Edit `.env`:
   ```ini
   BOT_TOKEN=your_telegram_bot_token
   DOWNLOAD_PATH=downloads
   MAX_CHUNK_SIZE_MB=50
   MAX_CONCURRENT_DOWNLOADS=30
   THREAD_POOL_SIZE=50
   LOG_FILE=logs/bot.log
   ```

## Usage

1. **Start the bot:**
   ```bash
   python -m bot.main
   ```

2. **Interact with the bot:**
   - Send `/start` to get a welcome message.
   - Send any video URL.
   - Select the desired quality from the inline buttons.
   - Wait for the bot to download, split, and send the parts.

## Merging Parts

The bot sends parts named like `Video Title - Part A.mp4`, `Video Title - Part B.mp4`.

**Linux/macOS:**
```bash
cat "Video Title - Part A.mp4" "Video Title - Part B.mp4" > "Full Video.mp4"
```

**Windows CMD:**
```cmd
copy /b "Part A.mp4"+"Part B.mp4" "Full Video.mp4"
```

**Android:**
Use a file manager like **MiXplorer** or **Total Commander**. Select all parts -> Long press -> Menu -> Merge/Join.

## Deployment on Termux (Android)

1. **Update and Install System Packages:**
   ```bash
   pkg update && pkg upgrade
   pkg install python ffmpeg rust binutils git
   ```

2. **Clone and Enter Directory:**
   ```bash
   git clone https://github.com/yourusername/video-splitter-bot.git
   cd video-splitter-bot
   ```

3. **Setup Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -U pip setuptools wheel
   pip install -r requirements.txt
   ```

4. **Configure:**
   Copy `.env.example` to `.env` and edit it with your bot token.

5. **Run:**
   ```bash
   python -m bot.main
   ```

## Deployment on pxxl.app (or generic Linux VPS)

1. **Ensure requirements are pinned:**
   The `requirements.txt` file contains pinned versions for stability.

2. **Environment Variables:**
   Set the `BOT_TOKEN` and other variables in your hosting provider's dashboard.

3. **Start Command:**
   ```bash
   python -m bot.main
   ```

4. **Disk Space:**
   Ensure the `DOWNLOAD_PATH` is writable and has sufficient space for temporary files. The bot cleans up files immediately after sending.

## Architecture & Performance

- **Non-Blocking Core**: The bot runs on `asyncio`. Heavy tasks (downloading) are offloaded to a thread pool to avoid blocking the event loop.
- **Streaming Uploads**: Files are streamed directly from disk to Telegram using `aiohttp` and `aiofiles` to minimize RAM usage.
- **Connection Pooling**: A shared `aiohttp.ClientSession` is used for uploads to reduce handshake overhead.
- **Concurrent Uploads**: Multiple chunks of the same video are uploaded in parallel (limited by semaphore) to saturate available bandwidth.

## Troubleshooting

- **"This link requires authentication"**: The bot only supports publicly accessible links. Private videos or those requiring login are rejected for security and technical reasons.
- **Download Fails**: Check logs (`logs/bot.log`) for details. Common issues include geo-restrictions (try a proxy or VPN on the server) or platform changes (update `yt-dlp`).
- **Upload Timeout**: If Telegram API is slow, the bot retries with exponential backoff.
- **Disk Full**: The bot monitors disk usage implicitly. Ensure regular cleanup if the process crashes (auto-cleanup on startup is not implemented, but per-task cleanup is robust).

## License

MIT License
