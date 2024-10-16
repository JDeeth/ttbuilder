from dataclasses import dataclass


@dataclass(frozen=True)
class Location:
    """A timetable location"""

    tiploc: str
