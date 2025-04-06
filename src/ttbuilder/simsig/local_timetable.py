from dataclasses import dataclass, field
from lxml import etree

from ttbuilder.common.location import Location
from ttbuilder.common.str_helper import xml_escape
from ttbuilder.common.timing_point import TimingPoint
from ttbuilder.common.train_id import TrainId
from ttbuilder.common.ttime import TTime
from ttbuilder.train.power_type import PowerType
from ttbuilder.train.train_category import TrainCategory


@dataclass
class LocalTimetable:
    """Timetable for a train within a single SimSig sim

    seeding_gap_m: distance from seeding point
    """

    # pylint: disable=too-many-instance-attributes
    train_id: TrainId
    train_type: TrainCategory
    timing_points: list[TimingPoint] = field(default_factory=list)
    entry_point: Location | None = None
    depart_time: TTime | None = None
    initial_power: PowerType | None = None
    description: str = "$template"
    as_required_pc: int = 50
    delay_min: int | None = None
    seeding_gap_m: int = 15

    origin: Location | None = None
    origin_dep: TTime | None = None
    destination: Location | None = None
    destination_arr: TTime | None = None
    notes: str | None = None

    def __post_init__(self):
        if self.initial_power is None and isinstance(self.train_type, TrainCategory):
            for pt in PowerType:
                if pt & self.train_type.power_type:
                    self.initial_power = pt
                    break

    @classmethod
    def from_xml(cls, xml_root):
        """Read relevant bits from the XML within a .WTT or .SSG file"""

        def findtext(match, default=""):
            return xml_root.findtext(match, default=default)

        def findtime(match):
            t = findtext(match)
            return TTime(int(t)) if t else None

        return cls(
            train_id=TrainId(findtext("ID"), findtext("UID")),
            train_type=TrainCategory(),
            timing_points=[TimingPoint.from_xml(x) for x in xml_root.find("Trips")],
            entry_point=Location(tiploc=findtext("EntryPoint")) or None,
            depart_time=findtime("DepartTime"),
            # initial_power
            description=findtext("Description"),
            # as_required_pc
            # delay_min
            # seeding_gap_m
            origin=findtext("OriginName"),
            origin_dep=findtime("OriginTime"),
            destination=findtext("DestinationName"),
            destination_arr=findtime("DestinationTime"),
            notes=findtext("Notes"),
        )

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
        subelem("Electrification", self.train_type.power_type.xml_value)
        subelem("StartTraction", self.initial_power.xml_value)
        subelem("Category", self.train_type.id)
        for elem, value in self.train_type.dwell_times.xml_values():
            subelem(elem, value)
        trips = etree.SubElement(result, "Trips")
        for tp in self.timing_points:
            trips.append(tp.xml())

        return result
