# module to add origin/dest to existing WTT
#
# 1. extract description and current origin/dest data to a file
# 2. manually edit
# 3. apply edited file to WTT

import csv
from dataclasses import dataclass, fields
from tkinter.filedialog import askopenfilename

from ttbuilder.common.ttime import TTime
from ttbuilder.simsig.local_timetable import LocalTimetable
from ttbuilder.simsig.wtt import Wtt


@dataclass
class ExportRow:
    """Train working details for export and review"""

    uid: str
    id: str
    description: str
    departure_time: TTime | None
    origin: str
    destination: str
    notes: str
    inferred_update: bool = False

    @classmethod
    def from_tt(cls, tt: LocalTimetable):
        """Constructor using parsed .WTT timetable data"""
        return cls(
            uid=tt.train_id.uid,
            id=tt.train_id.id,
            description=tt.description,
            departure_time=tt.origin_dep,
            origin=tt.origin,
            destination=tt.destination,
            notes=tt.notes,
        )

    def __post_init__(self):
        if self.description.startswith("$"):
            return
        desc, _, _ = self.description.partition("(")
        desc = str(desc)
        desc = desc.strip()
        time, *words = desc.split()
        # infer time from first word:
        if self.departure_time is None:
            try:
                hh, mm = int(time[:2]), int(time[-2:])
                self.departure_time = TTime(hh * 3600 + mm * 60)
                self.inferred_update = True
            except ValueError:
                pass

        # separate other words on "-"
        try:
            words = [word for word in words if "*" not in word]
            sep_pos = next(i for i, word in enumerate(words) if "-" in word)
            if not self.origin:
                self.origin = " ".join(words[:sep_pos])
                self.inferred_update = True
            if not self.destination:
                self.destination = " ".join(words[sep_pos + 1 :])
                self.inferred_update = True
        except (StopIteration, IndexError):
            return

    @classmethod
    def headers(cls):
        """dataclass field names"""
        return (field.name for field in fields(cls))

    def fields(self):
        """field values as string"""
        return (str(getattr(self, field.name) or "") for field in fields(self))


def export():
    """Extracts CSV from WTT with inferred dep time/origin/destination"""
    tt_path = askopenfilename(
        title="SimSig WTT to read",
        filetypes=[("SimSig WTT", "*.WTT")],
    )
    if not tt_path:
        return

    wtt = Wtt.from_file(tt_path)

    # csv_path = asksaveasfilename(
    #     title="CSV with train details",
    #     filetypes=[("CSV", "*.csv")],
    #     defaultextension=".csv",
    # )
    # if not csv_path:
    #     print(",".join(TrainRow.headers()))
    #     for tt in wtt.workings:
    #         row = TrainRow.from_tt(tt)
    #         print(",".join(row.fields()))
    #     return

    csv_path, _, _ = tt_path.rpartition(".")
    csv_path += ".csv"

    with open(csv_path, "w", newline="", encoding="utf8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(ExportRow.headers())
        writer.writerows(ExportRow.from_tt(tt).fields() for tt in wtt.workings)
