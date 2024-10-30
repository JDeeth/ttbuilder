from dataclasses import dataclass
from enum import Enum
from lxml import etree

from ttbuilder.common.train_id import TrainId


@dataclass
class Activity:
    """Timing point activity"""

    class Type(Enum):
        """Activity type, with SimSig XML values and timetable abbreviation"""

        INVALID = None, ":"
        NEXT = 0, "N"
        JOIN = 3, "J"
        DIVIDE_REAR = 1, "DR"
        DIVIDE_FRONT = 2, "DF"
        DETACH_ENGINE_REAR = 4, "DER"
        DETACH_ENGINE_FRONT = 5, "DEF"
        DROP_COACHES_REAR = 6, "DCR"
        DROP_COACHES_FRONT = 7, "DCF"
        PLATFORM_SHARE = 9, "PS"
        # CREW_CHANGE = 10, "CC" # does not use train ID, uses time instead

        def __init__(self, xml_code, label):
            self.xml_code = xml_code
            self.label = label

    activity_type: Type
    associated_train_id: TrainId

    def __post_init__(self):
        if isinstance(self.associated_train_id, str):
            _id, _, uid = self.associated_train_id.partition("/")
            self.associated_train_id = TrainId(_id, uid)

    @classmethod
    def next(cls, train_id: str | TrainId):
        """This timetable ends, and the train continues with the designated ID and timetable"""
        return cls(cls.Type.NEXT, train_id)

    @classmethod
    def join(cls, train_id: str | TrainId):
        """Train waits for and joins with other train. Both timetables should have Join
        activities, but only one should have subsequent timing points.
        The other timetable ends."""
        return cls(cls.Type.JOIN, train_id)

    @classmethod
    def divide_rear(cls, train_id: str | TrainId):
        """A new train forms from the rear of this train"""
        return cls(cls.Type.DIVIDE_REAR, train_id)

    @classmethod
    def divide_front(cls, train_id: str | TrainId):
        """A new train forms from the front of this train"""
        return cls(cls.Type.DIVIDE_FRONT, train_id)

    @classmethod
    def detach_engine_rear(cls, train_id: str | TrainId):
        """A new train forms from the rear of this train, and this train is left without power"""
        return cls(cls.Type.DETACH_ENGINE_REAR, train_id)

    @classmethod
    def detach_engine_front(cls, train_id: str | TrainId):
        """A new train forms from the front of this train, and this train is left without power"""
        return cls(cls.Type.DETACH_ENGINE_FRONT, train_id)

    @classmethod
    def drop_coaches_rear(cls, train_id: str | TrainId):
        """A new train forms from the rear of this train, without power"""
        return cls(cls.Type.DROP_COACHES_REAR, train_id)

    @classmethod
    def drop_coaches_front(cls, train_id: str | TrainId):
        """A new train forms from the front of this train, without power"""
        return cls(cls.Type.DROP_COACHES_FRONT, train_id)

    @classmethod
    def platform_share(cls, train_id: str | TrainId):
        """Permits ARS to signal this train into a platform occupied by the other or vice versa"""
        return cls(cls.Type.PLATFORM_SHARE, train_id)

    def __bool__(self):
        return self.activity_type != self.Type.INVALID

    def __str__(self):
        return f"{self.activity_type.label}:{self.associated_train_id.id}"

    def xml(self):
        """SimSig .WTT format"""
        result = etree.Element("Activity")
        etree.SubElement(result, "Activity").text = str(self.activity_type.xml_code)
        result.append(self.associated_train_id.activity_xml())
        return result
