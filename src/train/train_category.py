from dataclasses import dataclass, field
import secrets
from lxml import etree

from common import xml_escape
from .accel_brake import AccelBrake
from .dwell_times import DwellTimes
from .power_type import PowerType
from .speed_class import SpeedClass
from .weight import Weight


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
