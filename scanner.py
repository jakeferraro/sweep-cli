"""Filesystem scanning and filtering."""

import os
import subprocess
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


def scan_with_mdfind(config):
    """
    Use mdfind to scan for files.

    Returns: List[FileEntry] or None if mdfind fails
    """
    try:
        # Build mdfind query
        query_parts = []

        # Add path restriction
        onlyin_arg = ['-onlyin', str(config.path)]

        # Basic query to find files (not directories)
        query_parts.append('kMDItemContentTypeTree == "public.data"')

        # Build the full mdfind command
        cmd = ['mdfind'] + onlyin_arg + [' && '.join(query_parts)]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode != 0:
            return None

        # Process results
        file_list = []
        exclude_dirs = set(str(p) for p in config.exclude)

        for line in result.stdout.strip().split('\n'):
            if not line:
                continue

            filepath = Path(line)

            # Skip if in excluded directory
            if any(str(filepath).startswith(ex) for ex in exclude_dirs):
                continue

            # Skip hidden files
            if any(part.startswith('.') for part in filepath.parts):
                continue

            try:
                stat = filepath.stat()

                # Skip if not a regular file
                if not filepath.is_file():
                    continue

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

                file_list.append(FileEntry(
                    path=filepath,
                    size=stat.st_size,
                    modified=datetime.fromtimestamp(stat.st_mtime),
                    category=category
                ))

            except (PermissionError, OSError):
                # Skip files we can't access
                continue

        return file_list

    except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
        return None


def scan_with_walk(config):
    """
    Fallback scanning using os.walk.

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


def scan_filesystem(config):
    """
    Scan filesystem and return list of matching files.
    Uses mdfind as primary mechanism, falls back to os.walk.

    Returns: List[FileEntry]
    """
    # Try mdfind first
    results = scan_with_mdfind(config)

    # Fall back to os.walk if mdfind fails
    if results is None:
        results = scan_with_walk(config)

    return results