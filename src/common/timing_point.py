from dataclasses import dataclass, field
from lxml import etree

from .activity import Activity
from .location import Location
from .ttime import TTime


@dataclass
class TimingPoint:
    """One step in a timetabled path"""

    # pylint: disable=too-many-instance-attributes

    location: Location | str
    depart: TTime | str | None = None
    platform: str = ""
    activities: list[Activity] = field(default_factory=list)
    engineering_allowance: TTime = field(default_factory=TTime)
    performance_allowance: TTime = field(default_factory=TTime)
    pathing_allowance: TTime = field(default_factory=TTime)
    request_stop_percent: int = 100

    def __post_init__(self):
        if isinstance(self.location, str):
            self.location = Location(tiploc=self.location)
        if isinstance(self.depart, str):
            self.depart = TTime.from_str(self.depart)

    @classmethod
    def from_str(cls, text):
        """From timetable format e.g. DRBY.4 10/23H <2> J:1A23"""
        split_text = text.split()
        params = {}

        tiploc, _, platform = split_text[0].partition(".")
        params["location"] = Location(tiploc=tiploc)
        params["platform"] = platform
        params["depart"] = TTime.from_str(split_text[1])
        params["activities"] = []

        def get_time(elem, a, z):
            if elem.startswith(a) and elem.endswith(z):
                m, h, _ = elem[1:-1].partition("H")
                time = int(m or 0) * 60
                time += 30 if h else 0
            else:
                time = 0
            return TTime(time)

        for elem in split_text[2:]:
            for a, label, z in (
                "[ engineering_allowance ]".split(),
                "( pathing_allowance )".split(),
                "< performance_allowance >".split(),
            ):
                time = get_time(elem, a, z)
                if time:
                    params[label] = time
            activity = Activity.from_str(elem)
            if activity:
                params["activities"].append(activity)

        return cls(**params)

    def __str__(self):
        """To timetable format"""
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
        """To SimSig .WTT format"""
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
