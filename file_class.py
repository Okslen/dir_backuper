from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Files:
    name: str
    path: str
    mod_time: float
    attribute: Optional[int] = None  # add who file change
