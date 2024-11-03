from dataclasses import dataclass
from enum import Enum, auto


@dataclass(frozen=True)
class TTime:
    """Timetable time"""

    class StopMode(Enum):
        """Timing point stopping mode"""

        NOT_SPECIFIED = 0
        STOPPING = auto()
        PASSING = auto()
        SET_DOWN = auto()
        IF_REQUIRED = auto()
        REQUEST_STOP = auto()
        DWELL_TIME = auto()
        THROUGH_LINE = auto()

    seconds: int = 0
    stop_mode: StopMode = StopMode.NOT_SPECIFIED

    @classmethod
    def from_hms(
        # pylint: disable=too-many-arguments
        cls,
        hours: int = 0,
        minutes: int = 0,
        seconds: int = 0,
        stop_mode: StopMode = StopMode.NOT_SPECIFIED,
    ):
        """Create time from arbitrary numbers of hours, minutes, and seconds"""
        seconds = 3600 * hours + 60 * minutes + seconds
        return cls(seconds, stop_mode)

    @classmethod
    def stopping(cls, hours: int, minutes: int, seconds: int = 0):
        """Construct stopping time from HMS"""
        return cls.from_hms(hours, minutes, seconds, cls.StopMode.STOPPING)

    @classmethod
    def passing(cls, hours: int, minutes: int, seconds: int = 0):
        """Construct passign time from HMS"""
        return cls.from_hms(hours, minutes, seconds, cls.StopMode.PASSING)

    @property
    def halfminute(self):
        """Integer number of 30-second intervals in time"""
        return self.seconds // 30

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
            half = "H" if (self.halfminute % 2) else ""
            return f"{self.halfminute // 2}{half}"
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
