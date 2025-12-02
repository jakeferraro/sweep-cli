"""
Sweep - Filesystem analyzer with Finder tag integration
"""

import sys
import argparse
from pathlib import Path

from scanner import scan_filesystem
from tagger import check_tag_installed, apply_tags, remove_tags, clear_all_sweep_tags
from output import output_summary, output_json, output_csv
from config import Config
from utils import parse_size


def main():
    parser = argparse.ArgumentParser(
        description='Sweep - Tag files for visual review and deletion',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # File selection
    parser.add_argument('--min-size', type=str, help='Minimum file size (e.g., 100M, 1G)')
    parser.add_argument('--older-than', type=int, help='Files not modified in N days')
    parser.add_argument('--category', choices=['archive', 'disk_image', 'video', 'cache', 'log'])
    parser.add_argument('--path', type=str, default=str(Path.home()), help='Directory to scan')
    parser.add_argument('--exclude', type=str, default='/System,/Library,/Applications')
    
    # Tagging
    parser.add_argument('--tag', type=str, default='sweep', help='Tag name to apply')
    parser.add_argument('--no-tag', action='store_true', help='Skip tagging')
    parser.add_argument('--clear-existing', action='store_true')
    
    # Output
    parser.add_argument('--json', type=str, help='Output JSON to file')
    parser.add_argument('--csv', type=str, help='Output CSV to file')
    parser.add_argument('--format', choices=['json', 'csv', 'summary'], default='summary')
    parser.add_argument('--quiet', action='store_true')
    
    # Utility
    parser.add_argument('--untag', type=str, help='Remove specified tag')
    parser.add_argument('--clear-all-tags', action='store_true')
    parser.add_argument('--limit', type=int, help='Process top N results')
    parser.add_argument('--dry-run', action='store_true')
    
    # General
    parser.add_argument('--version', action='version', version='sweep 1.0.0')
    
    args = parser.parse_args()

    # Check for tag CLI
    if not check_tag_installed():
        print("Error: 'tag' CLI not found. Install with: brew install tag", file=sys.stderr)
        sys.exit(3)

    # Handle utility commands
    if args.untag:
        count = remove_tags(args.untag)
        print(f"Removed tag '{args.untag}' from {count} files")
        sys.exit(0)

    if args.clear_all_tags:
        count = clear_all_sweep_tags()
        print(f"Removed {count} sweep tags")
        sys.exit(0)

    # Build config
    config = Config(
        path=Path(args.path).expanduser(),
        min_size=parse_size(args.min_size) if args.min_size else 0,
        older_than=args.older_than,
        category_filter=args.category,
        exclude=[Path(p.strip()) for p in args.exclude.split(',')],
        tag_name=args.tag,
        no_tag=args.no_tag,
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

    # Apply tags
    if not config.no_tag and results:
        tagged = apply_tags(results, config.tag_name, config.dry_run)
        if not config.quiet:
            if config.dry_run:
                print(f"\n[DRY RUN] Would tag {tagged} files with '{config.tag_name}'")
            else:
                print(f"\nTagged {tagged} files with '{config.tag_name}'")
                print("Open Finder sidebar to review tagged files.")


if __name__ ==  "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted by user", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

