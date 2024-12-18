from enum import Enum


class AccelBrake(Enum):
    """SimSig train acceleration/braking categories"""

    VERY_LOW = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    VERY_HIGH = 4

    @property
    def xml_value(self):
        """As used in SimSig .WTT"""
        return self.value
