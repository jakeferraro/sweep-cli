"""Data model and formatting utilities for file entries."""

from dataclasses import dataclass
from pathlib import Path
from datetime import datetime


@dataclass
class FileTableRow:
    """Represents a row in the file table with formatted display values."""
    path: Path
    name: str
    size: str          # Formatted: "1.2 MB"
    size_bytes: int    # For sorting
    kind: str
    modified: str      # Formatted: "Jan 1, 2024"
    modified_ts: float # For sorting


def format_size(bytes_size: int) -> str:
    """
    Format file size in human-readable form.

    Args:
        bytes_size: Size in bytes

    Returns:
        Formatted string like "1.2 MB", "500 KB", etc.
    """
    if bytes_size < 1024:
        return f"{bytes_size} B"
    elif bytes_size < 1024 ** 2:
        return f"{bytes_size / 1024:.1f} KB"
    elif bytes_size < 1024 ** 3:
        return f"{bytes_size / (1024 ** 2):.1f} MB"
    else:
        return f"{bytes_size / (1024 ** 3):.2f} GB"


def format_date(dt: datetime) -> str:
    """
    Format datetime in readable form.

    Args:
        dt: datetime object

    Returns:
        Formatted string like "Jan 1, 2024, 3:45 PM"
    """
    return dt.strftime("%b %d, %Y, %I:%M %p")


def get_file_kind(path: Path) -> str:
    """
    Get file kind/type from extension or category.

    Args:
        path: File path

    Returns:
        File type description (e.g., "Video", "Archive", "Document")
    """
    suffix = path.suffix.lower()

    # Video extensions
    if suffix in ['.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv', '.m4v']:
        return 'Video'

    # Archive extensions
    if suffix in ['.zip', '.tar', '.gz', '.bz2', '.7z', '.rar', '.xz']:
        return 'Archive'

    # Disk image extensions
    if suffix in ['.dmg', '.iso', '.img']:
        return 'Disk Image'

    # Document extensions
    if suffix in ['.pdf', '.doc', '.docx', '.txt', '.rtf']:
        return 'Document'

    # Image extensions
    if suffix in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp']:
        return 'Image'

    # Audio extensions
    if suffix in ['.mp3', '.wav', '.flac', '.aac', '.m4a', '.ogg']:
        return 'Audio'

    # Code extensions
    if suffix in ['.py', '.js', '.java', '.c', '.cpp', '.h', '.sh', '.rb']:
        return 'Source Code'

    # Return extension without dot if no match
    if suffix:
        return suffix[1:].upper() + ' File'

    return 'File'


def create_table_row(file_entry) -> FileTableRow:
    """
    Convert a FileEntry to a FileTableRow with formatted display values.

    Args:
        file_entry: FileEntry object from scanner

    Returns:
        FileTableRow with formatted data
    """
    return FileTableRow(
        path=file_entry.path,
        name=file_entry.path.name,
        size=format_size(file_entry.size),
        size_bytes=file_entry.size,
        kind=file_entry.category.title() if hasattr(file_entry, 'category') else get_file_kind(file_entry.path),
        modified=format_date(file_entry.modified),
        modified_ts=file_entry.modified.timestamp()
    )
