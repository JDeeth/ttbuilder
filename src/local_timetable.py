from dataclasses import dataclass, field
from lxml import etree
from elements import CajonTime, Location, PowerType, TrainId
from helper import xml_escape
from train_category import TrainType

from timing_point import TimingPoint


@dataclass
class LocalTimetable:
    """Timetable for a train within a single SimSig sim

    seeding_gap_m: distance from seeding point
    """

    train_id: TrainId
    train_type: TrainType
    timing_points: list[TimingPoint] = field(default_factory=list)
    entry_point: Location | None = None
    depart_time: CajonTime | None = None
    initial_power: PowerType | None = None
    description: str = "$template"
    as_required_pc: int = 50
    delay_min: int | None = None
    seeding_gap_m: int = 15

    def __post_init__(self):
        if self.initial_power is None:
            for pt in PowerType:
                if pt & self.train_type.power_type:
                    self.initial_power = pt
                    break

    def xml(self):
        """XML as used in SimSig WTT files"""
        result = etree.Element("Timetable")

        def subelem(tag, value):
            if isinstance(value, bool):
                value = 1 if value else 0
            etree.SubElement(result, tag).text = str(value)

        subelem("ID", self.train_id.id)
        if self.train_id.uid:
            subelem("UID", self.train_id.uid)
        subelem("AccelBrakeIndex", self.train_type.accel.value)
        subelem("AsRequiredPercent", self.as_required_pc)
        if self.delay_min is not None:
            subelem("Delay", self.delay_min)
        if self.depart_time is not None:
            subelem("DepartTime", self.depart_time.seconds)
        subelem("Description", xml_escape(self.description))
        subelem("SeedingGap", self.seeding_gap_m)
        if self.entry_point is not None:
            subelem("EntryPoint", self.entry_point.tiploc)
        subelem("MaxSpeed", self.train_type.max_speed_mph)
        subelem("SpeedClass", self.train_type.speed_classes.value)
        subelem("TrainLength", self.train_type.length_m)
        subelem("Electrification", self.train_type.power_type.xml_value())
        subelem("StartTraction", self.initial_power.xml_value())
        subelem("Category", self.train_type.id)
        for elem, value in self.train_type.dwell_times.xml_values():
            subelem(elem, value)
        trips = etree.SubElement(result, "Trips")
        for tp in self.timing_points:
            trips.append(tp.xml())

        return result
