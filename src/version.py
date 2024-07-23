from dataclasses import dataclass
from typing import Optional


@dataclass
class Version:
    major: int
    minor: Optional[int] = None
    build: Optional[int] = None

    @property
    def text(self):
        return ".".join(
            f"{x}" for x in (self.major, self.minor, self.build) if x is not None
        )
