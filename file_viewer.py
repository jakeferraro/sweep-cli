#!/usr/bin/env python3
"""Standalone GUI application for viewing and managing files."""

import sys
import json
import os
import atexit
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass

from PyQt6.QtWidgets import QApplication

from gui.main_window import FileViewerWindow


@dataclass
class FileEntry:
    """Represents a file entry (matches scanner.FileEntry structure)."""
    path: Path
    size: int
    modified: datetime
    category: str


def load_file_data(input_source):
    """
    Load file data from various input sources.

    Args:
        input_source: Can be a JSON file path, list of file paths, or stdin

    Returns:
        List of FileEntry objects
    """
    file_entries = []

    # If input is a JSON file
    if isinstance(input_source, str) and input_source.endswith('.json'):
        with open(input_source, 'r') as f:
            data = json.load(f)

        for item in data:
            file_entries.append(FileEntry(
                path=Path(item['path']),
                size=item['size'],
                modified=datetime.fromisoformat(item['modified']),
                category=item.get('category', 'Unknown')
            ))

    return file_entries


def main():
    """Main entry point for the GUI application."""
    if len(sys.argv) < 2:
        print("Usage: file_viewer.py <json_file>")
        sys.exit(1)

    input_file = sys.argv[1]

    # Load file data
    try:
        file_entries = load_file_data(input_file)
    except Exception as e:
        print(f"Error loading file data: {e}")
        sys.exit(1)

    # Register cleanup for temp file
    if input_file.endswith('.json'):
        atexit.register(lambda: os.path.exists(input_file) and os.unlink(input_file))

    # Create and run Qt application
    app = QApplication(sys.argv)
    app.setApplicationName('Sweep File Viewer')

    # Create and show main window
    window = FileViewerWindow(file_entries)
    window.show()

    # Start event loop
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
