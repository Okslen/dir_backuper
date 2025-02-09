from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Files:
    path: Path
    mod_time: float
