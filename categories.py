"""File category detection based on extension and path."""

from pathlib import Path


CATEGORIES = {
    'archive': {'.zip', '.tar', '.gz', '.bz2', '.7z', '.rar', '.tgz', '.tar.gz'},
    'disk_image': {'.dmg', '.iso', '.img', '.vdi', '.vmdk'},
    'video': {'.mp4', '.mov', '.avi', '.mkv', '.m4v', '.flv'},
    'log': {'.log', '.out'}
}

CACHE_DIRS = {'node_modules', '__pycache__', '.cache', 'venv', '.venv'}


def detect_category(filepath):
    """
    Detect file category based on extension and path.
    
    Returns: str (category name)
    """
    # Check if in cache directory
    parts = filepath.parts
    if any(cache_dir in parts for cache_dir in CACHE_DIRS):
        return 'cache'
    
    # Check extension
    ext = filepath.suffix.lower()
    if not ext:
        return 'other'
    
    for category, extensions in CATEGORIES.items():
        if ext in extensions:
            # Special case for logs - must be in log directory
            if category == 'log':
                if any(log_dir in parts for log_dir in ('logs', 'var', 'tmp')):
                    return 'log'
                else:
                    return 'other'
            return category
    
    return 'other'