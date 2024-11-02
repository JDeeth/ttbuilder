from dataclasses import asdict, dataclass
from enum import Enum
from lxml import etree

from ttbuilder.common.train_id import TrainId


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


@dataclass
class Activity:
    """Timing point activity"""

    associated_train_id: TrainId
    activity_type: Type = Type.INVALID

    def __post_init__(self):
        if isinstance(self.associated_train_id, str):
            _id, _, uid = self.associated_train_id.partition("/")
            self.associated_train_id = TrainId(_id, uid)

    def __bool__(self):
        return self.activity_type != Type.INVALID

    def __str__(self):
        return f"{self.activity_type.label}:{self.associated_train_id.id}"

    def xml(self):
        """SimSig .WTT format"""
        result = etree.Element("Activity")
        etree.SubElement(result, "Activity").text = str(self.activity_type.xml_code)
        result.append(self.associated_train_id.activity_xml())
        return result

    def __eq__(self, other):
        """Permit comparison by value between base and subclass"""
        if not isinstance(self, other.__class__):
            return False
        return asdict(self) == asdict(other)


class Next(Activity):
    """This timetable ends, and the train continues with the designated ID and timetable"""

    def __init__(self, train_id: str | TrainId):
        super().__init__(train_id, Type.NEXT)


class Join(Activity):
    """Train waits for and joins with other train. Both timetables should have Join
    activities, but only one should have subsequent timing points.
    The other timetable ends."""

    def __init__(self, train_id: str | TrainId):
        super().__init__(train_id, Type.JOIN)


class DivideRear(Activity):
    """A new train forms from the rear of this train"""

    def __init__(self, train_id: str | TrainId):
        super().__init__(train_id, Type.DIVIDE_REAR)


class DivideFront(Activity):
    """A new train forms from the front of this train"""

    def __init__(self, train_id: str | TrainId):
        super().__init__(train_id, Type.DIVIDE_FRONT)


class DetachEngineRear(Activity):
    """A new train forms from the rear of this train, and this train is left without power"""

    def __init__(self, train_id: str | TrainId):
        super().__init__(train_id, Type.DETACH_ENGINE_REAR)


class DetachEngineFront(Activity):
    """A new train forms from the front of this train, and this train is left without power"""

    def __init__(self, train_id: str | TrainId):
        super().__init__(train_id, Type.DETACH_ENGINE_FRONT)


class DropCoachesRear(Activity):
    """A new train forms from the rear of this train, without power"""

    def __init__(self, train_id: str | TrainId):
        super().__init__(train_id, Type.DROP_COACHES_REAR)


class DropCoachesFront(Activity):
    """A new train forms from the front of this train, without power"""

    def __init__(self, train_id: str | TrainId):
        super().__init__(train_id, Type.DROP_COACHES_FRONT)


class PlatformShare(Activity):
    """Permits ARS to signal this train into a platform occupied by the other or vice versa"""

    def __init__(self, train_id: str | TrainId):
        super().__init__(train_id, Type.PLATFORM_SHARE)
