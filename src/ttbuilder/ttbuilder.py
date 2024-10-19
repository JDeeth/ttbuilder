from ttbuilder.simsig.ssg import Ssg


def main():
    """Temporary behaviour: open an .SSG and show the entry points and timing points"""
    ssg_path = input("Path to .SSG: ")
    ssg = Ssg.from_file(ssg_path)
    print("\nEntry points:")
    print(", ".join(pt for pt in sorted(ssg.entry_points)))
    print("\nTiming points:")
    print(", ".join(pt for pt in sorted(ssg.timing_points)))
