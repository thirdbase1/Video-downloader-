import re
import os
import shutil
import string

def sanitize_filename(name):
    """
    Sanitizes a string to be safe for filenames.
    Removes characters that are unsafe for filenames on Windows/Linux.
    """
    # Remove invalid characters
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    # Collapse whitespaces
    name = re.sub(r'\s+', ' ', name).strip()
    return name

def get_chunk_suffix(index):
    """
    Generates a suffix like 'Part A', 'Part B' ... 'Part Z', 'Part AA', etc.
    index is 0-based.
    """
    alphabet = string.ascii_uppercase

    if index < 0:
        raise ValueError("Index must be non-negative")

    if index < 26:
        return f"Part {alphabet[index]}"

    # For index >= 26, we need AA, AB, etc.
    # This is a base-26 conversion
    suffix = ""
    temp_index = index

    while temp_index >= 0:
        suffix = alphabet[temp_index % 26] + suffix
        temp_index = (temp_index // 26) - 1

    return f"Part {suffix}"

def cleanup_temp_dir(path):
    """
    Recursively deletes a directory and its contents.
    """
    if os.path.exists(path):
        try:
            shutil.rmtree(path)
        except Exception as e:
            print(f"Error cleaning up {path}: {e}")

def human_readable_size(size, decimal_places=2):
    """
    Converts bytes to a human readable string (e.g. 50.00 MB).
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.{decimal_places}f} {unit}"
        size /= 1024.0
    return f"{size:.{decimal_places}f} PB"
