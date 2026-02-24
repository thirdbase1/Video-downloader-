# Simple Telegram Video Splitter Bot

A robust, simple, and high-performance Telegram bot that downloads videos from 1000+ sites (YouTube, Dailymotion, etc.), splits them into 50MB chunks, and sends them to you.

It uses **only official Telegram Bot API methods** and standard libraries. No Docker, no complex setup. Just Python.

## Features

- **Downloads Everything**: Powered by `yt-dlp`.
- **Splits Automatically**: Chunks large videos into 50MB parts (Telegram's limit).
- **Smart Naming**: "My Video - Part A.mp4", "My Video - Part B.mp4".
- **Concurrent**: Handles multiple users and uploads parts in parallel.
- **Clean**: Auto-cleans temporary files.

## Installation

### 1. Requirements
- Python 3.9+
- FFmpeg (Install via your package manager: `apt install ffmpeg`, `brew install ffmpeg`, or `pkg install ffmpeg`)

### 2. Setup

Clone the repo:
```bash
git clone https://github.com/yourusername/video-splitter-bot.git
cd video-splitter-bot
```

Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac/Android(Termux)
# venv\Scripts\activate   # Windows
```

Install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Configuration

Create a `.env` file:
```bash
cp .env.example .env
```

Open `.env` and add your **BOT_TOKEN** from @BotFather.

### 4. Run

```bash
python -m bot.main
```

That's it. The bot is running.

## Merging Parts

Since the bot splits videos to bypass the 50MB limit, you might want to join them later.

- **Android**: Use **MiXplorer** or **Total Commander** (Select files -> Merge).
- **PC**: `cat "Part A.mp4" "Part B.mp4" > "Full.mp4"` (Linux/Mac) or `copy /b ...` (Windows).

## Deployment on Server (24/7)

Use `screen` or `tmux` to keep it running:

```bash
screen -S bot
python -m bot.main
# Press Ctrl+A, then D to detach
```

## Deployment on Termux (Android)

1. **Install Packages**:
   ```bash
   pkg update && pkg upgrade
   pkg install python ffmpeg git rust binutils
   ```

2. **Clone & Setup**:
   ```bash
   git clone https://github.com/yourusername/video-splitter-bot.git
   cd video-splitter-bot
   python -m venv venv
   source venv/bin/activate
   pip install -U pip wheel setuptools
   pip install -r requirements.txt
   ```

3. **Configure**:
   Edit `.env` with your token.

4. **Run**:
   ```bash
   python -m bot.main
   ```
