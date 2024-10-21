import os
from ttbuilder.simsig.ssg import Ssg


def main():
    """Temporary behaviour: open an .SSG, show what paths it contains"""
    while True:
        ssg_path = input("Path to .SSG: ")
        if os.path.exists(ssg_path):
            break

    ssg = Ssg.from_file(ssg_path)
    print("\nEntry points:")
    print(", ".join(pt for pt in sorted(ssg.entry_points)))
    print("\nTiming points:")
    print(", ".join(pt for pt in sorted(ssg.timing_points)))

    print("\nTrains:")
    for t in sorted(ssg.timetables, key=lambda t: t.train_id.id):
        print(f"{t.train_id.id} {t.description}")
        locations = []
        if t.entry_point:
            locations.append(t.entry_point.tiploc)
        locations.extend(pt.location.tiploc for pt in t.timing_points)
        print(" ".join(locations))
        print()

    ep_in_timetables = {t.entry_point.tiploc for t in ssg.timetables if t}
    ep_not_in_timetables = ssg.entry_points - ep_in_timetables
    print("\nEntry points not in timetables:")
    print(", ".join(sorted(ep_not_in_timetables)) or "None")

    tp_in_timetables = {
        pt.location.tiploc for t in ssg.timetables for pt in t.timing_points
    }
    tp_not_in_timetables = ssg.timing_points - tp_in_timetables
    print("\nLocations not in timetables:")
    print(", ".join(sorted(tp_not_in_timetables)) or "None")
