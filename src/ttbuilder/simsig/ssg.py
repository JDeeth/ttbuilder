from dataclasses import dataclass
from zipfile import ZipFile
from lxml import etree


@dataclass
class Ssg:
    """Extract sim data from a SimSig saved game (.SSG) file"""

    entry_points: set[str]
    timing_points: set[str]

    @classmethod
    def from_file(cls, filepath):
        """Parse from a .SSG file"""
        with ZipFile(filepath, "r") as zipfile:
            with zipfile.open("SavedSimulation.xml", "r") as savefile:
                parser = etree.XMLParser(remove_blank_text=True)
                xml = etree.parse(savefile, parser=parser).getroot()
                entry_points = set(x.attrib["ID"] for x in xml if x.tag == "TENT")
                timing_points = set(x.attrib["ID"] for x in xml if x.tag == "TLOC")
                return cls(entry_points=entry_points, timing_points=timing_points)
