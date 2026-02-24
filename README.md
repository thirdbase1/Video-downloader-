# Video-downloader-
Telegram Public Video Splitter Bot
A Telegram bot built with Python that downloads videos from any URL, splits them into 50 MB chunks, and sends them via the Telegram Bot API.
🛠 Tools & Libraries
Component
Purpose
python-telegram-bot
Interact with Telegram Bot API
yt-dlp
Extract video formats & metadata
aiohttp
Async HTTP requests
asyncio
Async task management
ffmpeg, split
Video info & binary splitting
python-dotenv
Environment variable loading
logging
Structured logging for diagnostics
📦 Installation
Create and activate a virtual environment:
Bash
Copy code
python3 -m venv venv
source venv/bin/activate
Install requirements:
Bash
Copy code
pip install -r requirements.txt
Create a .env file:
Bash
Copy code
echo "BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN" > .env
echo "DOWNLOAD_PATH=downloads" >> .env
🔍 How It Works
User sends any video URL to the bot.
Bot uses yt-dlp to extract available video formats, estimated sizes, and direct stream URLs.
Bot replies with resolution choices.
User selects resolution.
Bot downloads the video.
If size > 50 MB, bot splits it into 50 MB binaries.
Bot sends each part labeled clearly.
Bot gives user instructions to merge parts locally.
📋 Supported Sources
The bot accepts any URL from any platform. yt-dlp supports 1000+ sites out of the box including YouTube, Dailymotion, Vimeo, Twitter/X, Facebook, Instagram, TikTok, Reddit, Twitch, and many more.
For each platform, the bot must perform deep extraction research to understand:
How yt-dlp's extractor works for that specific platform (check yt_dlp/extractor/ source per site)
What format codes are available using:
yt-dlp --list-formats <url>
Whether the platform serves HLS, DASH, or direct MP4 and how to handle each
Any rate limits, geo-restrictions, or header requirements the platform enforces
Whether cookies or authentication tokens are needed using --cookies-from-browser or --cookies
How to pass a custom User-Agent or referer header to avoid blocks
Platform-specific throttling behavior and how yt-dlp works around it
This deep per-platform research ensures reliable downloads regardless of the source.
📌 How the Split Works
For large files: download full video temporarily, split binary file into 50 MB chunks, send each chunk through the Bot API, then delete temp files after sending.
Command examples:
Unix:
Bash
Copy code
split -b 50M video.mp4 part_
Windows:
Copy code

copy /b part_00+part_01 final.mp4
☁️ Deployment on pxxl.app
Create a GitHub repository with your code.
Ensure .env contains BOT_TOKEN and settings.
Add a requirements.txt.
Configure pxxl.app deployment with Python runtime and startup command:
Copy code

python main.py
Increase disk space if needed.
Use logging for crash monitoring.
🛡 Error Handling
The bot must safely handle:
Invalid URLs
Unsupported platforms
Extraction failures
Download interruptions
Splitting errors
Upload limits
API timeouts
Always respond to users with clear error messages.
📈 Future Improvements
Caching previously downloaded chunks
Hosting merged download links
Cleaner UX with inline keyboards
Auto-detection and per-platform download strategies
Cookie management for platforms requiring authentication
📌 Disclaimer
This bot is designed for personal and educational use. Always follow the terms of service of the platforms you access.
📍 Research Guidance
To make this work reliably, study:
Telegram Bot API upload limits
yt-dlp extractors and format selectors per platform
yt-dlp cookie and header handling
ffmpeg basics for format info
Binary splitting and safe concatenation
Async Python task control
Deployment environment constraints (memory, disk, timeouts)
