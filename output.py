"""Output formatting for scan results."""

import json
import csv
from datetime import datetime
from collections import defaultdict

from utils import format_size


def output_summary(results, config):
    """Output summary to stdout."""
    if config.quiet:
        return
    
    total_size = sum(f.size for f in results)
    
    print(f"Found {len(results)} files matching criteria ({format_size(total_size)} total)")
    
    if results:
        print("\nBy category:")
        
        # Group by category
        by_category = defaultdict(list)
        for file_entry in results:
            by_category[file_entry.category].append(file_entry)
        
        # Sort by total size descending
        sorted_categories = sorted(
            by_category.items(),
            key=lambda x: sum(f.size for f in x[1]),
            reverse=True
        )
        
        for category, files in sorted_categories:
            cat_size = sum(f.size for f in files)
            print(f"  {category}: {len(files)} files ({format_size(cat_size)})")


def output_json(results, config, filepath=None):
    """Output results as JSON."""
    data = {
        "scan_date": datetime.now().isoformat(),
        "criteria": {
            "min_size": config.min_size,
            "older_than_days": config.older_than,
            "category": config.category_filter
        },
        "summary": {
            "total_files": len(results),
            "total_size": sum(f.size for f in results),
            "tagged": len(results) if not config.no_tag else 0
        },
        "files": [
            {
                "path": str(f.path),
                "size": f.size,
                "modified": f.modified.isoformat(),
                "category": f.category
            }
            for f in results
        ]
    }
    
    if filepath:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        if not config.quiet:
            print(f"JSON output written to {filepath}")
    else:
        print(json.dumps(data, indent=2))


def output_csv(results, config, filepath=None):
    """Output results as CSV."""
    import sys
    from io import StringIO
    
    output = StringIO() if not filepath else None
    
    if filepath:
        f = open(filepath, 'w', newline='')
    else:
        f = sys.stdout if not config.quiet else StringIO()
    
    writer = csv.writer(f)
    writer.writerow(['path', 'size', 'modified', 'category'])
    
    for file_entry in results:
        writer.writerow([
            str(file_entry.path),
            file_entry.size,
            file_entry.modified.isoformat(),
            file_entry.category
        ])
    
    if filepath:
        f.close()
        if not config.quiet:
            print(f"CSV output written to {filepath}")