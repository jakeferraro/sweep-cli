"""Finder tag operations using tag CLI."""

import subprocess
import sys


def check_tag_installed():
    """Check if tag CLI is installed."""
    try:
        subprocess.run(['tag', '--version'], 
                      capture_output=True, 
                      check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def apply_tags(files, tag_name, dry_run=False):
    """
    Apply Finder tag to list of files.
    
    Returns: int (number of files tagged)
    """
    if dry_run:
        return len(files)
    
    tagged = 0
    for file_entry in files:
        try:
            subprocess.run(
                ['tag', '--add', tag_name, str(file_entry.path)],
                capture_output=True,
                check=True
            )
            tagged += 1
        except subprocess.CalledProcessError:
            # Log error but continue
            print(f"Warning: Could not tag {file_entry.path}", file=sys.stderr)
            continue
    
    return tagged


def remove_tags(tag_name):
    """Remove specified tag from all files."""
    try:
        # Find all files with this tag
        result = subprocess.run(
            ['tag', '--find', tag_name],
            capture_output=True,
            text=True,
            check=True
        )
        
        paths = result.stdout.strip().split('\n')
        
        for path in paths:
            if not path:
                continue
            subprocess.run(
                ['tag', '--remove', tag_name, path],
                capture_output=True,
                check=True
            )
        
        return len([p for p in paths if p])
    
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to remove tags: {e}")


def clear_all_sweep_tags():
    """Remove all tags starting with 'sweep'."""
    # Get all tags in use
    result = subprocess.run(
        ['tag', '--list'],
        capture_output=True,
        text=True,
        check=True
    )
    
    all_tags = result.stdout.strip().split('\n')
    sweep_tags = [t for t in all_tags if t.startswith('sweep')]
    
    for tag in sweep_tags:
        remove_tags(tag)
    
    return len(sweep_tags)