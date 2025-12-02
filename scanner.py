"""Filesystem scanning and filtering."""

import os
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass

from categories import detect_category


@dataclass
class FileEntry:
    """Represents a file matching scan criteria."""
    path: Path
    size: int
    modified: datetime
    category: str


def scan_filesystem(config):
    """
    Scan filesystem and return list of matching files.
    
    Returns: List[FileEntry]
    """
    results = []
    exclude_dirs = set(str(p) for p in config.exclude)
    
    for root, dirs, files in os.walk(config.path, topdown=True):
        # Remove excluded directories from traversal
        dirs[:] = [d for d in dirs if os.path.join(root, d) not in exclude_dirs]
        
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for filename in files:
            filepath = Path(root) / filename
            
            try:
                stat = filepath.stat()
                
                # Early filtering - size
                if stat.st_size < config.min_size:
                    continue
                
                # Early filtering - age
                if config.older_than:
                    age_days = (datetime.now() - datetime.fromtimestamp(stat.st_mtime)).days
                    if age_days < config.older_than:
                        continue
                
                # Category detection
                category = detect_category(filepath)
                
                # Category filter
                if config.category_filter and category != config.category_filter:
                    continue
                
                results.append(FileEntry(
                    path=filepath,
                    size=stat.st_size,
                    modified=datetime.fromtimestamp(stat.st_mtime),
                    category=category
                ))
                
            except (PermissionError, OSError):
                # Skip files we can't access
                continue
    
    return results