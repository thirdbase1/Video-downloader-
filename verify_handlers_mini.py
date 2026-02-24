import os
import sys

# Set env
os.environ["BOT_TOKEN"] = "TEST_TOKEN"
os.environ["DOWNLOAD_PATH"] = "test_downloads"

try:
    from bot.handlers import handlers
    print("Handlers verification OK")
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
