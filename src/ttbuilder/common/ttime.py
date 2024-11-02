from dataclasses import dataclass
from enum import Enum, auto


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

    @classmethod
    def from_hms(
        # pylint: disable=too-many-arguments
        cls,
        hours: int = 0,
        minutes: int = 0,
        seconds: int = 0,
        stop_mode=StopMode.STOPPING,
    ):
        """Create time from arbitrary numbers of hours, minutes, and seconds"""
        seconds = 3600 * hours + 60 * minutes + seconds
        return cls(seconds, stop_mode)

    @property
    def halfminute(self):
        s = int(self.seconds)
        return s // 30

    def __str__(self):
        """To timetable format e.g. 20:45H, 03/20"""
        s = int(self.seconds)
        h = s // 3600
        m = (s // 60) % 60
        s = s % 60
        sep = "/" if self.stop_mode == self.StopMode.PASSING else ":"
        half = "H" if s >= 30 else ""
        return f"{h:02}{sep}{m:02}{half}"

    def __format__(self, spec):
        """Spec MH for minutes+halfminutes, else timetable format"""
        if spec == "MH":
            m = self.halfminute // 2
            half = "H" if (self.halfminute % 2) else ""
            return f"{m}{half}"
        return self.__str__()

    def __bool__(self):
        return self.seconds != 0


@dataclass(frozen=True)
class Allowance:
    """Timetable allowance times"""

    # pylint: disable=missing-function-docstring

    class Type(Enum):
        """Allowance type"""

        ENGINEERING = "[x]"
        PATHING = "(x)"
        PERFORMANCE = "<x>"

    time: TTime
    type: Type

    @classmethod
    def engineering(cls, time: TTime):
        return cls(time, cls.Type.ENGINEERING)

    @classmethod
    def pathing(cls, time: TTime):
        return cls(time, cls.Type.PATHING)

    @classmethod
    def performance(cls, time: TTime):
        return cls(time, cls.Type.PERFORMANCE)
