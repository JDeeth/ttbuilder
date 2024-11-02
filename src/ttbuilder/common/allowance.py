from dataclasses import dataclass
from enum import Enum

from ttbuilder.common.ttime import TTime

# pylint: disable=too-few-public-methods


class Type(Enum):
    """Allowance type"""

    ENGINEERING = "[x]"
    PATHING = "(x)"
    PERFORMANCE = "<x>"


@dataclass(frozen=True)
class BaseAllowance:
    """Timetable allowance times"""

    time: TTime
    type: Type


class Engineering(BaseAllowance):
    """Engineering allowance"""

    def __init__(self, time: TTime):
        super().__init__(time=time, type=Type.ENGINEERING)


class Pathing(BaseAllowance):
    """Pathing allowance"""

    def __init__(self, time: TTime):
        super().__init__(time=time, type=Type.PATHING)


class Performance(BaseAllowance):
    """Performance allowance"""

    def __init__(self, time: TTime):
        super().__init__(time=time, type=Type.PERFORMANCE)
