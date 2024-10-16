from enum import Enum


class Weight(Enum):
    """SimSig train weight"""

    LIGHT = 1
    NORMAL = 0
    HEAVY = 2

    @property
    def xml_value(self):
        """As used in SimSig .WTT"""
        return self.value
