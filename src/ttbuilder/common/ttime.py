from dataclasses import asdict, dataclass
from enum import Enum, auto


class StopMode(Enum):
    """Timing point stopping mode"""

    NOT_DEFINED = 0
    STOPPING = auto()
    PASSING = auto()
    SET_DOWN = auto()
    IF_REQUIRED = auto()
    REQUEST_STOP = auto()
    DWELL_TIME = auto()
    THROUGH_LINE = auto()


@dataclass(frozen=True)
class TTime:
    """Timetable time"""

    seconds: int = 0
    stop_mode: StopMode = StopMode.NOT_DEFINED

    @classmethod
    def from_hms(
        # pylint: disable=too-many-arguments
        cls,
        hours: int = 0,
        minutes: int = 0,
        seconds: int = 0,
    ):
        """Create time from arbitrary numbers of hours, minutes, and seconds"""
        seconds = 3600 * hours + 60 * minutes + seconds
        return cls(seconds)

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
        sep = "/" if self.stop_mode == StopMode.PASSING else ":"
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

    def __eq__(self, other):
        """Permit comparison by value between base and subclass"""
        if not isinstance(self, other.__class__):
            return False
        return asdict(self) == asdict(other)


# pylint: disable=too-few-public-methods


class Stopping(TTime):
    """Train stops at this location"""

    def __init__(self, seconds: int):
        super().__init__(seconds=seconds, stop_mode=StopMode.STOPPING)


class Passing(TTime):
    """Train passes this location non-stop"""

    def __init__(self, seconds: int):
        super().__init__(seconds=seconds, stop_mode=StopMode.PASSING)


class SetDown(TTime):
    """Train stops only to set down passengers/crew"""

    def __init__(self, seconds: int):
        super().__init__(seconds=seconds, stop_mode=StopMode.SET_DOWN)


class IfRequired(TTime):
    """Train stops only if required"""

    def __init__(self, seconds: int):
        super().__init__(seconds=seconds, stop_mode=StopMode.IF_REQUIRED)


class RequestStop(TTime):
    """Train stops only on passenger request"""

    def __init__(self, seconds: int):
        super().__init__(seconds=seconds, stop_mode=StopMode.REQUEST_STOP)


class DwellTime(TTime):
    """Train stops and waits a minimum specified time"""

    def __init__(self, seconds: int):
        super().__init__(seconds=seconds, stop_mode=StopMode.DWELL_TIME)


class ThroughLine(TTime):
    """Train may stop at a non-platform line"""

    def __init__(self, seconds: int):
        super().__init__(seconds=seconds, stop_mode=StopMode.THROUGH_LINE)
