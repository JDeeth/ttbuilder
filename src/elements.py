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

    @property
    def xml_value(self):
        return self.value


class PowerType(Flag):
    """SimSig traction power categories

    Can be combined e.g. PowerType.DC_3RAIL | PowerType.AC_OVERHEAD"""

    NONE = 0
    AC_OVERHEAD = auto(), "O"
    DC_3RAIL = auto(), "3"
    DC_4RAIL = auto(), "4"
    DIESEL = auto(), "D"
    DC_OVERHEAD = auto(), "V"
    TRAMWAY = auto(), "T"
    SIM_1 = auto(), "X1"
    SIM_2 = auto(), "X2"
    SIM_3 = auto(), "X3"
    SIM_4 = auto(), "X4"

    def __new__(cls, flag, xml_code=""):
        obj = object.__new__(cls)
        obj._value_ = flag
        obj._xml_code = xml_code
        return obj

    def xml_value(self):
        return "".join(pt._xml_code for pt in PowerType if pt & self)


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
