from dataclasses import dataclass, field
from lxml import etree

from ttbuilder.common.activity import Activity
from ttbuilder.common.location import Location
from ttbuilder.common.ttime import Allowance, TTime


@dataclass
class TimingPoint:
    """One step in a timetabled path"""

    # pylint: disable=too-many-instance-attributes

    location: Location | str
    depart: TTime | str | None = None
    allowances: list[Allowance] = field(default_factory=list)
    activities: list[Activity] = field(default_factory=list)
    request_stop_percent: int = 100

    def __post_init__(self):
        if isinstance(self.location, str):
            self.location = Location(tiploc=self.location)

    def __str__(self):
        """To timetable format"""
        location = self.location.tiploc
        if self.location.platform:
            location += f".{self.location.platform}"
        rem = []
        if self.allowances:
            allowances = {x.type: x for x in self.allowances}
            for a in allowances.values():
                start, _, end = a.type.value.partition("x")
                rem.append(f"{start}{a.time:MH}{end}")
        rem.extend(str(act) for act in self.activities)
        rem = " ".join(x for x in rem if x)
        return f"{location:10} {self.depart:6} {rem}".strip()

    @classmethod
    def from_xml(cls, xml_root):
        """Read relevant bits from the XML within a .WTT or .SSG file"""

        def findtext(match, default=""):
            return xml_root.findtext(match, default=default)

        return cls(location=Location(tiploc=findtext("Location")))

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
            if self.depart.stop_mode == TTime.StopMode.PASSING:
                subelem("IsPassTime", "-1")
        if self.location.platform:
            subelem("Platform", self.location.platform)
        if self.activities:
            acts = etree.SubElement(result, "Activities")
            for a in self.activities:
                acts.append(a.xml())
        # allowances are recorded as multiples of 30 seconds
        if self.allowances:
            allowances = {x.type: x.time for x in self.allowances}
            eng = allowances.get(Allowance.Type.ENGINEERING, TTime(0))
            perf = allowances.get(Allowance.Type.PERFORMANCE, TTime(0))
            path = allowances.get(Allowance.Type.PATHING, TTime(0))
            if eng or perf:
                subelem("EngAllowance", eng.halfminute + perf.halfminute)
            if path:
                subelem("PathAllowance", path.halfminute)
        if self.request_stop_percent in range(0, 100):  # excludes 100%
            subelem("RequestPercent", self.request_stop_percent)

        return result
