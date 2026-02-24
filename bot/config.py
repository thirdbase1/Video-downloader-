import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_env_variable(var_name, default=None, required=False):
    value = os.getenv(var_name, default)
    if required and not value:
        print(f"Error: Environment variable {var_name} is required but not set.")
        sys.exit(1)
    return value

# Bot Configuration
BOT_TOKEN = get_env_variable("BOT_TOKEN", required=True)
DOWNLOAD_PATH = get_env_variable("DOWNLOAD_PATH", "downloads")
MAX_CHUNK_SIZE_MB = int(get_env_variable("MAX_CHUNK_SIZE_MB", 50))
MAX_CONCURRENT_DOWNLOADS = int(get_env_variable("MAX_CONCURRENT_DOWNLOADS", 30))
THREAD_POOL_SIZE = int(get_env_variable("THREAD_POOL_SIZE", 50))
LOG_FILE = get_env_variable("LOG_FILE", "logs/bot.log")
YTDLP_COOKIES_FILE = get_env_variable("YTDLP_COOKIES_FILE", "cookies.txt")
TELEGRAM_BASE_URL = get_env_variable("TELEGRAM_BASE_URL", "https://api.telegram.org/bot")

# Ensure download directory exists
if not os.path.exists(DOWNLOAD_PATH):
    os.makedirs(DOWNLOAD_PATH)

# Ensure log directory exists
log_dir = os.path.dirname(LOG_FILE)
if log_dir and not os.path.exists(log_dir):
    os.makedirs(log_dir)
