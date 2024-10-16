from dataclasses import dataclass
from lxml import etree


@dataclass
class TrainId:
    """Train headcode and optional UID"""

    id: str
    uid: str = ""

    def xml(self):
        """To SimSig .WTT format"""
        if self.uid:
            result = etree.Element("AssociatedUID")
            result.text = self.uid.upper()
        else:
            result = etree.Element("AssociatedTrain")
            result.text = self.id.upper()
        return result
