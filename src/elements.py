from dataclasses import dataclass
from enum import Enum, Flag, auto
from typing import Optional
from lxml import etree


@dataclass(frozen=True)
class Location:
    tiploc: str


@dataclass(frozen=True)
class CajonTime:
    seconds: int = 0

    @classmethod
    def from_hms(cls, hours: int = 0, minutes: int = 0, seconds: int = 0):
        return cls(seconds=seconds + 60 * minutes + 3600 * hours)

    @classmethod
    def from_str(cls, text):
        text = text.split(":")
        text.extend(("0", "0", "0"))
        h, m, s, *_ = (int(x) for x in text if x.isdigit())
        return cls.from_hms(h, m, s)

    def __bool__(self):
        return self.seconds != 0


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


class AccelBrake(Enum):
    """SimSig train acceleration/braking categories"""

    VERY_LOW = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    VERY_HIGH = 4


class PowerType(Flag):
    """SimSig traction power categories

    Can be combined e.g. PowerType.DC_3RAIL | PowerType.AC_OVERHEAD"""

    NONE = 0
    AC_OVERHEAD = auto()
    DC_3RAIL = auto()
    DC_4RAIL = auto()
    DIESEL = auto()
    DC_OVERHEAD = auto()
    TRAMWAY = auto()
    SIM_1 = auto()
    SIM_2 = auto()
    SIM_3 = auto()
    SIM_4 = auto()

    def str(self):
        """Format as in timetable XML"""
        powertype_str = {
            PowerType.AC_OVERHEAD: "O",
            PowerType.DC_3RAIL: "3",
            PowerType.DC_4RAIL: "4",
            PowerType.DIESEL: "D",
            PowerType.DC_OVERHEAD: "V",
            PowerType.TRAMWAY: "T",
            PowerType.SIM_1: "X1",
            PowerType.SIM_2: "X2",
            PowerType.SIM_3: "X3",
            PowerType.SIM_4: "X4",
        }

        return "".join(s for pt, s in powertype_str.items() if pt & self)


@dataclass
class TrainId:
    id: str
    uid: str = ""

    def activity_xml(self):
        if self.uid:
            result = etree.Element("AssociatedUID")
            result.text = self.uid
            return result
        else:
            result = etree.Element("AssociatedTrain")
            result.text = self.id
            return result
