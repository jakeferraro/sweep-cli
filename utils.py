"""Utility functions for size parsing and formatting."""


def parse_size(size_str):
    """
    Parse size string like '100M', '1G', '500K' to bytes.
    
    Returns: int (bytes)
    """
    size_str = size_str.strip().upper()
    
    multipliers = {
        'K': 1024,
        'M': 1024 ** 2,
        'G': 1024 ** 3,
        'T': 1024 ** 4
    }
    
    if size_str[-1] in multipliers:
        number = float(size_str[:-1])
        multiplier = multipliers[size_str[-1]]
        return int(number * multiplier)
    
    # Assume bytes if no suffix
    return int(size_str)


def format_size(bytes_val):
    """Format bytes as human-readable string."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_val < 1024.0:
            return f"{bytes_val:.1f} {unit}"
        bytes_val /= 1024.0
    return f"{bytes_val:.1f} PB"