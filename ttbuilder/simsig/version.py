from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Version:
    """Major.minor.build"""

    major: int
    minor: Optional[int] = None
    build: Optional[int] = None

    @property
    def text(self):
        """As string e.g. 3.11.5"""
        return ".".join(
            f"{x}" for x in (self.major, self.minor, self.build) if x is not None
        )
