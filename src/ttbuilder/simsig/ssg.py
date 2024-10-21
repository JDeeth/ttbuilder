from dataclasses import dataclass
from zipfile import ZipFile
from lxml import etree

from ttbuilder.simsig.local_timetable import LocalTimetable


@dataclass
class Ssg:
    """Extract sim data from a SimSig saved game (.SSG) file"""

    entry_points: set[str]
    timing_points: set[str]
    timetables: list[LocalTimetable]

    @classmethod
    def from_xml(cls, xml_root):
        """Parse from an XML object

        This method mostly exists to avoid excessive indentation in `from_file`
        """
        entry_points = set(x.attrib["ID"] for x in xml_root if x.tag == "TENT")
        timing_points = set(x.attrib["ID"] for x in xml_root if x.tag == "TLOC")
        timetables_elem = xml_root.find("Timetables")
        timetables = [LocalTimetable.from_xml(x) for x in timetables_elem]
        return cls(
            entry_points=entry_points,
            timing_points=timing_points,
            timetables=timetables,
        )

    @classmethod
    def from_file(cls, filepath):
        """Parse from a .SSG file"""
        with ZipFile(filepath, "r") as zipfile:
            with zipfile.open("SavedSimulation.xml", "r") as savefile:
                parser = etree.XMLParser(remove_blank_text=True)
                xml_root = etree.parse(savefile, parser=parser).getroot()
                return cls.from_xml(xml_root)
