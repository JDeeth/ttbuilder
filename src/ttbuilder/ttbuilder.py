import os
import re
from ttbuilder.simsig.ssg import Ssg


def _print_wrapped(text):
    print("\n".join(line for line in re.findall(r".{1,100}(?:\s+|$)", text)))


def main():
    """Temporary behaviour: open an .SSG, show what paths it contains"""
    while True:
        ssg_path = input("Path to .SSG: ")
        if os.path.exists(ssg_path):
            break

    ssg = Ssg.from_file(ssg_path)
    print("\nEntry points:")
    _print_wrapped(", ".join(pt for pt in sorted(ssg.entry_points)))
    print("\nTiming points:")
    _print_wrapped(", ".join(pt for pt in sorted(ssg.timing_points)))

    print("\nTrains:")
    for t in sorted(ssg.timetables, key=lambda t: t.train_id.id):
        print(f"{t.train_id.id} {t.description}")
        locations = []
        if t.entry_point:
            locations.append(t.entry_point.tiploc)
        locations.extend(pt.location.tiploc for pt in t.timing_points)
        _print_wrapped(" ".join(locations))
        print()

    ep_in_timetables = {t.entry_point.tiploc for t in ssg.timetables if t.entry_point}
    ep_not_in_timetables = ssg.entry_points - ep_in_timetables
    print("\nEntry points not in timetables:")
    _print_wrapped(", ".join(sorted(ep_not_in_timetables)) or "None")

    tp_in_timetables = {
        pt.location.tiploc for t in ssg.timetables for pt in t.timing_points
    }
    tp_not_in_timetables = ssg.timing_points - tp_in_timetables
    print("\nLocations not in timetables:")
    _print_wrapped(", ".join(sorted(tp_not_in_timetables)) or "None")
