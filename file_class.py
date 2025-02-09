from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Files:
    name: str
    path: Path
    mod_time: float
