from dataclasses import dataclass, field
from zipfile import ZipFile
from lxml import etree

from common import TTime, xml_escape
from train.train_category import TrainCategory
from .local_timetable import LocalTimetable
from .version import Version


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
