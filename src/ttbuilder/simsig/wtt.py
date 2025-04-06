from dataclasses import dataclass, field
from zipfile import ZipFile
from lxml import etree

from ttbuilder.simsig.local_timetable import LocalTimetable
from ttbuilder.simsig.version import Version
from ttbuilder.common.str_helper import xml_escape
from ttbuilder.common.ttime import TTime
from ttbuilder.train.train_category import TrainCategory


@dataclass
class Sim:
    """SimSig sim"""

    name: str
    version: Version


@dataclass
class Wtt:
    """SimSig timetable file"""

    # pylint: disable=too-many-instance-attributes

    sim: Sim
    name: str
    start_time: TTime = TTime.from_hms(0, 0, 0)
    end_time: TTime = TTime.from_hms(27, 0, 0)
    description: str = ""
    version: Version = Version(0)
    td_template: str = "$originTime $originName-$destName $operator ($stock)"
    train_types: list[TrainCategory] = field(default_factory=list)
    workings: list[LocalTimetable] = field(default_factory=list)

    def xml_header(self):
        """Timetable header data"""
        doc = etree.Element(
            "SimSigTimetable",
            ID=self.sim.name,
            Version=self.sim.version.text,
        )

        def elem(tag, content=""):
            etree.SubElement(doc, tag).text = str(content)

        elem("Name", self.name)
        elem("Description", xml_escape(self.description))
        elem("StartTime", self.start_time.seconds)
        elem("FinishTime", self.end_time.seconds)
        elem("VMajor", self.version.major)
        elem("VMinor", self.version.minor or 0)
        elem("VBuild", self.version.build or 0)
        elem(
            "TrainDescriptionTemplate",
            self.td_template,
        )
        elem("SeedGroupSummary")
        elem("ScenarioOptions")

        return doc

    def xml(self):
        """Full timetable data"""
        result = self.xml_header()
        if self.train_types:
            tt_elem = etree.SubElement(result, "TrainCategories")
            for t in self.train_types:
                tt_elem.append(t.xml())
        ltt_elem = etree.SubElement(result, "Timetables")
        if self.workings:
            for w in self.workings:
                ltt_elem.append(w.xml())

        return result

    def compile_wtt(self, filename):
        """Create header and full file in a Zip archive"""
        with ZipFile(filename, "w") as zipfile:
            zipfile.writestr(
                "TimetableHeader.xml",
                etree.tostring(self.xml_header(), pretty_print=True).decode(),
            )
            zipfile.writestr(
                "SavedTimetable.xml",
                etree.tostring(self.xml(), pretty_print=True).decode(),
            )

    @classmethod
    def from_xml(cls, xml_root):
        """Parse from an XML object"""

        def findtext(match, default=""):
            return xml_root.findtext(match, default=default)

        timetables_elem = xml_root.find("Timetables")
        if timetables_elem is None:
            timetables = []
        else:
            timetables = [LocalTimetable.from_xml(x) for x in timetables_elem]
        return cls(
            sim=Sim(
                xml_root.xpath("./@ID")[0],
                Version(*(int(x) for x in xml_root.xpath("./@Version")[0].split("."))),
            ),
            name=xml_root.findtext("Name", default=""),
            start_time=TTime(int(findtext("StartTime", "0"))),
            end_time=TTime(int(findtext("FinishTime", "0"))),
            description=findtext("Description", ""),
            version=Version(
                major=int(findtext("VMajor", "0")),
                minor=int(findtext("VMinor", "0")),
                build=int(findtext("VBuild", "0")),
            ),
            td_template=findtext("TrainDescriptionTemplate"),
            # train_types = ...,
            workings=timetables,
        )

    @classmethod
    def from_file(cls, filepath):
        """Parse from a .WTT file"""
        with ZipFile(filepath, "r") as zipfile:
            with zipfile.open("SavedTimetable.xml", "r") as timetable_file:
                parser = etree.XMLParser(remove_blank_text=True)
                xml_root = etree.parse(timetable_file, parser=parser).getroot()
                return cls.from_xml(xml_root)
