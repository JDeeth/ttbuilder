from dataclasses import dataclass
from enum import Enum
from elements import TrainId
from lxml import etree


class ActivityType(Enum):
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
    CREW_CHANGE = 10, "CC"

    def __init__(self, xml_code, label):
        self.xml_code = xml_code
        self.label = label


@dataclass
class Activity:
    """Timing point activity"""

    activity_type: ActivityType
    associated_train_id: TrainId

    def __post_init__(self):
        if isinstance(self.associated_train_id, str):
            self.associated_train_id = TrainId(id=self.associated_train_id)

    @classmethod
    def next(cls, train_id: str | TrainId):
        return cls(ActivityType.NEXT, train_id)

    @classmethod
    def join(cls, train_id: str | TrainId):
        return cls(ActivityType.JOIN, train_id)

    @classmethod
    def divide_rear(cls, train_id: str | TrainId):
        return cls(ActivityType.DIVIDE_REAR, train_id)

    @classmethod
    def divide_front(cls, train_id: str | TrainId):
        return cls(ActivityType.DIVIDE_FRONT, train_id)

    @classmethod
    def detach_engine_front(cls, train_id: str | TrainId):
        return cls(ActivityType.DETACH_ENGINE_FRONT, train_id)

    @classmethod
    def detach_engine_rear(cls, train_id: str | TrainId):
        return cls(ActivityType.DETACH_ENGINE_REAR, train_id)

    @classmethod
    def drop_coaches_front(cls, train_id: str | TrainId):
        return cls(ActivityType.DROP_COACHES_FRONT, train_id)

    @classmethod
    def drop_coaches_rear(cls, train_id: str | TrainId):
        return cls(ActivityType.DROP_COACHES_REAR, train_id)

    @classmethod
    def platform_share(cls, train_id: str | TrainId):
        return cls(ActivityType.PLATFORM_SHARE, train_id)

    @classmethod
    def crew_change(cls, train_id: str | TrainId):
        return cls(ActivityType.CREW_CHANGE, train_id)

    @classmethod
    def from_str(cls, text: str):
        text = text.upper()
        label, _, train_id = text.partition(":")
        train_id, _, train_uid = train_id.partition("/")
        try:
            activity_type = next(t for t in ActivityType if t.label == label)
        except StopIteration:
            return cls(ActivityType.INVALID, "")
        return cls(activity_type, TrainId(train_id, train_uid))

    def __bool__(self):
        return self.activity_type != ActivityType.INVALID

    def __str__(self):
        return f"{self.activity_type.label}:{self.associated_train_id.id}"

    def xml(self):
        result = etree.Element("Activity")
        etree.SubElement(result, "Activity").text = str(self.activity_type.xml_code)
        result.append(self.associated_train_id.activity_xml())
        return result
