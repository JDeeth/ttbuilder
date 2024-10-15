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
    passing: bool = False

    @classmethod
    def from_hms(
        cls, hours: int = 0, minutes: int = 0, seconds: int = 0, passing: bool = False
    ):
        seconds = 3600 * hours + 60 * minutes + seconds
        return cls(seconds, passing)

    @classmethod
    def from_str(cls, text: str):
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
        s = int(self.seconds)
        h = s // 3600
        m = (s // 60) % 60
        s = s % 60
        sep = "/" if self.passing else ":"
        half = "H" if s >= 30 else ""
        return f"{h:02}{sep}{m:02}{half}"

    def __format__(self, spec):
        if spec == "MH":
            m = self.seconds // 60
            half = "H" if (self.seconds % 60) >= 30 else ""
            return f"{m}{half}"
        return self.__str__()

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
            result.text = self.uid.upper()
            return result
        else:
            result = etree.Element("AssociatedTrain")
            result.text = self.id.upper()
            return result
