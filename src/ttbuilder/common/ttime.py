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

    @property
    def thirty_sec(self):
        """Duration in multiples of 30 seconds"""
        return self.minute * 2 + (1 if self.halfmin else 0)

    def __bool__(self):
        return self.minute > 0 or self.halfmin


@dataclass(frozen=True)
class Allowance:
    """Timetable allowance times"""

    # pylint: disable=missing-function-docstring

    class Type(Enum):
        """Allowance type"""

        ENGINEERING = "[x]"
        PATHING = "(x)"
        PERFORMANCE = "<x>"

    time: TMin
    type: Type

    @classmethod
    def engineering(cls, time: TMin):
        return cls(time, cls.Type.ENGINEERING)

    @classmethod
    def pathing(cls, time: TMin):
        return cls(time, cls.Type.PATHING)

    @classmethod
    def performance(cls, time: TMin):
        return cls(time, cls.Type.PERFORMANCE)


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
        # pylint: disable=too-many-arguments
        cls,
        hours: int = 0,
        minutes: int = 0,
        seconds: int = 0,
        passing: bool = False,
        stop_mode=StopMode.STOPPING,
        allowances=None,
    ):
        """Create time from arbitrary numbers of hours, minutes, and seconds"""
        seconds = 3600 * hours + 60 * minutes + seconds
        if passing is True:
            stop_mode = cls.StopMode.PASSING
        if allowances is None:
            allowances = []
        return cls(seconds, stop_mode, allowances)

    @classmethod
    def from_tmin(cls, tmin: TMin):
        """Create time from TMin

        TMin perhaps should be folded into TTime"""
        return cls(seconds=tmin.minute * 60 + tmin.second)

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
