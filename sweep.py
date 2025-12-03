"""
Sweep - Filesystem analyzer with native macOS GUI
"""

import sys
import argparse
import json
import tempfile
import subprocess
from pathlib import Path

from scanner import scan_filesystem
from output import output_summary, output_json, output_csv
from config import Config
from utils import parse_size


def serialize_file_entry(entry):
    """Serialize FileEntry to JSON-compatible dict."""
    return {
        'path': str(entry.path),
        'size': entry.size,
        'modified': entry.modified.isoformat(),
        'category': entry.category
    }


def launch_gui(results):
    """
    Launch GUI with file results.

    Args:
        results: List of FileEntry objects
    """
    try:
        # Create temporary JSON file
        temp_file = tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.json',
            delete=False
        )

        # Serialize results to JSON
        json.dump([serialize_file_entry(r) for r in results], temp_file)
        temp_file.close()

        # Launch GUI as subprocess (non-blocking)
        subprocess.Popen([
            sys.executable,
            'file_viewer.py',
            temp_file.name
        ])

    except Exception as e:
        print(f"Warning: Failed to launch GUI: {e}", file=sys.stderr)
        print("Results are still available via CLI output.", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description='Sweep - Filesystem analyzer with native macOS GUI',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # File selection
    parser.add_argument('--min-size', type=str, help='Minimum file size (e.g., 100M, 1G)')
    parser.add_argument('--older-than', type=int, help='Files not modified in N days')
    parser.add_argument('--category', choices=['archive', 'disk_image', 'video', 'cache', 'log'])
    parser.add_argument('--path', type=str, default=str(Path.home()), help='Directory to scan')
    parser.add_argument('--exclude', type=str, default='/System,/Library,/Applications')

    # Output
    parser.add_argument('--json', type=str, help='Output JSON to file')
    parser.add_argument('--csv', type=str, help='Output CSV to file')
    parser.add_argument('--format', choices=['json', 'csv', 'summary'], default='summary')
    parser.add_argument('--quiet', action='store_true')
    parser.add_argument('--no-gui', action='store_true', help='Skip GUI and only show CLI output')

    # Utility
    parser.add_argument('--limit', type=int, help='Process top N results')

    # General
    parser.add_argument('--version', action='version', version='sweep 1.0.0')

    args = parser.parse_args()

    # Build config
    config = Config(
        path=Path(args.path).expanduser(),
        min_size=parse_size(args.min_size) if args.min_size else 0,
        older_than=args.older_than,
        category_filter=args.category,
        exclude=[Path(p.strip()) for p in args.exclude.split(',')],
        limit=args.limit,
        quiet=args.quiet
    )

    # Scan filesystem
    if not config.quiet:
        print(f"Scanning {config.path}...")

    results = scan_filesystem(config)

    # Apply limit
    if config.limit:
        results = sorted(results, key=lambda x: x.size, reverse=True)[:config.limit]

    # Output results
    if args.format == 'json' or args.json:
        output_json(results, config, args.json)
    elif args.format == 'csv' or args.csv:
        output_csv(results, config, args.csv)
    else:
        output_summary(results, config)

    # Launch GUI unless --no-gui flag is set
    if not args.no_gui and results:
        launch_gui(results)


if __name__ ==  "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted by user", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

