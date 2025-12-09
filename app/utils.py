import hashlib
import time
import os


BASE_DIR = "uploads"
os.makedirs(BASE_DIR, exist_ok=True)


def random_hash_name(original_name: str) -> str:
    """Generate a random hash based on time + filename."""
    h = hashlib.sha256()
    h.update(f"{time.time()}_{original_name}".encode())
    return h.hexdigest()[:32]  # 32 chars

