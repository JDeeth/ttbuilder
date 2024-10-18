from dataclasses import dataclass, field, fields
from lxml import etree

from ..common.str_helper import pascal_case
from ..common.ttime import TTime


@dataclass
class DwellTimes:
    """Collection of dwell times for a SimSig train category"""

    # pylint: disable=too-many-instance-attributes

    red_signal_move_off: TTime = field(default_factory=TTime)
    station_forward: TTime = field(default_factory=TTime)
    station_reverse: TTime = field(default_factory=TTime)
    terminate_forward: TTime = field(default_factory=TTime)
    terminate_reverse: TTime = field(default_factory=TTime)
    join: TTime = field(default_factory=TTime)
    divide: TTime = field(default_factory=TTime)
    crew_change: TTime = field(default_factory=TTime)

    def __post_init__(self):
        """Assume plain-int values are seconds and convert"""
        for f in fields(self):
            value = getattr(self, f.name)
            if isinstance(value, int):
                setattr(self, f.name, TTime(value))

    def xml_values(self):
        """Tag-value tuples for SimSig XML"""
        if not any(getattr(self, field.name) for field in fields(self)):
            return
        for f in fields(self):
            time = getattr(self, f.name)
            yield (pascal_case(f.name), str(time.seconds))

    def xml(self):
        """As used in SimSig .WTT"""
        result = etree.Element("DwellTimes")
        for tag, value in self.xml_values():
            etree.SubElement(result, tag).text = value

        return result
