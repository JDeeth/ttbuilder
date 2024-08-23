from dataclasses import dataclass
from enum import Enum
from elements import TrainId
from lxml import etree

_ = """
Activity types:
- Next train
- Divides (new rear)
- Divides (new front)
- Joins
- Platform share
- Drop coaches (at rear)
- Drop coaches (at front)
- Detach engine (new rear)
- Detach engine (new front)
- Crew change

Params:
- Train ID or UID
- Duration
- Crew arrive at
- Decision
- Choice
"""


class ActivityType(Enum):
    NEXT = 0
    DIVIDE_REAR = 1
    DIVIDE_FRONT = 2
    JOIN = 3
    PLATFORM_SHARE = 9
    DROP_COACHES_REAR = 6
    DROP_COACHES_FRONT = 7
    DETACH_ENGINE_REAR = 4
    DETACH_ENGINE_FRONT = 5
    CREW_CHANGE = 10


@dataclass
class Activity:
    """Timing point activity"""

    activity_type: ActivityType

    associated_train_id: TrainId

    def xml(self):
        result = etree.Element("Activity")
        etree.SubElement(result, "Activity").text = str(self.activity_type.value)
        result.append(self.associated_train_id.activity_xml())
        return result
