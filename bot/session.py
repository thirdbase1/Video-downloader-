import asyncio
from typing import Dict
from .config import MAX_CONCURRENT_DOWNLOADS

class SessionManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SessionManager, cls).__new__(cls)
            cls._instance.semaphore = asyncio.Semaphore(MAX_CONCURRENT_DOWNLOADS)
            cls._instance.user_locks: Dict[int, asyncio.Lock] = {}
        return cls._instance

    async def acquire_global(self):
        """Acquire a global slot for download/processing."""
        await self.semaphore.acquire()

    def release_global(self):
        """Release a global slot."""
        self.semaphore.release()

    def get_user_lock(self, user_id: int) -> asyncio.Lock:
        """Get or create a lock for a specific user to prevent concurrent requests."""
        if user_id not in self.user_locks:
            self.user_locks[user_id] = asyncio.Lock()
        return self.user_locks[user_id]

    async def run_with_global_limit(self, func, *args, **kwargs):
        """Run a function ensuring global concurrency limit."""
        async with self.semaphore:
            return await func(*args, **kwargs)

    async def run_exclusive_user(self, user_id: int, func, *args, **kwargs):
        """Run a function ensuring the user processes only one request at a time."""
        lock = self.get_user_lock(user_id)
        # Using wait_for to prevent infinite waiting if something goes wrong?
        # For now, just acquire.
        if lock.locked():
             # Option: return False or raise exception if user is busy
             # Prompt says "queue it or notify them to wait".
             # With lock, it queues automatically (waits).
             pass

        async with lock:
            return await func(*args, **kwargs)

# Global instance
session_manager = SessionManager()
