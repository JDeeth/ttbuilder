from dataclasses import dataclass
from lxml import etree

from version import Version
from cajontime import CajonTime


@dataclass
class SimSigSim:
    name: str
    version: Version


@dataclass
class Wtt:
    sim: SimSigSim
    start_time: CajonTime
    end_time: CajonTime
    description: str = ""
    version: Version = Version(0)
    td_template: str = "$originTime $originName-$destName $operator ($stock)"

    def header(self, filename):
        doc = etree.Element(
            "SimSigTimetable",
            ID=self.sim.name,
            Version=self.sim.version.text,
        )

        def elem(tag, content=""):
            etree.SubElement(doc, tag).text = str(content)

        elem("Name", filename)
        elem("Description", self.description)
        elem("StartTime", self.start_time.value)
        elem("FinishTime", self.end_time.value)
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
