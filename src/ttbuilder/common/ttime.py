from dataclasses import dataclass, field
from enum import Enum, auto


@dataclass(frozen=True)
class TMin:
    """Minutes to the halfminute"""

    minute: int = 0
    halfmin: bool = False

    @property
    def second(self):
        """0 or 30 seconds"""
        return 30 if self.halfmin else 0


@dataclass(frozen=True)
class Allowance:
    """Timetable allowance times"""

    class Type(Enum):
        ENGINEERING = auto()
        PATHING = auto()
        PERFORMANCE = auto()

    time: TMin
    type: Type


@dataclass(frozen=True)
class TTime:
    """Timetable time"""

    class StopMode(Enum):
        """Timing point stopping mode"""

        STOPPING = auto()
        PASSING = auto()
        SET_DOWN = auto()
        IF_REQUIRED = auto()
        REQUEST_STOP = auto()
        DWELL_TIME = auto()
        THROUGH_LINE = auto()

    seconds: int = 0
    stop_mode: StopMode = StopMode.STOPPING

    allowances: list[Allowance] = field(default_factory=list)

    @property
    def passing(self):
        """Temp function to be deprecated"""
        return self.stop_mode == self.StopMode.PASSING

    @classmethod
    def from_hms(
        cls, hours: int = 0, minutes: int = 0, seconds: int = 0, passing: bool = False
    ):
        """Create time from arbitrary numbers of hours, minutes, and seconds"""
        seconds = 3600 * hours + 60 * minutes + seconds
        stop_mode = cls.StopMode.PASSING if passing else cls.StopMode.STOPPING
        return cls(seconds, stop_mode)

    @classmethod
    def from_str(cls, text: str):
        """HH:MM stopping, HH/MM passing, suffix H for +30sec"""
        ends_with_h = text.endswith("H")
        if ends_with_h:
            text = text[:-1]
        passing = "/" in text
        if passing:
            text = text.replace("/", ":")
        text = text.split(":")
        text.extend(("0", "0", "0"))
        h, m, s, *_ = (int(x) for x in text if x.isdigit())
        if ends_with_h:
            s += 30
        return cls.from_hms(h, m, s, passing)

    def __str__(self):
        """To timetable format e.g. 20:45H, 03/20"""
        s = int(self.seconds)
        h = s // 3600
        m = (s // 60) % 60
        s = s % 60
        sep = "/" if self.passing else ":"
        half = "H" if s >= 30 else ""
        return f"{h:02}{sep}{m:02}{half}"

    def __format__(self, spec):
        """Spec MH for minutes+halfminutes, else timetable format"""
        if spec == "MH":
            m = self.seconds // 60
            half = "H" if (self.seconds % 60) >= 30 else ""
            return f"{m}{half}"
        return self.__str__()

    def __bool__(self):
        return self.seconds != 0
