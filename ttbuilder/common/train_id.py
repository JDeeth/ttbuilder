from dataclasses import dataclass
from lxml import etree


@dataclass
class TrainId:
    """Train headcode and optional UID"""

    id: str
    uid: str = ""

    @classmethod
    def from_str(cls, text):
        """Construct ID from text. Optional UID after slash: 1A01 or 1A01/ABC123"""
        id_, _, uid = text.partition("/")
        return cls(id_, uid)

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
