# Sweep

Fast filesystem analyzer with native macOS GUI for reviewing and managing files.

## Features

- **GUI Interface**: Native PyQt6 interface for visual file management
- **Interactive**: Sort, search, and filter files in real-time
- **Safe Operations**: Move to trash (reversible), never permanent delete
- **Finder Integration**: Open files, show in Finder, reveal locations
- **Flexible**: Filter by size, age, and category
- **Export**: JSON and CSV output formats

## Requirements

- macOS 11+ (Big Sur or later)
- Python 3.9+
- PyQt6 (for GUI): `pip install PyQt6`

## Installation

```bash
# Clone repository
git clone git@github.com:jakeferraro/sweep-cli.git
cd sweep-cli

# Install dependencies
pip install -r requirements.txt

# Install sweep
pip install -e .

# Or copy to PATH (CLI only, no GUI)
chmod +x sweep.py
cp sweep.py /usr/local/bin/sweep
```

## Usage

### GUI Mode (Default)

By default, Sweep launches a native macOS GUI after scanning:

```bash
# Find files over 500MB - GUI opens automatically
sweep --min-size 500M --older-than 365d

# Find old disk images - review in GUI
sweep --category disk_image --older-than 180d

# Find large video files - interactive management
sweep --category video --min-size 2G
```

**GUI Features:**
- **Sortable columns**: Click headers to sort by Name, Size, Kind, or Date
- **Search box**: Real-time filtering by filename
- **Multi-select**: Cmd+Click or Shift+Click to select multiple files
- **Double-click**: Open files with default application
- **Right-click menu**: Open, Show in Finder, Copy Path, Move to Trash
- **Keyboard shortcuts**:
  - `Cmd+W` - Close window
  - `Cmd+F` - Focus search
  - `Delete/Backspace` - Move selected files to trash
- **Move to Trash**: Safe, reversible file removal (not permanent delete)

### CLI-Only Mode

Use `--no-gui` to skip the GUI and use CLI output only:

```bash
sweep --min-size 500M --older-than 365d --no-gui
```

### Data Export

Generate JSON for scripting:
```bash
sweep --min-size 100M --json results.json
```

Generate CSV for Excel:
```bash
sweep --older-than 365d --csv report.csv
```

## Command-Line Options

### File Selection
- `--min-size <size>` - Minimum file size (e.g., 100M, 1G, 500K)
- `--older-than <days>` - Files not modified in N days
- `--category <type>` - Filter by: archive, disk_image, video, cache, log
- `--path <directory>` - Start scan from directory (default: ~)
- `--exclude <dirs>` - Comma-separated dirs to skip

### Output
- `--json <file>` - Output results as JSON
- `--csv <file>` - Output results as CSV
- `--format <type>` - Output format: json, csv, summary (default: summary)
- `--quiet` - Suppress terminal output except errors
- `--no-gui` - Skip GUI and use CLI output only

### Utility
- `--limit <n>` - Only process top N results (by size)

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

