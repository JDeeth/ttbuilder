from dataclasses import dataclass
import string
from typing import Optional


@dataclass(frozen=True)
class Version:
    major: int
    minor: Optional[int] = None
    build: Optional[int] = None

    @property
    def text(self):
        return ".".join(
            f"{x}" for x in (self.major, self.minor, self.build) if x is not None
        )


def xml_escape(text: str) -> str:
    escape = {
        "<": "&lt;",
        ">": "&gt;",
        "&": "&amp;",
        "'": "&apos;",
        '"': "&quot;",
    }

    def escape_chr(c):
        if c in escape:
            return escape[c]
        elif ord(c) > 127:
            return f"&#x{ord(c):04X};"
        else:
            return c

    return "".join(escape_chr(c) for c in text)


def pascal_case(snakecase: str):
    return string.capwords(snakecase, sep="_").replace("_", "")
