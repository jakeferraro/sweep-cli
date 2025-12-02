"""Native macOS file operations."""

import subprocess
from pathlib import Path
from typing import List


def move_to_trash(file_paths: List[Path]) -> bool:
    """
    Move files to trash using macOS Finder.

    Args:
        file_paths: List of file paths to move to trash

    Returns:
        True if successful, False otherwise
    """
    if not file_paths:
        return False

    try:
        for file_path in file_paths:
            # Use osascript to tell Finder to delete the file (moves to trash)
            script = f'tell application "Finder" to delete POSIX file "{file_path}"'
            result = subprocess.run(
                ['osascript', '-e', script],
                capture_output=True,
                text=True,
                check=True
            )
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error moving files to trash: {e.stderr}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False


def open_file(file_path: Path) -> bool:
    """
    Open file with default application.

    Args:
        file_path: Path to file to open

    Returns:
        True if successful, False otherwise
    """
    try:
        subprocess.run(['open', str(file_path)], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error opening file: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False


def show_in_finder(file_path: Path) -> bool:
    """
    Reveal file in Finder.

    Args:
        file_path: Path to file to reveal

    Returns:
        True if successful, False otherwise
    """
    try:
        subprocess.run(['open', '-R', str(file_path)], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error showing file in Finder: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False


def copy_path_to_clipboard(file_path: Path) -> bool:
    """
    Copy file path to clipboard.

    Args:
        file_path: Path to copy

    Returns:
        True if successful, False otherwise
    """
    try:
        # Use pbcopy to copy to clipboard
        process = subprocess.Popen(
            ['pbcopy'],
            stdin=subprocess.PIPE,
            text=True
        )
        process.communicate(input=str(file_path))
        return process.returncode == 0
    except Exception as e:
        print(f"Error copying to clipboard: {e}")
        return False
