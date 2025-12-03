"""Configuration dataclass"""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional, List


@dataclass
class Config:
    """Configuration for sweep scan."""
    path: Path
    min_size: int
    older_than: Optional[int]
    category_filter: Optional[str]
    exclude: List[Path]
    limit: Optional[int]
    quiet: bool