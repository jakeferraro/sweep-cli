"""
Sweep - Filesystem analyzer with hardlink organization
"""

import sys
import argparse
from pathlib import Path

from scanner import scan_filesystem
from linker import create_hardlinks, remove_link_folder, clear_all_sweep_links
from output import output_summary, output_json, output_csv
from config import Config
from utils import parse_size


def main():
    parser = argparse.ArgumentParser(
        description='Sweep - Organize files using hardlinks for review and deletion',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # File selection
    parser.add_argument('--min-size', type=str, help='Minimum file size (e.g., 100M, 1G)')
    parser.add_argument('--older-than', type=int, help='Files not modified in N days')
    parser.add_argument('--category', choices=['archive', 'disk_image', 'video', 'cache', 'log'])
    parser.add_argument('--path', type=str, default=str(Path.home()), help='Directory to scan')
    parser.add_argument('--exclude', type=str, default='/System,/Library,/Applications')

    # Hardlink options
    parser.add_argument('--link-folder', type=str, default='sweep_links', help='Name of folder to create for hardlinks')
    parser.add_argument('--target-dir', type=str, default=str(Path.home() / 'Desktop'), help='Target directory for link folder')
    parser.add_argument('--no-link', action='store_true', help='Skip creating hardlinks')

    # Output
    parser.add_argument('--json', type=str, help='Output JSON to file')
    parser.add_argument('--csv', type=str, help='Output CSV to file')
    parser.add_argument('--format', choices=['json', 'csv', 'summary'], default='summary')
    parser.add_argument('--quiet', action='store_true')

    # Utility
    parser.add_argument('--remove-links', type=str, help='Remove specified link folder')
    parser.add_argument('--clear-all-links', action='store_true', help='Remove all sweep link folders')
    parser.add_argument('--limit', type=int, help='Process top N results')
    parser.add_argument('--dry-run', action='store_true')

    # General
    parser.add_argument('--version', action='version', version='sweep 2.0.0')

    args = parser.parse_args()

    # Handle utility commands
    if args.remove_links:
        target = Path(args.target_dir).expanduser()
        count = remove_link_folder(target, args.remove_links)
        print(f"Removed link folder '{args.remove_links}' containing {count} files")
        sys.exit(0)

    if args.clear_all_links:
        target = Path(args.target_dir).expanduser()
        count = clear_all_sweep_links(target)
        print(f"Removed {count} files from sweep link folders")
        sys.exit(0)

    # Build config
    config = Config(
        path=Path(args.path).expanduser(),
        min_size=parse_size(args.min_size) if args.min_size else 0,
        older_than=args.older_than,
        category_filter=args.category,
        exclude=[Path(p.strip()) for p in args.exclude.split(',')],
        link_folder=args.link_folder,
        target_dir=Path(args.target_dir).expanduser(),
        no_link=args.no_link,
        limit=args.limit,
        dry_run=args.dry_run,
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

    # Create hardlinks
    if not config.no_link and results:
        linked = create_hardlinks(results, config.target_dir, config.link_folder, config.dry_run)
        if not config.quiet:
            link_path = config.target_dir / config.link_folder
            if config.dry_run:
                print(f"\n[DRY RUN] Would create {linked} hardlinks in '{link_path}'")
            else:
                print(f"\nCreated {linked} hardlinks in '{link_path}'")
                print("Review files in link folder and delete as needed.")


if __name__ ==  "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted by user", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

