from dataclasses import dataclass, field
from lxml import etree
from activity import Activity
from elements import CajonTime, Location, PowerType, TrainId
from helper import xml_escape
from train_category import TrainType


@dataclass
class TimingPoint:
    location: Location | str
    depart: CajonTime | str | None = None
    platform: str = ""
    activities: list[Activity] = field(default_factory=list)
    engineering_allowance: CajonTime = field(default_factory=CajonTime)
    performance_allowance: CajonTime = field(default_factory=CajonTime)
    pathing_allowance: CajonTime = field(default_factory=CajonTime)
    request_stop_percent: int = 100

    def __post_init__(self):
        if isinstance(self.location, str):
            self.location = Location(tiploc=self.location)
        if isinstance(self.depart, str):
            self.depart = CajonTime.from_str(self.depart)

    @classmethod
    def from_str(cls, text):
        elem = text.split()
        tiploc, _, platform = elem[0].partition(".")
        location = Location(tiploc=tiploc)
        depart_str: str = elem[1]
        depart = CajonTime.from_str(depart_str)
        return cls(location=location, depart=depart, platform=platform)

    def __str__(self):
        location = self.location.tiploc
        if self.platform:
            location += f".{self.platform}"
        rem = []
        if self.engineering_allowance:
            rem.append(f"[{self.engineering_allowance:MH}]")
        if self.pathing_allowance:
            rem.append(f"({self.pathing_allowance:MH})")
        if self.performance_allowance:
            rem.append(f"<{self.performance_allowance:MH}>")
        rem.extend(str(act) for act in self.activities)
        rem = " ".join(x for x in rem if x)
        return f"{location:10} {self.depart:6} {rem}".strip()

    def xml(self):
        result = etree.Element("Trip")

        def subelem(tag, value):
            if isinstance(value, bool):
                value = 1 if value else 0
            etree.SubElement(result, tag).text = str(value)

        subelem("Location", self.location.tiploc)
        if self.depart is not None:
            subelem("DepPassTime", self.depart.seconds)
            if self.depart.passing:
                subelem("IsPassTime", "-1")
        if self.platform:
            subelem("Platform", self.platform)
        if self.activities:
            acts = etree.SubElement(result, "Activities")
            for a in self.activities:
                acts.append(a.xml())
        # allowances are recorded as multiples of 30 seconds
        eng_perf_allowance = (
            self.engineering_allowance.seconds + self.performance_allowance.seconds
        )
        if eng_perf_allowance:
            subelem("EngAllowance", eng_perf_allowance // 30)
        if self.pathing_allowance:
            subelem("PathAllowance", self.pathing_allowance.seconds // 30)
        if self.request_stop_percent in range(0, 100):  # excludes 100%
            subelem("RequestPercent", self.request_stop_percent)

        return result


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
        subelem("Electrification", self.train_type.power_type.str())
        subelem("StartTraction", self.initial_power.str())
        subelem("Category", self.train_type.id)
        for elem, value in self.train_type.dwell_times.xml_values():
            subelem(elem, value)
        trips = etree.SubElement(result, "Trips")
        for tp in self.timing_points:
            trips.append(tp.xml())

        return result
