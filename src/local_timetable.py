from dataclasses import dataclass
from lxml import etree
from elements import CajonTime, Location, PowerType
from helper import xml_escape
from train_category import TrainType


@dataclass
class TimingPoint:
    location: Location
    depart: CajonTime
    platform: str = ""
    passing: bool = False

    def xml(self):
        result = etree.Element("Trip")

        def subelem(tag, value):
            if isinstance(value, bool):
                value = 1 if value else 0
            etree.SubElement(result, tag).text = str(value)

        subelem("Location", self.location.tiploc)
        subelem("DepPassTime", self.depart.seconds)
        if self.platform:
            subelem("Platform", self.platform)
        if self.passing:
            subelem("IsPassTime", "-1")

        return result


@dataclass
class LocalTimetable:
    """Timetable for a train within a single SimSig sim

    seeding_gap_m: distance from seeding point
    """

    id: str
    uid: str
    depart_time: CajonTime
    entry_point: Location
    train_type: TrainType
    timing_points: list[TimingPoint]
    initial_power: PowerType | None = None
    description: str = "$template"
    as_required_pc: int = 50
    delay_min: int = 0
    seeding_gap_m: int = 15

    def __post_init__(self):
        if self.initial_power is None:
            self.initial_power = self.train_type.power_type

    def xml(self):
        """XML as used in SimSig WTT files"""
        result = etree.Element("Timetable")

        def subelem(tag, value):
            if isinstance(value, bool):
                value = 1 if value else 0
            etree.SubElement(result, tag).text = str(value)

        subelem("ID", self.id)
        subelem("UID", self.uid)
        subelem("AccelBrakeIndex", self.train_type.accel.value)
        subelem("AsRequiredPercent", self.as_required_pc)
        subelem("Delay", self.delay_min)
        subelem("DepartTime", self.depart_time.seconds)
        subelem("Description", xml_escape(self.description))
        subelem("SeedingGap", self.seeding_gap_m)
        subelem("EntryPoint", self.entry_point.tiploc)
        subelem("MaxSpeed", self.train_type.max_speed_mph)
        subelem("SpeedClass", self.train_type.speed_classes.value)
        subelem("TrainLength", self.train_type.length_m)
        subelem("Electrification", self.train_type.power_type.str())
        subelem("StartTraction", self.initial_power.str())
        subelem("Category", self.train_type.id)
        for elem, value in self.train_type.dwell_times.xml_values():
            subelem(elem, value)
        trips = etree.SubElement(result, "Trips")
        for tp in self.timing_points:
            trips.append(tp.xml())

        return result
