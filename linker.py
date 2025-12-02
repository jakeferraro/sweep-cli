"""Hardlink operations for organizing files."""

import os
import sys
from pathlib import Path


def create_hardlinks(files, target_dir, folder_name, dry_run=False):
    """
    Create hardlinks to files in a specified directory.

    Args:
        files: List of FileEntry objects
        target_dir: Base directory where the folder will be created
        folder_name: Name of the folder to create for hardlinks
        dry_run: If True, don't actually create links

    Returns: int (number of files linked)
    """
    link_dir = Path(target_dir) / folder_name

    if dry_run:
        return len(files)

    # Create target directory if it doesn't exist
    try:
        link_dir.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        raise RuntimeError(f"Failed to create directory {link_dir}: {e}")

    linked = 0
    for file_entry in files:
        try:
            # Generate unique link name if file already exists
            link_path = link_dir / file_entry.path.name
            counter = 1
            while link_path.exists():
                stem = file_entry.path.stem
                suffix = file_entry.path.suffix
                link_path = link_dir / f"{stem}_{counter}{suffix}"
                counter += 1

            # Create hardlink
            os.link(file_entry.path, link_path)
            linked += 1
        except OSError as e:
            # Log error but continue
            print(f"Warning: Could not link {file_entry.path}: {e}", file=sys.stderr)
            continue

    return linked


def remove_link_folder(target_dir, folder_name):
    """Remove the hardlink folder and its contents."""
    link_dir = Path(target_dir) / folder_name

    if not link_dir.exists():
        return 0

    count = 0
    try:
        # Remove all files in the folder
        for item in link_dir.iterdir():
            if item.is_file():
                item.unlink()
                count += 1

        # Remove the folder itself
        link_dir.rmdir()

        return count
    except OSError as e:
        raise RuntimeError(f"Failed to remove link folder: {e}")


def clear_all_sweep_links(target_dir):
    """Remove all folders starting with 'sweep' in target directory."""
    target_path = Path(target_dir)

    if not target_path.exists():
        return 0

    count = 0
    for item in target_path.iterdir():
        if item.is_dir() and item.name.startswith('sweep'):
            folder_count = remove_link_folder(target_dir, item.name)
            count += folder_count

    return count
