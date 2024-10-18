from dataclasses import dataclass, field
import secrets
from lxml import etree

from ..common.str_helper import xml_escape
from ..train.accel_brake import AccelBrake
from ..train.dwell_times import DwellTimes
from ..train.power_type import PowerType
from ..train.speed_class import SpeedClass
from ..train.weight import Weight


@dataclass
class TrainCategory:
    """SimSig train category as represented in timetable files"""

    # pylint: disable=too-many-instance-attributes

    description: str = ""
    length_m: int = 0
    max_speed_mph: int = 0

    id: str = None

    accel: AccelBrake = AccelBrake.MEDIUM
    weight: Weight = Weight.NORMAL
    defensive_driving: None = None

    power_type: PowerType = PowerType(0)
    speed_classes: SpeedClass = SpeedClass(0)

    use_freight_linespeeds: bool = False
    can_use_freight_lines: bool = False

    dwell_times: DwellTimes = field(default_factory=DwellTimes)

    def __post_init__(self):
        if self.id is None:
            self.id = secrets.token_hex(4)

    def xml(self):
        """XML as used in SimSig .WTT"""
        result = etree.Element("TrainCategory", ID=self.id)

        def subelem(tag, value):
            if isinstance(value, bool):
                value = 1 if value else 0
            etree.SubElement(result, tag).text = str(value)

        subelem("Description", xml_escape(self.description))
        subelem("AccelBrakeIndex", self.accel.xml_value)
        subelem("IsFreight", self.use_freight_linespeeds)
        subelem("CanUseGoodsLines", self.can_use_freight_lines)
        subelem("MaxSpeed", self.max_speed_mph)
        subelem("TrainLength", self.length_m)
        subelem("SpeedClass", self.speed_classes.xml_value)
        subelem("PowerToWeightCategory", self.weight.xml_value)
        result.append(self.dwell_times.xml())
        if self.power_type != PowerType.NONE:
            subelem("Electrification", self.power_type.xml_value())

        return result

    @classmethod
    def from_str(cls, text):
        """Construct train type from text"""
        params = {}
        lines = text.strip().splitlines()
        params["description"] = lines[0]
        line2: list[str] = [x.strip() for x in lines[1].split(",")]
        for s in line2:
            if s[:-1].isnumeric() and s.endswith("m"):
                params["length_m"] = int(s[:-1])
            if s[:-3].isnumeric() and s.endswith("mph"):
                params["max_speed_mph"] = int(s[:-3])
            if s.upper() in PowerType.__members__:
                pt = params.get("power_type", PowerType.NONE)
                pt |= PowerType[s.upper()]
                params["power_type"] = pt
        line3 = lines[2] if len(lines) > 2 else ""
        _, _, dwell_times = line3.upper().partition("DWELL TIMES")
        if dwell_times:
            dwell_times = [x.strip() for x in dwell_times.split(",")]
            dwell_times = [x.rpartition(":") for x in dwell_times]
            dwell_times = [int(m or 0) * 60 + int(s) for m, _, s in dwell_times]
            params["dwell_times"] = DwellTimes(*dwell_times)

        return cls(**params)
