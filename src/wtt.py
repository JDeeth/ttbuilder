from dataclasses import dataclass, field
from zipfile import ZipFile
from local_timetable import LocalTimetable
from lxml import etree

from elements import CajonTime, Version
from helper import xml_escape
from train_category import TrainType


@dataclass
class SimSigSim:
    name: str
    version: Version


@dataclass
class Wtt:
    sim: SimSigSim
    name: str
    start_time: CajonTime = CajonTime.from_hms(0, 0, 0)
    end_time: CajonTime = CajonTime.from_hms(27, 0, 0)
    description: str = ""
    version: Version = Version(0)
    td_template: str = "$originTime $originName-$destName $operator ($stock)"
    train_types: list[TrainType] = field(default_factory=list)
    workings: list[LocalTimetable] = field(default_factory=list)

    def xml_header(self):
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
        with ZipFile(filename, "w") as zip:
            zip.writestr(
                "TimetableHeader.xml",
                etree.tostring(self.xml_header(), pretty_print=True).decode(),
            )
            zip.writestr(
                "SavedTimetable.xml",
                etree.tostring(self.xml(), pretty_print=True).decode(),
            )
