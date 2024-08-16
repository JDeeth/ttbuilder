from dataclasses import dataclass, field
from lxml import etree
from elements import CajonTime, Location, PowerType
from helper import xml_escape
from train_category import TrainType


@dataclass
class Activity:
    """this will need expanding on"""

    next_uid: str

    def xml(self):
        result = etree.Element("Activity")
        etree.SubElement(result, "Activity").text = "0"
        etree.SubElement(result, "AssociatedUID").text = self.next_uid
        return result


@dataclass
class TimingPoint:
    location: Location
    depart: CajonTime | None = None
    platform: str = ""
    passing: bool = False
    activities: list[Activity] = field(default_factory=list)

    def xml(self):
        result = etree.Element("Trip")

        def subelem(tag, value):
            if isinstance(value, bool):
                value = 1 if value else 0
            etree.SubElement(result, tag).text = str(value)

        subelem("Location", self.location.tiploc)
        if self.depart is not None:
            subelem("DepPassTime", self.depart.seconds)
        if self.platform:
            subelem("Platform", self.platform)
        if self.passing:
            subelem("IsPassTime", "-1")
        if self.activities:
            acts = etree.SubElement(result, "Activities")
            for a in self.activities:
                acts.append(a.xml())

        return result


@dataclass
class LocalTimetable:
    """Timetable for a train within a single SimSig sim

    seeding_gap_m: distance from seeding point
    """

    id: str
    uid: str
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

        subelem("ID", self.id)
        subelem("UID", self.uid)
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
        subelem("Electrification", self.train_type.power_type.str())
        subelem("StartTraction", self.initial_power.str())
        subelem("Category", self.train_type.id)
        for elem, value in self.train_type.dwell_times.xml_values():
            subelem(elem, value)
        trips = etree.SubElement(result, "Trips")
        for tp in self.timing_points:
            trips.append(tp.xml())

        return result