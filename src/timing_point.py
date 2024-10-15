from dataclasses import dataclass, field
from lxml import etree
from activity import Activity
from elements import CajonTime, Location


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
