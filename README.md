# Sweep

Fast, read-only filesystem analyzer that tags files with macOS Finder tags for visual review and manual deletion.

## Features

- **Read-only**: Never deletes or modifies files
- **Visual**: Uses Finder tags for easy review
- **Flexible**: Filter by size, age, and category
- **Export**: JSON and CSV output formats

## Requirements

- macOS 11+ (Big Sur or later)
- Python 3.9+
- `tag` CLI tool: `brew install tag`

## Installation

```bash
# Clone repository
git clone git@github.com:jakeferraro/sweep-cli.git
cd sweep

# Install
pip install -e .

# Or copy to PATH
chmod +x sweep.py
cp sweep.py /usr/local/bin/sweep
```

## Usage

### Basic Examples

Find files over 500MB older than 1 year:
```bash
sweep --min-size 500M --older-than 365d
```

Find old disk images:
```bash
sweep --category disk_image --older-than 180d
```

Find large video files:
```bash
sweep --category video --min-size 2G
```

### Custom Tagging

Use custom tag name:
```bash
sweep --min-size 1G --tag "LargeFiles2024"
```

Tag without terminal output:
```bash
sweep --min-size 500M --older-than 730d --quiet
```

### Data Export

Generate JSON for scripting:
```bash
sweep --min-size 100M --json results.json
```

Generate CSV for Excel:
```bash
sweep --older-than 365d --csv report.csv --no-tag
```

### Cleanup

Remove tags after review:
```bash
sweep --untag "sweep"
```

Remove all sweep tags:
```bash
sweep --clear-all-tags
```

### Dry Run

Preview what would be tagged:
```bash
sweep --min-size 1G --older-than 365d --dry-run
```

## Command-Line Options

### File Selection
- `--min-size <size>` - Minimum file size (e.g., 100M, 1G, 500K)
- `--older-than <days>` - Files not modified in N days
- `--category <type>` - Filter by: archive, disk_image, video, cache, log
- `--path <directory>` - Start scan from directory (default: ~)
- `--exclude <dirs>` - Comma-separated dirs to skip

### Tagging
- `--tag <name>` - Tag name to apply (default: "sweep")
- `--no-tag` - Skip tagging, only output data
- `--clear-existing` - Remove existing tags before applying new ones

### Output
- `--json <file>` - Output results as JSON
- `--csv <file>` - Output results as CSV
- `--format <type>` - Output format: json, csv, summary (default: summary)
- `--quiet` - Suppress terminal output except errors

### Utility
- `--untag <name>` - Remove specified tag from all files
- `--clear-all-tags` - Remove all "sweep*" tags from filesystem
- `--limit <n>` - Only process top N results (by size)
- `--dry-run` - Show what would be tagged without tagging

### General
- `--version` - Show version
- `--help` - Show help message

## File Categories

Categories are determined by file extension only:

- **archive**: .zip, .tar, .gz, .bz2, .7z, .rar, .tgz, .tar.gz
- **disk_image**: .dmg, .iso, .img, .vdi, .vmdk
- **video**: .mp4, .mov, .avi, .mkv, .m4v, .flv
- **cache**: node_modules/*, .cache/*, __pycache__/*, .venv/*, venv/*
- **log**: .log, .out (when in logs/, var/, tmp/ directories)
- **other**: everything else

