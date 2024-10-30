from dataclasses import dataclass
from lxml import etree


@dataclass
class TrainId:
    """Train headcode and optional UID"""

    id: str
    uid: str = ""

    def __str__(self):
        if self.uid:
            result = f"{self.id}/{self.uid}"
        else:
            result = self.id
        return result

    def activity_xml(self):
        """As seen in Activities"""
        if self.uid:
            result = etree.Element("AssociatedUID")
            result.text = self.uid.upper()
        else:
            result = etree.Element("AssociatedTrain")
            result.text = self.id.upper()
        return result
