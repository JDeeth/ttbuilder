from enum import Enum, Flag, auto
from dataclasses import dataclass, fields
import secrets
from lxml import etree

from cajontime import CajonTime
from helper import pascal_case


@dataclass
class DwellTimes:
    """Collection of dwell times for a SimSig train category"""

    red_signal_move_off: CajonTime = CajonTime(0)
    station_forward: CajonTime = CajonTime(0)
    station_reverse: CajonTime = CajonTime(0)
    terminate_forward: CajonTime = CajonTime(0)
    terminate_reverse: CajonTime = CajonTime(0)
    join: CajonTime = CajonTime(0)
    divide: CajonTime = CajonTime(0)
    crew_change: CajonTime = CajonTime(0)

    def __post_init__(self):
        """Assume plain-int values are seconds and convert"""
        for field in fields(self):
            value = getattr(self, field.name)
            if isinstance(value, int):
                setattr(self, field.name, CajonTime(value))

    def xml(self):
        """Returns data in XML format"""
        result = etree.Element("DwellTimes")
        for field in fields(self):
            time = getattr(self, field.name)
            text = str(time.seconds)
            etree.SubElement(result, pascal_case(field.name)).text = text

        return result


class AccelBrake(Enum):
    """SimSig train acceleration/braking categories"""

    VERY_LOW = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    VERY_HIGH = 4


class PowerType(Flag):
    """SimSig traction power categories

    Combine with |"""

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
        if self not in (PowerType.NONE, PowerType.DIESEL):
            raise NotImplementedError()
        result = ""
        if self & PowerType.DIESEL:
            result += "D"
        return result


class SpeedClass(Flag):
    """SimSig speed restriction/easement categories

    Combine with |"""

    EPS_E = 2**0
    EPS_D = 2**1
    HST = 2**2
    EMU = 2**3
    DMU = 2**4
    SP = 2**5
    CS_67 = 2**6
    MGR = 2**7
    TGV_373 = 2**8
    LOCO_H = 2**9
    METRO = 2**10
    WES_442 = 2**11
    TRIPCOCK = 2**12
    STEAM = 2**13
    SIM_1 = 2**14
    SIM_2 = 2**15
    SIM_3 = 2**16
    SIM_4 = 2**17


Mph = int
Meters = int


class Weight(Enum):
    """SimSig train weight"""

    LIGHT = None
    NORMAL = 0
    HEAVY = None


@dataclass
class TrainType:
    """SimSig train category as represented in timetable files"""

    description: str = ""
    length: Meters = 0
    max_speed: Mph = 0

    id: str = None

    accel: AccelBrake = AccelBrake.MEDIUM
    weight: Weight = Weight.NORMAL
    defensive_driving: None = None

    power_type: PowerType = PowerType(0)
    speed_classes: SpeedClass = SpeedClass(0)

    use_freight_linespeeds: bool = False
    can_use_freight_lines: bool = False

    dwell_times: DwellTimes = DwellTimes()

    def __post_init__(self):
        if self.id is None:
            self.id = secrets.token_hex(4)

    def xml(self):
        """XML as used in SimSig timetables"""
        result = etree.Element("TrainCategory", ID=self.id)

        def subelem(tag, value):
            if isinstance(value, bool):
                value = 1 if value else 0
            etree.SubElement(result, tag).text = str(value)

        subelem("Description", self.description)
        subelem("AccelBrakeIndex", self.accel.value)
        subelem("IsFreight", self.use_freight_linespeeds)
        subelem("CanUseGoodsLines", self.can_use_freight_lines)
        subelem("MaxSpeed", self.max_speed)
        subelem("TrainLength", self.length)
        subelem("SpeedClass", self.speed_classes.value)
        subelem("PowerToWeightCategory", self.weight.value)
        result.append(self.dwell_times.xml())
        subelem("Electrification", self.power_type.str())

        return result
